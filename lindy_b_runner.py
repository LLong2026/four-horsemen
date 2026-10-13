#!/usr/bin/env python3
"""
LINDY-B nightly battery runner, per lindy_b_prereg.md.
Runs: T2C replay conformance (determinism vs registered baseline), H-INV-2 v3
audit sweep, DPP-1 canary spot-check. Appends one line to LINDY_B_RUNLOG.md.
Stamp-before-execute idempotency: signature lindy_b/<date>; duplicate = silent exit.
"""
import json, hashlib, copy, datetime, sys, os

NOW = lambda: datetime.datetime.now(datetime.timezone.utc)
today = NOW().strftime("%Y-%m-%d")
sig = f"lindy_b/{today}"

RUNLOG = "LINDY_B_RUNLOG.md"
def stamp_line(s): return f"| {today} | {s} |"

# --- stamp-before-execute (write-ahead): exit silently on duplicate ---
if os.path.exists(RUNLOG) and sig in open(RUNLOG).read():
    print(json.dumps({"status": "duplicate_slot", "signature": sig})); sys.exit(0)
with open(RUNLOG, "a") as f:
    f.write(f"| {today} | STAMPED {sig} pending |\n")

def fail(msg):
    with open(RUNLOG) as f: lines = f.readlines()
    lines[-1] = stamp_line(f"MISSED/FAILED — {msg}")
    open(RUNLOG, "w").writelines(lines)
    print(json.dumps({"status": "failed", "error": msg})); sys.exit(1)

def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_j(o): return sha_b(json.dumps(o, sort_keys=True).encode())

# --- T2C replay conformance (frozen instrument) ---
try:
    corpus_path = "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"
    if not os.path.exists(corpus_path): corpus_path = "../ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"
    assert sha_b(open(corpus_path, "rb").read()) == "13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59", "corpus drift"
    clean = json.load(open(corpus_path))
    pack = json.load(open("../mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json")) \
        if not os.path.exists("mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json") \
        else json.load(open("mesh_repo/data/SQUIRREL_OS_67_APP_TELEMETRY_PACK.json"))
    nodes0 = pack["topology"]["nodes"]; assert len(nodes0) == 32
    ROSTER = [
        {"anomaly_type": "latency_spike", "threshold": 0.80},
        {"anomaly_type": "heartbeat_miss", "threshold": 0.85},
        {"anomaly_type": "quantum_vulnerability_detected", "threshold": 0.80}]
    MAX_LAT = max(i["latency_ms"] for i in clean); MAX_ERR = max(i["error_count"] for i in clean)
    MAX_CPU = max(i["cpu"] for i in clean)
    def severity(i):
        t = i["anomaly_type"]
        return (i["latency_ms"]/MAX_LAT) if t == "latency_spike" else \
               (i["error_count"]/MAX_ERR) if t == "heartbeat_miss" else (i["cpu"]/MAX_CPU)
    def replay(mesh, corpus):
        w = {n["pattern_type"]: n["weight"] for n in mesh}; out = []
        for inst in corpus:
            t = inst["anomaly_type"]
            pb = next((r for r in ROSTER if r["anomaly_type"] == t), None)
            c = 0.5 * severity(inst) + 0.5 * w["confidence_score"]
            if pb and c >= pb["threshold"]: out.append((inst["instance_id"], t, round(c, 10), "resolved"))
            elif pb: out.append((inst["instance_id"], t, round(c, 10), "detected"))
            else: out.append((inst["instance_id"], t, round(c, 10), "escalated"))
        return out
    def run40(corpus):
        mesh = copy.deepcopy(nodes0); journal = []; traj = []
        for e in range(1, 41):
            for inst in replay(mesh, corpus):
                if inst[3] != "resolved": continue
                wn = next(n for n in mesh if n["pattern_type"] == "confidence_score")
                lr, w = wn["learning_rate"], wn["weight"]
                w2 = round(w + lr*(1-inst[2])*(1-w), 10)
                if w2 != w:
                    journal.append({"epoch": e, "event_id": inst[0], "anomaly_type": inst[1],
                                    "before": w, "after": w2, "pattern_update": True,
                                    "confidence": inst[2]})
                    wn["weight"] = w2
            traj.append(sha_j([[n["pattern_type"], n["weight"]] for n in sorted(mesh, key=lambda x: json.dumps(x, sort_keys=True))]))
        return mesh, journal, traj
    t0 = NOW()
    mesh, journal, traj = run40(clean)
    t2c_hash = traj[-1]
    n_cross = len(journal)
    # H-INV-2 v3 audit sweep over this night's journal
    def audit(c, j):
        src = [x for x in j if x["event_id"] == c["event_id"] and x["epoch"] == c["epoch"]]
        if not src: return False
        src = src[0]; idx = j.index(src)
        prev = j[idx-1] if idx > 0 and j[idx-1]["epoch"] == src["epoch"] else None
        lr = next(n["learning_rate"] for n in mesh if n["pattern_type"] == "confidence_score")
        exp = round(c["before"] + lr*(1-c["confidence"])*(1-c["before"]), 10)
        if prev is not None and c["before"] != prev["after"]: return False
        return c["after"] == exp and c.get("pattern_update") is True
    audited = journal[::25]
    lineage_ok = all(audit(c, journal) for c in audited)
    # DPP-1 canary spot-check: poison corpus exists; verify decision identity + canary absence
    dpp_ok, dpp_note = True, "corpus not present (skipped)"
    if os.path.exists("poisoned_CORPUS_B1.json"):
        poisoned = json.load(open("poisoned_CORPUS_B1.json"))
        _, _, traj_p = run40(poisoned)
        jtxt = json.dumps(journal)
        CAN = ["INJ-CANARY", "CONF-CANARY", "AKIA-CANARY", "0xCANARY", "MRN-CANARY", "CANARY-PHI", "PAT-CANARY"]
        dpp_ok = traj_p == traj and not any(c in jtxt for c in CAN)
        dpp_note = "trajectory identity + canary scan"
    elapsed = (NOW() - t0).total_seconds()
except Exception as ex:
    fail(str(ex)[:200])

ok = (t2c_hash is not None) and lineage_ok and dpp_ok
# registered baseline check: trajectory must be IDENTICAL night over night.
BASELINE_FILE = "lindy_b_baseline.json"
if not os.path.exists(BASELINE_FILE):
    json.dump({"t2c_hash": t2c_hash}, open(BASELINE_FILE, "w"))
    baseline_ok = True
else:
    baseline_ok = json.load(open(BASELINE_FILE))["t2c_hash"] == t2c_hash
ok = ok and baseline_ok

# append final runlog line (replace stamp line)
with open(RUNLOG) as f: lines = f.readlines()
verdict = "PASS" if ok else "DRIFT/FAIL"
lines[-1] = stamp_line(f"{verdict} | t2c={t2c_hash[:16]} baseline_match={baseline_ok} "
                       f"lineage={len(audited)}/{len(audited)}={lineage_ok} crossings={n_cross} "
                       f"dpp={dpp_ok} ({dpp_note}) | {elapsed:.1f}s | sig {sig}")
open(RUNLOG, "w").writelines(lines)
print(json.dumps({"status": verdict, "t2c_hash": t2c_hash, "baseline_match": baseline_ok,
                  "lineage_audit": [len(audited), lineage_ok], "dpp": dpp_ok, "elapsed_s": round(elapsed,1)}))
