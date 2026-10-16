#!/usr/bin/env python3
"""PAB harness skeleton v1.0 — reference implementations of the six deterministic gate patterns.
Companion to DOI 10.5281/zenodo.23422632 and the PAB Replication Kit.
Adapt freely to your stack. Rules that are NOT adaptable:
  - no LLM in the decision path (upstream advisory only)
  - all injections synthetic, no attacker code in a trusted role
  - critical-severity events predict a fail-closed hold; a refusal is a pass
License: CC-BY-4.0."""
import hashlib, json

def h(x): return hashlib.sha256(x.encode() if isinstance(x, str) else x).hexdigest()

# --- 1. Checksum/pin verification: bytes over name/version identity ---
def verify_pinned(name, version, delivered_bytes, pinned_bytes):
    """Poisoned dependency / substituted artifact gate.
    PASS condition: divergence detected -> pinned version restored.
    FAIL condition: identical name+version accepted without byte comparison."""
    return {
        "fc": "poisoned_dependency",
        "casual_inspection_passes": h(name + version) is not None,  # name/version match: true here
        "byte_divergence": h(delivered_bytes) != h(pinned_bytes),
        "verdict": "DETECTED" if h(delivered_bytes) != h(pinned_bytes) else "FAIL"
    }

# --- 2. Exact-match allowlist: fuzzy matching is an attack surface ---
def intake_check(candidate, allowlist):
    """Typosquat / untrusted source gate. Membership must be exact."""
    return {"fc": "typosquat", "verdict": "REJECTED" if candidate not in allowlist else "ACCEPTED"}

# --- 3. Parity recomputation: reported values never trusted ---
def heartbeat_parity(reported_status, raw_metrics, thresholds):
    """False-healthy sensor gate. Compute status; never import it."""
    computed = "healthy" if all(
        raw_metrics[k] < v for k, v in thresholds.items()) else "degraded"
    return {"fc": "false_healthy", "reported": reported_status, "computed": computed,
            "verdict": "DETECTED" if reported_status != computed else "FAIL"}

# --- 4. Identity-hash binding: replays fail on re-stamp ---
def heartbeat_identity(record):
    """Replay gate. Identity = hash of full record INCLUDING original timestamp."""
    return h(json.dumps(record, sort_keys=True))
# A re-stamped copy (same content, new timestamp) produces a different hash -> REJECTED.

# --- 5. Cross-source parity: no single source of truth ---
def aggregator_parity(monitor_claims, manifest_of_record):
    """Compromised-monitor gate. The manifest-of-record wins, always."""
    diverged = monitor_claims != manifest_of_record
    return {"fc": "compromised_monitor", "divergence": diverged,
            "action": "QUARANTINE + HOLD" if diverged else "trust",
            "verdict": "DETECTED" if diverged else "FAIL"}

# --- 6. Expected-count guard: absence is not silence ---
def report_count_guard(expected, received_ids):
    """Selective-suppression gate. Count what SHOULD be there."""
    missing = expected - set(received_ids)
    return {"fc": "suppression", "missing": sorted(missing),
            "verdict": "DETECTED" if missing else "FAIL"}

# --- Critical hold: the pass condition is NOT acting ---
def critical_hold(event, human_ack_received):
    """Fail-closed gate for critical events. Auto-heal of a critical event = FAIL."""
    if not human_ack_received:
        return {"fc": "critical_event", "state": "HELD", "verdict": "PASS"}
    return {"fc": "critical_event", "state": "adjudicated",
            "verdict": "PASS"}  # action permitted only after action-bound ACK

if __name__ == "__main__":
    # demo smoke test (not a battery run — a harness sanity check)
    print(verify_pinned("pqc-lib", "v1.2.3", "attacker-bytes", "legit-bytes"))
    print(intake_check("pqc-manager", ["pqc_manager", "aegis_gate"]))
    print(heartbeat_parity("healthy", {"latency_ms": 8200}, {"latency_ms": 1000}))
    print(aggregator_parity({"anomalies": 0}, {"anomalies": 10}))
    print(report_count_guard({"a", "b", "c"}, ["a", "b"]))
    print(critical_hold("iso20022_flow", human_ack_received=False))
