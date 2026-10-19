# CFR-9 TRAINING RUNLOG — THE INTELLIGENT ROUTING CROSSFIRE (IR-2 test)

**Date:** 2026-10-19, fired ~15:55-16:30 CT
**Authorization:** Leon GO (chat authorization, 2026-10-19 ~12:58 CT); prereg frozen ~13:05 CT
(sha 171f0c57). Scope stamp cfr9_crossfire_2026-10-19 written before first broadcast (G2).
**Artifact:** SQUIRL-IP-011 patent draft "Caging the Large Language Model", 18,372 bytes,
SHA-256 bf9b8b4c608cdf68655efd9a1d8bce80f55969c0196fac9b9f1abea377c28909 (G1 verified).
**Payload envelope:** SQDR + 0x04 + 32-byte digest (37 bytes; hex-ASCII on UTF-8 rails).

## Result: 10/10 legs broadcast, 10/10 keyless read-backs byte-exact (G3 PASS)
Completion basis was 9 rails (HBAR waived, ledger 0243); DOT certified before fire, and the
DOGE rail — certified the same day — was included as a 10th leg. Both are disclosed here
as exceeding the prereg basis in scope (beneficial variance, forward-only disclosure).

## Leg receipts (fire order = latency-ranked per IR doctrine)

| # | Rail | Mechanism | txid / ref | Measured | Fee |
|---|------|-----------|-----------|----------|-----|
| 1 | SOL | SPL Memo v2 (hex-ASCII) | 2BZeGFzuYtVAvqJNGm8sGWrhADrAgR5avSwrmh4bUD5ss5SfscRcchxCcueshQFQvseGKf6mbVdtUUbUkgUPpH7, slot 458980939 | 2.3 s | 5000 lamports + 10000 failed-attempt lamports |
| 2 | ALGO | note field | VRAP53KKBN55EXZQF5EYYSEUZTTG6PMQWY6F7U4CA26LEEYAVOGQ, round 66144322 | 4.9 s | 0.001 ALGO |
| 3 | AVAX | C-chain calldata | 0x40c141cb06d3790f568281897220bd20a8355f05898caa69595eddf532896d34, block 98002159 | 2.2 s | 21,592 gas |
| 4 | Stellar | ManageData "SQDR-CFR-9" | hash 26b423f875b2a55a62cc087bc464a94d421178c66f1c2f6de1d979271ec8afbc, ledger 65031803 | 6.6 s | 100 stroops |
| 5 | XRP | AccountSet memo | 7F5C069397EDE77037999A3304F71B624146D9B06C83BC74D077D9355A1C66D2, ledger 107770015 (VALIDATED) | 8.4 s | 10 drops |
| 6 | DOT | System.remark (hex-ASCII) | extrinsic 0x96e72de9d2cd6af6106c720b97e6633b6978d53fa8ca9ab34ad5d303c2c7784d | 10.0 s | 0.195 DOT |
| 7 | Cardano | metadata 1968 | edea6182bcbfaa2dd488e7073468d62b5c58134b8873896f5abd3bba59b32b1c, block 14090269 | submit-accept 0.6 s; indexed <=5 min | 0.172 ADA |
| 8 | ETH | calldata | 0xdf2c3f1bab0489f42b162c28a762fde5f02eed5d6ab82ac6c8fdfa98d06ab712, block 26229286 | 43.4 s (receipt poll) | 22,480 gas @ 0.1174 gwei |
| 9 | DOGE | OP_RETURN | a634c34e2242612627c8604e36acb1789715eb7354803c5b4dcd5025979ec1b4, block 6422195 | ~60 s (block cadence) | 0.05 DOGE |
| 10 | BTC | OP_RETURN (segwit writer) | 83f7ba0db20ac13e19c30dfa3adb19b997fbf5181b7619b6fe13228f10010d0b | pending at seal (3.3 sat/vB) | 790 sats |

## IR-2 receipt: predicted vs observed finality (deviation >3 s raises operational note)

