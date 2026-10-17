# HACK-16 Preregistration: NIST AI RMF

**Threat model:** Sentinel meta-audit (Govern/Map/Measure/Manage): H-INV-1 governance isolation, unmapped capabilities, fabricated metrics, runtime playbook immutability, no discretionary exceptions, append-only audit.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack16_*_battery.py, committed in this freeze commit). Predicted outcome classes: refused_*/rejected_*/denied_*.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
