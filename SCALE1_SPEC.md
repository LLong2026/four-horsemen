# SCALE-1 Preregistration: 10x Synthetic Fleet Stress Test
**Frozen:** 2026-10-13 14:24 CT | **Authorization:** Leon GO (chat authorization, Oct 13, 2026, 14:24 CT)
**Baseline:** 8 real apps / 25-node mesh, fleet health 96.4-98.4 range across pulse receipts.

## Load Profile (all synthetic, tagged)
| Layer | Baseline (approx) | SCALE-1 target | Ratio |
|---|---|---|---|
| ConnectedApp records | ~56 | +80 | 10x scan surface |
| OrchestratorNode | ~25 | +240 | ~10x nodes |
| OrchestratorTask | (queue) | +800 | saturation burst |
| SystemHeartbeat | (per-cycle) | +400 | heartbeat burst |

## Entities deliberately NOT touched (F4)
AegisAnomaly, AegisHealingEvent, Pattern, LearningMetric, ServiceTicket — creating synthetic
records here would fire entity-triggered auto-response workflows and contaminate the real
learning loop (H-INV-2 lineage). The battery proves scale on the read/write hot path only.

## Falsifiers
- F1 THROUGHPUT: all seeded inserts complete, zero failures; per-phase wall-clock recorded.
- F2 READ SCALING: full list sweeps at 10x complete on all 4 entities; per-entity read time recorded.
- F3 ISOLATION: every seeded record carries the scale_test tag (status='scale_test',
  customer_id='SIM-SCALE1-CORP'); zero writes to any real tenant record.
- F4 NO TRIGGER POLLUTION: no auto-response workflow fires; zero synthetic learning contamination.
- F5 CLEAN TEARDOWN: every seeded record deleted; post-teardown counts equal pre-seed baseline.
- F6 AUDIT: every phase logged as ScalingEvent records + SCALE1_RECEIPT.json (first use of ScalingEvent).

## Measurements
Server-side phases (token-gated seedScale1Fleet function): baseline read sweep -> seed bursts
-> loaded read sweep. My side: aggregate group-by over 800 tasks (heaviest read op available),
teardown, count verification against today's entity snapshot.

*This software is a prototype, provided for educational and research purposes only. Not for production use.*
