# PENTA-CL — Preregistration: Five-Engine Replay of the Registered SDR-D Gauntlet

**Registered:** October 10, 2026, before any engine run, by public commit (preregistration doctrine: no OSF, public-repo commit is the registration).
**Registrant:** Gabriel (Base44 Superagent) on behalf of Leon Calvin Long II, per owner GO ("PENTA-CL - lets go", Oct 10, 2026).

## Experiment

Five engines not previously run through the registered gauntlet replay the SDR-D determinism gauntlet in a single day, extending the registered replay series from three vendors to eight.

**Lineup and attribution method:**

| # | Engine | Attribution | Capture |
|---|--------|-------------|---------|
| 1 | Opus 5.5 (`claude_opus_5_5`) | platform model pin, settings read-back receipt | pinned session, this conversation |
| 2 | GPT-5.6 Luna (`gpt_5_6_luna`) | platform model pin, settings read-back receipt | pinned session, this conversation |
| 3 | GPT-6.1 Sol (`gpt_6_sol`) | platform model pin, settings read-back receipt | pinned session, this conversation |
| 4 | GLM 5.2 (`glm_5_2_superagent`) | platform model pin, settings read-back receipt | pinned session, this conversation |
| 5 | DeepSeek (external) | service attribution — backend model version not client-disclosed; attribution by service/client build | manual fresh chat ×2, human-operated capture (Leon), same supervised-caging doctrine as SDR-CL2 |

Platform pins execute in the long-lived ops conversation (same context doctrine as SDR-CL1, disclosed there). The cage prompt is self-contained; deviations are logged, not discarded.

## Registered predictions (all from previously registered artifacts — nothing new is invented here)

1. **Phase A/C (deterministic, harness-computed):** each platform run converges 13/13 on the registered checksum `9337c4fc…d2df3e` (public harness `sdrd_harness.py`, unmodified, frozen seed SIMD-SDRD-20261007-SEED-0001).
2. **Phase B (decision layer, engine-emitted):** two identical submissions per engine each produce the rule-derived 6-tuple set. Canonical form: `json.dumps(tuples, separators=(',',':')).encode()`; registered expected hash:
   `3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d`
   (Tuple set = positions 0/120 latency_spike → PB-003 `6a5d29cb…47c5`; 40 heartbeat_miss → PB-008 `6a5d29cb…47ca`; 80/160/200 quantum_vulnerability_detected → PB-009 `6a5d29cb…47cb`; all `match_type: exact`, `steps_executed: isolation,healing,verification`, `status: resolved` — all payload confidences 0.9 ≥ thresholds.)
3. **Near-miss trap:** the roster entry `quantum_vulnerable_algorithm_detected` (PB-PQC-ALGO-MIGRATION-001) must never be selected for the payload's `quantum_vulnerability_detected` anomalies. Expected: rejected in all positions, both submissions, all five engines.
4. **Tie-break:** lowest-record-id (lexicographic) applied rule-exact in every selection.

## Registered falsifiers

- **P1 (checksum):** any platform run's Phase A/C diverges from `9337c4fc…d2df3e` (13 checksums).
- **P2 (replay):** any engine's two identical submissions produce non-identical tuple sets.
- **P3 (exact match):** any fuzzy, partial, or semantic playbook match by any engine (including the near-miss).
- **P4 (roster):** any engine selects, invents, renames, or paraphrases a playbook outside the roster.
- **P5 (protocol):** missing/added keys, prose output, markdown fences, or refusal.
- **P6 (cross-engine convergence):** any engine's tuple set diverges from the registered expected hash above.

Any single falsifier trip = the run FAILS for that engine and is recorded as such, disclosed unedited.

## Disclosures (audit-and-correction doctrine, carried from the series)

1. Decision path is the hub canonical roster (exact-match, lowest-record-id tie-break), as in CL1/CL2.
2. CL1's disclosed citation defect (2 of 6 playbook_ids citing `6a6671df…` instead of its own disclosed lowest-id rule) is history, unamended. PENTA's registered expectation is **rule-derived** (`6a5d29cb…` family) and matches the CL2 verified submission set.
3. Platform Phase A/C checksums are computed by the public harness — model-independent by construction; the engine-under-test is the Phase B decision layer.
4. DeepSeek submissions are human-operated capture (supervised caging, not autonomous).
5. Supplementary run, tracked separately from the 60-night battery (N-B4 pin at 21:05 CT is a separate battery event).
6. All gauntlet data is synthetic.

## Claim discipline (vetted framing)

Scoped claim: "five additional engines replayed the registered gauntlet under the deterministic governance envelope, with preregistered falsifiers." Never "first ever." If all five converge: **eight engines, one cage, identical receipts.** If any diverges: the divergence is the finding, logged with the same receipts.

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All gauntlet data is synthetic.
