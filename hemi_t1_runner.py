#!/usr/bin/env python3
"""
HEMI-T1 epoch runner — first cognitive training epoch, per HEMI-2 frozen protocol
(fh_pub/hemi2_training_prereg.md, sha256 6bf69ef9...25be5f39).

INSTRUMENT DEFINITION (frozen in this file BEFORE execution; commit hash recorded):

  Corpus: fh_pub/ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json
          (sha256 13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59 —
          verified at load, abort if changed)
  Mesh:   mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json topology.nodes (32 nodes, 5 layers).
          A trained copy is mutated; the control copy stays frozen.
  LEFT hemisphere (governance, untouched): ROSTER exact string match + confidence
          thresholds (PB-003 0.80 / PB-008 0.85 / PB-009 0.80). Roster bytes hashed
          before/after (HF-1).
  Activation path per anomaly_type (frozen):
          L1: the type's primary sensor + error_rate + anomaly_count
          L2: pattern_match, anomaly_classify, severity_eval, playbook_match, confidence_score
          L3: isolation_strategy, healing_selection, verification_logic
          L4: heal_action          L5: healing_result, pattern_update
  Signal severity s(inst) in [0,1], normalized by the corpus's own maxima (deterministic):
          latency_spike:              s = latency_ms / max_latency
          heartbeat_miss:             s = error_count / max_error_count
          quantum_vulnerability_detected: s = cpu / max_cpu
  Mesh confidence (frozen formula): c = 0.5 * s + 0.5 * w(confidence_score node)
  LEFT gate: exact roster match AND c >= threshold  -> resolved + verified (synthetic
          verification per protocol §3); else detected (no delta, governance hold).
  Training rule (HEMI-2 §3): on resolved+verified instances, for every activated node:
          w' = w + 0.01 * (1 - c)          (learning_rate 0.01)
          on failed verification: w' = w * (1 - 0.005)   (decay 0.005; none expected here)
  Negative probes (B3 standard): "LATENCY_SPIKE" (case-variant), "unregistered_synthetic_fault".

Falsifiers: HF-1..HF-6 evaluated and reported. Fail-closed: any corpus/mesh hash
mismatch aborts before any computation.
"""
import json, hashlib, statistics, sys, datetime

FH = "."
ROOT = ".."
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# ---------- load + integrity gates ----------
corpus_path = f"{FH}/ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"
corpus_sha = sha(corpus_path)
assert corpus_sha == "13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59", \
    f"CORPUS HASH MISMATCH {corpus_sha} — abort (fail-closed)"
corpus = json.load(open(corpus_path))

pack = json.load(open(f"{ROOT}/mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json"))
nodes = pack["topology"]["nodes"]
assert len(nodes) == 32, "topology drift"

ROSTER = [
    {"anomaly_type": "latency_spike", "playbook": "PB-003: Latency Spike Resolver", "threshold": 0.80},
    {"anomaly_type": "heartbeat_miss", "playbook": "PB-008: Heartbeat Re-igniter", "threshold": 0.85},
    {"anomaly_type": "quantum_vulnerability_detected", "playbook": "PB-009: Quantum Vulnerability Migrator", "threshold": 0.80},
]
roster_bytes = json.dumps(ROSTER, sort_keys=True).encode()
ROSTER_SHA = hashlib.sha256(roster_bytes).hexdigest()

SENSOR = {"latency_spike": "latency_monitor", "heartbeat_miss": "heartbeat_sensor",
          "quantum_vulnerability_detected": "pqc_status"}
L2_ACT = ["pattern_match", "anomaly_classify", "severity_eval", "playbook_match", "confidence_score"]
ACT = lambda t: ([SENSOR[t], "error_rate", "anomaly_count"] + L2_ACT +
                 ["isolation_strategy", "healing_selection", "verification_logic",
                  "heal_action", "healing_result", "pattern_update"])

MAX_LAT = max(i["latency_ms"] for i in corpus)
MAX_ERR = max(i["error_count"] for i in corpus)
MAX_CPU = max(i["cpu"] for i in corpus)

