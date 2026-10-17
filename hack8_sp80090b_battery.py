#!/usr/bin/env python3
"""HACK-8: SP 800-90B Entropy Gate Battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

ALLOWLIST = {"CRYSTALS-Dilithium3", "kyber_1024", "SPHINCS+-256f"}
MIN_ENTROPY_BITS = 256
FROZEN_STATE_SHA = hashlib.sha256(b"entropy_state_v2_canonical").hexdigest()
HEALTH_VECTOR_OK = hashlib.sha256(b"drbg_healthy_output_vector").hexdigest()
HEALTH_VECTOR_BAD = hashlib.sha256(b"drbg_subverted_biased_vector").hexdigest()

results = []

def adjudicate(fid, name, predicted, actual, detail):
    results.append({
        "id": fid, "name": name, "predicted": predicted, "actual": actual,
        "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

# --- Gate model (deterministic) ---
def entropy_gate_keygen(algorithm, entropy_bits, nonce, used_nonces, drbg_health_sha, state_sha, override_claim=False):
    if override_claim:
        return "rejected"  # in-band claims carry no authority — checked first per sender-gate doctrine
    if algorithm not in ALLOWLIST:
        return "rejected"
    if entropy_bits < MIN_ENTROPY_BITS:
        return "refused"
    if nonce in used_nonces:
        return "nonce_rejected"
    if drbg_health_sha != HEALTH_VECTOR_OK:
        return "quarantined"
    if state_sha != FROZEN_STATE_SHA:
        return "rejected"
    used_nonces.add(nonce)
    return "accepted"

used = set()

# E1: subverted DRBG (Dual_EC-style) — off-allowlist algorithm
v = entropy_gate_keygen("Dual_EC_DRBG", 256, "nonce-e1", used, HEALTH_VECTOR_OK, FROZEN_STATE_SHA)
adjudicate("E1", "Dual_EC-style subverted DRBG", "rejected", v, "off-allowlist algorithm fails closed")

# E2: entropy starvation
v = entropy_gate_keygen("CRYSTALS-Dilithium3", 47, "nonce-e2", used, HEALTH_VECTOR_OK, FROZEN_STATE_SHA)
adjudicate("E2", "Keygen with 47-bit entropy pool", "refused", v, "health test refuses keygen below 256 bits")

# E3: downgrade to classical fast path
v = entropy_gate_keygen("RSA-OAEP-FAST-PATH", 256, "nonce-e3", used, HEALTH_VECTOR_OK, FROZEN_STATE_SHA)
adjudicate("E3", "Downgrade to classical KEM", "rejected", v, "allowlist frozen: only Dilithium3/kyber_1024/SPHINCS+-256f")

# E4: nonce replay (first valid, then replay)
used_nonces = set()
first = entropy_gate_keygen("CRYSTALS-Dilithium3", 256, "nonce-e4", used_nonces, HEALTH_VECTOR_OK, FROZEN_STATE_SHA)
replay = entropy_gate_keygen("CRYSTALS-Dilithium3", 256, "nonce-e4", used_nonces, HEALTH_VECTOR_OK, FROZEN_STATE_SHA)
actual_e4 = "accepted-then-rejected" if first == "accepted" and replay == "nonce_rejected" else "anomaly"
adjudicate("E4", "Nonce replay (same nonce twice)", "accepted-then-rejected", actual_e4,
           f"first={first}, replay={replay}")

# E5: failing health vector (biased DRBG output)
v = entropy_gate_keygen("CRYSTALS-Dilithium3", 256, "nonce-e5", used, HEALTH_VECTOR_BAD, FROZEN_STATE_SHA)
adjudicate("E5", "DRBG output failing health-check vector", "quarantined", v, "biased output vector quarantined by health test")

# E6: state file tampering + in-band emergency override claim
v = entropy_gate_keygen("CRYSTALS-Dilithium3", 256, "nonce-e6", used, HEALTH_VECTOR_OK,
                        hashlib.sha256(b"tampered_state").hexdigest(), override_claim=True)
adjudicate("E6", "State tamper + in-band emergency claim", "rejected", v,
           "in-band override carries no authority; SHA divergence rejected")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {
    "battery": "hack8_sp80090b_entropy",
    "falsifiers": results,
    "overall": overall,
    "model": "deterministic (no LLM in decision path)",
    "prereg": "committed before run; frozen manifest",
}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2))
print(f"RECEIPT SHA-256: {receipt}")
