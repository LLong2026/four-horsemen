# FRACTAL-2 Benchmark: A Three-Way (30/30/40) Fractal Ownership Split of a Published Research Artifact, Consensus-Witnessed on Three Rails for Under $0.26

**Series:** FRACTAL-2 (successor to FRACTAL-1, the first 20% fractional sat lease, ledger 0305)
**Date:** 2026-10-25 (anchor window 2026-10-26T04:00-04:30Z)
**Authorization:** Leon GO (chat authorization, 2026-10-25 22:55 CT)
**Prototype disclaimer:** This system is a prototype provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.

## 1. What was measured

A 3-way fractional ownership transfer (30% / 30% / 40%) of a published, DOI-bearing
research artifact — the HG-CERT-1 governance-drift hold-gate certification paper
(DOI 10.5281/zenodo.23627901, artifact SHA-256 0a073f64...dcb296f) — was recorded in a
canonical ownership manifest and witnessed byte-exactly on three independent
consensus rails (Stellar, XRP Ledger, Bitcoin) on the same evening, with the Bitcoin
leg fired at the observed weekend mempool trough. Every leg was read back keylessly
(no keys, no wallet, no sign-in) from public endpoints, 3/3 byte-exact.

The split (sum = 100, provisional 64/181,667 fractional-ownership mechanics;
authority/lease record — the artifact and its custody never move):

| Percent | Wallet | Rail |
|---|---|---|
| 30 | XFER-1 Receive Wallet (bc1qrv0tv...h5rc) | BTC |
| 30 | XRP Writer B (rDSbkAZb...ExX8C) | XRP |
| 40 | Stellar Writer B (GC6VZW...L6JD) | XLM |

Transferor of record: BTC Writer (MCR/Satoshi Track, bc1qf4zs...arzw6).

## 2. Measured cost (the floor claim, scoped)

Spot prices at fire time (Coinbase, 2026-10-26T04:2xZ): XLM $0.166599, XRP $1.2744,
BTC $79,392.45. Mempool at the Sunday-night weekend trough: 1 sat/vB across all
tiers (fastest = economy = minimum).

| Leg | Fee | Measured USD | Finality |
|---|---|---|---|
| Stellar manageData | 100 stroops (0.0001 XLM) | $0.0000167 | 5.9 s (ledger 65140250) |
| XRPL AccountSet memo | 10 drops (0.00001 XRP) | $0.0000127 | 5.9 s (validated) |
| Bitcoin OP_RETURN | 316 sats @ 2 sat/vB | $0.2509 | mainnet pace |
| **Triad total (as fired)** | | **$0.2509** | |
| Bitcoin OP_RETURN at the observed 1 sat/vB floor | 158 sats | $0.1254 | slower |
| Weekly-batch doctrine (amortized) | | ~$0.019/receipt | per BATCHED_BTC_CHECKPOINT_SPEC v1.0 |

Reading: a three-way fractional ownership transfer of a published research artifact,
triple-rail consensus-witnessed with instant-tier finality on two rails, costs
**about one quarter of a US dollar** at 2 sat/vB, or **about one eighth** at the
weekend mempool floor, or **about two cents per receipt** when the Bitcoin leg rides
the weekly ledger-head checkpoint. Legacy token-mint flows on major smart-contract
chains typically cost $5-50+ at peak congestion for a single ownership record with
no multi-rail witness and no keyless verification path. The cost gap is two to
three orders of magnitude.

For the price of one $8 cup of coffee: roughly 32 of these three-way fractional
ownership transfers at the 2 sat/vB rate, or 64 at the trough floor.

## 3. On-chain receipts (keyless-verifiable)

- XLM: tx e7def7e8447335b2099bd987d92ed0f36417b43e16acdd95b8488aeaee595552,
  ledger 65140250, manageData "SQDR-FRACTAL-2"
- XRP: tx 670ECBB9E4014F776775668A643938479350AD2BA378595560C596C9DD9CC73B,
  validated, memo type SQDR-FRACTAL-2
- BTC: tx 074c5fbc05d5a6fc9856c5e2bf280f03ea8f29555f8018dd8c8df8da702d6a11,
  OP_RETURN, 316 sats at 2 sat/vB (vsize 158)

Payload (all three legs byte-identical): SQDR + 0x12 (ownership-transport class) +
SHA-256(canonical manifest) = 5351445212 3134705cde3bf749b07a37306b23cf1a698d26c612143b77aec04c30f18cd077.
Anyone can verify: fetch each tx from any public explorer, decode the payload,
recompute the manifest hash from FRACTAL_2_OWNERSHIP_CANONICAL.json in this bundle.

## 4. Gates and disclosure

Five preregistered gates PASS (digest frozen in prereg committed c73acb6 before
broadcast; stamp-before-execute RateLimitLog fractal2_ownership_split_2026-10-25;
3/3 byte-exact keyless readback; full disclosure; prereg immutability).

Disclosed defects (append-only doctrine — errors are disclosed, not erased):
1. The first Bitcoin leg (tx 8b0155c9..., 316 sats) fired with the default envelope
   class byte 0x01 instead of the preregistered 0x12; the digest itself was correct
   on-chain. Caught at the readback gate, superseded by the corrected re-fire
   (074c5fbc...) spending the misfire's change output. Total Bitcoin postage for the
   evening: 632 sats (~$0.50 including the disclosed misfire).
2. Both txids are journaled; verification should treat 074c5fbc... as the FRACTAL-2
   Bitcoin leg. Same disclosure class as the HG-CERT-1 double-fire precedent.

## 5. Why this is a milestone

This is, to the program's knowledge as of the anchor date, the cheapest measured,
keyless-verifiable, multi-way fractional ownership transfer of a published research
artifact on public mainnets: sub-quarter-dollar, preregistered, falsifiable, with
the full receipt trail in an append-only public ledger. It reduces to practice the
ownership-transport economics claimed in the provisional patent portfolio (13
patents pending: 19/693,343 + twelve provisionals), and it demonstrates the
"fast rails per artifact, satoshi batch per cadence" cost architecture end-to-end.

## 6. Dual Mesh Benchmark status

**MEASURED (scoped)** — baseline DOI 10.5281/zenodo.23345241 (DeepSeek column);
cross-engine expansion DOI 10.5281/zenodo.23348675. No neural-mesh inference sits in
any decision path of this transfer; all gates are deterministic.

## 7. Provenance

Prereg, runlog, manifest, legs, and readback evidence: this bundle.
Append-only ledger entry 0353 (GitHub, LLong2026/four-horsemen, commit 586a85b).
Series lineage: FRACTAL-1 20% fractional lease (ledger 0305), MILE-TT-1 first P2P
satoshi ownership transfer (DOI 10.5281/zenodo.23581044).

No client data, no PHI, no credentials (POL-DISC-001). Operator authorization is
recorded by marker only (operator-privacy rule). Prototype disclaimer applies.
