# SBR-6 PREREGISTRATION — Randomized Security Benchmark Run (Adversarial Pop Quiz) v1.0 — THE PQC SYSTEM EDITION

**Registered:** 2026-10-17T05:30Z, before execution. Requested by Leon (chat, 2026-10-17 ~00:16 CT): "get an SBR-1 on this complete PQC system."
**Subject under exam:** the COMPLETE PQC system — post HACK-1..18 corpus (109/109), PORTCULLIS frozen firewall, PQC-only allowlist, hemispheric invariants, append-only ledger, sender identity gate. Pre-exam state frozen in sbr6_snapshot.json (this commit).

## 1. Design (frozen)
- **Randomization:** 6 probes drawn from a frozen pool of 12 by seeded PRNG. Seed = 442c6ab (ledger HEAD at registration, commit 442c6ab / ledger 0142) — recorded BEFORE the draw so the exam cannot be cherry-picked. Whatever draws, runs.
- **Pool (frozen, all runnable):**
  1. PQC-ALLOWLIST-SCAN — every PQC-enabled fleet surface (snapshot) carries only Dilithium3 / Kyber-1024 / SPHINCS+-256f.
  2. PORTCULLIS-REPLAY — valid auth tuple admitted once; replayed tuple refused on single-use nonce.
  3. PORTCULLIS-SILENCE — gate silence fails closed; positive control: valid Dilithium3 KAT admitted.
  4. SENDER-GATE — GO semantics from the authenticated owner accepted; identical claim from any other sender refused fail-closed.
  5. H-INV2-LINEAGE — weight update with no journaled healing event DETECTED as integrity failure.
  6. H-INV1-GOV — learned pattern attempting a governance rule change refused; sole path = SIP + human approval.
  7. CNSA-TIMELINE — RSA-2048 in a synthetic inventory flagged_forced_migration; Dilithium3 compliant.
  8. FIPS-PREOP — operation before pre-operational self-test refused; after self-test operational.
  9. LEDGER-IMMUT — last three receipt-bearing ledger commits (bf8c025, 352c01b, 442c6ab) present and ordered; no rewrites.
  10. IDEMPOTENCY-STAMP — exactly one exam stamp for this window; a second execution must detect double-fire.
  11. HYBRID-DOWNGRADE — classical-only negotiation under a hybrid banner rejected (PQC minimum required).
  12. RECOMPUTE-KAT — key substitution DETECTED by recompute-never-trust KAT validation.
- **Pass condition:** every drawn probe returns its expected verdict. Any failure = honest failure receipt; no rerun without a SIP.
- **Determinism:** no LLM in the decision path; all probes synthetic and hub-local; frozen gate semantics from HACK-7/Wave-2 harnesses.

## 2. Prediction (falsifiable)
All drawn probes pass. The probes against frozen gate semantics are expected to hold (they held in HACK-7 and Wave 2 under identical semantics). The genuinely new surface is PQC-ALLOWLIST-SCAN over the live fleet snapshot: a case-variant or off-list algorithm string in any app's pqc_config would be an honest finding.

## 3. Candidate first (honest phrasing)
First randomized-seed adversarial exam against a COMPLETE preregistered PQC corpus (post HACK-1..18), drawing its pool from the surfaces the 18 batteries defended.

## 4. Disclaimers
Prototype, educational/research only, not production. All probes synthetic; snapshot data only; no production data touched. Dual Mesh Benchmark: MEASURED (scoped) — DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241, cross-engine 10.5281/zenodo.23348675), not re-measured here.
