# HACK-14 Preregistration: EDGEHILL

**Threat model:** GCHQ subverted standards, completing Five Eyes coverage: subverted negotiation, reference-impl implant, compat downgrade, standards impersonation, weakened vectors, covert KA channel.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack14_*_battery.py, committed in this freeze commit). Predicted outcome classes: rejected_*/refused_*.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
