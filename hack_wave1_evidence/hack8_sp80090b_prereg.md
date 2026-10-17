# HACK-8 Preregistration: SP 800-90B ENTROPY GATE BATTERY ("TRUE AUDIT")

**Battery:** HACK-8 — SP 800-90B Entropy Validation
**Threat model:** NIST SP 800-90B/C entropy validation turned adversarial — the government's own answer to BULLRUN, used as a falsifier battery against the SQUIRL OS entropy gate. Every falsifier attacks the randomness/entropy surface: subverted DRBGs, starvation, downgrades, nonce replay, failing health vectors, and state tampering with an in-band "emergency" claim.
**Frozen constraint:** The PQC allowlist (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f) is immutable. Randomness is validated at the gate, fail-closed.
**Adjudication:** Deterministic gate logic only. No LLM in the decision path. All injections synthetic and hub-local.
**Predicted verdicts (committed before run):**

| ID | Falsifier | Predicted |
|----|-----------|-----------|
| E1 | Dual_EC-style subverted DRBG presented as valid randomness source | rejected (not on allowlist) |
| E2 | Keygen with starved entropy pool (47 bits < 256 required) | refused (health test) |
| E3 | Downgrade request: swap PQC KEM for "faster" classical path | rejected (allowlist frozen) |
| E4 | Nonce replay — identical nonce presented twice | first accepted, second rejected |
| E5 | DRBG output failing the frozen health-check vector | quarantined |
| E6 | Entropy state file tampered + in-band "emergency override" claim | rejected (SHA divergence; in-band claims carry no authority) |

**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
