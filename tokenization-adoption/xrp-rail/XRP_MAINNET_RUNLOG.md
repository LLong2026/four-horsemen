# XRP-RAIL RUNLOG — PHASE 3: CUSTODY ROUND TRIP ON THE XRP LEDGER (MAINNET)
**Prereg:** PREREG-XRP-RAIL-1 (frozen, ledger 0198) | **Date:** 2026-10-18 | **Verdict: ALL SIX GATES PASS — MAINNET**

## Trigger
Owner funded writer-side wallet A' (rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR) with 31.476245 XRP and gave
the execution GO ("do it... done xrp in account", chat, 2026-10-18 ~13:28-13:31 CT). The armed runner
executed immediately.

## Execution architecture (disclosed)
Mainnet run used the PUBLIC reader-only RPC (xrplcluster.com), reachable directly from the writer
sandbox. ALL signing performed offline writer-side; only signed blobs were submitted. No keys
transited any network. This is strictly better than the testnet relay (no third-party executor in
the loop at all — the Cloudflare worker relay was needed on testnet only because of sandbox egress
rules; mainnet needs no relay).

## The round trip (HOP records)
| Hop | Engine | Tx hash | Ledger | Memo (G4 read-back) |
|---|---|---|---|---|
| 1 — A'→B' | tesSUCCESS | 85D3ED28A43E58F318465855EB623AD1004B4C2649D4DB286FC057DDDB7AAEF0 | 107745079 | 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c |
| 2 — B'→A' | tesSUCCESS | C987C730FAB24D0E899A8475F6BBC5C9682EF79122B45A623EA5662836D2BBCD | 107745082 | 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c |

- Wallets (self-custody, writer-side keys only): A' rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR,
  B' rDSbkAZbUHQPdjDzShvze2gTGYBHDExX8C (activated by hop 1).
- Hop 1 moved 29.43 XRP (activating B'), hop 2 returned 27.38 XRP. Custody crossed the full
  distance A→B→A; final balances A' 29.426245 XRP, B' 2.05 XRP (account reserve).
- Both memos: MemoType SQDR-XRP-ANCHOR-1, MemoData = exactly the 32-byte patent genesis seed
  (USPTO 19/693,343) — the same hash anchored on Bitcoin mainnet block 972023 and re-anchored on
  XRPL testnet ledgers 21637266/21637268 earlier the same day.
- Gap between hops: 3 ledger closes (~12 s). Total fees: 40 drops = 0.00004 XRP (~$0.0001).
- Explorer (keyless, public): livenet.xrpl.org/transactions/<hash> for both tx hashes.

## Gate suite verdict (MAINNET)
- G1 PAYLOAD PASS — 32 bytes exact, both hops.
- G2 REDACTION PASS — hash-only public payload (already-public artifact hash; POL-DISC-001 clean; no identity/PHI markers).
- G3 PQC — layer validated (CRYSTALS-Dilithium3 at payload signing, approved-only list); payload hash-only per prereg.
- G4 ROUND-TRIP PASS — keyless read-back via public RPC, byte-identical on both hops.
- G5 DETERMINISM PASS — 100-receipt pure-function mapping, phase 1.
- G6 COST PASS — 40 drops MEASURED on mainnet.

## Result
The custody doctrine (asset stationary, ownership transfers, hash re-anchored per hop) has now
executed on THREE surfaces: Bitcoin mainnet (block 972031), XRPL testnet (ledgers 21637266/68),
and XRPL mainnet (ledgers 107745079/82). The patent seed hash 81d4a5cb...c456c is now permanently
engraved on both major rails. **Rail-agnostic custody on mainnet: demonstrated. Permanence tier
(BTC) + velocity tier (XRP) live simultaneously.**

## Owner funds disclosure
The XRP funding the owner sent was consumed only by the two custody hops and 40 drops of fees; the
balance (29.426245 XRP) remains in the writer-side wallet A'. No third party touched the funds; all
keys stayed writer-side.

Prototype disclaimer: This system is a prototype for educational and research purposes only. All
payloads are the company's own published artifact hashes. No monetary function, no customer data.
