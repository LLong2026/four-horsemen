#!/usr/bin/env python3
"""B1 baseline leg: 20 single-anomaly LLM resolutions, fresh conversation each, wall-clocked request->validated tuple."""
import os
import json
import time
import statistics
from pathlib import Path

import requests

root = Path(__file__).resolve().parent
corpus = json.loads((root / "CORPUS_B1.json").read_text())
convs = [
    "6acbd858a9daa555fe641b1a", "6acbd85a45d52716dc6d3182", "6acbd85d625044663fe6121c",
    "6acbd85fb9e36879a84151d7", "6acbd86245d52716dc6d318e", "6acbd86595d2236ac9e0edff",
    "6acbd8677c02b0c92062e860", "6acbd869d51d3568d4f7e875", "6acbd86c545711756a2cd721",
    "6acbd8729980b98eec915e36", "6acbd8778b6427344e0744f3", "6acbd87a51fa7837fb207082",
    "6acbd87c51ab75ee4e544f5e", "6acbd87f063cc5e119e2d5f1", "6acbd883bb4b9c3e749e4b8d",
    "6acbd885dd141e5fea91526b", "6acbd88816f5bf331650577b", "6acbd88ba5e7a5803014a07b",
    "6acbd88d34f759439626face", "6acbd8906c04f5d041d78011",
]
assert len(convs) == 20

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


s = requests.Session()
s.headers.update({"api_key": os.environ["BASE44_API_KEY"]})
base = "https://base44.app/api/agents/69b57683f2623117603736bc"
results = []
for i, (cid, inst) in enumerate(zip(convs, corpus[:20])):
    cr = s.get(f"{base}/conversations/{cid}", timeout=60)
    cr.raise_for_status()
    if cr.json().get("messages"):
        print(f"{i}: NONEMPTY {cid}", flush=True)
        results.append({"i": i, "conversation_id": cid, "error": "nonempty"})
        continue
    prompt = make_prompt(json.dumps(inst))
    t0 = time.perf_counter()
    try:
        r = s.post(f"{base}/conversations/{cid}/messages", json={"content": prompt}, timeout=600)
        dt = (time.perf_counter() - t0) * 1000
        (root / f"baseline_raw_{i:02d}.json").write_text(r.text)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.Timeout:
        dt = (time.perf_counter() - t0) * 1000
        results.append({"i": i, "conversation_id": cid, "status": "timeout", "wall_ms": round(dt, 1)})
        print(f"{i}: TIMEOUT", flush=True)
        continue
    content = None
    if isinstance(data, dict) and data.get("role") == "assistant":
        content = data.get("content")
    if content is None and isinstance(data, dict):
        cands = [m for m in (data.get("messages") or []) if m.get("role") == "assistant"]
        if cands:
            content = cands[-1].get("content")
    valid = False
    detail = ""
    if isinstance(content, str) and content.strip():
        (root / f"baseline_content_{i:02d}.txt").write_text(content)
        try:
            arr = json.loads(content)
            if isinstance(arr, list) and len(arr) == 1:
                t = arr[0]
                if (t.get("playbook") == inst["expected_playbook"]
                        and t.get("match_type") == "exact"
                        and t.get("steps_executed") == "isolation,healing,verification"
                        and t.get("status") == "resolved"
                        and t.get("position") == 0
                        and t.get("anomaly_type") == inst["anomaly_type"]):
                    valid = True
                else:
                    detail = "wrong content"
            else:
                detail = "bad shape"
        except Exception as e:
            detail = f"parse: {str(e)[:60]}"
    else:
        detail = "no content"
    results.append({"i": i, "conversation_id": cid, "wall_ms": round(dt, 1), "valid": valid, "detail": detail})
    print(f"{i}: valid={valid} wall_ms={round(dt, 1)} {detail}", flush=True)

ok = sorted(r["wall_ms"] for r in results if r.get("valid"))


def pct(p):
    return ok[min(len(ok) - 1, int(len(ok) * p))] if ok else None


summary = {
    "leg": "B1-baseline", "n_requested": 20, "n_valid": len(ok), "n_failed": 20 - len(ok),
    "min_ms": ok[0] if ok else None, "median_ms": statistics.median(ok) if ok else None,
    "p95_ms": pct(0.95) if ok else None, "max_ms": ok[-1] if ok else None,
    "failures": [{"i": r.get("i"), "detail": r.get("detail", "timeout")} for r in results if not r.get("valid")],
    "all_runs_recorded": True,
}
(root / "B1_BASELINE_RESULTS.json").write_text(json.dumps({"summary": summary, "runs": results}, indent=2) + "\n")
print("BASELINE SUMMARY:", json.dumps(summary), flush=True)
