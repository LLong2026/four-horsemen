# DRIFT-1 — FIRST REAL METRICS OF THE 60-DAY RUN
## Drift Report, Nightly Epoch 20261019 (SQUIRL OS, SQUIRL OS Technologies LLC)

**Report date:** 2026-10-19. **Class:** Drift report — the first measured (not projected, not
simulated) drift metrics of the 60-day sustained run (ledger 0060; runs to 2026-12-11).
**Program:** SQUIRL OS self-healing AI infrastructure, four-horsemen containment corpus.

---

## 1. What was measured

Every night (Sun-Tue learning window, 03:00 CT) the system executes a REAL training epoch: its
healing brain updates its own weights on the record. Epoch 20261019 ran at 2026-10-19T08:07:56Z.
The question the 60-day run exists to answer: can the thing that learns be governed?

### Nightly epoch receipt (hemi_n_receipt_20261019.json, committed same night)

| Metric | Measured value |
|---|---|
| Weight updates (real, applied) | 280 |
| Total training drift (sum abs delta) | 0.0094030562 |
| Governance roster SHA-256, pre | cd45a44eb3810123e7f96cf07a1ab4475972ee34f80a5fb1f657f3f9177ebd06 |
| Governance roster SHA-256, post | cd45a44eb3810123e7f96cf07a1ab4475972ee34f80a5fb1f657f3f9177ebd06 |
| Governance drift | ZERO (byte-identical) |
| Determinism (run1 vs run2 delta-log hash) | 4beb1771000da98b == 4beb1771000da98b (byte-identical) |
| Negative-probe false positives | 0 (LATENCY_SPIKE + unregistered_synthetic_fault both caught) |
| Boundedness (max weight) | 0.9954403917 — inside (0, 1) |
| Lineage (deltas to logged outcomes) | 280/280, 0 orphans |
| No catastrophic forgetting (old corpus) | 68/68 preserved (T2C convergence point intact) |
| Epoch falsifiers passed | 7/7 (HF-N1..HF-N5 + standing collision + control) |
| Heal pool stability | 20 resolved / 40 detected, identical pre and post |

### Cage watch scan (same morning pass)

| Wall | State |
|---|---|
| Receipted adversarial/containment cycles | 54 (TROPHY_ROSTER.csv) |
| Falsifiers held (cumulative) | 109/109 (DOI 10.5281/zenodo.23430655) |
| Escapes | 0 (DOI 10.5281/zenodo.23425579) |
| Blind attacker seams found / fixed / pending | 7 / 7 / 0 (DOI 10.5281/zenodo.23431720; SIEGE DOI 10.5281/zenodo.23445047) |
| BLIND-1R re-verification | 6/6 repelled |
| BLIND-2R re-verification | 20/20 repelled |
| Lindy wall week 2026-10-15 | LINDY-B PASS / LINDY-C PASS |
| Lindy wall week 2026-10-17 | LINDY-B PASS (re-run after disclosed miss) / LINDY-C PASS |

## 2. Disclosed defects and repairs (honesty spine)

1. **LINDY-B weekly slot 2026-10-17T03:00Z MISSED** — runner input telemetry pack displaced from
   the execution workspace (FileNotFoundError pre-adjudication). Disclosed same morning, repaired
   same night (telemetry pack located, sha a1d2fc45621dcfc0e1ae6be8635fee7c73316a72b206d9cc2b2d7e00a85b9170,
   expected path restored; no harness or corpus bytes modified), re-run PASS, recorded as a miss
   per the miss-disclosure doctrine. Ledger 0129.
2. **Cage watch feed count drift** — recorded_cycles 53 vs roster 54 rows; repaired forward-only
   (commit 3fc5feb, 2026-10-19). The repair is part of this report's same-morning record.
3. **Cardano identifier doctrine note** — the QWR-1 prereg described the Cardano transaction hash
   as "sha256 over tx body CBOR"; the on-chain convention is blake2b256 over the body. The QWR-1
   on-chain identifier a6c6a1df... was always correct and was verified byte-exact on-chain;
   the prose label was imprecise. Corrected in the QWR-2 prereg (this ceremony).

## 3. Interpretation (receipted, scoped)

The epoch's brain moved: 280 real weight updates, total drift 0.0094, contained by the frozen
bounded rule (HEMI-2.2). The governance plane did not move: the roster hash is byte-identical
before and after training. This is the hemispheric invariant H-INV-1 measured on a live nightly
run, not asserted. "AI that improves itself" is only safe if the improvement path provably cannot
touch governance. That is not a policy. It is a hash.

Publication note: the LinkedIn post announcing these metrics was approved and published the same
day under the two-key curation doctrine (Gabriel vet + Leon GO, GO + timestamp recorded; no
operator wording quoted per the operator-privacy rule).

## 4. Scope and limits

- The 60-day run (LINDY-B / LINDY-C) is at week 2 of its window; results to date are early-window.
- All epoch adjudications are deterministic; no LLM in any decision path.
- Training instances are generated faults (frozen corpus-builder semantics, deterministic UTC-date
  seed); no production, customer, or personal data involved (POL-DISC-001).
- HEMI series lineage: DOIs 10.5281/zenodo.23330308, 23330348, 23330361.

## 5. Dual Mesh Benchmark

MEASURED (scoped) — DeepSeek column, DOI 10.5281/zenodo.23345241. All other figures are receipted
as stated or explicitly not measured.

## 6. Prototype disclaimer

This software is a prototype and is provided for educational and research purposes only. It is
not intended for production use, commercial deployment, or safety-critical environments. All
systems are experimental and may contain defects.
