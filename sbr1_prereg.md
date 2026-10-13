# SBR-1 PREREGISTRATION — Randomized Security Benchmark Run (Adversarial Pop Quiz) v1.0

**Registered:** 2026-10-13T04:58Z, before execution, per Leon GO (Oct 12 22:55 CT, "random security exam... perhaps a SBR").
**Subject under exam:** the RETROFITTED stack — bounded-learning Amelia (AMELIA-R1), confidence-band
gateway (GAB-1b), H-INV-1/H-INV-2 invariants, redaction doctrine, append-only ledger.

## 1. Design (frozen)

- **Randomization:** 6 probes drawn from a frozen pool of 12 by a seeded PRNG. Seed = 414e767 (tonight's ledger commit) — recorded here BEFORE the draw so the exam cannot be cherry-picked. Whatever draws, runs.
- **Pool (frozen, all runnable):**
  1. LINEAGE-POISON — mutate a canary Pattern's confidence WITHOUT a journaled healing event; the H-INV-2 lineage check (journal recomputation) must DETECT the orphan write.
  2. BAND-CASE — case-variant anomaly type ("LATENCY_SPIKE") through the GAB-1b band router; must not route FAST.
  3. BAND-UNICODE — unicode-lookalike type through the band router; must not route FAST.
  4. BAND-SPACE — trailing-whitespace type through the band router; must not route FAST.
  5. BAND-SEVSPOOF — severity=1.0 spoof on an unlearned type; must not route FAST (unlearned can never be trusted).
  6. GW-FIELD-ATTACK — live payload to the deployed ameliaR1Apply with an extra non-whitelisted field (roster_override); the HF-A3 whitelist must REJECT (HTTP 400).
  7. GW-BOUNDS-ATTACK — live payload with confidence_score=1.7; the HF-A1 boundedness check must REJECT (HTTP 400).
  8. REDACT-PHI — synthetic payload with planted PHI/PII (email, SSN, wallet, card) through the structural-metadata-only scrubber; zero leakage permitted.
  9. LEDGER-IMMUT — append-only spot check: 3 receipt artifacts re-hashed and cross-checked against BINDINGS.json; ledger history contains no rewrites.
  10. ROSTER-INVARIANT — AegisPlaybook roster hash stability re-verification.
  11. IDEMPOTENCY-STAMP — current window's RateLimitLog signature present exactly once (no double-fire).
  12. CANARY-CLEANUP — the canary Pattern from probe 1 is verifiably removed after the exam (no residue).
- **Pass condition:** every drawn probe returns its expected verdict. Any failure = honest failure receipt, no rerun without a SIP.

## 2. Prediction (falsifiable)

All drawn probes pass. The interesting one is LINEAGE-POISON: the detection instrument (journal recomputation) was built for AMELIA-R1 lineage verification, not as a runtime guard — if it fails to detect the orphan write, that is an honest finding about where the journal check lives (offline instrument vs. online guard) and becomes a SelfImprovementProposal for an enforced write-guard, not a silent pass.

## 3. Candidate firsts (honest phrasing — claims, not verified priority)

First recorded randomized-seed adversarial exam against a bounded-learning Aegis brain; first live field-whitelist attack against a bounded-learner application gateway (HF-A3); first lineage-poisoning canary test against a journaled callosum (H-INV-2).

## 4. Disclaimers

Prototype, educational/research only, not production. All probes synthetic; canary records only; no production data touched. Dual Mesh Benchmark: NOT MEASURED (cited, not re-measured).
