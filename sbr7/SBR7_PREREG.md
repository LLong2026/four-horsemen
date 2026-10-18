# SBR-7 PREREGISTRATION — Randomized Blockchain-Interaction Battery (frozen before execution)
**Series:** SQUIRL Battery Run 7 (adversarial pop-quiz format, following SBR-6, DOI 10.5281/zenodo.23445047)
**Target:** The SIP-034..037 chain-of-custody stack (STAMP / RECOVER / RECONCILE / four-layer graph)
**Sealed:** 2026-10-18 | **Authorization:** Leon GO (chat authorization, 2026-10-17 ~22:57 CT)

## Method (identical doctrine to SBR-6)
1. This prereg is committed publicly BEFORE the draw. The draw seed is the four-horsemen
   HEAD commit sha at prereg-commit time. 6 probes are drawn from the frozen pool of 12
   below by a seeded PRNG (python random.Random(seed).sample). The seed is committed
   before the draw, so the exam cannot be cherry-picked. Whatever draws, runs.
2. All probes execute in an isolated lab directory (sbr7_lab/) against synthetic test
   artifacts — the live corpus is never modified by any probe. The only external effect is
   digest submission (32-byte SHA-256) to the free OpenTimestamps calendars, which is the
   exact activity under test. No tokens, no wallets, no non-digest data crosses any
   boundary (POL-DISC-001, INV-2).
3. Adjudication is deterministic: every probe is bash/python/sha256 logic with a binary
   PASS/FAIL verdict written to the receipt. No LLM in the decision path. A probe PASSES
   when the stack behaves as its doctrine requires (fail-closed, drift-detected,
   digest-only, history-retained). The battery PASSES only if all drawn probes PASS.
4. Receipt: JSON with seed, drawn probes, verdicts, per-probe evidence digests; sealed with
   sha256; appended to the ledger and committed.

## Frozen pool of 12 probes (any 6 may draw)
- P01 RECEIPT-SWAP: a receipt for artifact A presented as proof of artifact B must NOT
  match (digest mismatch => orphan => fail-closed).
- P02 TIP-LAG-DRIFT: a stamped artifact amended afterward must be detected as drift
  (INV-1-C).
- P03 RECOVER-ARC: a drifted artifact re-anchored must yield a receipt matching the new
  state, with the superseded receipt retained (INV-1).
- P04 FALSE-GREEN: a truncated/corrupted .ots receipt must fail parsing (fail-closed, no
  false success).
- P05 DIGEST-ONLY-BOUNDARY: the committed digest must equal sha256(artifact) — proof that
  artifact bytes never transit (INV-2).
- P06 MERKLE-PARSE: every .ots receipt must parse to a well-formed merkle proof path with a
  calendar attestation.
- P07 HISTORY-RETENTION: a superseded receipt moved to history must remain byte-identical
  (nothing rewritten).
- P08 CERTIFIED-STATE: an archived state snapshot must match its recorded digest exactly.
- P09 REPLAY-STAMP: stamping the same artifact twice must produce two valid receipts of the
  same digest (idempotent existence proof; no nonce/replay failure mode).
- P10 CALENDAR-FAIL: a dead calendar endpoint must fail closed — no fabricated receipt.
- P11 PQC-AUTHORITY-NON-NEGOTIABLE: the anchor protocol must disclose the PQC split and
  contain no substitution of chain proof for PQC authority (INV-4).
- P12 GO-LINEAGE: every sealed ledger entry of the anchor arc (0162-0167) must record
  owner authorization (Leon GO + timestamp; Operator Privacy rule).

## Disclosures
- Calendar submissions create real (free) pending Bitcoin attestation commitments; this is
  the system's normal operation, not an attack on any third party.
- This is a prototype research system; all payloads synthetic; no production warranty.
