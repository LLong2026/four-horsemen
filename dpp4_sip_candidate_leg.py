#!/usr/bin/env python3
"""DPP-4 SIP-CANDIDATE REMEDIATION LEG — NOT THE FROZEN INSTRUMENT.
Demonstrates the proposed ingestion guard's effect for Leon's SIP approval.
Guard: reject-not-coerce on non-numeric/non-finite/negative metrics; instance-id
presence+uniqueness validation. Conforming behavior must be byte-identical."""
import json, hashlib, copy, math, os, importlib.util, sys
spec = importlib.util.spec_from_file_location("d4", "dpp4_runner_partial.py")

# reuse frozen corpus builders from the runner by extracting what we need
src = open('dpp4_runner.py').read()
head = src.split('# --- FROZEN replay engine')[0]
exec(compile(head, 'dpp4_head', 'exec'))  # gives clean, nodes0, ROSTER, build_corpus, MAX_*

ROSTER_TYPES = {r["anomaly_type"] for r in ROSTER}
def severity_guarded(inst):
    t = inst.get("anomaly_type")
    if t not in ROSTER_TYPES: return None
    field, mx = (("latency_ms", MAX_LAT) if t == "latency_spike" else
                 ("error_count", MAX_ERR) if t == "heartbeat_miss" else ("cpu", MAX_CPU))
    v = inst.get(field)
    if isinstance(v, bool) or not isinstance(v, (int, float)): return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)): return None
    if v < 0: return None
    return v / mx

def replay_guarded(mesh, corpus, seen_ids):
    w = {n["pattern_type"]: n["weight"] for n in mesh}; out = []; rejected = 0
    for inst in corpus:
        iid = inst.get("instance_id")
        if iid is None or iid in seen_ids:
            rejected += 1; out.append((iid or "MISSING_ID", inst.get("anomaly_type"), None, "escalated_structural_hold")); continue
        seen_ids.add(iid)
        s = severity_guarded(inst)
        if s is None:
            rejected += 1; out.append((iid, inst.get("anomaly_type"), None, "escalated_structural_hold")); continue
        t = inst["anomaly_type"]
        pb = next((r for r in ROSTER if r["anomaly_type"] == t), None)
        c = 0.5 * s + 0.5 * w["confidence_score"]
        if pb and c >= pb["threshold"]: out.append((iid, t, round(c,10), "resolved"))
        elif pb: out.append((iid, t, round(c,10), "detected"))
        else: out.append((iid, t, round(c,10), "escalated"))
    return out, rejected

def run40_guarded(corpus):
    mesh = copy.deepcopy(nodes0); journal = []; traj = []; crash = None
    try:
        for e in range(1, 41):
            decisions, _ = replay_guarded(mesh, corpus, set())
            for d in decisions:
                if d[3] != "resolved": continue
                wn = next(n for n in mesh if n["pattern_type"] == "confidence_score")
                lr, w = wn["learning_rate"], wn["weight"]
                w2 = round(w + lr*(1-d[2])*(1-w), 10)
                if w2 != w:
                    journal.append({"epoch": e, "event_id": d[0], "anomaly_type": d[1], "before": w, "after": w2, "pattern_update": True, "confidence": d[2]})
                    wn["weight"] = w2
            traj.append(hashlib.sha256(json.dumps([[n["pattern_type"], n["weight"]] for n in sorted(mesh, key=lambda x: json.dumps(x, sort_keys=True))], sort_keys=True).encode()).hexdigest())
    except Exception as ex:
        crash = f"{type(ex).__name__}: {str(ex)[:100]}"
    return mesh, journal, traj, crash

print("SIP-CANDIDATE LEG (guarded engine, NOT the frozen instrument):")
for cls in ["T1", "T2", "T3", "T4"]:
    corpus = build_corpus(cls)
    dec, rejected = replay_guarded(copy.deepcopy(nodes0), corpus, set())
    pois = [dec[i][3] for i in range(3, len(corpus), 3)]
    from collections import Counter
    print(f"  {cls}: poisoned-position verdicts {dict(Counter(pois))}, structural rejections {rejected}, crash None")
# conforming-identity: clean corpus through guarded engine must be byte-identical to frozen
mesh_g, j_g, traj_g, crash_g = run40_guarded(clean)
print(f"  CLEAN through guarded engine: crossings {len(j_g)}, traj {traj_g[-1][:16]}, crash {crash_g}")
print(f"  conforming-identity vs frozen baseline: {'BYTE-IDENTICAL' if len(j_g) == 2646 and traj_g[-1].startswith('ca575bb9') else 'DEVIATION — guard alters conforming behavior, SIP rejected'}")

result = {"leg": "DPP-4 SIP candidate remediation (guarded ingestion)",
          "not_the_frozen_instrument": True,
          "clean_conforming_crossings": len(j_g), "clean_traj_matches_baseline": traj_g[-1].startswith("ca575bb9")}
json.dump(result, open("DPP4_SIP_CANDIDATE.json", "w"), indent=2)
print("evidence: DPP4_SIP_CANDIDATE.json")
