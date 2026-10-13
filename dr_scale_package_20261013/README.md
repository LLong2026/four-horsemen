# DR-1 + SCALE-1: Disaster-Recovery Entity-Export Surface and 10x Synthetic Fleet Stress Test

**Date:** October 13, 2026 | **Operator:** Leon Calvin Long, II — SquirlOS Technologies LLC
**Authorization:** Leon GO (chat authorization, Oct 13, 2026, 13:15 / 14:24 CT) | **Vetted:** Gabriel (two-key curation)

## DR-1: Entity-Export Backup Surface (closes BackupStatus 4/4)

The hub entity store had no byte-exact backup surface. Direct REST export was unavailable to the
agent credential; chat-context transport was payload-infeasible. The working architecture is a
token-gated backend function (`exportEntitySnapshot`, source included): service-role reads,
server-side PII stripping (created_by fields never leave the store), 403 for unauthenticated calls.

**Baseline committed:** 56 entities, 15,497 records, 11 MB — hygiene-scanned with a disclosed
redaction doctrine: third-party vendor contacts redacted; the owner's personal-finance entity
(HouseholdBill) EXCLUDED from the public snapshot as not covered by the company open-book doctrine;
synthetic seeded customer corpus (~555 records) verified fair-game. Nightly automation registered
(04:00 CT, stamp-before-execute idempotency).

**Disclosed instrument quirk:** server SDK list() returns EMPTY under any numeric limit param;
no-param list() returns records (probed, probe deleted). AegisAnomaly capped at 5,000 most-recent.

## SCALE-1: 10x Synthetic Fleet Stress Test (first use of ScalingEvent)

Preregistered spec (frozen before execution) with six falsifiers, ALL PASS. 2,320 synthetic records
(80 ConnectedApp, 240 OrchestratorNode, 1,600 OrchestratorTask, 400 SystemHeartbeat), all tagged
`scale_test` + `SIM-SCALE1-CORP`.

**Read path (the strength):** sub-second full sweeps at 10-26x record counts — 441ms over 1,632
tasks, 344ms over 1,011 heartbeats; aggregate group-by instant, summing 3.35M tokens.

**Write boundary (measured):** ~4-6 records/sec per server-side connection; 2,320 records in ~5.5 min.
Batched bulk insert is the identified next engineering step for live 10x scale.

**Honest findings, both receipted:** (1) OrchestratorTask.priority is a string field — v1 seeder
sent integers, 800/800 rejected, fixed and reseeded. (2) The task seed DOUBLE-FIRED (1,600 vs 800)
under a session error — the exact race the stamp-before-execute amendment formalized the same day;
the tag-filter teardown absorbed it completely, verified 2,320/2,320 BY FILTER, and post-teardown
counts returned byte-exact to baseline (85/75/32/611).

**Safety:** anomaly, healing, pattern, learning, and ticket entities untouched; no auto-response
workflow could fire; zero learning contamination; the real fleet was never at risk.

## Dual Mesh Benchmark

**NOT MEASURED** for the DR-1 and SCALE-1 batteries. Per policy, the Dual Mesh Benchmark is marked
MEASURED only for the DeepSeek column (DOI 10.5281/zenodo.23345241) and NOT MEASURED otherwise.

## Contents

- README.md (this file) — DR1_RECEIPT.json — SCALE1_SPEC.md (frozen preregistration)
- SCALE1_RECEIPT.json — LEDGER_0091_0093.md (append-only ledger entries: key escrow 0091,
  entity-export live 0092, SCALE-1 0093) — MANIFEST.json (snapshot manifest) — exportEntitySnapshot.ts

The full 11 MB baseline entity snapshot is public in the transparency repository
(commit e3af11e) and is referenced, not duplicated, here.

> This software is a prototype and is provided for educational and research purposes only. It is not
> intended for production use, commercial deployment, or safety-critical environments. All data is synthetic.
