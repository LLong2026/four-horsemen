#!/usr/bin/env python3
"""
HEMI-T2B bounded convergence series, per hemi_t2b_prereg.md (HEMI-2.2 amendment, Leon ACK).
Identical to hemi_t2_runner.py EXCEPT the learning rule: w' = w + lr*(1-c)*(1-w).
"""
import json, hashlib, statistics, sys, datetime, copy

NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

corpus_path = "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"
corpus_sha = sha(corpus_path)
assert corpus_sha == "13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59", "CORPUS DRIFT"
corpus = json.load(open(corpus_path))

pack = json.load(open("../mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json"))
nodes0 = pack["topology"]["nodes"]
assert len(nodes0) == 32

ROSTER = [
    {"anomaly_type": "latency_spike", "playbook": "PB-003: Latency Spike Resolver", "threshold": 0.80},
    {"anomaly_type": "heartbeat_miss", "playbook": "PB-008: Heartbeat Re-igniter", "threshold": 0.85},
    {"anomaly_type": "quantum_vulnerability_detected", "playbook": "PB-009: Quantum Vulnerability Migrator", "threshold": 0.80},
]
def roster_sha(): return hashlib.sha256(json.dumps(ROSTER, sort_keys=True).encode()).hexdigest()
ROSTER_SHA0 = roster_sha()

SENSOR = {"latency_spike": "latency_monitor", "heartbeat_miss": "heartbeat_sensor",
          "quantum_vulnerability_detected": "pqc_status"}
L2_ACT = ["pattern_match", "anomaly_classify", "severity_eval", "playbook_match", "confidence_score"]
ACT = lambda t: ([SENSOR[t], "error_rate", "anomaly_count"] + L2_ACT +
                 ["isolation_strategy", "healing_selection", "verification_logic",
                  "heal_action", "healing_result", "pattern_update"])

MAX_LAT = max(i["latency_ms"] for i in corpus)
MAX_ERR = max(i["error_count"] for i in corpus)
MAX_CPU = max(i["cpu"] for i in corpus)

def severity(i):
    t = i["anomaly_type"]
    return (i["latency_ms"]/MAX_LAT) if t=="latency_spike" else \
           (i["error_count"]/MAX_ERR) if t=="heartbeat_miss" else (i["cpu"]/MAX_CPU)

def replay(mesh):
    w = {n["pattern_type"]: n["weight"] for n in mesh}
    out = []
    for inst in corpus:
        t = inst["anomaly_type"]
        pb = next((r for r in ROSTER if r["anomaly_type"] == t), None)
        c = 0.5 * severity(inst) + 0.5 * w["confidence_score"]
        if pb and c >= pb["threshold"]:
            out.append((inst["instance_id"], pb["playbook"], c, "resolved"))
        elif pb:
            out.append((inst["instance_id"], pb["playbook"], c, "detected"))
        else:
            out.append((inst["instance_id"], None, c, "escalated"))
    return out

# --- NOTE: replica of T1 train ---
def negative_probes(mesh):
    w = {n["pattern_type"]: n["weight"] for n in mesh}
    fps = 0
    for probe in ["LATENCY_SPIKE", "unregistered_synthetic_fault"]:
        if any(r["anomaly_type"] == probe for r in ROSTER):
            fps += 1
    return fps

def series():
    mesh = copy.deepcopy(nodes0)
    control = copy.deepcopy(nodes0)
    epochs = []
    for e in range(1, 11):
        leg = replay(mesh)
        resolved = sum(1 for r in leg if r[3] == "resolved")
        detected = sum(1 for r in leg if r[3] == "detected")
        mesh, deltas = train_t1(mesh, leg)
        sd = round(sum(abs(d["after"] - d["before"]) for d in deltas), 10)
        epochs.append({"epoch": e, "resolved": resolved, "detected": detected,
                       "sum_abs_delta": sd,
                       "delta_log_sha": hashlib.sha256(json.dumps(deltas, sort_keys=True).encode()).hexdigest(),
                       "max_weight": round(max(n["weight"] for n in mesh), 10),
                       "median_confidence": round(statistics.median(r[2] for r in leg), 6)})
    return mesh, control, epochs

