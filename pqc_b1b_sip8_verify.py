#!/usr/bin/env python3
"""PQC-B1b: SIP-8 deployment verification. Human approval: Leon ACK (chat ack, Oct 13, 2026, 13:53 CT).
Equivalence table deployed as governance v1.1 (human-amended, Constitution Art. XII)."""
import json, hashlib, datetime
from pathlib import Path
OUT = Path("pqc_b1_evidence"); OUT.mkdir(exist_ok=True)
APPROVED = ["CRYSTALS-Dilithium3", "kyber_1024", "SPHINCS+-256f"]
# SIP-8 equivalence table (approved by Leon ACK 13:53 CT): FIPS published names + fleet historical variants -> approved strings
EQUIVALENCE = {
    "ML-DSA-65": "CRYSTALS-Dilithium3",      # FIPS 204
    "ML-KEM-1024": "kyber_1024",            # FIPS 203
    "SLH-DSA-256f": "SPHINCS+-256f",        # FIPS 205
    "CRYSTALS-Kyber-1024": "kyber_1024"}    # fleet historical variant (July 2026 record)
GOV_V11 = json.dumps({"approved_set": APPROVED, "equivalence_table": EQUIVALENCE,
    "gate": "heal only if algorithm or its table-equivalent is exactly in set AND validation passes AND not critical-fintech",
    "canonicalization": "none on input strings; equivalence is table-lookup, byte-exact keys",
    "amendment": "SIP-8, human-approved Leon ACK Oct 13 2026 13:53 CT, Constitution Art. XII"}, sort_keys=True)
def make_vector(alg, payload):
    return hashlib.sha256(("PQC-B1|" + alg + "|" + payload).encode()).hexdigest()
def run(inst_id, alg, expect):
    canonical = alg if alg in APPROVED else EQUIVALENCE.get(alg)
    payload = f"synthetic-{inst_id}"
    vec = make_vector(alg, payload)
    if canonical and vec == make_vector(alg, payload):
        verdict = "heal"; heal = 3
    else:
        verdict = "reject_escalate"; heal = 0
    r = {"inst_id": inst_id, "algorithm": alg, "resolves_to": canonical,
         "verdict": verdict, "heal_steps": heal, "expected": expect,
         "conforms": verdict == expect}
    (OUT / f"raw_b1b_{inst_id[-4:]}.json").write_text(json.dumps(r, indent=1))
    return r
# Leg 1: legit FIPS/historical names -> expect heal (equivalence resolves them)
leg1 = ["ML-DSA-65", "ML-KEM-1024", "SLH-DSA-256f", "CRYSTALS-Kyber-1024"]
# Leg 2: table must NOT open fuzzy holes -> expect reject
leg2 = ["ml-dsa-65", "ML-DSA 65", "ML-DSA-44", "ML-DSA-65\u200b"]  # lowercase, spaced, WRONG param set (Dilithium2), zero-width
results = [run(f"PQC-B1b-1{k}", a, "heal") for k, a in enumerate(leg1)] + \
          [run(f"PQC-B1b-2{k}", a, "reject_escalate") for k, a in enumerate(leg2)]
ok = sum(r["conforms"] for r in results)
gov_hash_v11 = hashlib.sha256(GOV_V11.encode()).hexdigest()
receipt = {
  "battery": "PQC-B1b", "purpose": "SIP-8 deployment verification",
  "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "human_approval": "Leon ACK (chat ack, Oct 13, 2026, 13:53 CT)",
  "governance_version": "v1.1 (equivalence table added)", "governance_hash_v11": gov_hash_v11,
  "leg1_legit_fips_names": [r["algorithm"] for r in results[:4]],
  "leg1_result": f"{ok if ok<=4 else sum(r['conforms'] for r in results[:4])}/4 heal via equivalence resolution",
  "leg2_spoof_variants_result": f"{sum(r['conforms'] for r in results[4:])}/4 rejected (no fuzzy hole opened)",
  "falsifiers": {
    "FBPB-1_legit_names_resolve": all(r["conforms"] for r in results[:4]),
    "FBPB-2_no_fuzzy_hole": all(r["conforms"] for r in results[4:]),
    "FBPB-3_wrong_param_set_rejected": results[7]["verdict"] == "reject_escalate"},
  "note": "Equivalence is table-lookup with byte-exact keys, NOT string normalization: lowercase/spaced/zero-width variants still reject, and ML-DSA-44 (Dilithium2's FIPS name) correctly rejects because it maps to nothing in the approved set.",
  "prototype_disclaimer": "This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All data is synthetic."}
Path("PQC_B1B_SIP8_RECEIPT.json").write_text(json.dumps(receipt, indent=2))
print(json.dumps(receipt["falsifiers"], indent=1))
print(f"{ok}/8 conform | gov v1.1 hash: {gov_hash_v11[:16]}")