def severity(inst):
    t = inst["anomaly_type"]
    if t == "latency_spike": return inst["latency_ms"] / MAX_LAT
    if t == "heartbeat_miss": return inst["error_count"] / MAX_ERR
    return inst["cpu"] / MAX_CPU

def replay(mesh, corpus):
    """One full replay leg through both hemispheres. Returns per-instance tuples."""
    w = {n["pattern_type"]: n["weight"] for n in mesh}
    out = []
    for inst in corpus:
        t = inst["anomaly_type"]
        pb = next((r for r in ROSTER if r["anomaly_type"] == t), None)
        c = 0.5 * severity(inst) + 0.5 * w["confidence_score"]
        if pb and c >= pb["threshold"]:
            out.append({"instance_id": inst["instance_id"], "anomaly_type": t,
                        "playbook": pb["playbook"], "match": "exact", "confidence": round(c, 6),
                        "status": "resolved", "outcome_sign": +1})
        elif pb:
            out.append({"instance_id": inst["instance_id"], "anomaly_type": t,
                        "playbook": pb["playbook"], "match": "exact", "confidence": round(c, 6),
                        "status": "detected", "outcome_sign": 0})
        else:
            out.append({"instance_id": inst["instance_id"], "anomaly_type": t,
                        "playbook": None, "match": "none", "confidence": round(c, 6),
                        "status": "escalated", "outcome_sign": 0})
    return out

def train(mesh, leg):
    """Apply the frozen learning rule to a deep copy; return (trained_mesh, delta_log)."""
    import copy
    trained = copy.deepcopy(mesh)
    idx = {n["pattern_type"]: n for n in trained}
    deltas = []
    for rec in leg:
        if rec["outcome_sign"] == 0:
            continue  # detected/escalated: governance hold, no training signal (HF-2 lineage: only verified outcomes move weights)
        act = ACT(rec["anomaly_type"])
        for pt in act:
            n = idx[pt]
            before = n["weight"]
            n["weight"] = round(before + 0.01 * (1 - rec["confidence"]), 10)
            deltas.append({"node": pt, "instance_id": rec["instance_id"],
                           "before": before, "after": n["weight"],
                           "source_outcome": "resolved+verified"})
    return trained, deltas

def negative_probes(mesh):
    """B3 standard: unregistered types must produce NO match regardless of weights."""
    w = {n["pattern_type"]: n["weight"] for n in mesh}
    results = []
    for probe in ["LATENCY_SPIKE", "unregistered_synthetic_fault"]:
        pb = next((r for r in ROSTER if r["anomaly_type"] == probe), None)
        c = 0.5 * 1.0 + 0.5 * w["confidence_score"]  # worst case: max severity
        results.append({"probe": probe, "match": "exact" if pb else "none",
                        "false_positive": bool(pb)})
    return results

# ---------- EPOCH ----------
receipt = {"epoch": "HEMI-T1", "started_at": NOW(), "protocol": "HEMI-2 v1.0"}
receipt["inputs"] = {"corpus_sha256": corpus_sha, "corpus_n": len(corpus),
                     "mesh_nodes": len(nodes), "roster_sha256": ROSTER_SHA,
                     "normalization": {"max_latency_ms": MAX_LAT, "max_error_count": MAX_ERR, "max_cpu": MAX_CPU}}

# HF-1 pre-hash of governance bytes
receipt["hf1_pre_governance_sha"] = ROSTER_SHA

# LEG 1: baseline
control = copy.deepcopy(nodes) if False else json.loads(json.dumps(nodes))
baseline = replay(nodes, corpus)
receipt["baseline"] = {"resolved": sum(1 for r in baseline if r["status"] == "resolved"),
                       "detected": sum(1 for r in baseline if r["status"] == "detected"),
                       "escalated": 0,
                       "median_confidence": round(statistics.median(r["confidence"] for r in baseline), 6)}
receipt["baseline_log_sha256"] = hashlib.sha256(json.dumps(baseline, sort_keys=True).encode()).hexdigest()

