"""DMB-X legs (prereg dual_mesh_bench_X_20261013, commit b293d58): 8 engine columns,
instrument byte-identical to the DeepSeek B1 leg. Fresh stateless request per instance,
20 instances per leg, raw preserved verbatim, no retries, no substitutions."""
import json, os, time, re, urllib.request, urllib.error, statistics, hashlib, datetime
from pathlib import Path

root = Path(__file__).resolve().parent
key = os.environ["OPENROUTER_API_KEY"]
corpus = json.load(open(root.parent / "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"))
assert hashlib.sha256(open(root.parent / "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json", "rb").read()).hexdigest() == \
    "13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59"
assert len(corpus) == 200

ENGINES = [
  ("anthropic_opus_5_5", "anthropic/claude-opus-5.5"),
  ("openai_gpt_6_1_sol", "openai/gpt-6.1-sol"),
]

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
    arr = json.loads(text)
    assert isinstance(arr, list) and len(arr) == 1 and isinstance(arr[0], dict)
    return arr[0]

def normalize(text):
    t = re.sub(r"^\s*```(json)?\s*|\s*```\s*$", "", text.strip())
    m = re.search(r"\[.*\]", t, re.S)
    return m.group(0) if m else t

all_legs = {}
payment_error = False
for fam, model in ENGINES:
    if payment_error: break
    leg_dir = root / fam
    if (leg_dir / f"{fam}_B1_LEG_RESULTS.json").exists():
        print(f"=== LEG {fam} already recorded — resume mode skips it (FBX-3: no re-runs) ===", flush=True)
        all_legs[fam] = {"summary": json.load(open(root / "DMB_FRONTIER_RECEIPT.json"))["legs"][fam] if (root / "DMB_FRONTIER_RECEIPT.json").exists() else {}, "results": []}
        continue
    leg_dir.mkdir(exist_ok=True)
    results = []
    print(f"=== LEG {fam} ({model}) ===", flush=True)
    for i, inst in enumerate(corpus[:20]):
        prompt = make_prompt(json.dumps(inst))
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps({"model": model,
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
            (leg_dir / f"{fam}_raw_{i:02d}.json").write_text(json.dumps(resp, indent=1))
            content = resp.get("choices", [{}])[0].get("message", {}).get("content")
            (leg_dir / f"{fam}_content_{i:02d}.txt").write_text(content or "")
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
            rec["http_error"] = e.code
            try: rec["error_body"] = e.read().decode()[:300]
            except Exception: pass
            if e.code in (402, 403):  # payment/credit: abort batch per prereg credit guard
                payment_error = True
                results.append(rec); break
        except Exception as e:
            rec["error"] = str(e)[:200]
            if "payment" in str(e).lower() or "credit" in str(e).lower(): payment_error = True
            results.append(rec); break
        results.append(rec)
        print(f"  {i:02d} {inst['instance_id']} {rec.get('wall_ms','ERR')}ms strict={rec.get('strict_valid')} norm={rec.get('norm_valid')} correct={rec.get('correct')}", flush=True)
    walls = [r["wall_ms"] for r in results if "wall_ms" in r]
    leg = {"family": fam, "model_requested": model, "n_run": len(results), "n_correct": sum(1 for r in results if r.get("correct")),
           "n_strict": sum(1 for r in results if r.get("strict_valid")), "n_norm": sum(1 for r in results if r.get("norm_valid")),
           "cost_usd": round(sum(r.get("cost") or 0 for r in results), 4),
           "model_returned": results[0].get("model_returned") if results else None,
           "aborted": payment_error}
    if walls:
        s = sorted(walls); leg["median_ms"] = round(statistics.median(s), 1)
        leg["p95_ms"] = round(s[min(len(s)-1, int(0.95 * len(s)))], 1)
    all_legs[fam] = {"summary": leg, "results": results}
    json.dump(results, open(leg_dir / f"{fam}_B1_LEG_RESULTS.json", "w"), indent=1)
    print(f"  LEG {fam}: {leg['n_correct']}/{leg['n_run']} correct, strict {leg['n_strict']}, norm {leg['n_norm']}, median {leg.get('median_ms')}ms, cost ${leg['cost_usd']}", flush=True)

total_cost = round(sum(v["summary"]["cost_usd"] for v in all_legs.values()), 4)
receipt = {
  "series_signature": "dual_mesh_benchmark_frontier_20261023",
  "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "operator_authorization": "Leon GO (chat authorization, 2026-10-23, 21:50 CT)",
  "prereg": "dual_mesh_bench_frontier_20261023_PREREG.md, committed BEFORE execution",
  "instrument": "byte-identical to the DeepSeek B1 leg (frozen prompt contract, CORPUS_B1 sha 13295d19..., first-20 selection rule, fresh stateless request per instance, wall-clock request->full response)",
  "legs": {k: v["summary"] for k, v in all_legs.items()},
  "total_cost_usd": total_cost,
  "payment_abort": payment_error,
  "raw_preserved": "fh_pub/dmb_frontier_evidence/<family>/ raw json + content per instance",
  "comparisons": {"dmb_x_matrix_ref": "ledger 0081, DMB-X 8-column matrix (Oct 13, 2026)",
                  "deepseek_v4_pro_median_ms_ref": "see DMB DeepSeek column (DOI 10.5281/zenodo.23345241)",
                  "mesh_median_ms_ref": 0.000443, "v1_loop_median_ms_ref": 4509.1,
                  "doctrine": "raw-API legs are comparable within their substrate only; cross-substrate comparisons are directional (XPLAT-2/3)"},
  "disclaimer": "This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All data is synthetic."}
json.dump(receipt, open(root / "DMB_FRONTIER_RECEIPT.json", "w"), indent=2)
json.dump({"completed": True, "executed_at": receipt["executed_at"], "total_cost_usd": total_cost,
           "payment_abort": payment_error}, open(root / "DMB_FRONTIER_STATUS.json", "w"), indent=2)
print(f"\nRECEIPT: DMB_FRONTIER_RECEIPT.json | total spend ${total_cost} | aborted={payment_error}")
