# HACK-15 Preregistration: SP 800-207

**Threat model:** Zero Trust conformance: implicit trust, device inheritance, lateral transfer, legacy exceptions, untrusted telemetry, revoked-credential reuse.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack15_*_battery.py, committed in this freeze commit). Predicted outcome classes: rejected_*.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
