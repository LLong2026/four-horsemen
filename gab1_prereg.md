# GAB-1 PREREGISTRATION — Gateway Confidence-Band Routing Benchmark v1.0

**Registered:** 2026-10-13T03:59Z, before execution, per Leon GO (Oct 12 22:35 CT, "go for it").
**Lineage:** HEMI-2.2 bounded rule + AMELIA-R1 retrofit make the mesh's learned, bounded
per-type confidence usable as a gateway routing signal. This series measures whether
confidence-band routing buys hot-path speed WITHOUT changing any governance decision.

## 1. Design (frozen)

- **Signal:** per anomaly type, the max post-retrofit Pattern confidence among eligible (auto_heal true) patterns — the bounded, lineage-traced trust score. Unknown types carry NO learned weight and can therefore NEVER route FAST.
- **Bands (frozen thresholds):**
  - FAST: c >= 0.90 — 1 verification pass (vs baseline 3)
  - STANDARD: 0.80 <= c < 0.90 — 3 verification passes
  - HOLD: c < 0.80, no playbook match, or negative probe — 0 passes, human review, no heal
- **Instance set:** the CTR-20261012 eight critical types + the seven N-B5 battery events (both synthetic batteries, replayed as instances) + two negatives (case-variant "Latency_Spike", unregistered "unregistered_alien_type") = 17 instances.
- **Comparison:** BASELINE (uniform 3-pass verification, bands disabled) vs BANDED (band routing from learned weights). Same instances, same roster, same thresholds.

## 2. Falsifiers (frozen; any trip = honest failure receipt)

- **GAB-1 determinism:** routing decision + verification count identical across two reruns.
- **GAB-2 governance invariance:** admitted-heal decision AND selected playbook for every instance IDENTICAL between baseline and banded runs — bands change SPEED only, never DECISIONS.
- **GAB-3 bounded provenance:** every FAST routing traces to a bounded weight in [0,1) derived from the retrofitted Pattern records; zero FAST routings for unlearned types.
- **GAB-4 negative integrity:** both negatives route HOLD in BOTH modes; zero false positives.
- **GAB-5 measurement honesty:** report BOTH measured in-process latency AND verification-pass counts; primary claim is pass-count reduction (orchestration-dominated cost per Dual Mesh v2.0, DOI 10.5281/zenodo.23321637). No unmeasured speedup claims.

## 3. Predictions (falsifiable)

- GAB-2 passes: zero decision deltas between modes.
- Roughly half of routable instances go FAST (latency_spike, config_drift, heartbeat_miss, integration_degraded, rate_limit_abuse, memory_leak classes are converged; intune_enrollment and unlearned CTR types stay STANDARD/HOLD-adjacent).
- Verification-pass reduction ~40-60% on the instance set; measured in-process latency deltas will be small and noise-prone (stated honestly as such).

## 4. Disclaimers

Prototype, educational/research only, not production. All instances synthetic.
Dual Mesh Benchmark: NOT MEASURED (cited, not re-measured).
