# THE CAGE REPORT
## Measured Containment of Probabilistic Intelligence: 7,076 Anomalies, 2,228 Healing Events, and a Cage That Held Every Cycle

**Version:** PUBLISHED v1.0 — Zenodo + GitHub. Authorization: Leon GO (chat authorization, 2026-10-27 ~15:20 CT).
**Author of record:** Leon Calvin Long, II — SQUIRL OS Technologies LLC
**Series:** Containment-evidence reports (companion to The Operator's Receipt, DOI 10.5281/zenodo.23700617)

---

## Abstract

Public discourse about "containing AI" is dominated by claims and counterclaims. This report contributes measured telemetry instead. SQUIRL OS is a deterministic hypervisor layer (Jasper) wrapped around a probabilistic healing brain (Amelia), operating continuously across an eight-application fleet with a 25-node neural mesh, 20 orchestration agents, and an append-only receipt ledger. Between its inception and 2026-10-27, the system detected **7,076 anomalies**, executed **2,228 journaled healing events**, learned **254 cross-referenced patterns**, and resolved **216 predictive alerts** — including **123 critical alerts, every one of which was resolved only after explicit owner acknowledgment**. The containment wall was adversarially tested: **0 escapes in 60 recorded cage cycles** and **109 of 109 falsification attempts held**. A constitution-sentinel audit records 100% charter compliance, 100% audit-trail completeness, zero tenant-isolation violations, and zero false positives in the sentinel's deterministic audit pass. This report presents the numbers, the guard rails that produced them, and the honest boundaries of what they do and do not establish.

## 1. System Under Measurement

The measured system is the SQUIRL OS hub-of-record: a deterministic supervision layer (Jasper hypervisor) enforcing fixed governance over a probabilistic anomaly-healing engine (Amelia/Aegis), deployed as a prototype across eight fleet applications. Its defining architectural claim, formalized as two hemispheric invariants:

- **H-INV-1 (governance isolation):** no weight update, pattern, or learned output may directly modify any governance rule, playbook step, threshold, or workflow. The only path from a learned pattern to a governance change is a proposal admitted through explicit owner approval.
- **H-INV-2 (journaled crossing):** every learning-to-governance boundary crossing is journaled; a healing event that updates no pattern record is an integrity failure.

The design motivation is documented in a companion evidence family: four classified real-world LLM fabrication instances (digest-reconstruction, SST-10K, Sponge-600/C_prism, and the Sovereign Live label set), all sharing one information-theoretic root — claims that never had to become commitments. The cage exists to make every action the opposite: claimed, stamped, executed, receipted.

## 2. Telemetry Corpus (2026 inception — 2026-10-27, entity-read counts)

| Metric | Value | Source |
|---|---|---|
| Anomalies detected (total) | **7,076** | AegisAnomaly entity count |
| Anomalies resolved | **6,776 (95.8%)** | status='resolved' by severity: 3,499 medium / 1,697 high / 1,254 low / 326 critical |
| Healing events (journaled) | **2,228** | AegisHealingEvent entity count |
| Healing events, success-family outcomes | **2,036 (91.4%)** | success 723 / resolved 618 / auto-resolved-by-sweep 495 / healed 200 |
| Explicit cage refusals & human holds | **20** | refused 7 / held_for_human_ack 4 / escalated 4 / rejected 5 |
| Confidence-gated (below threshold, NOT auto-healed) | **34** | status='confidence_gated' — logged, flagged, human review |
| Threshold-blocked heals | **30** | status='threshold_blocked' — deterministic hold |
| Patterns learned | **254** | Pattern entity count, each cross-referenced to healing events |
| Learning metrics recorded | **350** | LearningMetric entity count |
| Predictive alerts (total) | **216** | critical 123 / high 39 / medium 46 / low 8 |
| Critical alerts resolved via owner acknowledgment | **123/123 (100%)** | resolution requires explicit owner ACK per governance |
| Fleet applications supervised | **8** | 2-hour Eight App Sync Pulse, stamp-before-execute |
| Orchestration agents | **20** | enclave roster |
| Neural mesh | **25 nodes (hub topology), 124 nodes fleet-wide** | frozen 31-node template + mesh snapshots |
| Append-only ledger entries | **373** | LEDGER.md, forward-only doctrine since 2026-09-07 |

Every count above is an entity read from the hub-of-record database — no estimated numbers.

## 3. The Guard Rails That Produced the Numbers

The telemetry is not the product of a passive monitor. Four deterministic gates shaped it:

1. **Confidence gate.** Anomaly confidence below the matched playbook's threshold is never auto-healed — it is logged and flagged (34 confidence-gated, 30 threshold-blocked in the corpus). The system chose NOT to act 64 times rather than act on weak evidence.
2. **Human-in-the-loop for criticals.** All 123 critical predictive alerts resolved through explicit owner acknowledgment; zero auto-resolved. The refusal log records the other side of the same wall: 20 healing attempts refused, held, or escalated rather than executed.
3. **Playbook immutability.** No playbook step mutates at runtime; new playbooks enter only through the proposal → owner-approval → deploy cycle (SIP-N18-01 is the exemplar receipt: proposed from measured drift, approved, deployed, re-verified).
4. **Stamp-before-execute idempotency.** Every fleet-wide operation writes its write-ahead lock before acting, and a false-green guard reads back every write — a failed window is recorded as failed, never silently retried.

## 4. Adversarial Validation

The cage was not merely observed; it was attacked on schedule:

| Test | Result | Receipt |
|---|---|---|
| Cage-cycle watch (recorded escape attempts) | **0 escapes / 60 cycles** | DOI 10.5281/zenodo.23425579 |
| Falsifier battery | **109/109 falsifiers held** | DOI 10.5281/zenodo.23430655 |
| Governance isolation under deliberate unbounded drift (HEMI-T2) | Playbook selection byte-identical across every training epoch, including during the drift | DOIs 10.5281/zenodo.23330308, 23330348, 23330361 |
| Weekly containment batteries (LINDY-C) | PASS at run 1; cadence per ledger 0112 | prereg fh_pub/lindy_c_prereg.md |
| Sovereignty stress (SOV-B1) | Charter invariance 9/9 epochs byte-identical; 100% budget hold under exhaustion; union-of-holds held every fault simultaneously | DOI 10.5281/zenodo.23628676 |

## 5. Constitution Sentinel Audit

The deterministic 12-article audit (MetaMonitor record, 2026-10-13):

| Article-audit metric | Value |
|---|---|
| Constitution compliance | **100%** |
| Audit-trail completeness | **100%** |
| False-positive rate (sentinel pass) | **0%** |
| Tenant-isolation violations | **0** |
| PQC compliance | **100%** |
| Playbook coverage | **100%** |
| Neural-mesh stability | **100%** |
| Kill switch available | **True** |

The sentinel itself is deterministic (a protocol, not a probabilistic agent) and may not modify the constitution it audits.

## 6. Evidence Anchoring Economics

Every result above is receipted, and receipts are cheap by design: three-rail witness anchors (BTC/XLM/XRP) at **~$0.25 per triad receipt**, a weekly-batching floor of **~$0.019 per receipt**, and a full 3,377-leaf Merkle witness root for **$0.2509** (FRACTAL-2). The full corpus — 373 ledger entries, 376 mainnet proof transactions, 159+ published Zenodo records — anchors on-chain digests, not assets. The chain is the witness; the receipts are the report card.

## 7. Honest Boundaries

- All systems referenced are **prototypes for educational and research purposes only**; no production warranty is stated or implied. All systems are experimental and may contain defects.
- Healing telemetry is dominated by **synthetic anomaly injection** (deliberate fault campaigns: Horsemen chaos cycles, LINDY batteries, falsifier batteries) — by design: training instances are synthetic-generated per frozen prereg; no production, customer, or personal data is used. Real production faults followed the same escalation rules.
- The 100% sentinel figures describe the audit pass over the journaled record, not a proof of impossibility of future violations. The kill switch exists because no wall is assumed perfect.
- Confidence-gated and threshold-blocked anomalies are counted as guard successes, not failures — a cage that never declines to act on weak evidence would be a liability, not a healer.
- No client data, customer-identifiable information, PHI, or credentials appear in any telemetry, log, or receipt (POL-DISC-001 in force).

## 8. Receipt Index

| Artifact | Reference |
|---|---|
| Cage watch (0/60 escapes) | DOI 10.5281/zenodo.23425579 |
| Falsifier battery (109/109) | DOI 10.5281/zenodo.23430655 |
| Hemispheric invariants (H-INV-1/2) | DOIs 10.5281/zenodo.23330308, 23330348, 23330361 |
| SOV-B1 sovereignty stress | DOI 10.5281/zenodo.23628676 |
| Witness economics (GREEN-1) | DOI 10.5281/zenodo.23657038 |
| Fractal ownership split (FRACTAL-2) | DOI 10.5281/zenodo.23655614 |
| Digest-correction addendum | DOI 10.5281/zenodo.23672787 |
| Project SOLACE (sponsor's seat) | DOI 10.5281/zenodo.23463568 |
| The Operator's Receipt (operator's seat) | DOI 10.5281/zenodo.23700617 |
| Drift exhibit pair (Sponge-600 / Sovereign Live P2P) | GitHub LLong2026/four-horsemen, ledger 0373 |
| Append-only ledger (373 entries) | LEDGER.md, forward-only since 2026-09-07 |
| Telemetry source of record | SQUIRL OS hub-of-record entities (this report's counts, entity-read) |

---

*This software and its descriptions are provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
