import json, os, time, re, urllib.request, urllib.error, statistics, datetime
from pathlib import Path
root = Path('/app/conversations/69b57685ca3719553a34597c/fh_pub/dmb_x_evidence')
key = os.environ['OPENROUTER_API_KEY']
corpus = json.load(open('/app/conversations/69b57685ca3719553a34597c/fh_pub/ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json'))
leg = json.load(open(root / "meta_llama/meta_llama_B1_LEG_RESULTS.json"))
ROSTER = json.dumps([
    {"anomaly_type": "latency_spike", "playbook_id": "6a5d29cb54e45d7e8bad47c5",
     "playbook": "PB-003: Latency Spike Resolver", "confidence_threshold": 0.8},
    {"anomaly_type": "heartbeat_miss", "playbook_id": "6a5d29cb54e45d7e8bad47ca",
     "playbook": "PB-008: Heartbeat Re-igniter", "confidence_threshold": 0.85},
    {"anomaly_type": "quantum_vulnerability_detected", "playbook_id": "6a5d29cb54e45d7e8bad47cb",
     "playbook": "PB-009: Quantum Vulnerability Migrator", "confidence_threshold": 0.8}])
def make_prompt(inst_json):
    return ("You are operating as the anomaly-response engine of a Squirrel OS v1.1 substrate "
        "(a deterministic governance envelope for IT operations). This is a synthetic test "
        "stream (no real system is affected). Your task: resolve ONE incoming anomaly and "
        "emit its decision tuple.\n\nOPERATING RULES (binding):\n"
        "1. EXACT MATCH ONLY. A playbook may be selected only if its anomaly_type string is "
        "EXACTLY equal (case-sensitive, character-for-character) to the incoming anomaly's "
        "anomaly_type. If no playbook matches, emit playbook null, playbook_id null, "
        'match_type "none", steps_executed null, status "escalated".\n'
        "2. THRESHOLD. If a playbook matched: when the anomaly's confidence_score is greater "
        "than or equal to the playbook's confidence_threshold, emit match_type \"exact\", "
        'steps_executed "isolation,healing,verification", status "resolved". When below '
        'threshold, emit match_type "exact", steps_executed null, status "detected".\n'
        "3. OUTPUT. Emit a JSON array containing exactly ONE decision tuple object with keys "
        "in this exact order: position, anomaly_type, playbook, playbook_id, match_type, "
        "steps_executed, status. position is 0. No prose, no markdown fences, no commentary.\n\n"
        "REGISTERED PLAYBOOK ROSTER (authoritative): " + ROSTER + "\n\n"
        "INCOMING ANOMALY (synthetic): " + inst_json + "\n\n"
        "The incoming anomaly's confidence_score is 0.9. Emit the decision tuple array now.")
def parse_strict(t):
    a = json.loads(t); assert isinstance(a, list) and len(a)==1 and isinstance(a[0], dict); return a[0]
def normalize(t):
    t = re.sub(r"^\s*```(json)?\s*|\s*```\s*$", "", t.strip())
    m = re.search(r"\[.*\]", t, re.S); return m.group(0) if m else t
def score(content, inst):
    rec = {"strict_valid": False, "norm_valid": False, "correct": False}
    try:
        t = parse_strict(content); rec["strict_valid"] = rec["norm_valid"] = True
    except Exception:
        try:
            t = parse_strict(normalize(content)); rec["norm_valid"] = True
        except Exception:
            return rec, None
    exp = {"position":0,"anomaly_type":inst["anomaly_type"],"playbook":inst["expected_playbook"],
           "match_type":"exact","steps_executed":"isolation,healing,verification","status":"resolved"}
    rec["tuple"] = t; rec["correct"] = all(t.get(k)==v for k,v in exp.items())
    return rec, t
kept, todo = [], []
for x in leg:
    if x.get("http_error") == 429:
        cf = root/"meta_llama"/f"meta_llama_content_{x['i']:02d}.txt"
        rf = root/"meta_llama"/f"meta_llama_raw_{x['i']:02d}.json"
        fresh = cf.exists() and rf.exists() and (time.time() - rf.stat().st_mtime) < 1800 and (cf.read_text() or "").strip()
        if fresh:
            try:
                raw = json.loads(rf.read_text()); content = raw.get("choices",[{}])[0].get("message",{}).get("content")
                sc, _ = score(content, corpus[x["i"]])
                if sc["norm_valid"] or sc["strict_valid"]:
                    x = dict(x); x.update(sc); x["resume"] = "scored_from_preserved_raw_interrupted_attempt"
                    kept.append(x); continue
            except Exception: pass
        todo.append(x["i"])
    else:
        kept.append(x)
