# HACK-12 Preregistration: MUSCULAR

**Threat model:** bulk fiber interception + HNDL: 100-packet bulk replay, forged receipts, harvest-derived state, selective blocking, authority-pattern derivation, captured-ACK replay.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack12_*_battery.py, committed in this freeze commit). Predicted outcome classes: all_refused/rejected/refused_gap.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
