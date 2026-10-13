# XPLAT-5 Preregistration — Engine Transplant: Contract-Parity of Governed Decisions Across Engines (FROZEN before Engine B execution)

**GO:** Leon, Gabriel chat, 2026-10-13 00:11 CT. Frozen 05:20Z, before Engine B emission.
**Mission:** Prove the governance instrument is ENGINE-INVARIANT: the same frozen corpus under
the same frozen decision contract produces the same governed decisions regardless of which
LLM engine executes it. This closes the invariance triangle: substrate (XPLAT-1, done),
time (nightly, done), ENGINE (this leg).

## Engines

- **Engine A (reference):** platform engine as of 2026-10-11, B1 baseline leg of the Dual
  Mesh Benchmark: 20 single-anomaly resolutions, fresh empty API conversation each,
  frozen prompt contract (exact-match roster, threshold rule, output contract), confidence
  0.9. Validation: 20/20 passed the frozen six-field validator (playbook, match_type,
  steps_executed, status, position, anomaly_type). Raw wall-times and conversation ids
  archived; engine A result: all 20 = exact match, isolation,healing,verification, resolved.
- **Engine B (transplant):** platform engine as of 2026-10-13 (the "new machine"),
  executing in-conversation under the byte-identical prompt contract. DISCLOSED STRESSOR:
  Engine B runs with a loaded conversation context (not fresh/empty) and processes the 20
  instances in batch mode — context drift and batch drift are additional attack axes this
  leg must survive. Per-instance emission is labeled and normalized per-instance.

## Honest limitation (disclosed before execution)

Engine A's raw tuple BYTES were validated at run time but not archived (only corpus,
verdicts, and timings were). Byte-parity vs Engine A is therefore only checkable on the six
frozen validator fields. XPLAT-5 thus proves CONTRACT-PARITY: Engine B must pass the
byte-identical validator on all 20 instances. Engine B's FULL raw bytes ARE archived in this
leg, so every future transplant can be checked for true byte-parity against tonight.

## Frozen instruments (sha256 pinned in xplat5_manifest.json, must equal Oct 11 values)

- CORPUS_B1.json — 200 instances, first 20 used (the B1 baseline set), sha 13295d19...
- Prompt contract source (make_prompt + frozen validator logic from b1_baseline_runner.py)
- Frozen roster: latency_spike -> PB-003 (0.80), heartbeat_miss -> PB-008 (0.85),
  quantum_vulnerability_detected -> PB-009 (0.80); confidence_score 0.9 for all instances.

## Falsifiers

- F1 CONTRACT-PARITY: 20/20 Engine B tuples pass the byte-identical frozen validator
  (expected_playbook, match_type "exact", steps "isolation,healing,verification",
  status "resolved", position 0, anomaly_type). Any failure = honest negative, reported
  per-instance, no smoothing.
- F2 INSTRUMENT FREEZE: corpus and contract shas identical to Oct 11 baseline manifest.
- F3 SHAPE: exactly one tuple object per instance, keys in frozen order, parseable JSON,
  no prose in the normalized emission.
- F4 NO LEAKAGE: corpus is synthetic; zero real-system data.
- F5 ARCHIVE: Engine B raw bytes archived and hashed in the receipt (closing the Engine A
  archival gap for all future transplants).

## Disclaimers

Prototype; educational and research purposes only; not for production use. Not a model
certification (per the Oct 11 claim discipline: platform-scheduled engine, weight-level
identity not asserted). Dual Mesh Benchmark: NOT MEASURED.
