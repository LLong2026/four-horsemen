# DMB Frontier Leg — Dual Mesh Benchmark (Opus 5.5 + GPT-6.1 Sol raw-API columns)

Series: dual_mesh_benchmark_frontier_20261023. Preregistration committed BEFORE
execution (repo commit d802b83, 2026-10-23). Instrument byte-identical to the
DMB-X runner (commit b293d58). Corpus: CORPUS_B1.json, sha256
13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59, first-20
selection rule (same as every B1 leg).

## Results (MEASURED, scoped)

- anthropic/claude-opus-5.5 via OpenRouter: 20/20 correct, 20/20 strict-valid
  (zero normalization), median 3346.2 ms, p95 3983.0 ms (one 8688.9 ms outlier
  disclosed), cost $0.1335
- openai/gpt-6.1-sol via OpenRouter: 20/20 correct, 20/20 strict-valid,
  median 2225.6 ms, p95 2916.5 ms, cost $0.0377
- Deterministic mesh in-memory lookup reference (v1.0 B1): median 0.000443 ms
- Total spend $0.1712; no payment abort; 40/40 raw responses preserved verbatim

## Falsifiers (all clean)

FBF-1 raw logs preserved (40/40) · FBF-2 corpus byte-identical (sha re-verified
post-run) · FBF-3 zero retries or omissions · FBF-4 no post-execution metric
additions · FBF-5 synthetic corpus only, no PHI/PII/credentials · FBF-6 claims
scoped to the two tested columns on the raw-API substrate

## Lineage

DMB v1.0 DOI 10.5281/zenodo.23303081 · v2.0 DOI 10.5281/zenodo.23321637 ·
DeepSeek column concept DOI 10.5281/zenodo.23345060 (v2 10.5281/zenodo.23345241) ·
DMB-X 8-column matrix (ledger 0081) · XPLAT-2/3 doctrine: cross-substrate
wall-clock comparisons directional only.

## Scope (load-bearing)

Sampled-baseline measurement of two engines via OpenRouter on the frozen
20-instance corpus, October 2026. Not an engine certification, not a universal
performance claim, not a cross-substrate wall-clock equality claim.

This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or
safety-critical environments. All benchmark data is synthetic.

## Provenance disclosure (audit-and-correction doctrine)

The preregistration document (sha256 ebaa3aab...ca43f5e) was authored and
timestamped in the working workspace at 2026-10-23 21:50 CT, BEFORE execution
(run start 21:52 CT), and the instrument runner was committed publicly before
execution (commit d802b83). The prereg document itself enters the public
repository tree with this publication entry (forward-only addition). No metric
was added post-execution; the receipt's numbers are the run's numbers.
