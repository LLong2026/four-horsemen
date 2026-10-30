# CORRECTION — Telemetry Composition Disclosure (forward-only)

**Status:** PUBLISHED v1.0 — Zenodo + GitHub. Authorization: Leon GO (chat authorization, 2026-10-30 11:20 CT).
**Corrects:** THE CAGE REPORT, `CAGING_TELEMETRY_REPORT_v1.0.md`, DOI 10.5281/zenodo.23703012
(v1.0, published Zenodo + GitHub, Leon GO 2026-10-27 ~15:20 CT; companion DOI 10.5281/zenodo.23700617).
**Doctrine:** append-only since 2026-09-07. The original record is NOT edited or withdrawn. This
amendment is published alongside it and linked from its description.
**Author of record (on GO):** Leon Calvin Long, II — SQUIRL OS Technologies LLC
**Measured:** 2026-10-30T16:25Z, hub-of-record entity reads.

---

## Why this correction exists

Version 1.0 reports "7,076 anomalies detected" and states correctly that every figure is an entity
read rather than an estimate. That provenance statement is true and stands: no count in v1.0 was
invented, and any third party with entity access reproduces the same totals today (7,117 anomalies,
2,279 healing events, 223 predictive alerts, all consistent with three further days of operation).

What v1.0 does not disclose is the **composition** of that corpus. A substantial share of anomaly
rows are produced by the system's own test batteries, chaos ramps, and simulated-scenario generators
rather than by operational detection. A reader of the v1.0 abstract reasonably infers that 7,076
incidents occurred on a live fleet. That inference is not supported by the underlying rows, and the
omission is corrected here.

This is a characterization defect, not a numeric one. It is disclosed by the same principle the
report itself argues for: a claim that cannot survive an independent recount is not evidence.

## Measured composition (2026-10-30T16:25Z; 7,117 anomaly rows)

| Bucket | Rows | Share | Basis |
|---|---|---|---|
| Battery-labelled rows | 435 | 6.1% | `category` in {`V34-C1-L1000`, `centurion_r1`, `centurion_r2_heal`, `mega_heal`} |
| Simulated scenario family | 2,503 | 35.2% | `anomaly_type` in 12 generated types (see appendix) |
| Unclassified by label | 4,179 | 58.7% | no battery label; provenance not individually established |
| **Linked to a journaled healing event** | **123** | **1.7%** | `linked_healing_event_id` populated |

Demonstrably battery-generated: **2,938 rows (41.3%)**. Rows carrying a healing-event link:
**123 (1.7%)**. The remainder are not classified as organic; their provenance is unestablished and
they are reported as such rather than counted as operational incidents.

Mass-generation is visible in the write pattern: 77% of all anomaly rows arrived in eight bulk
bursts, and a single burst on 2026-07-19/20 wrote 1,256 rows of one type (`heartbeat_miss`), which
is 90% of that type's lifetime total.

## Further corrections to v1.0

1. **"Anomalies resolved 6,776 (95.8%)."** The status field reads `resolved` on 6,821 rows, but only
   123 rows carry a healing-event link. "Resolved" therefore denotes a status transition, not a
   journaled engineered remedy. v1.0 must not be read as "6,776 anomalies were healed."
2. **"123/123 critical alerts resolved via owner acknowledgment (100%)."** As of 2026-10-30T16:25Z
   there are 126 critical predictive alerts: 125 resolved, 1 open. The ACK-sufficiency standard was
   only defined in the 2026-10-23 amendment (SIP DOORS-1), which implies that acknowledgments
   predating it were not tested against it. The claim is restated as: criticals were resolved
   through the owner-acknowledgment path per the governance in force at the time, and the strict
   standard now in force has been applied since 2026-10-23.
3. **"Zero false positives."** Contradicted by findings after publication: playbook success counts
   were seeded rather than event-derived (corrected 2026-10-29 by the ledger reconciliation), and the
   fleet heartbeat layer reported success over failing sub-tasks (identified 2026-10-30). The metric
   described the sentinel's own deterministic pass, not the system. Restated as scoped to that pass.
4. **Fleet size.** v1.0 reports eight applications; the roster now carries ten members (SteamPulse
   added 2026-10-30, hub counted as a member). Means over different roster sizes are not comparable
   and will be reported with the roster size attached.

## What stands unchanged

No correction is required to, and no part of this amendment withdraws:

- Cage-cycle watch: 0 escapes / 60 recorded cycles (DOI 10.5281/zenodo.23425579)
- Falsifier battery: 109/109 held (DOI 10.5281/zenodo.23430655)
- Governance isolation under unbounded drift, HEMI-T2 (DOIs 10.5281/zenodo.23330308, 23330348, 23330361)
- Sovereignty stress SOV-B1: charter invariance 9/9 epochs, 100% budget hold (DOI 10.5281/zenodo.23628676)
- SIP-N18-01 playbook genesis receipt, and the DR-2 byte-exact restore drill
- Every independent-measurement result: these are re-runnable by a stranger from the artifacts, which
  is the property that separates them from the corpus counts above.

## Method (re-runnable)

All figures derive from `AegisAnomaly`, `AegisHealingEvent`, and `PredictiveAlert` entity reads on the
hub-of-record at the timestamp stated. Bucket definitions are the label sets in the appendix; the
"linked to a healing event" bucket is `linked_healing_event_id` non-null. The classification is
mechanical and reproducible by any reader with entity access; no bucket depends on judgment.

## Forward commitment

Every future public telemetry figure separates **organic** (detection with a journaled event chain),
**battery/simulated** (generated by a named test or chaos source), and **unclassified** (provenance
not established). A headline number may not combine them without stating the split. Where a metric
cannot be independently recounted, it is reported as scoped, not as measured.

## Appendix — simulated scenario family (12 types)

`heartbeat_miss` (1,402), `certificate_mass_expiry` (173), `cooling_system_failure` (171),
`ransomware_lateral_movement` (99), `hvac_cascade_failure` (99), `ups_battery_cascade` (96),
`data_center_fire` (96), `supply_chain_compromise` (93), `dns_failure_cascade` (93),
`firmware_corruption_cascade` (91), `fire_suppression_disaster` (90), `cloud_provider_regional_outage` (90).

These are facility-scale scenarios (data-centre fire, UPS cascade, fire suppression) that exceed the
operational footprint of a prototype deployment. They are retained as battery evidence and are not
claimed as detected incidents.
