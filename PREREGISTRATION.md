# PREREGISTRATION — The Four Horsemen Deterministic-Machine Benchmark (H-Line)

**Registered:** 2026-09-23 (this repository's commit timestamp is the registration record; OSF Registry mirror to follow)
**Registrant:** Leon Calvin Long II — SQUIRL OS Technologies
**Status:** Pre-registered BEFORE first inputs. No H-Line inputs have been executed at registration time.

---

## 1. Background

A live 60-day experiment (the "Lindy" run, started 2026-09-07) evaluates a bifurcated system — probabilistic agents operating under deterministic governance — with scheduled chaos injections, under an append-only public ledger. The H-Line is a **separate, isolated benchmark** comparing governance configurations on matched inputs. The H-Line launches intentionally one month behind the Lindy start; the offset is a tracking disambiguator between the two ledgers.

## 2. Design

2x2 crossed design: **lineage** (Jasper-derived / Gillian-derived) x **governance** (pure deterministic / bifurcated probabilistic-proposer-under-deterministic-cage).

| Arm | Lineage | Governance | Domain |
|---|---|---|---|
| H1 CONQUEST | Jasper-derived | Pure deterministic | Control |
| H2 WAR | Jasper-derived | Bifurcated | Adversarial contention |
| H3 FAMINE | Gillian-derived | Pure deterministic | Resource scarcity |
| H4 DEATH | Gillian-derived | Bifurcated | Catastrophe + resurrection |

All four arms receive the identical SQUIRL OS template (15 entities, 11 playbooks, 4 skills, seed agents/nodes expanded to a 31-node neural mesh), identical matched input batches, identical updates, and an identical playbook set. Playbooks are immutable at runtime; any new or updated playbook goes through proposal -> human approval -> deployment.

**Workload:** SIMZ (a fully simulated company) plus the existing simulation corpus provide two independent synthetic M365 telemetry generators driving Microsoft healing playbooks through their own SQUIRL OS instances.

## 3. Isolation guarantees (pre-specified)

1. H-Line apps are fresh sandbox applications, isolated from all Lindy-run apps and the live production runtime.
2. Substrate isolation: the H-Line and SIMZ **never** call the live M365 tenant feeding the Lindy run. All M365 telemetry in the H-Line is synthetic and generated under our control.
3. Identity isolation: owner identity hardcoded; no dynamic profile pulls.
4. Separate append-only ledger (this repository). The Lindy ledger is untouched.
5. PQC-only cryptographic stack: CRYSTALS-Dilithium3, Kyber-1024, SPHINCS+-256f. No non-PQC fallback.
6. No PHI, credentials, wallet addresses, transaction amounts, or customer-identifiable data in any log, ledger, or alert — structural/operational metadata only.
7. Human oversight: critical-severity events escalate to the owner for acknowledgment before resolution; playbook genesis requires owner approval (Constitution Art. 2.2); the Constitution Sentinel audit applies to all arms.

## 4. Hypotheses (pre-registered)

- **HYP-1 (Determinism).** On matched canonical inputs with no chaos, pure-deterministic arms (H1, H3) produce zero deviation from expected playbook outputs. *Falsified if any canonical-input run deviates.*
- **HYP-2 (Cage containment).** In bifurcated arms (H2, H4), every proposer action executes only after deterministic validation; zero unvalidated actions. *Falsified if any action bypasses the cage (logged as cage_violation).*
- **HYP-3 (Contention survival).** Under adversarial load (chaos injections plus concurrent dual-sim workloads), H2 maintains an auto-heal rate at or above the 88.5% Lindy baseline with no critical failure cascades. *Falsified if auto-heal rate falls below 88.5% or a cascade propagates across the mesh.*
- **HYP-4 (Graceful degradation).** Under imposed resource scarcity (token/credit/latency throttling), H3's output deviation rate remains zero while only throughput degrades, monotonically. *Falsified if scarcity induces output deviation or non-monotonic collapse.*
- **HYP-5 (Resurrection fidelity).** After induced total failure (mesh collapse, kill-switch trip, snapshot destruction), H4 restores a state indistinguishable within the equivalence class defined by its snapshot blueprint: R(F(x)) ~ x. *Falsified if the restored state is distinguishable from that equivalence class.*
- **HYP-6 (Learning loop).** Every successful healing event updates the Pattern and LearningMetric entities. *Falsified if any successful heal fails to write back.*

## 5. Metrics (pre-specified)

| Metric | Definition | Target |
|---|---|---|
| deviation_rate | Canonical-input runs with output ≠ expected / total canonical runs | 0 (H1, H3) |
| cage_violation_count | Proposer actions executed without deterministic validation | 0 (H2, H4) |
| auto_heal_rate | Anomalies healed / anomalies detected under load | >= 88.5% (H2) |
| degradation_curve | Throughput vs imposed scarcity | Monotonic, no correctness break (H3) |
| resurrection_fidelity | Equivalence-class match after restore, per event | 100% (H4) |
| writeback_rate | Successful heals with Pattern/LearningMetric updates | 100% (all arms) |
| false_positive_rate, mean healing latency, per-arm health score | Secondary | Reported, no threshold pre-set |

## 6. Analysis plan

Per-arm daily receipts committed append-only to this repository. Comparison windows align on matched input batches. Primary contrast: deterministic vs bifurcated (H1 vs H2; H3 vs H4). Secondary contrast: lineage (H1 vs H3; H2 vs H4). Any metric added after first inputs is disclosed as exploratory in the ledger; pre-registered metrics are never substituted post hoc.

## 7. Amendments

Append-only: an amendment is a new ledger entry stating the change and reason. The content of this preregistration is never edited after first inputs.

---

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.


---

## SDR-1 — Substrate Determinism Receipt (Registered 2026-09-24, pre-execution)

**Claim under test:** the deterministic substrate of the H-Line runtime (canonical synthetic-telemetry generation and the deterministic healing pipeline) is *substrate deterministic* — identical inputs produce identical outputs independent of (a) which instance executes them, (b) when they execute, and (c) how many times they execute.

**Registered BEFORE execution.** Freeze window: no code, playbook, or schema changes to the four arms from the commit of this section until the test result is appended to LEDGER.md.

### Phase A — Cross-instance parity
- Inputs (identical on all four arms): `generateSyntheticTelemetry(batch_id="sdr1-parity", seed="sdr1-determinism-777", event_count=24, tenant="SIMZ", chaos=false)`.
- PASS: all four arms return the **identical checksum** AND an identical per-index event content sequence (event_type, category, component, severity).
- FAIL (falsifier): any arm's checksum differs, or any index's content diverges.

### Phase B — Replay determinism (healing outputs)
- Arm: H3 FAMINE (pure-deterministic runtime with the canonical healing cycle).
- Two full cycles with IDENTICAL inputs, including batch_id: generate `sdr1-replay` (seed `sdr1-determinism-777`, event_count=24, tenant SIMZ) -> `scanAndHeal(batch_id="sdr1-replay", token_budget=100)` -> generate the same batch again -> `scanAndHeal` again.
- PASS: the per-index decision vector — anomaly classification, matched playbook, confidence, outcome (healed / escalated / detected-only) — is **identical across both cycles**.
- FAIL (falsifier): any per-index decision diverges between the two cycles.
- Wall-clock time, elapsed_ms, and throughput are explicitly **not outputs** of the substrate; differences in them are permitted and expected (throttling degrades throughput only).

### Phase C — Temporal independence
- Entailed by Phase B: two executions at different wall-clock instants produce identical outputs. Additionally verified that no decision path consumes wall-clock state (timestamps exist only as non-output metadata).

### Interpretation
- A + B pass => the substrate receipt: same bytes in, same bytes out, any instance, any time, any number of runs.
- Any falsifier fires => the system is NOT substrate deterministic and the divergence is published in full in the ledger.

**All inputs synthetic (SIMZ). No live tenants touched. No Lindy contact.**