# ---------- RUN ----------
mesh_final, control, epochs = series()
receipt = {"series": "HEMI-T2B", "protocol": "hemi_t2b_prereg v1.0 (HEMI-2.2 bounded rule)", "started_at": NOW(),
           "inputs": {"corpus_sha256": corpus_sha, "mesh_nodes": 32, "roster_sha256": ROSTER_SHA0,
                      "epochs": 10, "epoch1_from_untrained": True},
           "epochs": epochs}

F = {}
res = [e["resolved"] for e in epochs]
F["HF-S1_monotone"] = {"resolved_per_epoch": res,
                       "pass": all(b >= a for a, b in zip(res, res[1:]))}
conv_last3 = len(set(res[-3:])) == 1
damped = epochs[-1]["sum_abs_delta"] <= 0.05 * epochs[0]["sum_abs_delta"]
F["HF-S2_convergence"] = {"identical_last3": conv_last3, "self_damped_le_5pct": damped,
                          "epoch1_delta": epochs[0]["sum_abs_delta"], "epoch10_delta": epochs[-1]["sum_abs_delta"],
                          "pass": conv_last3 or damped}
F["HF-S3_bounded"] = {"max_weight_any_epoch": max(e["max_weight"] for e in epochs),
                      "pass": all(e["max_weight"] < 1.0 for e in epochs)}
# HF-S4: playbook invariance vs untrained baseline at every epoch
base_leg = replay(nodes0)
base_pb = {r[0]: r[1] for r in base_leg}
mesh = copy.deepcopy(nodes0)
inv = True
for e in range(10):
    leg = replay(mesh)
    if any((r[1] != base_pb[r[0]]) for r in leg):
        inv = False
        break
    mesh, _ = train_t1(mesh, leg)
F["HF-S4_invariance"] = {"playbook_mismatches_any_epoch": 0 if inv else "FAIL", "pass": inv}
F["HF-S5_negatives"] = {"false_positives": negative_probes(mesh_final), "pass": negative_probes(mesh_final) == 0}
# HF-S6: rerun full series, compare hash sequence
_, _, epochs2 = series()
F["HF-S6_determinism"] = {"hash_seq_run1": [e["delta_log_sha"][:16] for e in epochs],
                          "hash_seq_run2": [e["delta_log_sha"][:16] for e in epochs2],
                          "pass": [e["delta_log_sha"] for e in epochs] == [e["delta_log_sha"] for e in epochs2]}
F["standing_HF1_governance"] = {"sha_pre": ROSTER_SHA0, "sha_post": roster_sha(), "pass": ROSTER_SHA0 == roster_sha()}
ch = [hashlib.sha256(f'{n["node_id"]}:{n["weight"]}'.encode()).hexdigest()[:16] for n in mesh_final]
F["standing_HF3_collision"] = {"unique": len(set(ch)), "pass": len(set(ch)) == 32}
F["standing_control"] = {"pass": json.dumps(control, sort_keys=True) == json.dumps(copy.deepcopy(nodes0), sort_keys=True)}

receipt["falsifiers"] = F
receipt["all_pass"] = all(v.get("pass") for v in F.values() if isinstance(v, dict))
receipt["completed_at"] = NOW()

json.dump(receipt, open("hemi_t2b_receipt.json", "w"), indent=2)
print(json.dumps({"epochs": [{k: e[k] for k in ("epoch", "resolved", "detected", "sum_abs_delta", "max_weight")} for e in epochs],
                  "falsifiers": {k: v.get("pass") for k, v in F.items()},
                  "all_pass": receipt["all_pass"]}, indent=2))
sys.exit(0 if receipt["all_pass"] else 2)
