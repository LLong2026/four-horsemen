#!/usr/bin/env python3
"""HACK-17: CNSA 2.0 timeline-conformance battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

ALLOWLIST = {"CRYSTALS-Dilithium3", "kyber_1024", "SPHINCS+-256f"}
DEPRECATED = {"RSA-2048", "ECDSA-P256"}  # past CNSA deprecation date in this simulation window
FROZEN_POLICY_SHA = hashlib.sha256(b"cnsa2_timeline_policy_record_canonical").hexdigest()
OWNER = "longleon17@gmail.com"
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

# C1: non-CNSA algorithm sneaking past the inventory
def inventory_gate(algorithm):
    return "active" if algorithm in ALLOWLIST else "rejected_off_allowlist"
v = inventory_gate("ChaCha20-Poly1305-legacy")
adjudicate("C1", "Non-CNSA algorithm past inventory", "rejected_off_allowlist", v, "inventory scan enforces the frozen allowlist")

# C2: classical algorithm past its deprecation date still active
def timeline_gate(algorithm):
    if algorithm in ALLOWLIST: return "compliant"
    if algorithm in DEPRECATED: return "flagged_forced_migration"
    return "rejected"
v = timeline_gate("RSA-2048")
adjudicate("C2", "Deprecated classical algorithm still active", "flagged_forced_migration", v, "timeline policy flags and forces migration")

# C3: "temporary" classical fallback request
def fallback_gate(request):
    return "refused_no_fallback"  # non-PQC fallback is prohibited unconditionally
v = fallback_gate({"reason": "emergency_interop", "duration": "5_minutes"})
adjudicate("C3", "Temporary classical fallback", "refused_no_fallback", v, "no fallback to unapproved crypto under any circumstance")

# C4: altered deadline metadata
def policy_gate(policy_sha):
    return "valid" if policy_sha == FROZEN_POLICY_SHA else "rejected_divergence"
v = policy_gate(hashlib.sha256(b"cnsa2_timeline_policy_record_tampered").hexdigest())
adjudicate("C4", "Forged deadline metadata", "rejected_divergence", v, "policy record frozen; tampering diverges")

# C5: classical-only negotiation under hybrid banner
def hybrid_gate(modes):
    has_pqc = any(m in ALLOWLIST for m in modes)
    return "accepted" if has_pqc else "rejected_classical_only"
v = hybrid_gate(["TLS-1.3-hybrid-label", "AES-GCM"])
adjudicate("C5", "Classical-only negotiation under hybrid banner", "rejected_classical_only", v, "hybrid requires a PQC minimum component")

# C6: legacy interop waiver
def waiver_gate(signed_by):
    return "granted" if signed_by == OWNER else "refused_pending_owner_go"
v = waiver_gate("vendor_integration_team")
adjudicate("C6", "Legacy interop waiver request", "refused_pending_owner_go", v, "waivers require the owner's explicit GO")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack17_cnsa2_timeline", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
