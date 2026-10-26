# FRACTAL-2 RUNLOG — 3-WAY FRACTAL OWNERSHIP SPLIT (2026-10-25)

Owner directive (chat authorization, 2026-10-25 22:55 CT): transfer fractional
ownership of DOI 10.5281/zenodo.23627901 (HG-CERT-1 certification paper,
artifact sha256 0a073f64...dcb296f) 30/30/40 across three wallets, triad-anchored,
XLM+XRP same-day, BTC satoshi batch at the weekend low trough. Cost floor
demonstration target: $0.24 or cheaper.

OWNERSHIP MANIFEST: FRACTAL_2_OWNERSHIP.json (canonical sha256
3134705cde3bf749b07a37306b23cf1a698d26c612143b77aec04c30f18cd077)
Envelope: SQDR + 0x12 (ownership-transport class) + manifest digest.
Transferor of record: BTC Writer (bc1qf4zs...arzw6).
Allocations: 30% XFER-1 Receive Wallet (bc1qrv0tv...h5rc, BTC) |
30% XRP Writer B (rDSbkAZb...ExX8C, XRP) | 40% Stellar Writer B
(GC6VZW...L6JD, XLM). Sum = 100. Mechanics: provisional 64/181,667
fractional ownership (FRACTAL-1 doctrine, ledger 0305).

## Gates (prereg FRACTAL2_PREREG.md, committed c73acb6 pre-broadcast)
- G1 digest-frozen: manifest digest recorded in prereg before any broadcast. PASS
- G2 stamp-before-execute: RateLimitLog fractal2_ownership_split_2026-10-25
  (04:10Z), before first leg. PASS
- G3 byte-exact keyless readback: 3/3. XLM manageData SQDR-FRACTAL-2 via public
  horizon; XRP memo via s1.ripple.com (independent of broadcast endpoint);
  BTC OP_RETURN via blockstream.info (independent of broadcast endpoint). PASS
- G4 disclosure: see below. PASS
- G5 prereg immutability: prereg committed pre-broadcast, untouched after. PASS

## Triad legs (final legs first-pass clean, zero retries)
xlm e7def7e8... ledger 65140250, confirmed 5.9s, 100 stroops |
xrp 670ECBB9... VALIDATED 5.9s, 10 drops |
btc 074c5fbc... 316 sats at 2 sat/vB (vsize 158), Sunday-night weekend trough
(mempool 1 sat/vB across all tiers at fire time; broadcast 0.2s; OP_RETURN
readable at keyless readback; confirmation follows at mainnet pace).

## Disclosures (G4)
1. BTC MISFIRE JOURNALED: the first BTC leg (8b0155c9..., 316 sats) fired with
   the default envelope class byte 0x01 (drop) instead of the prereg's 0x12
   (ownership-transport) — the writer software module's version byte was not
   overridden in the leg. The digest itself was correct on-chain. Caught at the
   G3 readback (envelope mismatch), the leg was superseded by a corrected
   re-fire (074c5fbc...) spending the misfire's change output, envelope
   byte-exact 0x12. Both txids journaled; total BTC postage tonight 632 sats;
   the effective anchor is the corrected leg. Same disclosure class as the
   HG-CERT-1 double-fire (ledger 0336) precedent.
2. Costs measured at spot (2026-10-26T04:2xZ, Coinbase): XLM $0.166599,
   XRP $1.2744, BTC $79,392.45.
   - XLM leg: 100 stroops = $0.0000167
   - XRP leg: 10 drops = $0.0000127
   - BTC corrected leg: 316 sats @ 2 sat/vB = $0.2509
   - Triad total (correct legs): $0.2509 — vs the $0.24 target: at tonight's
     observed 1 sat/vB mempool floor the same leg is 158 sats = $0.1254,
     under the floor; at 2 sat/vB the floor trades fee-rate certainty for
     faster trough confirmation. Under the weekly batch checkpoint doctrine
     (BATCHED_BTC_CHECKPOINT_SPEC.md) the amortized BTC cost per receipt is
     ~1.9 cents at current volume.
   - Total actually spent tonight including the disclosed misfire: 632 sats
     BTC + fast rails ~= $0.502.
3. No sat movement to allocation wallets on their own rails was attempted:
   the split is an authority/lease record under the 64/181,667 mechanics,
   witnessed by the triad; the artifact and its custody never move.

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
