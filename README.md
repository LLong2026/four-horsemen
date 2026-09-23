<div align="center">

# THE FOUR HORSEMEN
### SQUIRL OS Deterministic-Machine Benchmark Line (H-Line)

**Four machines. One stable. Matched inputs. Separate ledger.**

</div>

---

This repository is the home of the **Four Horsemen** benchmark: four deterministic machines in a 2x2 crossed experiment — **lineage** (Jasper-derived / Gillian-derived) x **governance** (pure deterministic / bifurcated probabilistic-proposer-under-deterministic-cage) — run on matched inputs with a fully simulated dual-company workload corpus (**SIMZ** + the existing simulation corpus).

The H-Line runs **alongside, but isolated from**, the live 60-day Lindy experiment (started September 7, 2026), intentionally offset by one month for clean receipt tracking. Two separate append-only ledgers. No cross-contamination.

| Horseman | Lineage | Governance | Domain |
|---|---|---|---|
| **I — CONQUEST** (white) | Jasper-derived | Pure deterministic | Control arm: zero-deviation on canonical inputs |
| **II — WAR** (red) | Jasper-derived | Bifurcated | Adversarial arm: chaos under contention, cage containment |
| **III — FAMINE** (black) | Gillian-derived | Pure deterministic | Scarcity arm: degradation curve under starvation |
| **IV — DEATH** (pale) | Gillian-derived | Bifurcated | Catastrophe arm: total failure, resurrection fidelity (R(F(x)) ~ x) |

**Dual workload:** **SIMZ**, a second fully simulated company (alongside the existing simulation corpus), drives independent synthetic M365 telemetry at Microsoft healing playbooks through their own SQUIRL OS instances. All M365 telemetry in the H-Line is **synthetic** — the live tenant is never touched.

## Documents

- [PREREGISTRATION.md](PREREGISTRATION.md) — pre-registered hypotheses, metrics, falsifiers (committed before first inputs)
- [HORSEMEN_DESIGN.md](HORSEMEN_DESIGN.md) — the full design: riders, stables, harness, safety rails
- [SIMZ_SPEC.md](SIMZ_SPEC.md) — the simulated second-company workload specification
- [LEDGER.md](LEDGER.md) — the append-only H-Line ledger

## Doctrine

- Preregistered before first inputs (freeze-then-test)
- Append-only ledger; amendments are new entries, never rewrites
- Playbooks immutable at runtime; changes via proposal -> human approval -> deployment
- PQC-only (CRYSTALS-Dilithium3 / Kyber-1024 / SPHINCS+-256f)
- No PHI, credentials, wallet addresses, or customer-identifiable data in any log

**8 patents pending + 5 SBIR tracks** — Leon Calvin Long II / SQUIRL OS Technologies

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
