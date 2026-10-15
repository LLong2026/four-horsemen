# LINDY-B PREREGISTRATION — 60-Day Sustained Battery Run

Series: LINDY-B | Committed: 2026-10-13 (before first nightly run)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 10:46 CT).
Run window: Oct 13 – Dec 11, 2026 (60 nightly runs; closing receipt Dec 11/12).

## 1. Purpose

Every battery to date is single-run evidence. LINDY-B answers the question an
examiner actually asks: does the instrument still conform on run N+1, and the one
after that, for 60 consecutive days? Sustained conformance under an append-only
public ledger — the durability receipt the corpus does not yet have.

## 2. Instrument (frozen — all previously published, byte-identical)

Nightly battery, executed by the agent on a scheduled trigger (03:30 CT, after the
HEMI-N1 training window), per the stamp-before-execute idempotency protocol
(RateLimitLog signature lindy_b + date; duplicate slots exit silently):

1. **T2C replay conformance** — the frozen CORPUS_B1 (sha 13295d19), 32-node mesh,
   frozen ROSTER, bounded rule; 40 epochs. Determinism falsifier: the resulting
   trajectory hash MUST equal the registered trajectory hash every night. Any
   deviation = conformance failure, critical alert, run halt.
2. **H-INV-2 audit sweep** — the v3 audit-mode lineage check over the night's
   journal (every 25th crossing), chain + bounded-rule recomputation.
3. **DPP-1 canary spot-check** — the poisoned corpus replay; trajectory must equal
   the clean baseline; all canaries absent from outputs.

Per-night receipt: one line appended to LINDY_B_RUNLOG.md in this repo
(date, slot, signature, three pass/fail flags, trajectory hash, elapsed seconds).
The runlog is append-only (Lindy doctrine).

## 3. Frozen falsifiers (evaluated at day 60 closure; drift alarms nightly)

- **FB1 (sustained determinism):** all 60 nightly trajectory hashes identical to
  the registered T2C baseline; zero drift nights.
- **FB2 (sustained lineage):** every nightly audit sweep passes; the journal chain
  is unbroken across the entire 60-day corpus.
- **FB3 (sustained ingestion discipline):** every nightly canary scan clean; zero
  canary leaks in 60 days.
- **FB4 (ledger integrity):** the runlog is append-only and complete: 60 entries,
  no gaps, no edits (git history proves it).
- **FB5 (honesty):** any drift, failure, or missed slot is reported as-it-happens
  and appears in the closing receipt — no smoothing, no gap-filling. Missed slots
  due to platform outage are recorded as MISSED, not skipped.

## 4. Receipt cadence (per the established convention)

- Nightly: runlog line only (no DOI noise).
- Weekly (Sundays): weekly runlog bundle committed; DOI binding optional per
  Leon's weekly batch preference.
- Day 60: closing receipt LINDY_B_RECEIPT.json + Zenodo publication under the
  standard two-key gate (Gabriel vet + Leon GO).

## 5. Scope honesty

Proves THIS registered instrument holds determinism, lineage, and ingestion
discipline across 60 consecutive scheduled runs on this platform. NOT a claim
about production uptime, other deployments, or adversarial variation over time
(the nightly battery is non-adaptive and fixed). If a nightly run fails, the
battery continues nightly while the failure is escalated — a failure does not
end the run; it is recorded.

## 6. Hygiene

Synthetic corpus only; no PII/PHI/credentials; no operator chat text in any
artifact; operator authorization recorded as GO + timestamp. Prototype
disclaimer applies to all outputs.

## 7. AMEND-1 (Leon GO, chat authorization, 2026-10-15, 18:03-18:06 CT)

The weekly operating rhythm directive (ledger 0111) amends this prereg. Forward-only,
disclosed, per the append-only doctrine; sections 1-6 remain on the record unchanged.

- **Cadence:** nightly → WEEKLY, Fridays 22:00 CT. Run 1 executed 2026-10-15
  immediately on Leon GO (the program's first executed run — the Oct 13-14 nightly
  slots never executed; LINDY-B was paused under the demo freeze before the first
  night, disclosed in ledger 0108). Signature protocol unchanged: lindy_b/<date>.
- **Run window:** Oct 15 – Dec 11, 2026 (Fridays: Oct 16 window's run 1 executed
  Oct 15; expected run count at closure: 9).
- **Closing basis (Leon decision, 18:06 CT):** the program CLOSES ON DATE
  2026-12-11 with the run count as accumulated under the weekly cadence. The
  closing receipt is presented at the 2026-12-11 run under the standard two-key
  gate. After Leon's review, the program RESETS; rebaseline decisions for the next
  cycle are Leon's, never auto-decided.
- **Falsifiers:** FB1-FB5 unchanged in substance, evaluated at the Dec 11 closure
  over the accumulated weekly corpus (all executed runs). FB4 read as: one runlog
  entry per scheduled Friday slot, no gaps among scheduled slots, no edits; any
  missed scheduled slot recorded MISSED per FB5 (the freeze-paused Oct 13-14
  nightly slots predate run 1 and are disclosed here, not counted as misses).
- **Instrument:** unchanged and frozen (CORPUS_B1 sha 13295d19, T2C registered
  trajectory baseline, H-INV-2 v3 audit sweep, DPP-1 canaries, SIP-3/SIP-4
  stage-1 wiring).

Run 1 result (2026-10-15): PASS — t2c ca575bb9...f93d50 baseline_match=True,
lineage 106/106, crossings 2646, dpp clean, recon closure 0.00e+00, sentinel ok.
