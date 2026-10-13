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
