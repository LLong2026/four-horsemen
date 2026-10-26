# CAGE-M1 RUNLOG — LLM-CAGING MOUNTAIN GENESIS (2026-10-25)

Genesis fold of the dedicated caging corpus (tokenization-adoption/cage_m1_corpus/),
4 leaves: Deterministic Caging of Probabilistic LLMs v1.1 (DOI 10.5281/zenodo.23284729,
round-trip sha256-verified), TROPHY_ROSTER.csv (canonical receipts), cage_watch_feed.json
(today's feed regen, 58 cycles), hemi_n_receipt_20261025.json (today's falsifier epoch,
all_pass). Starting point per owner directive (chat authorization, 2026-10-25):
the Caging-of-LLM paper plus today's caging update.

ROOT: 3bde5c53278573962e93c87bed912612d263def15748398e5b73d4aa91db461e
Envelope: SQDR + 0x07 + root (CAGE series version byte, new; distinct from the
MCR series 0x06). MCR-4 root 38089f07... and its twelve anchors unaffected.

## Gates (prereg CAGE_M1_PREREG.md, committed 144fa57 pre-broadcast)
- G1 root-frozen: root predicted in prereg before any broadcast. PASS
- G2 stamp-before-execute: RateLimitLog cage_m1_mountain_genesis_2026-10-25
  (03:15Z), before first leg. PASS
- G3 byte-exact keyless readback: 3/3. XLM manageData SQDR-CAGE-M1 ledger
  65139654 (hex-ASCII payload exact); XRP memo validated via s1.ripple.com
  (independent of broadcast endpoint); BTC OP_RETURN via blockstream.info
  (independent of broadcast endpoint). PASS
- G4 disclosure: see below. PASS
- G5 prereg immutability: prereg committed pre-broadcast, untouched after. PASS

## Triad legs (first-pass clean, zero retries, zero failures)
xlm 268582d2... ledger 65139654 (6.7s) |
xrp C7E4DCFB... VALIDATED (14.9s) |
btc df0bc9d9... 790 sats (broadcast 03:2x UTC; OP_RETURN readable at readback
via blockstream.info; confirmation follows at mainnet pace).

## Disclosures (G4)
1. PRE-FIRE FOLD DEFECT CAUGHT AND CORRECTED BEFORE BROADCAST: the first draft
   of cage_m1_fold.py bagged peaks by height-prefixed concatenation instead of
   the covenant's hash-chain bagging (bag = SHA-256(0x01||peak||bag) leftward).
   Root from that draft (42f0e1f6...) was never broadcast, never committed as
   final, and appears nowhere on-chain. The committed tool carries the corrected
   covenant semantics and a determinism gate (fold byte-identical to the proven
   mcr4_fold.py on random leaf sets n=1,2,3,4,7,12,33, PASS pre-freeze). The
   broadcast root 3bde5c53... is from the corrected fold only.
2. XLM readback uses the public horizon (keyless), same public API family as
   the MCR-4 harness precedent; XRP and BTC readbacks use endpoints independent
   of their broadcast endpoints.
3. Costs: XLM 100 stroops; XRP 10 drops; BTC 790 sats. Triad postage under $0.20
   (triad cost doctrine holds).

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
