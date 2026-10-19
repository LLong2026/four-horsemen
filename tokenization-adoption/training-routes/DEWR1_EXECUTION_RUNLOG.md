# DeWR-1 EXECUTION RUNLOG — Leg Set 1 (six funded rails) — 2026-10-19 ~12:20-12:40 CT

**Ceremony:** DeWR-1, the Deca-Write Receipt. Leon GO (chat authorization, 2026-10-19 ~12:18 CT).
**Artifact:** RAIL_PERFORMANCE_RECORD_v1.md | SHA-256: 99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6
**Prereg frozen pre-broadcast:** sha 4bf51de4e3e469d0caf9a22e2fce6a06f51a4b90b86ae1d714edc734eeb1f600 (commit 0376f73)
**Doctrine:** the document that measures the rails, engraved on the rails. Same digest on every leg.

## Legs executed and keyless-verified (6/10)

| Rail | Mechanism | Identifier of record | Confirmed | Cost | Byte-exact |
|------|-----------|---------------------|-----------|------|-----------|
| Bitcoin | OP_RETURN (SQDR+0x01) | canonical txid 266b17804fd3631b16eaa66b9992e8b177b1c2814f61e98abee9486ea5384dc6 | mempool at seal, payload verified | 785 sats | YES |
| XRPL | AccountSet memo (SQDR-DEWR-1) | txid A790E84B7FE19EE875578F43733AA1656755CA34A92E9E36078605ABE93B8CBD | VALIDATED 2026-10-19T17:20:40Z | 10 drops | YES |
| Stellar | ManageData SQDR-DEWR-1 | network hash 44aa16c82ec0662077cba56274479b6f58e20551c8a35f7b42f0ccd89e5985f2 | ledger 65028938, 5.3s | 100 stroops | YES |
| Cardano | metadata 1968 {CER: DEWR-1} | tx hash cab9d69fe828cb026e90c730f0416f2a6a508ecf62de260598b9addbc12580f5 | block 14089541 | 171000 lovelace | YES |
| Ethereum | calldata zero-value self-send | txid 0x607a24a06679b7dae491f07c5d12f8dc960f5043a4b626873916ef093611635d | block 26228092, 33.8s | 22280 gas (~$0.00002) | YES |
| Algorand | note field (T3 CERTIFICATION LEG) | txid VXGGJXVYDMGV2H6S5KF32FXS55H54HDHZRFIUEJKVEVABKA7ERAA | round 66139095, 4.6s | 0.001 ALGO | YES |

## ALGORAND T3 CERTIFICATION + CROSSFIRE (route 6 → Tier 1)

- T3 leg: VXGGJXVYDMGV2H6S5KF32FXS55H54HDHZRFIUEJKVEVABKA7ERAA (self-payment, note=digest, lease-bound)
- Crossfire hop 1 (A→B, 1.5 ALGO): NPCZPKWMJC7D6CCCT2IP22CGEPDDQLCGAIN7YPU2UBC7ON6GIFAQ, round 66139097, 6.7s
- Crossfire hop 2 (B→A, 1.399 ALGO): IY2NOA7CKUQVX432VEQ5FVJIWC7OGEPAFN2THVTYKFHQBXAJFJFA, round 66139114, 4.4s
- All three read back keyless byte-exact via public indexer (mainnet-idx.algonode.cloud).
- DISCLOSED (forward-only): hop 2 first attempt sent 1.499 ALGO, rejected by the account-min-balance
  rule (0.1 ALGO reserve, no state change); adjusted to 1.399 and confirmed. Algorand min-balance rule
  now in the route playbook.
- ALGORAND IS NOW TIER 1 CERTIFIED (route 6 of 10).

## Disclosures (forward-only, no silent retries)

- BTC leg in mempool at runlog seal; payload verified via mempool read; block confirmation follows
  normal PoW cadence (will be recorded when sealed).
- XRP: no self-payments on XRPL — the DeWR leg used AccountSet (memo carrier, no state change);
  disclosed in prereg lineage. One response-parse retry after validation (no duplicate broadcast:
  exactly one AccountSet with the DeWR digest on-chain).
- Stellar: transaction succeeded on first submit; read-back parse initially used a wrong response
  shape, corrected — data entry SQDR-DEWR-1 verified byte-exact from account state.

## Remaining legs (4/10)
- Polkadot, Solana, Avalanche: T2 training legs armed via Training Route Watch workflow (fires on
  funding arrival); DOT signing path pre-verified against live Polkadot mainnet.
- Hedera: alias auto-create two-hop pending.
- DeWR-1 completes (and DOI mints) when all ten legs carry the digest — same digest, no re-cut.

This software is a prototype and is provided for educational and research purposes only. It is not
intended for production use, commercial deployment, or safety-critical environments. All systems are
experimental and may contain defects.

## Leg set addendum — 2026-10-19 ~12:30 CT — AVAVALANCHE (route 7)

| Rail | Mechanism | Identifier of record | Confirmed | Cost | Byte-exact |
|------|-----------|---------------------|-----------|------|-----------|
| Avalanche | calldata zero-value self-send (T2+T3) | T3 txid 0x671d7002098803f53b8bcc7785ba1a0e2048168bb196f55dab3f810973c29988 | block 97987712, 1.1s | 21512 gas, 0.000083 AVAX | YES |

- Funding: 2.5 AVAX from Coinbase (Leon, inbond 2026-10-19 ~12:27 CT). Fired manually on operator notice.
- T2 rehearsal txid 0x7ebb433c...770443 (disclosed deviation: marker string instead of 32-byte training digest).
- AVALANCHE T3 PASSED → Tier 1 CERTIFIED (route 7 of 10). DeWR-1 legs now 7/10.
- Remaining: DOT, SOL (watcher armed), HBAR (alias two-hop pending).

## Leg set addendum 2 — 2026-10-19 ~12:40 CT — SOLANA (route 8)

| Rail | Mechanism | Identifier of record | Confirmed | Cost | Byte-exact |
|------|-----------|---------------------|-----------|------|-----------|
| Solana | SPL Memo (hex-ASCII digest) | sig 3nJzuipjPmMj9Uq5rSNLXb5CtdEqjUXhfmjRUg7wETYCohKWPCz6dkWTsUaBEg7UE33MFr2UN4rggQf6cMGUP4aT | slot 458918736 | 5000 lamports | YES |

- Funding: 0.2844 SOL from Coinbase. T2 rehearsal sig 67Cdt1Uid... (byte-exact).
- SOLANA T3 PASSED → Tier 1 CERTIFIED (route 8 of 10). DeWR-1 legs now 8/10.
- Remaining: DOT (watcher armed), HBAR (operator deciding — alias address delivered, exchange caveat).

## Scope note — 2026-10-19 ~12:42 CT — HBAR WAIVED BY OWNER

Leon (chat, 2026-10-19 ~12:41 CT): Hedera rail waived — route 10 dropped from the DeWR-1 scope.
Basis: owner decision (alias auto-create friction; exchange incompatibility). No HBAR leg will fire;
the armed ed25519 writer key stands down (key retained, rail re-openable later under a new ceremony).
DeWR-1 completion basis is now 9 rails: BTC, XRP, Stellar, Cardano, ETH, ALGO (certified),
AVAX, SOL (certified), DOT (pending funding — watcher armed). The record closes when DOT lands,
or stands at 8/9 with the waiver disclosed.
