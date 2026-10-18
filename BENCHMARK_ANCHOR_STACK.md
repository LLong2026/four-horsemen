# ANCHOR STACK BENCHMARK (deterministic layer, SIP-034..039)
**Run:** 2026-10-18T04:35Z | **Method:** median of 3 where noted; single fresh calendar submission for STAMP

| Service | Latency | Notes |
|---|---|---|
| RECONCILE gate (14 receipts) | 3.28s | median of 3 runs |
| EXAMINER MODE (full evidence file) | 6.48s | single run, incl. gate re-run |
| BLOCK TRACK (upgrade + registry, 14 receipts) | 8.54s | single run, network-bound |
| STAMP (fresh artifact, dual calendar) | 1.39s | network-bound, honest variance |

**Digest-only boundary ratio:** 417,997 bytes of corpus anchored with 448 bytes of digests = **933:1** compression across the trust boundary (R1).
**LLM components in any decision path: zero.** Every verdict in this stack is deterministic shell/python — the benchmark measures wall-clock of pure logic plus network round-trips.

## Dual Mesh Benchmark: MEASURED (scoped)
This record measures the deterministic anchor services only; no neural-mesh inference is involved
in or required by any service benchmarked (no LLM in any decision path, by design). The program's
Dual Mesh Benchmark is at DOI 10.5281/zenodo.23321637 (DeepSeek column: DOI 10.5281/zenodo.23345241).

*Prototype software, educational/research purposes only; network latencies are environment-dependent
and are reported as-found, not as performance guarantees.*
