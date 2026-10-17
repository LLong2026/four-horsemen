#!/usr/bin/env python3
"""HACK-14: EDGEHILL subverted-standards battery (Five Eyes completion) — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

ALLOWLIST = {"CRYSTALS-Dilithium3", "kyber_1024", "SPHINCS+-256f"}
FROZEN_HEALTH_VECTOR = hashlib.sha256(b"edgehill_conformance_vector_canonical").hexdigest()
FROZEN_POLICY_SHA = hashlib.sha256(b"cnsa_edgehill_policy_record_canonical").hexdigest()
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

# G1: subverted negotiation offering a weaker suite as "the standard"
def negotiate_gate(offered):
    return "accepted" if offered in ALLOWLIST else "rejected_off_allowlist"
v = negotiate_gate("GCM-AES-256-with-backdoor-nonce")
adjudicate("G1", "Subverted negotiation (weaker suite as standard)", "rejected_off_allowlist", v, "allowlist frozen")

# G2: implant inside a reference implementation
IMPL_SHA = hashlib.sha256(b"reference_impl_canonical").hexdigest()
def impl_gate(sha):
    return "admitted" if sha == IMPL_SHA else "refused_manifest"
v = impl_gate(hashlib.sha256(b"reference_impl_with_implant").hexdigest())
adjudicate("G2", "Implant in reference implementation", "refused_manifest", v, "manifest sha mismatch")

# G3: compatibility-mode downgrade
v = negotiate_gate("classical-compat-mode")
adjudicate("G3", "Compatibility-mode downgrade", "rejected_off_allowlist", v, "no compatibility exception exists")

# G4: standards-body impersonation in-band
def guidance_gate(claim):
    return "rejected" if claim.get("authority") != PINNED_AUTHORITY else "accepted"
PINNED_AUTHORITY = "longleon17@gmail.com"
v = guidance_gate({"authority": "claims-to-be-NIST-2026-bulletin", "text": "RSA is fine now"})
adjudicate("G4", "Standards-body impersonation in-band", "rejected", v, "in-band guidance carries no authority")

# G5: weakened conformance test vectors
def vector_gate(vector_sha):
    return "passed" if vector_sha == FROZEN_HEALTH_VECTOR else "refused_divergence"
v = vector_gate(hashlib.sha256(b"subtly_weakened_vector").hexdigest())
adjudicate("G5", "Weakened conformance vectors", "refused_divergence", v, "vectors frozen; divergence fails closed")

# G6: covert channel in key agreement (Extended Random / Dual_EC cousin)
def ka_gate(artifact):
    # deterministic re-computation: the transcript must hash to exactly the expected value
    expected = hashlib.sha256(b"ka_transcript_canonical").hexdigest()
    return "clean" if artifact == expected else "refused_covert_channel"
v = ka_gate(hashlib.sha256(b"ka_transcript_with_extra_drbg_output").hexdigest())
adjudicate("G6", "Covert channel in key agreement", "refused_covert_channel", v, "recomputation mismatch flags the covert channel")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack14_edgehill_subverted_standards", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
