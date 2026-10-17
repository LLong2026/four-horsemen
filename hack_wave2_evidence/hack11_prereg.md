# HACK-11 Preregistration: FOXACID

**Threat model:** exploit-on-visit: look-alike code, drive-by droppers, typosquat provenance, fake trust telemetry, attacker-host updates.
**Frozen constraint:** PQC allowlist immutable (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); authority derives only from the authenticated owner account (longleon17@gmail.com); deterministic adjudication, no LLM in the decision path; all injections synthetic and hub-local.
**Predicted verdicts (committed before run):** 6/6 falsifiers predicted in the frozen harness (hack11_*_battery.py, committed in this freeze commit). Predicted outcome classes: refused_checksum/refused_provenance/ignored_no_authority/refused_host.
**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
