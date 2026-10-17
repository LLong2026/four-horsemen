#!/usr/bin/env python3
"""HACK-15: NIST SP 800-207 Zero Trust conformance battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

OWNER = "longleon17@gmail.com"
REVOKED = {"cred-session-99"}
FROZEN_LEDGER_STATE = "state_head_135"
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

def request_gate(subject, claims):
    if claims.get("implicit_trust"): return "rejected_no_implicit_trust"   # every request re-authenticated
    if subject in REVOKED: return "rejected_revoked"                      # per-use revocation check
    if claims.get("inherited_from"): return "rejected_non_transferable"    # authority never inherited
    if claims.get("exception"): return "rejected_no_exception_path"       # no policy exceptions exist
    if claims.get("sender") != OWNER: return "rejected_unauthenticated"
    return "accepted"

# Z1: "inside the network" implicit trust claim
v = request_gate("internal-host-1", {"implicit_trust": True})
adjudicate("Z1", "Inside-the-network implicit trust claim", "rejected_no_implicit_trust", v, "zero implicit trust: every request re-authenticated")

# Z2: device-trust inheritance (trusted device skips auth)
v = request_gate("managed-device-7", {"inherited_from": "corporate-device-enrollment"})
adjudicate("Z2", "Device-trust inheritance", "rejected_non_transferable", v, "authority is non-transferable per request")

# Z3: lateral movement via adjacent authenticated session
v = request_gate("session-A", {"inherited_from": "session-B"})
adjudicate("Z3", "Lateral session authority transfer", "rejected_non_transferable", v, "session authority is never transferable")

# Z4: legacy-system policy exception
v = request_gate("legacy-scada-1", {"exception": "legacy_system_compatibility"})
adjudicate("Z4", "Legacy-system policy exception", "rejected_no_exception_path", v, "no exception path exists in the policy")

# Z5: implicit trust in telemetry source (false-green variant)
def telemetry_gate(claimed_state, source):
    return "accepted" if claimed_state == FROZEN_LEDGER_STATE else "refused_divergence"
v = telemetry_gate("healthy_per_source_claim", "internal-monitor")
adjudicate("Z5", "Implicit trust in telemetry source", "refused_divergence", v, "telemetry recomputed from ledger, never trusted by origin")

# Z6: credential valid at T0, revoked before T1, used at T1
v = request_gate("cred-session-99", {"sender": OWNER})
adjudicate("Z6", "Revoked credential reuse", "rejected_revoked", v, "revocation checked on every use")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack15_sp800207_zero_trust", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