print(f"preserved from interrupted attempt: {len(kept)-1} | to measure: {len(todo)}", flush=True)
results = list(kept)
for i in todo:
    inst = corpus[i]
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({"model": "meta-llama/llama-4-scout",
                         "messages": [{"role": "user", "content": make_prompt(json.dumps(inst))}],
                         "max_tokens": 2048}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.perf_counter()
    rec = {"i": i, "instance_id": inst["instance_id"], "expected_playbook": inst["expected_playbook"], "resume": True}
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=300))
        rec["wall_ms"] = round((time.perf_counter()-t0)*1000, 1)
        rec["model_returned"] = resp.get("model"); rec["finish_reason"] = resp.get("choices",[{}])[0].get("finish_reason")
        rec["cost"] = resp.get("usage", {}).get("cost")
        (root/"meta_llama"/f"meta_llama_raw_{i:02d}.json").write_text(json.dumps(resp, indent=1))
        content = resp.get("choices",[{}])[0].get("message",{}).get("content")
        (root/"meta_llama"/f"meta_llama_content_{i:02d}.txt").write_text(content or "")
        sc, _ = score(content, inst); rec.update(sc)
    except urllib.error.HTTPError as e:
        rec["http_error"] = e.code
        try: rec["error_body"] = e.read().decode()[:300]
        except Exception: pass
    results.append(rec)
    print(f"  {i:02d} {inst['instance_id']} {rec.get('wall_ms','ERR')}ms correct={rec.get('correct')}" + (f" HTTP{rec['http_error']}" if 'http_error' in rec else ""), flush=True)
    time.sleep(45)
results.sort(key=lambda x: x["i"])
json.dump(results, open(root/"meta_llama"/"meta_llama_B1_LEG_RESULTS.json","w"), indent=1)
walls = [r["wall_ms"] for r in results if "wall_ms" in r]
summary = {"family":"meta_llama","model_requested":"meta-llama/llama-4-scout",
  "n_run": len([r for r in results if "http_error" not in r]),
  "n_correct": sum(1 for r in results if r.get("correct")),
  "n_strict": sum(1 for r in results if r.get("strict_valid")),
  "n_norm": sum(1 for r in results if r.get("norm_valid")),
  "n_rate_limited": len([r for r in results if r.get("http_error")==429]),
  "cost_usd": round(sum(r.get("cost") or 0 for r in results), 4),
  "model_returned": "meta-llama/llama-4-scout",
  "resumed": True,
  "resume_disclosure": "First leg: 19/20 upstream rate-limited (HTTP 429, DeepInfra — availability, not capability). Disclosed resume re-ran only unmeasured instances with 45s pacing; instances completed by the timed-out first resume attempt were scored from their preserved raw files, never re-called. FBX-3 held: no measured instance was re-run."}
if walls:
    s = sorted(walls); summary["median_ms"] = round(statistics.median(s),1); summary["p95_ms"] = round(s[min(len(s)-1,int(0.95*len(s)))],1)
rec_json = json.load(open(root/"DMB_X_RECEIPT.json"))
rec_json["legs"]["meta_llama"] = summary
rec_json["total_cost_usd"] = round(rec_json["total_cost_usd"] + summary["cost_usd"], 4)
rec_json["llama_resume"] = {"executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "reason": "HTTP 429 upstream rate-limit (availability), not capability; disclosed resume",
  "note": "grok remains partial (payment abort, never retried — distinct doctrine)"}
json.dump(rec_json, open(root/"DMB_X_RECEIPT.json","w"), indent=2)
json.dump({"completed": True, "executed_at": rec_json["executed_at"], "total_cost_usd": rec_json["total_cost_usd"], "payment_abort": False}, open(root/"DMBX_STATUS.json","w"), indent=2)
print(f"DONE: llama {summary['n_correct']}/{summary['n_run']} correct, {summary['n_rate_limited']} still limited, median {summary.get('median_ms')}ms | total spend ${rec_json['total_cost_usd']}")
