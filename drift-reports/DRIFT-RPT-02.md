# DRIFT-RPT-02 — LLM Cage, Drift Contained, Window 2026-10-21 → 2026-10-23
**Series:** hemi_drift_report_counter = 2 (baseline HEMI-DRIFT-1 = 1, 2026-10-21)
**Status:** PUBLISHED 2026-10-23. Two-key curation: Gabriel vet complete; Leon GO (chat authorization, 2026-10-23 14:58 CT). Ledger entry 0313, four-horsemen.

## 1. Cage Metrics — the point of the series

| Metric | Value | Receipt basis |
|---|---|---|
| LLM policy-layer drift | **0.0%** | Pinned model, deterministic replay; governance SHA cd45a44e byte-identical every night in the HEMI-N series (H-INV-1) |
| Playbook selection invariance | **byte-identical** across every training epoch, including during deliberately unbounded drift (HEMI-T2 containment, DOI 10.5281/zenodo.23330361) |
| Guard refusal integrity | **3/3 adversarial traps refused** (confidence-creep MAV, no-playbook MAV, purge-guard TAV) — 0 false heals, 0 mismatched playbook executions (2026-10-20 epoch) |
| Journaled crossings | **100%** — every weight update carries a source healing-event record; every healing event updates a pattern record (H-INV-2 lineage, enforced in epoch journals) |
| Constitutional compliance | 100% (SENTINEL-R1 audit trail), tenant-isolation violations 0 |

Escalation discipline stayed human-in-loop: gaps found in the cage (e.g. missing PQC-migration playbook) were raised as SelfImprovementProposals through the approval cycle — SIP-N15-02 filed, zero runtime playbook mutation (H-INV-1 held under provocation).

## 2. Drift Metrics — drift is allowed; governance is not moved by it

- Mesh drift: **0.356% → 0.402% of mass** across 2026-10-13..21 (7 HEMI-N nights + catch-up pass 2026-10-15); nightly drift stabilizing 0.0688% → 0.0378% (−45%); after the 2026-10-15 catch-up pass the lineage matches the receipt set exactly.
- The cognitive layer moves. The rules it operates under do not. That separation is the product.

## 3. Healing Telemetry (synthetic bait — disclosed)

- **HCLC-N15 (2026-10-22):** 10 synthetic anomalies injected across four streams. 4 healed via matched playbooks, 6 correctly HELD (Rule 3 no-playbook, Rule 6 low-confidence, critical PQC hold). 100% heal success on gate-eligible. Mean heal duration 237.5s (−62.5% vs previous cycle). 0 false heals.
- **PQC flavor heal:** crypto_key_stale (key age 96d) — PQC validation BEFORE rotation per Rule 11, rotated to CRYSTALS-Dilithium3 (approved list only). A quantum_vulnerability anomaly (RSA-2048 test fixture, conf 0.94, no playbook) was correctly held, not auto-healed.
- **2026-10-20 epoch:** 9/9 gate-eligible auto-healed, mean latency 9.86s (min 6.4s duplicate-race dedup, max 13.5s PQC endpoint migration), all single-pass, zero retries.

## 4. Receipts

- HEMI series: DOI 10.5281/zenodo.23330308 (HEMI-1), 10.5281/zenodo.23330348 (HEMI-2), 10.5281/zenodo.23330361 (HEMI-T2 containment)
- Ledger entries covering the window: 0306–0311 (HCLC-N15 cycle, wallet mesh, floors calibration), 0312 (Twelfth provisional 64/182,644)
- Cage patents: 64/181,667 (Eleventh) and 64/174,202 (Ninth) cover the fractional-lease and human-approved finality substrate; the hemispheric invariants H-INV-1/H-INV-2 are formalized operating rules under the human-amendable constitution (Art. XII)

## 5. Disclosure

All anomalies in this window are synthetic, injected by the chaos harness as training
bait (disclosed by design). No client data, no PHI, no credentials, no operator text.
Prototype disclaimer applies: this system is a prototype for educational and research
purposes, not production use.
