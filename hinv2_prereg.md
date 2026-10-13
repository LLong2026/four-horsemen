# H-INV-2 LINEAGE FORGERY BATTERY PREREGISTRATION

Series: HINV2-1 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 10:28 CT).

## 1. Hypothesis under test

H-INV-2 (journaled crossing): every mesh weight update maps to a real source healing
event, and every accepted healing event feeds a pattern update. This battery attacks
the lineage ledger itself: it forges crossings in both directions (orphan weight
updates, orphan events, forged event ids, temporal forgeries, duplicates, mismatched
pattern lineage) and requires the crossing validator to accept every legitimate
crossing while rejecting every forgery — with zero silent drops.

Where SBR-2 asked "can an adversary perturb the mesh mid-learning?" (answer: no),
this battery asks "can an adversary fabricate history the mesh will believe?"
(predicted answer: no).

## 2. Instrument

Built on the HEMI-T2C runner lineage (frozen corpus CORPUS_B1 sha
13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59, 32-node mesh,
frozen ROSTER, bounded rule w' = w + lr*(1-c)*(1-w)). Phase 1: standard 40-epoch
training run producing the true crossing journal (epoch, event_id, node, weight
before/after, pattern_update flag) — every accepted crossing journaled at write time.
Phase 2: the battery fires against the live journal and mesh state.

## 3. Frozen probe battery

Controls (C): every 25th accepted crossing from the true journal — expected VALID
with complete lineage (real event id, matching epoch, matching node, pattern fed).

Forgeries (8 instances per class, constructed from real journal state):

- **B1 — Orphan weight update**: crossing with no source event id. Expected: INTEGRITY_FAILURE.
- **B2 — Forged event id**: crossing citing an event id that does not exist in the journal. Expected: INTEGRITY_FAILURE.
- **B3 — Temporal forgery**: real event id, but claiming a different epoch than it occurred in. Expected: INTEGRITY_FAILURE.
- **B4 — Duplicate crossing**: byte-identical replay of an already-accepted crossing. Expected: REJECTED_DUPLICATE, journal unchanged, no double-count of learning.
- **B5 — Orphan healing event**: event whose crossing carries no pattern update (learning that updates nothing). Expected: INTEGRITY_FAILURE per Rule 7 / H-INV-2 (a healing event that feeds no learning is an integrity failure).
- **B6 — Mismatched pattern lineage**: pattern update claiming a source event that exists but belongs to a different anomaly type / node lineage. Expected: INTEGRITY_FAILURE.

## 4. Frozen falsifiers (all must PASS)

- **F1 (true positives):** 100% of control crossings validate as VALID with complete lineage.
- **F2 (true negatives, journaled):** 100% of B1-B6 forgeries rejected AND each rejection
  journaled as a probe record (probe id, class, verdict). Zero silent drops.
- **F3 (zero side effects):** mesh state hash byte-identical before and after the battery;
  no accepted journal record altered; rejected crossings produce zero weight deltas.
- **F4 (determinism + append-only):** battery re-run produces byte-identical verdicts;
  the accepted-journal hash is unchanged by the battery and by its re-run.
- **F5 (hygiene):** no PII, PHI, customer identity, credentials, or verbatim operator
  chat text in any artifact (synthetic corpus only).

## 5. Scope honesty

Proves the LOCAL registered instrument's crossing validator under THIS frozen battery.
NOT a claim about every journal implementation, distributed ledgers, or untested
forgery classes. Battery is preregistered and non-adaptive; any FAIL ships as FAIL.

## 6. Receipt plan

Runner: hinv2_runner.py. Outputs: HINV2_RECEIPT.json (journal stats, verdict ledger
for every control and forgery, mesh-state hashes, determinism check). Two-key before
any public post: Gabriel vet + Leon GO.
