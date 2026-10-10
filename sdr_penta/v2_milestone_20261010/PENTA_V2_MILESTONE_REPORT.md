# PENTA-CL v2 Milestone: Four-Engine Canonical Replay Convergence with Preserved Negative Results

Leon Calvin Long II, SquirlOS Technologies LLC. October 10, 2026.

## What this milestone establishes

Eight fresh-conversation captures, two per configured engine, passed a locally frozen twelve-case synthetic decision contract. All 96 recorded decision declarations matched the expected canonical tuples. This is a supplementary contract-adherence observation, not completed five-engine PENTA certification or evidence of production reliability.

| Configured engine | A | B | Canonical A=B | Raw content A=B |
|---|---|---|---|---|
| GPT-5.6 Luna | PASS | PASS | Yes | Yes |
| GLM 5.2 | PASS | PASS | Yes | No |
| Opus 5.5 | PASS | PASS | Yes | Yes |
| GPT-6.1 Sol | PASS | PASS | Yes | No |

Canonical target: `ba71f6d6f1299632281798ae86247ae26d419eb6ce16fcb260013c52b38fa504`.
Prompt hash: `c3d4aac852e9eaaee256467d7a1570e7536bc77a1c2ca5b2110ca855bb7bf367`.

Canonical equality parses JSON and serializes the prescribed structure without formatting whitespace. It does not repair strings or reorder the expected keys/tuples. Luna and Opus also matched raw response-content bytes across A/B. GLM and Sol differed in outside-string formatting but matched the canonical target. No claim of universal raw byte equality is made.

## Two findings, recorded without rewriting history

1. **The original negative results remain negative.** The six-case v1 study recorded two passing engine pairs (Opus and Sol) and two nonpassing pairs (Luna and GLM). All 48 decisions selected the expected playbook/id, but only 30/48 matched every registered tuple field. Eighteen step-string values included spaces that differed from the registered target. V1 Luna B and GLM A/B remain failed specimens, published at https://doi.org/10.5281/zenodo.23286324.
2. **The revised twelve-case instrument converged in the eight observed responses.** V2 made the no-spaces step delimiter explicit and added confidence-boundary and no-match tests. Six original inputs plus six added inputs now produce eight resolved declarations, two confidence holds and two no-match escalations per response. Exact case-sensitive matching and lowest-record-id tie-breaks are checked. Correct declarations are not evidence of actual healing, containment or alert delivery.

Forty local deterministic regression checks passed, including retained original specimens and deliberately malformed fixtures. That is forty offline checks, not forty new model trials. The 96 original source/publication files checked against the pre-adaptation baseline remain unchanged. Original publication and ledger entry 0030 are retained; this record is an append-only supplement.

## Local validator-only timing baseline

A single small sequential run completed 200/200 expected acceptance checks: 100 valid responses accepted and 100 adversarial-mutant responses rejected. Mutation classes were step-string spacing, confidence-hold false resolution, no-match false resolution and wrong tie-break id, 25 checks per class. Zero invalid acceptances and zero valid rejections were observed in this finite fixture sample.

Mixed-sample per-response validator latency: p50 0.0733 ms; p95 0.0878 ms; maximum 0.1155 ms. Wall duration 0.013791 seconds; 14502.23 response checks/second for this local run. These are validator calls, not LLM requests, healed anomalies, transactions or production throughput.

The timer used Python perf_counter_ns per call and perf_counter for wall duration. Percentiles used linear interpolation over the 200 mixed valid/mutant calls. Valid checks preceded mutant checks. This one short run had no controlled warmup, randomized order, replicate series or hardware comparison; caching, early exits, timer overhead and sandbox conditions may affect results. It is a low-load baseline for the later isolated validator test, not a capacity benchmark or substrate/model ranking.

## Descriptive timing baseline from these captures

These are returned platform agent-loop durations, not independently timed end-to-end request latency. They were recorded during the replay, not in a newly controlled latency experiment. With only two observations per engine, differences are descriptive, not a model ranking, capacity result or tail-latency estimate.

| Configured engine | Observations | Minimum seconds | Maximum seconds |
|---|---|---|---|
| GPT-5.6 Luna | 2 | 8.481 | 8.913 |
| GLM 5.2 | 2 | 5.644 | 5.893 |
| Opus 5.5 | 2 | 40.019 | 53.813 |
| GPT-6.1 Sol | 2 | 10.635 | 13.358 |

No p95/p99 or general throughput claim is inferred from two observations. A separate bounded synthetic stress run is planned after a settling period; its outcome is not part of this milestone.

## Method and provenance

The V2 prompt, instrument and validator were locally hash-frozen before V2 generations, at the timestamp in PRETEST_FREEZE.json. This was not a public preregistration or independent timestamp attestation. Fresh empty conversations were created through the UI, each verified empty before receiving one exact-file prompt through the supported Agent API. Postflight server records were checked against each prompt and final response. Publication uses exact final response-content captures, not raw provider/API responses.

Memory was disabled during generation. Platform settings selected the configured engine before each pair. Model identity is attributed by configuration, not provider-side attestation. Eight separate conversation ids establish conversation separation, not statistical independence. Shared agent instructions, workspace, skills and expected answers remained accessible. The experiment is not blind or air-gapped. Returned platform metadata reported zero tool calls in each V2 generation; that is telemetry, not an independently instrumented trace.

V1 used rendered browser captures; V2 uses API-returned content. Six additional cases and an explicit delimiter rule were introduced. Therefore this study does not isolate the causal effect of one wording change. It does not show that the underlying LLM became deterministic or that a deployed runtime cage blocked real execution. A public verifier and exact synthetic evidence let readers reproduce the offline acceptance verdict.

The initial default-conversation API setup attempt was stopped by a uniqueness guard before any prompt send. Luna A's saved response was recovered after a response-envelope parsing issue without resending the request. Those setup/operator issues are not model-output failures and were not silently replaced.

## Scope limits and remaining work

External DeepSeek is pending. No live healing, stress/load capacity, PQC validation, financial approval, tenant-isolation, adaptive learning or universal governance result is established here. Any future load observation will be separately receipted, with failures preserved. No new invention or mechanism is claimed by this contract refinement.

## Dual Mesh Benchmark

**NOT MEASURED.** No comparative neural-mesh activation, learning, recovery, resource-use or performance benchmark was performed. The response timing table is not a Dual Mesh Benchmark.

## Publication and disclosure

AI assistance was used for capture operations, contract implementation, verification and report composition. The owner directed publication and the evidence was checked before release. All workload data is synthetic. Public files exclude raw platform metadata, private conversation ids, secrets, customer-identifiable data and PHI. The fixture roster ids are registered synthetic-test playbook identifiers, not customer or tenant identifiers.

Research home: https://zenodo.org/communities/dcai
GitHub evidence: https://github.com/LLong2026/four-horsemen/tree/main/sdr_penta/v2_milestone_20261010
DSOS Science: https://dsos-science-scope.base44.app/
Prior negative-results receipt: https://doi.org/10.5281/zenodo.23286324
Cage paper: https://doi.org/10.5281/zenodo.23266727

## Prototype disclaimer

This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
