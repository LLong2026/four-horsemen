#!/usr/bin/env python3
"""SQUIRL OS INGESTION GUARD v1 — deployed per SIP approval (Leon GO, Oct 13, 2026, 11:22 CT).
Reject-not-coerce validation at anomaly ingestion, per DPP-4 findings.
Runtime patch ONLY: the registered instruments (frozen corpus/mesh/roster/replay,
LINDY-B runner) are untouched.
Conforming-identity receipt: clean corpus through guarded engine byte-identical
to frozen baseline (2646 crossings, trajectory ca575bb9) — DPP4_SIP_CANDIDATE.json."""
import math

ROSTER_TYPES = {"latency_spike", "heartbeat_miss", "quantum_vulnerability_detected"}

def metric_field(anomaly_type):
    if anomaly_type == "latency_spike": return "latency_ms"
    if anomaly_type == "heartbeat_miss": return "error_count"
    return "cpu"

def validate_record(record, seen_ids=None):
    """Returns (action, reason). action in {'accept','structural_hold'}.
    Checks: instance_id presence (+ uniqueness vs seen_ids set, if provided),
    anomaly_type known, consumed metric numeric/finite/non-negative."""
    iid = record.get("instance_id")
    if not iid or not isinstance(iid, str) or not iid.strip():
        return ("structural_hold", "instance_id_missing_or_malformed")
    if seen_ids is not None:
        if iid in seen_ids:
            return ("structural_hold", "instance_id_duplicate")
        seen_ids.add(iid)  # every PRESENTED id counts, even if the record is later held (fail-closed)
    t = record.get("anomaly_type")
    if t not in ROSTER_TYPES:
        return ("structural_hold", "anomaly_type_not_in_roster")
    f = metric_field(t)
    v = record.get(f)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return ("structural_hold", f"metric_{f}_not_numeric")
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return ("structural_hold", f"metric_{f}_non_finite")
    if v < 0:
        return ("structural_hold", f"metric_{f}_negative")
    return ("accept", "conforming")

# self-test on DPP-4 poison classes (deployment verification)
if __name__ == "__main__":
    cases = [
        ({"instance_id": "OK-1", "anomaly_type": "latency_spike", "latency_ms": 187}, "accept"),
        ({"instance_id": "OK-2", "anomaly_type": "latency_spike", "latency_ms": "187"}, "structural_hold"),
        ({"instance_id": "OK-3", "anomaly_type": "latency_spike", "latency_ms": "187,5"}, "structural_hold"),
        ({"instance_id": "OK-4", "anomaly_type": "heartbeat_miss", "error_count": float("nan")}, "structural_hold"),
        ({"instance_id": "OK-5", "anomaly_type": "latency_spike", "latency_ms": float("inf")}, "structural_hold"),
        ({"instance_id": "OK-6", "anomaly_type": "latency_spike", "latency_ms": -500}, "structural_hold"),
        ({"instance_id": "OK-7", "anomaly_type": None, "latency_ms": 100}, "structural_hold"),
        ({"instance_id": "OK-8", "anomaly_type": "latency_spike"}, "structural_hold"),
        ({"anomaly_type": "latency_spike", "latency_ms": 100}, "structural_hold"),
        ({"instance_id": "OK-9", "anomaly_type": "latency_spike", "latency_ms": 210}, "accept"),
    ]
    seen = set()
    fails = 0
    for rec, expected in cases:
        got, reason = validate_record(rec, seen)
        ok = got == expected
        fails += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'}: expected {expected}, got {got} ({reason})")
    print(f"\nDEPLOYMENT SELF-TEST: {'ALL PASS' if fails == 0 else f'{fails} FAILURES'}")
    raise SystemExit(0 if fails == 0 else 1)
