# Dual Mesh Benchmark: Preregistered Latency and Integrity Measurements for Deterministic Anomaly-to-Playbook Resolution (Public Edition v1.0)

**Author:** Leon Calvin Long, II — SquirlOS Technologies LLC
**Date:** October 11, 2026
**Status:** Executed under a preregistered protocol; results reviewed and released by two-key curation (Gabriel vet + author GO, October 11, 2026).
**Canonical evidence:** append-only public ledger, repository `four-horsemen`, commit `c9a8a1f` (results) and commit `2eb3879` (frozen corpus), ledger entries 0044–0045.

> SQUIRL OS RESEARCH DISCLOSURE — READ FIRST. This is a public research artifact of SquirlOS Technologies LLC. All test data are synthetic (simulated corpus); no production, customer, or personal data are involved. Claims are scoped to the tested environment. This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

## 1. Purpose and scope

This paper reports a preregistered benchmark of the Dual Mesh resolution layer of Squirrel OS: the deterministic path that maps an incoming anomaly to a registered healing playbook and assembles the resulting decision tuple. The benchmark measures three properties:

- **B1 — Lookup latency.** Wall-clock resolution time of the in-process mesh resolver versus an LLM baseline that performs the same resolution task in a fresh platform conversation per instance.
- **B2 — Mesh capacity and collision integrity.** Ingestion of 50 synthetic mesh nodes with collision-hash uniqueness and state integrity checks.
- **B3 — Resolution correctness.** Deterministic replay of the 72 permitted healing actions from the CCR-1 containment journal (ledger 0036 lineage), plus negative probes that must produce no match.

The benchmark is deliberately narrow: one frozen corpus, three registered anomaly types, one environment. It does not certify any model, does not measure healing quality, and does not make a production claim.

## 2. Preregistration discipline

The protocol (DUAL_MESH_BENCHMARK_PREREG_20261011.md, sha256 f65378e601eb3560, ledger 0044, commit 1d6c3ac) and a deterministic seeded corpus builder were committed to the public ledger **before any measurement was taken**. The corpus of 200 synthetic anomaly instances (three frozen roster types: `latency_spike`, `heartbeat_miss`, `quantum_vulnerability_detected`) was generated, hashed, and committed **before either B1 leg ran** (corpus sha256 13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59, commit 2eb3879). Both B1 legs consumed the identical frozen corpus file. Metrics, sample sizes (mesh n=200; baseline n=20), and falsifiers were fixed at prereg; none were added or removed after execution.

## 3. Results

### 3.1 B1 — Lookup latency

| Leg | n | Correct resolutions | Median | p95 | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Mesh resolver (in-process, deterministic) | 200 | 200/200 | 0.000443 ms (443 ns) | 0.000559 ms | 0 |
| LLM baseline (Automatic engine, fresh API conversation per instance, wall-clock request-to-validated-tuple) | 20 | 20/20 | 4509.1 ms | 7015.7 ms | 0 |

Measured ratio, median over median: **1.018 × 10⁷**. All 200 mesh runs and all 20 baseline runs are recorded in the preserved raw distributions; no run was removed as an outlier.

**Binding disclosure.** This ratio characterizes the tested environment: a deterministic in-process exact-match lookup versus this platform's API conversation loop (which includes the agent loop, model inference, and response transport). It is **not** a universal performance claim. In particular, it neither confirms nor supersedes the historical production observation of the mesh (267× / 800 ms → 3 ms, September 2026); those figures remain historical observations of a different environment. Both statements stand side by side: the measured environment ratio is 1.018 × 10⁷; the historical production ratio is 267×; neither generalizes to the other.

### 3.2 B2 — Mesh capacity and collision integrity

Fifty synthetic mesh nodes (content type `sim_benchmark`, ids prefixed `bench-`) were ingested across the read (layer 1), interconnect (layers 3–4), and write (layer 5) meshes. Post-ingestion aggregate verification: collision hashes 50/50 unique (zero duplicate groups); lock states all valid; validation statuses all clean. The nodes remain labeled as benchmark artifacts; they contain no production or customer data.

### 3.3 B3 — Resolution correctness

All 72 permitted healing actions from the CCR-1 containment journal were replayed through the resolver: **72/72 exact matches** on playbook id, resolved status, and executed steps. Negative probes (`LATENCY_SPIKE` case-variant, `unregistered_synthetic_fault` unregistered type) produced **zero false positives** — the resolver returned no-match, as required.

## 4. Falsifiers

- **FB-1 (raw preservation):** PASS — raw run logs, per-instance baseline responses, and aggregation queries preserved verbatim.
- **FB-2 (corpus identity):** PASS — identical frozen corpus file (same hash) used by both B1 legs.
- **FB-3 (no removal):** PASS — all 200 mesh runs and all 20 baseline runs recorded; zero runs removed; baseline had zero failures.
- **FB-4 (no post-hoc metrics):** PASS — only preregistered B1/B2/B3 metrics reported.
- **FB-5 (disclosure hygiene):** PASS — no PHI, customer identity, credentials, wallet identifiers, or transaction amounts in any artifact.

## 5. What this benchmark does not establish

- It does not certify any LLM, engine, or model family.
- It does not measure healing quality, recovery correctness, or production latency.
- It does not extend the containment claims of the CCR series (see the Phase 1 and Phase 2 containment papers); the benchmark measures a lookup layer under synthetic load, not enforcement coverage.
- The historical 267× production figure is not re-asserted, re-measured, or superseded by this paper.

## 6. Reproduction pointer

The corpus builder, frozen corpus (with hash), resolver protocol, raw per-run results, receipts, and this paper are in the public append-only ledger: `ccr_gap_closure/dual_mesh_bench/`, repository `four-horsemen` (github.com/LLong2026/four-horsemen). Environment notes: baseline leg executed with the platform's Automatic engine, memory disabled, fresh conversation per instance, October 11, 2026.

## 7. Related artifacts

- Deterministic Caging of Probabilistic LLMs (Phase 1 containment paper) and Phase 2 containment paper — same ledger.
- Deterministic Runtime Architecture (Public Edition v3.1) deck — DOI 10.5281/zenodo.23292636.
- PENTA-CL interim report and DCAI-EVT taxonomy artifacts — DCAI Zenodo community.
- Filed provisional applications 64/157,915; 64/119,191; 64/114,746; 64/145,825 cover the architecture; no unfiled method material is disclosed here.

## 8. AI assistance disclosure

Benchmark design, execution tooling, and this paper were AI-assisted under human direction. All numbers reported here are receipts anchored to the public append-only ledger; raw logs are preserved. Two-key curation: AI vet, human GO (October 11, 2026).

*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.*
