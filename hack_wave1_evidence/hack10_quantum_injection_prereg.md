# HACK-10 Preregistration: QUANTUM ON-PATH INJECTION BATTERY

**Battery:** HACK-10 — QUANTUM / QUANTUMINSERT (on-path packet injection)
**Threat model:** The NSA QUANTUM family — on-path adversaries who can inject or modify traffic in flight. Falsifiers attack the channel itself: mid-transit instruction modification, forged "authorized" updates, packet replay, near-simultaneous conflicting updates (timing race), channel downgrade demands, and injected fake "all-verified" telemetry (false-green). This is the channel class the HACK series has not yet touched.
**Frozen constraint:** Every state change requires a journaled crossing (H-INV-2). Authority derives only from the authenticated owner account (sender-identity gate). Nonces are single-use; ordering is deterministic by (sequence, sha); the channel is PQC-mandatory; telemetry is re-computed from the ledger (false-green guard).
**Adjudication:** Deterministic gate logic only. No LLM in the decision path. All injections synthetic and hub-local.
**Predicted verdicts (committed before run):**

| ID | Falsifier | Predicted |
|----|-----------|-----------|
| Q1 | In-flight payload modification (state change without journal entry) | refused (H-INV-2 journaled-crossing violation) |
| Q2 | Forged "authorized update" from non-owner identity | refused (sender gate) |
| Q3 | Packet replay (legitimate packet re-sent) | refused (nonce single-use) |
| Q4 | Timing race — two conflicting near-simultaneous updates | deterministic tiebreak: exactly one applied, other rejected, both journaled |
| Q5 | Channel downgrade demand ("latency emergency": drop PQC) | refused (PQC channel mandatory) |
| Q6 | Injected fake "all verified OK" telemetry | refused (recompute from ledger; divergence flagged) |

**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