| Rail | Predicted (source) | Observed | Dev | Note |
|------|--------------------|----------|-----|------|
| SOL | 2.3 s (DeWR-1 T3) | 2.3 s | 0.0 | - |
| ALGO | 4.9 s (DeWR-1) | 4.9 s | 0.0 | - |
| AVAX | 1.1 s (Route 7 cert) | 2.2 s | +1.1 | - |
| Stellar | 6.5 s (IR-1 router) | 6.6 s | +0.1 | - |
| XRP | 7.09 s (XTR-1 avg) | 8.4 s | +1.3 | - |
| DOT | 10 s (DOT T3 same-day) | 10.0 s | 0.0 | - |
| Cardano | 30 s (IR-1 router) | submit-accept 0.6 s; inclusion <=5 min | n/a | acceptance != finality; block 14090269 |
| ETH | 13.0 s (IR-1 router) | 43.4 s | +30.4 | OPERATIONAL NOTE: 3-4 block inclusion at a low-gas window; gasPrice sampled at broadcast lagged next-block rate. |
| DOGE | ~60 s (block cadence) | ~60 s | 0 | nominal |
| BTC | 900 s (IR-1 router) | pending at seal (~40 min) | n/a | OPERATIONAL NOTE: effective 3.3 sat/vB (239 vB actual vs ~140 vB estimate) vs a 1-3 sat/vB market — edge-priority; inclusion receipt appends forward-only when mined. |

Router error profile: 6/10 rails within 1.3 s of prediction; ETH and BTC are the two
mempool-priced rails and account for all deviation >3 s — consistent with the IR-1
doctrine that market-priced rails carry variance risk.

## Failed attempts disclosed (G4, honest forward-only)
- SOL: 2 failed broadcasts with raw binary memo data (InvalidInstructionData, 5000 lamports
  each, ~0.003 USD) before the proven hex-ASCII + signer-meta form (DeWR-1 doctrine) landed.
- XRP: 4 library-shape failures (xrpl-py Wallet constructor / arg order / Memo model), all
  local — no ledger effect, no fees.
- Cardano: 3 submissions rejected pre-acceptance (era decode + missing aux-data-hash),
  no ledger effect, no fees.
- DOGE: 1 UTXO query HTTP 400 (API shape), no ledger effect. Final leg spent the verified
  unspent DeWR-1 T3 change output 075e7656...329aa:1 (14.9 DOGE -> 14.85 change returned).
- All fees disclosed above; total failed-attempt postage: 0.02 SOL (~0.003 USD).

## Gates
- G1 artifact digest vs frozen sha: PASS (byte-exact)
- G2 scope stamp before first broadcast: PASS (cfr9_crossfire_2026-10-19)
- G3 keyless read-back byte-exact on all legs: PASS (10/10; independent endpoints incl.
  blockstream.info, horizon.stellar.org, koios.rest, algonode indexer, xrplcluster, Etherscan RPC)
- G4 fees recorded, failed attempts disclosed: PASS
- G5 independent public endpoint read-back: PASS (every read-back used a public node,
  not the submitting writer)

## Pending at seal
- BTC block inclusion (byte-exact verified in mempool via blockstream.info); inclusion
  block/height appends forward-only when mined.
- Ledger seal (next open entry) awaits Leon GO per the two-key gate.
- No DOI mint (per prereg, unless Leon GOs a Zenodo record separately).

Prototype disclaimer: this software is a prototype, educational/research purposes only,
not intended for production use.

## BTC INCLUSION RECEIPT (forward-only append, 2026-10-19 ~16:35 CT)
BTC leg 83f7ba0db20ac13e19c30dfa3adb19b997fbf5181b7619b6fe13228f10010d0b CONFIRMED in
block 972214. OP_RETURN payload byte-exact (blockstream.info keyless read-back).
ALL 10 RAILS NOW BLOCK-INCLUDED. CFR-9 fully closed on-chain.
Ledger seal: entry 0258, Leon GO (chat authorization, 2026-10-19 ~16:32 CT).
