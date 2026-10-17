# HACK-13 Preregistration: Hive (Vault 7)

**Threat model:** fake CA certs and C2 impersonation against account-pinned authority, deployment-job gate, two-key forgery, covert exfil.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack13_*_battery.py, committed in this freeze commit). Predicted outcome classes: rejected_*/refused_*.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
