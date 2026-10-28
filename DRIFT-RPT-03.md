# DRIFT-RPT-03 — LLM Cage, Drift Contained, Window 2026-10-23 → 2026-10-28

**Series:** `hemi_drift_report_counter = 3` (previous report DRIFT-RPT-02; this draft is not published)
**Status:** PUBLISHED v1.0 as documentation (GitHub + Zenodo). Authorization: Leon GO (chat authorization,
2026-10-28 09:54 CT) for documentation surfaces only — **no social-media posting accompanies this version**.
Figures verified against the HEMI-N receipts of 2026-10-25/26/27 on 2026-10-28.

## 1. Cage Metrics — governance stays fixed while the mesh learns

| Metric | Window result | Evidence / boundary |
|---|---|---|
| `llm_policy_layer_drift_pct` | **0.0% observed** | HEMI-N receipts for Oct 25, 26, and 27 each report identical pre/post governance roster SHA-256 `cd45a44e…7ebd06`; HF-N1 PASS each night. The LearningMetric's numeric value remains the last formal aggregate, 0.0% for Oct 13–20. |
| Playbook-selection invariance | **No change evidenced** | Current HEMI receipts show governance-roster invariance; the established byte-identical playbook-selection test under unbounded drift is the HEMI-T2 containment receipt (DOI 10.5281/zenodo.23330361). No new playbook-selection hash series was found for Oct 23–28. |
| Guard refusal integrity | **4 expected holds / 4 adversarial holds; 0 false heals** | HCLC-N18 held the critical-fintech bait and no-playbook domain-shift probe (2); HCLC-N20 held the low-confidence re-probe and critical-fintech bait (2). N19's purge guard refused destructive purge while safely draining a task-bearing node. |
| Journaled crossings (H-INV-2) | **770 HEMI-N weight deltas; 0 orphan deltas** | Receipts: Oct 25 = 252 deltas / 0 orphans; Oct 26 = 224 / 0; Oct 27 = 294 / 0. All three lineage falsifiers PASS. HCLC heals are represented by healing-event and Pattern records in the window. |
| Latest constitutional monitor | **No in-window MetaMonitor audit** | Latest `constitution_sentinel_r1_audit` record is dated Oct 13, 2026 and reports 100% compliance and 100% audit-trail completeness. HCLC-N18 and N20 record their required critical-fintech constitutional checks as PASS. This is not a fresh full 12-article audit. |

## 2. Drift Metrics — mesh movement is allowed; governance movement is not

- `hemi_mesh_drift_pct_of_mass`: **0.356% last formally measured**, covering Oct 13–20. No updated mass-normalized drift value for Oct 23–28 was present in LearningMetric or the inspected HEMI-N receipts, so this report does not extrapolate a new percentage from raw weight deltas.
- The three current HEMI-N receipts report bounded training changes, with `sum_abs_delta` values of 0.0067605661, 0.0065370678, and 0.0068485307. They do not provide a directly comparable `hemi_mesh_drift_pct_of_mass` calculation. Trend for this window: **not recalculated**. The prior measured trend was stabilizing (0.0688% to 0.0378% nightly, Oct 13–20).

## 3. Healing Telemetry — synthetic test activity disclosed

Window HCLC-N18 through HCLC-N20, across four Horsemen arms plus SIM-B, SIM-C, and SIM-D:

- **21 synthetic probes:** 7 each in N18, N19, and N20.
- **17 healed; 4 correctly held.** Gate-eligible healing was 5/5 in N18, 7/7 in N19, and 5/5 in N20: **17/17 = 100% gate-eligible heal success**. Held cases were not counted as heal failures.
- **False heals: 0.** Holds included low-confidence/no-playbook probes and critical-fintech synthetic bait held for the required human gate. These were expected guard outcomes, not production incidents.
- **Mean heal latency:** the five N20 HealingEvent durations average **2.88 seconds** (reported only for N20; no complete, consistently populated duration set was verified for all 17 heals in the window).
- **Auto-heal ratio:** 100% for each cycle's gate-eligible cases; 17/17 aggregate.
- **PQC validation:** three documented PASS events, one per cycle (N18, N19, N20); approved algorithms only. The N20 event used CRYSTALS-Dilithium3 with pre-heal pqcManager validation.

## 4. Receipts

- HEMI series: [10.5281/zenodo.23330308](https://doi.org/10.5281/zenodo.23330308), [10.5281/zenodo.23330348](https://doi.org/10.5281/zenodo.23330348), [10.5281/zenodo.23330361](https://doi.org/10.5281/zenodo.23330361).
- Ledger coverage: prior-report publication 0313–0314; HCLC-N18 0355–0358; HEMI-N Oct 26 receipt 0361; HCLC-N19 0367–0370; HEMI-N Oct 27 receipt 0371; HCLC-N20 0375–0378. DRIFT-RPT-02 is ledger 0313. These references identify the source receipts; this draft creates no ledger entry.
- Series counter: LearningMetric `hemi_drift_report_counter = 3` (draft record created with this report).
- Current HEMI-N receipt files: `fh_pub/hemi_n_receipt_20261025.json`, `fh_pub/hemi_n_receipt_20261026.json`, `fh_pub/hemi_n_receipt_20261027.json`.

## 5. Disclosure

Anomalies and probes summarized here are synthetic test inputs; they do not describe customer events. No client-identifiable data, PHI, credentials, or operator quotations are included. Prototype disclaimer applies:

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

---

# LinkedIn draft — NOT POSTED

Three HEMI-N epochs. 770 weight deltas. Governance roster SHA-256 unchanged across all three; all lineage falsifiers passed. In the paired synthetic HCLC cycles, 17 of 17 gate-eligible heals succeeded, while four probes were correctly held. Three PQC pre-validation checks passed. The mass-normalized mesh-drift metric was not recalculated for this window, so we are not claiming a new percentage.

Receipts: [HEMI-1](https://doi.org/10.5281/zenodo.23330308) | [HEMI-2](https://doi.org/10.5281/zenodo.23330348) | [HEMI-T2 containment](https://doi.org/10.5281/zenodo.23330361). Ledger references: 0355–0358, 0361, 0367–0371, 0375–0378. All anomalies described are synthetic; no customer data or PHI is included.

This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

---

## Derivation note (2026-10-28)

Verified against the receipt files themselves, not against summaries: the three HEMI-N receipts
(`hemi_n_receipt_20261025/26/27.json`) report 252, 224, and 294 weight deltas — 770 total — with 0 orphans
each and every falsifier (HF-N1 through HF-N5) passing. The governance roster SHA-256 is
`cd45a44e…7ebd06` in the pre and post fields of all three receipts, which is the basis for the 0.0% policy
drift statement. The report's own limitation is retained deliberately: no fresh mass-normalized drift
percentage was recalculated for this window, and none is claimed.
