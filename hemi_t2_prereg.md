# HEMI-T2 PREREGISTRATION — Multi-Epoch Convergence Series v1.0

**Registered:** 2026-10-13T02:55Z, before execution, per Leon GO (chat authorization, Oct 12 21:52 CT).
**Lineage:** HEMI-1 topology freeze (1779355) -> HEMI-2 protocol (254e58e) -> HEMI-T1 epoch
(DOI 10.5281/zenodo.23330308, all six falsifiers pass).

## 1. Question under test

Does repeated cognitive training CONVERGE, OSCILLATE, or DIVERGE? T1 measured one epoch
(58 -> 68 resolved, bounded calibration shift). T2 measures the full curve from the
untrained state and answers whether the learning rule is self-damping or uncontrolled.

## 2. Frozen series definition

- **N = 10 epochs.** Epoch 1 starts from the ORIGINAL untrained mesh weights (the
  T1-frozen telemetry-pack state, NOT T1's trained copy — the series measures the full
  curve from scratch; T1's epoch remains independently receipted).
- Each epoch: full 200-instance replay (baseline instrument, identical to T1: activation
  paths, severity normalization, confidence formula, thresholds), then the HEMI-2 frozen
  learning rule applied to the trained mesh. The trained mesh carries forward epoch to
  epoch. A frozen control copy is never trained.
- **Instrument:** byte-identical replay/resolve logic to hemi_t1_runner.py (committed
  0a2638b / 5b258d2); the corpus hash gate aborts on any drift.

## 3. Series falsifiers (frozen before execution; any trip = honest failure)

- **HF-S1 monotone convergence:** the per-epoch resolved count is NON-DECREASING across
  all 10 epochs (no oscillation of the calibration gate).
- **HF-S2 convergence reached:** either the resolved count is identical across the last
  3 epochs, OR epoch-10's sum of |weight delta| is at most 5% of epoch-1's (learning
  rate self-damps toward zero).
- **HF-S3 weight boundedness:** every node weight remains in [0, 1.0) at every epoch —
  no saturation blow-up, no weight escape.
- **HF-S4 per-epoch invariance (extends HF-5):** playbook selection identical to the
  untrained baseline on ALL 200 instances at EVERY epoch (training may never change
  governance decisions, only calibration).
- **HF-S5 final drift guard (extends HF-4):** zero false positives on both negative
  probes against the fully-trained epoch-10 mesh.
- **HF-S6 series determinism (extends HF-6):** rerunning the full 10-epoch series on
  the frozen corpus reproduces the identical per-epoch delta-log hash sequence.
- **Standing:** governance roster bytes identical before/after the whole series (HF-1),
  collision integrity on the final mesh (HF-3), control copy untouched.

## 4. Prediction (falsifiable)

All six series falsifiers pass. Resolved count rises monotonically and converges before
epoch 10; the convergence ceiling is set by the severity distribution of the frozen
corpus against the frozen thresholds (structural: only instances whose severity can
ever lift c above threshold can resolve). Per-epoch sum |delta| self-damps toward zero.
If resolved oscillates at any epoch, or any weight reaches 1.0, the series FAILS and is
receipted as such.

## 5. Disclaimers

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All training data are synthetic; no production, customer, or personal data
are involved.

Dual Mesh Benchmark: NOT MEASURED (cited, not re-measured).
