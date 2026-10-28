<div align="center">

# THE FOUR HORSEMEN
### SQUIRL OS Deterministic-Machine Benchmark Line (H-Line)

## TERMINOLOGY NOTE (reset, Oct 19 2026 — ledger 0244)

The word "tokenization" is retired from forward-facing language. What this program does is
**multi-rail evidence anchoring**: non-custodial, keyless-verifiable inscription of artifact
digests across independent mainnets. No tokens are created, moved, or needed — tokens were
never the point, and they add nothing to moving assets on-chain in this architecture.
Historical records below keep their original wording (append-only doctrine); everything
new says anchoring.

## SERIES NAMING NOTE (2026-10-28 — ledger 0384)

Test series are named after mechanisms, not after historical events. Names that reference armed
conflicts, landings, campaigns, or the people who died in them are retired from forward use: a
codename should describe what a test does to a system, never borrow gravity from a real event.
The compound blackout storm family is named **BLACKOUT** from this date, with `BLACKOUT-1` reserved
for its next execution. Published records keep their names (append-only) and are cited by identifier
alone in cross-border material. Measurements are untouched; vocabulary changed only.
Full convention: [NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md).

**Four machines. One stable. Matched inputs. Separate ledger.**

</div>

---

## The Proof-Day Record — Four Anchors in One Day (originally titled "Tokenization Without Tokens"; see terminology note, ledger 0244)

Four artifacts tokenized in a single day across Bitcoin and XRP mainnets, with zero tokens:
only 32-byte SHA-256 fingerprints ever touch a chain. The session record (with live receipts)
is at https://doi.org/10.5281/zenodo.23462705, and every Zenodo publication in this corpus
now links to it. Public verification portal: https://deterministic-code-dsos.base44.app/genesis-viewer

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
- [MILESTONE_HITL_N10_Critical_Receipt.md](MILESTONE_HITL_N10_Critical_Receipt.md) — first fully receipted human-in-the-loop critical resolution cycle (N10-ACK)
- [SOVEREIGN_BRIEFING_HITL_N10-ACK.md](SOVEREIGN_BRIEFING_HITL_N10-ACK.md) — sovereign-audience briefing on the N10-ACK cycle (archived: DOI 10.5281/zenodo.23152633, concept DOI — latest version 10.5281/zenodo.23173948)
- [SOV-B1 Announcement](tokenization-adoption/sov_b1/SOV_B1_ANNOUNCEMENT.md) — sovereign territory battery research announcement: charter, borders, treasury, no-self-pardon on a zero-lineage LLM consensus cluster (DOI 10.5281/zenodo.23628676)

## Doctrine

- Preregistered before first inputs (freeze-then-test)
- Append-only ledger; amendments are new entries, never rewrites
- Playbooks immutable at runtime; changes via proposal -> human approval -> deployment
- PQC-only (CRYSTALS-Dilithium3 / Kyber-1024 / SPHINCS+-256f)
- No PHI, credentials, wallet addresses, or customer-identifiable data in any log

**13 patents pending + 5 SBIR tracks** — Leon Calvin Long II / SQUIRL OS Technologies

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.
