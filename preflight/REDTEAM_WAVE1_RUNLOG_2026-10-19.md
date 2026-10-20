# Red-Team Internal Wave 1 — 2026-10-19

Scope stamp: `redteam_internal_wave1_2026-10-19` (RateLimitLog 2026-10-20T03:08Z, stamp-before-execute)
Authorization: Leon GO (chat authorization, 2026-10-19 ~22:07 CT)
Mode: internal, non-destructive, deterministic. No LLM in any decision path.

## New attack classes probed (beyond frozen HACK-3/4/5/6 corpus)

### P1 — Envelope forgery falsifier (reader path)
Question: can any non-canonical envelope pass the doctrine reader?
v0 harness FAIL (DISCLOSED): the wave-1 v0 harness validated shape only and omitted the final
byte-exact digest comparison — two "forgeries" (zero-drift digest, double-encoded hex-ASCII)
passed shape checks. Harness defect, not a system break: the doctrine reader's final step is
digest equality (payload doctrine §2.5), which v0 did not implement.
v1.1 harness (shape + byte-exact match): PASS — genuine envelope accepted, 8/8 forgeries rejected
(truncated 31B, extended 33B, marker typo SQDE, unapproved version 0x99, zero-drift digest,
double-encoded hex-ASCII, no-marker raw digest, single-bit digest flip).

### P2 — Cross-endpoint consensus (reader path, multi-source)
Question: do independent public endpoints agree, byte-exact?
- BTC MCR-1 leg (txid 8728d021...74195): mempool.space == blockstream.info, envelope canonical,
  digest == frozen MMR root 2d1a3214...c23a. PASS.
  (v0 harness slice bug DISCLOSED: [5:] applied to full script hex including the 6a25 OP_RETURN
  prefix; corrected to [2:] envelope extraction. Endpoint agreement held throughout.)
- XRP MCR-1 leg (txid C42468F0...59480): xrplcluster.com == s2.ripple.com, both validated, memo
  carries SQDR-MCR-1 label + 0x25 length byte + raw 37-byte envelope, digest == frozen root. PASS.
  (Two encoding-assumption iterations DISCLOSED: harness first assumed hex-ASCII memo, then
  mis-set the needle; the memo on this leg carries the raw binary envelope — the binary/UTF-8 rail
  nuance of payload doctrine §2.5 verified live in both directions.)

### P3 — Preimage spot-check (digest binding)
Question: does the public artifact still hash to its receipted digest?
IR2_FINAL_ROUTING_CHAPTER.md sha256 a4f67436... == ledger 0259 recorded sha a4f67436. PASS.

## Wave 1 verdict

4/4 probes PASS under the v1.1 harness. Three harness defects were caught and disclosed during
the wave (v0 shape-only reader, v0 BTC slice bug, XRP encoding assumption ×2) — all in the
newly-written wave-1 harness, zero in the frozen corpus, zero in the on-chain record. This is the
HACK-series doctrine working: a FAIL indicts the harness first, and the fix is forward-only with
full disclosure.

## Standing result for the charter

The preflight (7/7) plus wave 1 (4/4) give the event charter's "prelude evidence" its receipts:
the reader path rejects all non-canonical envelopes, independent endpoints agree byte-exact,
and digest bindings still hold. Corpus expansion continues in subsequent internal waves
(social-engineering simulation, viewer fuzzing, scoring-attack simulation) before the
invite-only round opens after the 2026-12-11 LINDY close.

MEASURED (scoped): all probes deterministic, no LLM in any decision path (program benchmark DOI
10.5281/zenodo.23321637). DMB MEASURED (scoped) DeepSeek column DOI 10.5281/zenodo.23345241.
No client data, no PHI, no credentials (POL-DISC-001). Training/demo material only. Prototype
disclaimer applies.
