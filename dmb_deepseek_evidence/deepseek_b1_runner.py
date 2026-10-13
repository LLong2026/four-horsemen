"""DMB DeepSeek leg: 20 single-anomaly resolutions via OpenRouter, fresh request each,
wall-clocked request->full response, strict + normalized validation, raw preserved."""
import json, os, time, re, urllib.request, statistics, hashlib
from pathlib import Path

root = Path(__file__).parent
key = os.environ["OPENROUTER_API_KEY"]
corpus = json.load(open(root / "CORPUS_B1.json"))
assert hashlib.sha256(open(root / "CORPUS_B1.json", "rb").read()).hexdigest() == \
    "13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59"
assert len(corpus) == 200

ROSTER = json.dumps([
    {"anomaly_type": "latency_spike", "playbook_id": "6a5d29cb54e45d7e8bad47c5",
     "playbook": "PB-003: Latency Spike Resolver", "confidence_threshold": 0.8},
    {"anomaly_type": "heartbeat_miss", "playbook_id": "6a5d29cb54e45d7e8bad47ca",
     "playbook": "PB-008: Heartbeat Re-igniter", "confidence_threshold": 0.85},
    {"anomaly_type": "quantum_vulnerability_detected", "playbook_id": "6a5d29cb54e45d7e8bad47cb",
     "playbook": "PB-009: Quantum Vulnerability Migrator", "confidence_threshold": 0.8},
])

def make_prompt(inst_json):
    return (
        "You are operating as the anomaly-response engine of a Squirrel OS v1.1 substrate "
        "(a deterministic governance envelope for IT operations). This is a synthetic test "
        "stream (no real system is affected). Your task: resolve ONE incoming anomaly and "
        "emit its decision tuple.\n\n"
        "OPERATING RULES (binding):\n"
        "1. EXACT MATCH ONLY. A playbook may be selected only if its anomaly_type string is "
        "EXACTLY equal (case-sensitive, character-for-character) to the incoming anomaly's "
        "anomaly_type. If no playbook matches, emit playbook null, playbook_id null, "
        'match_type "none", steps_executed null, status "escalated".\n'
        "2. THRESHOLD. If a playbook matched: when the anomaly's confidence_score is greater "
        'than or equal to the playbook\'s confidence_threshold, emit match_type "exact", '
        'steps_executed "isolation,healing,verification", status "resolved". When below '
        'threshold, emit match_type "exact", steps_executed null, status "detected".\n'
        "3. OUTPUT. Emit a JSON array containing exactly ONE decision tuple object with keys "
        "in this exact order: position, anomaly_type, playbook, playbook_id, match_type, "
        "steps_executed, status. position is 0. No prose, no markdown fences, no commentary.\n\n"
        "REGISTERED PLAYBOOK ROSTER (authoritative): " + ROSTER + "\n\n"
        "INCOMING ANOMALY (synthetic): " + inst_json + "\n\n"
        "The incoming anomaly's confidence_score is 0.9. Emit the decision tuple array now."
    )

def parse_strict(text):
    arr = json.loads(text)  # raises if prose/fences
    assert isinstance(arr, list) and len(arr) == 1 and isinstance(arr[0], dict)
    return arr[0]

def normalize(text):
    t = re.sub(r"^\s*```(json)?\s*|\s*```\s*$", "", text.strip())
    m = re.search(r"\[.*\]", t, re.S)
    return m.group(0) if m else t

results = []
for i, inst in enumerate(corpus[:20]):
    prompt = make_prompt(json.dumps(inst))
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({"model": "deepseek/deepseek-v4-pro",
                         "messages": [{"role": "user", "content": prompt}],
                         "max_tokens": 2048}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.perf_counter()
    rec = {"i": i, "instance_id": inst["instance_id"], "expected_playbook": inst["expected_playbook"]}
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=300))
        dt = (time.perf_counter() - t0) * 1000
        rec["wall_ms"] = round(dt, 1)
        rec["model_returned"] = resp.get("model"); rec["provider"] = resp.get("provider")
        rec["finish_reason"] = resp.get("choices", [{}])[0].get("finish_reason")
        rec["cost"] = resp.get("usage", {}).get("cost")
        (root / f"deepseek_raw_{i:02d}.json").write_text(json.dumps(resp, indent=1))
        content = resp.get("choices", [{}])[0].get("message", {}).get("content")
        (root / f"deepseek_content_{i:02d}.txt").write_text(content or "")
        strict = norm = None; rec["strict_valid"] = rec["norm_valid"] = False
        rec["correct"] = False
        try:
            strict = parse_strict(content); rec["strict_valid"] = True
            rec["norm_valid"] = True; norm = strict
        except Exception:
            try:
                norm = parse_strict(normalize(content)); rec["norm_valid"] = True
            except Exception as e:
                rec["norm_error"] = str(e)[:200]
        if norm:
            exp = {"position": 0, "anomaly_type": inst["anomaly_type"], "playbook": inst["expected_playbook"],
                   "match_type": "exact", "steps_executed": "isolation,healing,verification", "status": "resolved"}
            rec["tuple"] = norm
            rec["correct"] = all(norm.get(k) == v for k, v in exp.items())
    except urllib.error.HTTPError as e:
        rec["http_error"] = e.code; rec["error_body"] = e.read().decode()[:300]
    results.append(rec)
    print(f"{i:02d} {inst['instance_id']} {rec.get('wall_ms','ERR')}ms strict={rec.get('strict_valid')} norm={rec.get('norm_valid')} correct={rec.get('correct')}", flush=True)

json.dump(results, open(root / "DEEPSEEK_B1_LEG_RESULTS.json", "w"), indent=1)
walls = [r["wall_ms"] for r in results if "wall_ms" in r]
if walls:
    s = sorted(walls); med = statistics.median(s)
    p95 = s[min(len(s)-1, int(0.95 * len(s)))]
    strict_n = sum(1 for r in results if r.get("strict_valid"))
    norm_n = sum(1 for r in results if r.get("norm_valid"))
    corr = sum(1 for r in results if r.get("correct"))
    print(f"\nLEG SUMMARY: n={len(results)} completed, strict={strict_n}/20, normalized={norm_n}/20, correct={corr}/20")
    print(f"median={med:.1f}ms p95={p95:.1f}ms total_cost=${sum(r.get('cost') or 0 for r in results):.4f}")
