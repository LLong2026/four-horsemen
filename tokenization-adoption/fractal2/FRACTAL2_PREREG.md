# FRACTAL-2 PREREG — 3-WAY FRACTAL OWNERSHIP SPLIT (2026-10-25)

Frozen before any broadcast. Owner directive (chat authorization, 2026-10-25
22:55 CT): transfer fractional ownership of DOI 10.5281/zenodo.23627901
(HG-CERT-1 certification paper) 30/30/40 across three wallets, triad-anchored,
with XLM+XRP fired same-day and the BTC leg as a satoshi batch at the weekend
low trough; target measured cost at or under the $0.24 floor.

## Instrument
FRACTAL_2_OWNERSHIP.json — canonical manifest (FRACTAL_2_OWNERSHIP_CANONICAL.json,
compact sorted-key JSON). sha256 of canonical bytes:
3134705cde3bf749b07a37306b23cf1a698d26c612143b77aec04c30f18cd077
Envelope: SQDR + 0x12 (ownership-transport class, registered entries
0303/0304/0305 cycle) + manifest digest.
Payload hex: 53514452123134705cde3bf749b07a37306b23cf1a698d26c612143b77aec04c30f18cd077

## Allocations (sum = 100)
- 30% XFER-1 Receive Wallet (bc1qrv0tvjz4hham7cyx0cercfajrs4f6cqjjvh5rc, BTC)
- 30% XRP Writer B (rDSbkAZbUHQPdjDzShvze2gTGYBHDExX8C, XRP)
- 40% Stellar Writer B (GC6VZWZXARDOCAJP7WGQUHRPNKCVLTCSO7XTEG5YDGZR6ATGEIMDL6JD, XLM)
Transferor of record: BTC Writer (MCR/Satoshi Track)
(bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6).

## Hypotheses (falsifiable)
- H1: All three legs (XLM, XRP, BTC) carry the envelope byte-exact with
  independent public keyless readback 3/3.
- H2: Measured total triad postage is at or under the $0.24 floor
  (XLM 100 stroops, XRP 10 drops, BTC 2 sat/vB at the observed weekend trough
  of 1 sat/vB across all mempool tiers at 2026-10-26T04:00Z).
- H3: XLM and XRP confirm same-day (instant-tier finality); the BTC batch leg
  confirms at mainnet pace at the trough rate.

## Gates (deterministic)
- G1 digest-frozen: manifest digest recorded here before any broadcast.
- G2 stamp-before-execute: RateLimitLog scope
  fractal2_ownership_split_2026-10-25 before the first leg.
- G3 byte-exact keyless readback: every leg verified from a public endpoint
  not used for broadcast.
- G4 disclosure: any leg failure, retry, or defect disclosed in the runlog.
- G5 prereg immutability: this file committed before the first broadcast;
  forward-only corrections in new commits only.

## Cost envelope
XLM 100 stroops; XRP 10 drops; BTC fee_rate 2 sat/vB at the weekend trough
(mempool floor observed 1 sat/vB all tiers). Expected total under $0.25.
Under the weekly batch checkpoint doctrine (BATCHED_BTC_CHECKPOINT_SPEC.md),
amortized BTC cost per receipt is ~1.9 cents at current volume.

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
