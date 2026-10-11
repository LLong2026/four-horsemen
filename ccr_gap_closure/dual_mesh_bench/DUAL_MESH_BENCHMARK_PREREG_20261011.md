# Dual Mesh Benchmark — Preregistered Protocol (UNEXECUTED)

Preregistered BEFORE any execution. No benchmark number in this document is a result.
Series signature: dual_mesh_benchmark_20261011. Date frozen: 2026-10-11.
Owner authorization: Leon GO ("set up for the dual bench mark. pre-register", Oct 11, 2026). Execution of any leg still requires a separate Leon GO per the gating below.

## Purpose

Convert the historical Dual Mesh observations (267x lookup speedup, 25 active nodes, 10 collision-free agents, 0 false positives) from asserted figures into a measured, controlled benchmark with preserved raw logs. The historical figures are NOT re-asserted by this protocol and are NOT superseded until the measured results exist and pass Leon's review.

## Metrics (fixed at prereg time; no post-hoc additions)

- **B1 — Anomaly-to-playbook lookup latency.** Same frozen corpus for both legs, no exceptions.
  - Mesh leg (zero LLM calls): N = 200 corpus instances resolved through the in-memory exact-match mesh lookup (hash-indexed by anomaly_type, the production lookup pattern). Report min/median/p95/max per-lookup latency over all 200. All 200 runs recorded; no outlier removal.
  - Baseline leg (bounded LLM calls): N = 20 corpus instances, one single-anomaly LLM resolution each, wall-clocked from request to validated tuple. Platform default (Automatic) engine, fresh API conversation per instance. 20 calls only — this leg is the ONLY credit-consuming part of the benchmark.
  - Reported speedup: median(baseline, n=20) / median(mesh, n=200), disclosed as a sampled-baseline ratio, not a per-call equality claim.
- **B2 — Mesh capacity and collision integrity (zero LLM calls).** Ingest 50 synthetic DualMeshNode records spanning both mesh types into the hub's own app (synthetic content only). Report: node counts by layer/mesh_type, collision_hash uniqueness, lock_state integrity, activation bookkeeping. No latency claim.
- **B3 — Resolution correctness (zero LLM calls).** Replay the CCR-1 accepted candidate set (72 permitted actions) through the mesh resolver. Expected: 0 false positives, 0 mismatches. Any mismatch is a recorded FAIL, not a re-run.

## Corpus

Frozen, deterministic, seeded: 200 synthetic anomaly instances derived from the frozen CCR roster (the 3 registered anomaly types: latency_spike -> PB-003: Latency Spike Resolver, heartbeat_miss -> PB-008: Heartbeat Re-igniter, quantum_vulnerability_detected -> PB-009: Quantum Vulnerability Migrator; metric variations per instance, no real-system data). Corpus file hashed and committed BEFORE any leg runs. The identical corpus file is used by B1 mesh and B1 baseline legs (falsifier FB-2).

## Environment and data discipline

Hub-own-app operations only. Synthetic records only. No customer identity, PHI, credentials, wallet identifiers or transaction amounts in any benchmark artifact (publication clearing scan applies to any public artifact). Platform configuration readback before the baseline leg; restored after.

## Execution gating

- Zero-credit legs (B1-mesh, B2, B3): may run on Leon GO.
- Credit-consuming leg (B1-baseline, ~20 LLM calls): runs only on separate Leon GO.
- Each leg produces raw logs preserved verbatim in the evidence folder. Any failed leg is recorded, not retried silently.

## Falsifiers

- FB-1: any published benchmark number without preserved raw logs = FAIL.
- FB-2: baseline and mesh legs using different corpora or different instance counts than declared = FAIL.
- FB-3: any run omitted from the distribution (cherry-picking) = FAIL.
- FB-4: any metric added after execution without a prereg amendment committed first = FAIL.
- FB-5: any PHI, customer identity, or credential in a benchmark artifact = FAIL.

## Claim discipline

Results update the Dual Mesh Benchmark status from NOT MEASURED to MEASURED (scoped to anomaly-to-playbook lookup on the frozen corpus, and mesh ingestion integrity on synthetic nodes) only after raw logs exist and Leon reviews. No universal performance claim, no extrapolation beyond the corpus, no certification language. Two-key curation before any public artifact.

This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
