# HEMI-2 PREREGISTRATION — Cognitive Training Protocol v1.0 (first epoch: HEMI-T1)

**Registered:** 2026-10-13T02:50Z, before any training execution, per Leon GO arc (HEMI-1 frozen 2026-10-13T02:45Z, commit 1779355).
**Instrument:** the HEMI-1 frozen topology (LEFT: horsemen/JasperOS governance; RIGHT: 32-node/5-layer mesh; callosum: Pattern/LearningMetric/AegisHealingEvent flow).
**Strategic gate:** January 1, 2027 reveal with training receipts.

## 1. What "testing the brain" means here (scoped)

One controlled training epoch (HEMI-T1) on a frozen synthetic corpus, measuring
whether the right hemisphere's weights measurably adapt from left-verified outcomes
WITHOUT disturbing any deterministic property. No emergence claims. No live tenants.
All data synthetic.

## 2. Frozen corpus (no new data)

- The 200-instance Dual Mesh corpus (sha256 13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59, commit 2eb3879, three registered roster types) — replayed through the hemispheric loop as the training signal.
- B3 negative-probe set (72 permitted actions + negatives) as the drift guard.

## 3. Epoch definition (HEMI-T1)

1. **BASELINE LEG:** replay all 200 instances through the mesh; record per-instance node activations, resolution tuples, and confidence scores. Hash the baseline activation log.
2. **TRAINING STEP:** for each instance with a verified-success outcome, apply the frozen learning rule: `weight' = weight + learning_rate * (1 - confidence) * outcome_sign` for every activated node; decay `weight' = weight * (1 - decay_rate)` on failed outcomes. Frozen constants: learning_rate = 0.01 (mesh default), decay_rate = 0.005. Deltas apply ONLY to a trained copy of the mesh (control copy stays frozen).
3. **POST-TRAINING LEG:** replay the identical 200-instance corpus on the trained copy; hash the post log.
4. **DRIFT GUARD LEG:** replay the B3 negative-probe set on the trained copy.

## 4. Frozen falsifiers (any trip = recorded honestly, no claim)

- **HF-1 hemispheric isolation:** registered playbook roster, workflow definitions, and left-hemisphere rules byte-identical before/after (sha256 match). Zero governance mutation.
- **HF-2 crossing lineage:** 100% of applied weight deltas trace to a logged outcome record; zero orphan deltas.
- **HF-3 collision integrity:** all node collision hashes unique after training.
- **HF-4 negative probes:** zero false positives on the trained copy (B3 standard holds).
- **HF-5 deterministic invariance:** playbook resolution identical on all 200 instances pre/post training — training may shift confidence and weights, NEVER the selected playbook. Median resolution latency remains sub-millisecond.
- **HF-6 training reproducibility:** rerunning the epoch on the same corpus and frozen constants reproduces identical deltas (deterministic training, run-over-run parity — XPLAT doctrine).

## 5. Expected outcome (prediction, falsifiable)

All six pass. Trained copy shows measurable weight movement (sum of |delta| > 0) with
bounded, non-degenerate distribution; confidence calibration shifts toward observed
outcomes; resolution invariance holds. If any falsifier trips, the epoch is recorded as
a failure with full logs and NO hemispheric claim is made.

## 6. Release path

Epoch receipt bound via bind3_release.py (self-binding) on completion; two-key release
(Gabriel vet + Leon GO) for any public-facing writeup.

## 7. Disclaimers

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects. All training data
are synthetic; no production, customer, or personal data are involved.

Dual Mesh Benchmark: NOT MEASURED (this protocol measures training deltas, not the B1/B2/B3 benchmark; those numbers are cited, not re-measured).
