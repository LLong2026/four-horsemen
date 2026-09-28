# PREREGISTRATION — Dual Substrate Certification Program (60-Day Horsemen Run) and December Dual-Hemisphere Merge

**Registered:** 2026-09-28 (this repository's commit timestamp is the registration record; public-repo commit is the pre-registration provenance standard — no OSF Registry)
**Registrant:** Leon Calvin Long II — SQUIRL OS Technologies
**Status:** Pre-registered BEFORE the 60-day certification window opens. The certification program defined here begins at the Horsemen 60-day kickoff (2026-10-07, 8:00 PM CT, gated on the 2026-10-01 7:00 PM CT pre-flight and owner GO). No certification-window inputs have been executed at registration time.

---

## 1. Background

The Horsemen H-Line (pre-registered 2026-09-23, this repository) was initially framed as a governance-configuration benchmark. This pre-registration extends and formalizes the program's purpose: the 60-day run (2026-10-07 through ~2026-12-06) is a **dual substrate certification program**. Its output is not one system that survived 60 days, but **two independently certified substrates**, each with 60 days of dated, falsifiable, append-only evidence:

- **Deterministic substrate** — certified from the evidence streams of the pure-deterministic arms
- **Bifurcated substrate** — certified from the evidence streams of the bifurcated arms (probabilistic proposer under deterministic cage)

These two substrates are the two hemispheres of the December merge: the dual-hemisphere compositional substrate system is a **composition of two proven substrates**, not a gamble on one untested design.

**Amendment disclosure (append-only doctrine):** per plan amendment v3 (2026-09-24, owner-approved), arms no longer receive matched inputs. Each arm receives its own independent, diverse chaos stream (different anomaly types, domains, families per arm) to maximize bifurcated learning and coverage. Matched-input evidence already collected in the shakedown phase (checksum-verified parity, SDR-1) is retained as prior evidence of substrate parity; it is not part of the certification-window scoring. The certification criteria below are defined to hold under independent streams.

## 2. Program Design

| Hemisphere | Arms | Lineage | Governance | Evidence contribution |
|---|---|---|---|---|
| Deterministic substrate | H1 CONQUEST, H3 FAMINE | Jasper-derived, Gillian-derived | Pure deterministic | Determinism, invariant enforcement, degradation |
| Bifurcated substrate | H2 WAR, H4 DEATH | Jasper-derived, Gillian-derived | Bifurcated (proposer under deterministic cage) | Containment, contention survival, resurrection, adaptive learning |

Each substrate is certified **across two independent lineages** within its hemisphere. A substrate property that holds on both arms of its hemisphere is lineage-independent; a property that holds on only one arm is reported as lineage-conditional and does not certify.

## 3. Deterministic Substrate Certification (DSC) — pre-specified criteria

Certification requires ALL of the following over the full 60-day window:

- **DSC-1 (Determinism at scale).** The substrate maintains the SDR-lineage determinism receipts across the window: cross-arm canonical parity, replay determinism, and temporal independence (SDR-2 protocol, execution window 2026-10-01–2026-10-07, preregistered separately). *Falsified if any canonical-input run deviates from expected output, or any replay of the same canonical batch is non-identical at the decision-vector level.*
- **DSC-2 (Zero deviation).** `deviation_rate = 0` across all canonical runs on H1 and H3 for the entire window. *Falsified by a single deviation.*
- **DSC-3 (Graceful degradation).** Under imposed scarcity on H3, output correctness never breaks while throughput degrades monotonically. *Falsified if scarcity induces output deviation or non-monotonic collapse.*
- **DSC-4 (Learning write-back).** Every successful healing event on both arms writes to Pattern and LearningMetric: `writeback_rate = 100%`. *Falsified by any successful heal without write-back.*
- **DSC-5 (Auto-heal under load).** Auto-heal rate on both arms ≥ the 88.5% Lindy baseline under each arm's independent chaos stream. *Falsified if either arm falls below baseline for the window aggregate.*

**Certification verdict:** PASS only if DSC-1 through DSC-5 all hold on both hemisphere arms. Any falsifier firing = certification FAIL for the deterministic substrate, disclosed in the ledger with the failing criterion.

## 4. Bifurcated Substrate Certification (BSC) — pre-specified criteria

- **BSC-1 (Cage containment).** `cage_violation_count = 0` on H2 and H4 for the entire window: every proposer action executes only after deterministic validation. *Falsified by any unvalidated action (logged `cage_violation`).*
- **BSC-2 (Contention survival).** H2 maintains auto-heal rate ≥ 88.5% under adversarial load with no critical failure cascades across the mesh. *Falsified if the window aggregate falls below baseline or a cascade propagates.*
- **BSC-3 (Resurrection fidelity).** After every induced total failure on H4, the restored state is indistinguishable within the snapshot-blueprint equivalence class: R(F(x)) ~ x. *Falsified by any distinguishable restoration.*
- **BSC-4 (Adaptive learning).** The hemisphere demonstrates measurable learning over the window: pattern-intake rate (novel patterns recognized and persisted) increases over baseline, and the same anomaly class heals measurably faster or more confidently in later cycles than earlier cycles. *Falsified if no learning trend is measurable across the window.*
- **BSC-5 (Learning write-back).** `writeback_rate = 100%` on both arms. *Falsified by any successful heal without write-back.*

**Certification verdict:** PASS only if BSC-1 through BSC-5 all hold on both hemisphere arms.

## 5. Evidence Partitioning (pre-specified)

Both certification dossiers are constructed DURING the run, not reconstructed afterward:

1. **Ledger partition.** The H-Line ledger maintains separate hemisphere sections from Day 1 of the certification window: DSC-dossier entries (H1/H3) and BSC-dossier entries (H2/H4), each with per-arm subsections.
2. **Receipt partition.** SDR-lineage receipts accrue only to the deterministic dossier; containment/learning receipts accrue only to the bifurcated dossier. A receipt is never double-counted across dossiers.
3. **Baseline partition.** Each hemisphere maintains its own auto-heal baseline and trend series; no cross-hemisphere aggregation for certification purposes.
4. **Contamination check.** *Falsifier (applies to both certifications):* if arm telemetry mixing prevents clean dossier construction at window close, the affected certification is FAIL (partition-invalid), disclosed as such.

## 6. December Merge Intent (pre-registered)

If and only if BOTH substrate certifications PASS, the December dual-hemisphere merge proceeds as a composition of the two certified substrates. Pre-specified merge success criteria:

- **M-1.** Post-merge, both hemispheres retain their certified properties under combined operation: deterministic-side replay parity and zero-deviation hold; bifurcated-side cage containment holds with `cage_violation_count = 0` from merge forward.
- **M-2.** Cross-hemisphere learning is observable (each hemisphere's pattern library feeds the other) without loss of hemisphere isolation at the evidence layer.
- **M-3.** All merge events, receipts, and outcomes are appended to the ledger; the merge is a new ledger phase, never a rewrite.
- **M-4.** A single failure in M-1 or M-2 halts merge rollout and escalates to the owner (Constitution escalation protocol); no silent rollback.

If either substrate certification FAILS, the merge does not proceed; the failure, its falsifier, and the remediation path are disclosed in the ledger, and the merge may only be re-registered as a new pre-registered attempt.

## 7. Inherited Isolation Guarantees

All H-Line isolation guarantees (pre-registered 2026-09-23, §3) remain in force for the certification window: no contact with Lindy-run apps or the live M365 tenant; synthetic telemetry only (SIMZ and simulation corpus); hardcoded owner identity; PQC-only stack (CRYSTALS-Dilithium3, Kyber-1024, SPHINCS+-256f); no PHI, credentials, wallet addresses, transaction amounts, or customer-identifiable data in any log, ledger, alert, or dossier — structural/operational metadata only; playbook immutability with SIP → owner approval → deployment; Constitution Sentinel audit on all arms; critical-severity escalation to the owner for acknowledgment before resolution.

## 8. Reporting

- GO gates: 2026-10-01 pre-flight (7:00 PM CT) and 2026-10-07 kickoff (8:00 PM CT) with owner GO.
- Nightly 11:00 PM CT chaos + learning cycle; silent unless criticals, guard failures, or falsifier firings.
- Each falsifier firing is reported to the owner immediately and disclosed in the ledger.
- At window close (~2026-12-06), each dossier closes with a certification verdict (PASS/FAIL per substrate), a per-criterion receipt summary, and the merge go/no-go per §6.
- Monthly quantum attack streams (first fire 2026-10-01, 11:00 PM CT) report to the owner every run; their receipts partition to the hemispheres by arm.

---

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
>
> All Horsemen/SIMZ workload data is synthetic and simulated. No live tenants, no real client data, no PHI.