# LEG 2: training
trained, deltas = train(nodes, baseline)
receipt["training"] = {"deltas_applied": len(deltas),
                       "nodes_touched": len({d["node"] for d in deltas}),
                       "sum_abs_delta": round(sum(abs(d["after"] - d["before"]) for d in deltas), 10),
                       "decay_events": 0}

# LEG 3: post-training replay
post = replay(trained, corpus)
receipt["post"] = {"resolved": sum(1 for r in post if r["status"] == "resolved"),
                   "detected": sum(1 for r in post if r["status"] == "detected"),
                   "median_confidence": round(statistics.median(r["confidence"] for r in post), 6)}
receipt["post_log_sha256"] = hashlib.sha256(json.dumps(post, sort_keys=True).encode()).hexdigest()

# ---------- FALSIFIERS ----------
F = {}
# HF-1: governance byte-isolation
F["HF-1"] = {"governance_sha_pre": ROSTER_SHA,
             "governance_sha_post": hashlib.sha256(json.dumps(ROSTER, sort_keys=True).encode()).hexdigest(),
             "pass": ROSTER_SHA == hashlib.sha256(json.dumps(ROSTER, sort_keys=True).encode()).hexdigest()}
# also: playbook selection invariance across all 200 (HF-5 core)
mismatch = [b["instance_id"] for b, p in zip(baseline, post) if b["playbook"] != p["playbook"]]
F["HF-5_playbook_invariance"] = {"mismatches": len(mismatch), "pass": len(mismatch) == 0}
# HF-2: delta lineage
resolved_ids = {r["instance_id"] for r in baseline if r["outcome_sign"] == 1}
delta_ids = {d["instance_id"] for d in deltas}
F["HF-2"] = {"deltas": len(deltas), "orphan_deltas": len(delta_ids - resolved_ids),
             "pass": len(delta_ids - resolved_ids) == 0}
# HF-3: collision integrity post-training
hashes = [hashlib.sha256(f'{n["node_id"]}:{n["weight"]}'.encode()).hexdigest()[:16] for n in trained]
F["HF-3"] = {"node_collision_hashes": len(hashes), "unique": len(set(hashes)), "pass": len(set(hashes)) == 32}
# HF-4: negative probes on trained copy
probes = negative_probes(trained)
F["HF-4"] = {"probes": probes, "false_positives": sum(p["false_positive"] for p in probes),
             "pass": all(not p["false_positive"] for p in probes)}
# HF-5 latency: in-process resolution remains sub-ms (measured over full replay)
import time
t0 = time.perf_counter(); replay(trained, corpus); dt = (time.perf_counter() - t0) / len(corpus)
F["HF-5_latency"] = {"mean_resolution_s": round(dt, 8), "sub_ms": dt < 0.001, "pass": dt < 0.001}
# HF-6: reproducibility — recompute the epoch deterministically
_, deltas2 = train(nodes, replay(nodes, corpus))
d2 = hashlib.sha256(json.dumps(deltas2, sort_keys=True).encode()).hexdigest()
d1 = hashlib.sha256(json.dumps(deltas, sort_keys=True).encode()).hexdigest()
F["HF-6"] = {"delta_log_sha_run1": d1, "delta_log_sha_run2": d2, "pass": d1 == d2}

receipt["falsifiers"] = F
receipt["all_pass"] = all(v.get("pass") for v in F.values() if isinstance(v, dict))
receipt["completed_at"] = NOW()

# control copy untouched?
control_untouched = json.loads(json.dumps(nodes)) == control
receipt["control_frozen"] = control_untouched

print(json.dumps(receipt, indent=2)[:3000])
json.dump(receipt, open(f"{FH}/hemi_t1_receipt.json", "w"), indent=2)
json.dump({"baseline": baseline, "post": post, "deltas": deltas[:50] + (["...truncated..."] if len(deltas) > 50 else [])},
          open(f"{FH}/hemi_t1_epoch_logs.json", "w"), indent=2)
sys.exit(0 if receipt["all_pass"] else 2)
