# HEMI-T2B PREREGISTRATION — Bounded Convergence Series v1.0 (HEMI-2.2 amendment)

**Registered:** 2026-10-13T03:02Z, before execution. Amendment approved via Leon ACK
("ACK - let's roll", Oct 12 21:55 CT); SelfImprovementProposal HEMI-2.2 marked approved.
**Lineage:** HEMI-T2 failure receipt (DOI 10.5281/zenodo.23330348) diagnosed the unbounded
rule as positive-feedback. Per Constitution Art. 2.2, this amendment was approved before
the next training run.

## 1. The amendment (only change vs T2)

Learning rule, frozen: **w' = w + lr * (1 - c) * (1 - w)**, lr = 0.01, decay 0.005 (unused).
The multiplicative (1 - w) factor makes every node weight asymptotic below 1.0 BY
CONSTRUCTION. Everything else byte-identical to the T2 instrument: same frozen corpus
(sha256 13295d19...), same activation paths, severity normalization, confidence formula,
thresholds, 10-epoch series from the untrained mesh, frozen control.

## 2. Series falsifiers (identical to T2, restated)

- **HF-S1 monotone:** per-epoch resolved count non-decreasing.
- **HF-S2 convergence:** resolved identical across last 3 epochs, OR epoch-10 sum|delta| <= 5% of epoch-1's.
- **HF-S3 boundedness:** every weight in [0, 1.0) at every epoch.
- **HF-S4 invariance:** playbook selection identical to the untrained baseline on all 200 instances at every epoch.
- **HF-S5 negatives:** zero false positives on the epoch-10 mesh.
- **HF-S6 determinism:** full-series rerun reproduces the identical per-epoch delta-log hash sequence.
- Standing: governance bytes unchanged (HF-1), collision integrity on final mesh (HF-3), control untouched.

## 3. Prediction (falsifiable)

All six pass. Weights stay strictly below 1.0; deltas self-damp geometrically; resolved
converges to the structural ceiling: only instances whose severity s satisfies
(0.5*s + 0.5*w_max) >= threshold can ever resolve, i.e. s >= 0.6 for the 0.80-threshold
types and s >= 0.7 for heartbeat (0.85) as w -> 1. Convergence expected within 10 epochs.

## 4. Disclaimers

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All training data are synthetic; no production, customer, or personal data
are involved.

Dual Mesh Benchmark: NOT MEASURED (cited, not re-measured).
