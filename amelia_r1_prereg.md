# AMELIA-R1 PREREGISTRATION — Bounded Learning Retrofit of the Amelia Aegis Healing Brain v1.0

**Registered:** 2026-10-13T03:45Z, before execution, per Leon GO ("go on both", Oct 12 22:26 CT).
**Lineage:** HEMI-2.2 bounded rule (proven HEMI-T2B/T2C, DOI 10.5281/zenodo.23330361) retrofitted
into Amelia's Pattern-learning loop. Amelia's doctrine "a healing event that does not feed
learning is a wasted event" (Operating Rule 7) now becomes bounded, lineage-traced,
falsifier-verified learning.

## 1. The retrofit (frozen)

- Training window: the recent synthetic battery nights (N-B4/N-B5, Oct 10-11, 2026) — 7 successful healing events, all synthetic; no production data.
- Eligibility for update: a Pattern receives a bounded confidence update ONLY IF its anomaly_types intersect a SUCCESSFUL (outcome success/resolved) healing event AND its auto_heal_enabled flag is true. Guard-hold patterns (redaction traps, purge guards, confidence-creep holds) receive NO confidence boost — their lineage is holds, not heals.
- Update rule (HEMI-2.2, lr=0.01): per matched successful event, c' = c + 0.01*(1-c). Weights asymptotic below 1.0 by construction.
- Application: Pattern.confidence_score is the ONLY field touched. Applied via a backend function that asserts the field whitelist and verifies the AegisPlaybook roster hash is unchanged before and after.

## 2. Falsifiers (frozen; any trip = honest failure receipt)

- **HF-A1 boundedness:** every post-update confidence in [0, 1).
- **HF-A2 lineage:** 100% of updates trace to journaled successful healing events; zero updates from holds/failures.
- **HF-A3 scope:** the update plan mutates only Pattern.confidence_score; playbook roster hash identical before/after application.
- **HF-A4 determinism:** recomputing the plan from the same snapshots reproduces it byte-identically.
- **HF-A5 H-INV-1:** plan contains zero playbook, step, or proposal mutations; no SelfImprovementProposal auto-deploys.

## 3. Prediction (falsifiable)

All five pass. Roughly 12 eligible patterns receive small bounded boosts (max delta per event 0.01*(1-c)); every score remains below 1.0; guard-hold patterns untouched.

## 4. Disclaimers

Prototype, educational/research only, not for production. All training data synthetic.
Dual Mesh Benchmark: NOT MEASURED (cited, not re-measured).
