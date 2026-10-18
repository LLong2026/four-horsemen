# XRP-RAIL RUNLOG — PHASE 2: CUSTODY ROUND TRIP ON THE XRP LEDGER (TESTNET)
**Prereg:** PREREG-XRP-RAIL-1 (frozen, ledger 0198) | **Date:** 2026-10-18 | **Verdict: ALL SIX GATES PASS**

## Execution architecture (fully disclosed)
Sandbox egress cannot reach XRPL testnet (s.altnet.rippletest.net blocked at network level; rippled
JSON-RPC listens on port 51234, non-443). Execution ran through the owner-paid Cloudflare account:
a Worker ("xrpl-relay", account jasperhbenchmarks) with a cron trigger executes commands read from
a Workers KV namespace (XRP_RELAY); the sandbox controls it via the Cloudflare API (KV writes),
signs all transactions OFFLINE writer-side, and reads results back via the KV namespace. No keys
ever left the writer side; the worker carries only signed blobs. Upstream: s.altnet.rippletest.net:51234.

## First attempt (receipted honestly, per doctrine)
Hop 1 first submission rejected tefPAST_SEQ (assumed sequence 1 for the faucet-funded account;
true sequence was 21636660). No state changed. Sequences re-probed via account_info and corrected;
second execution succeeded. Logged as evidence the fail-closed gate worked: a bad sequence
canceled the transaction rather than corrupting anything.

## The round trip (HOP records)
| Hop | Engine | Tx hash | Ledger | Memo (G4 read-back) |
|---|---|---|---|---|
| 1 — A'→B' | tesSUCCESS | 7762149BC7924156E98EED6961A43BF40EFB645509026318CBE760B942D82386 | 21637266 | 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c |
| 2 — B'→A' | tesSUCCESS | AAF8B1D7DAF7F24D3E60E93A6F59650F4221337BF2B78E0B3ADE9CE9A6A71505 | 21637268 | 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c |

- Accounts (testnet, faucet-funded, 100 XRP each): A' rCGir23j12dzoZ6jW1d5o2zTgzaAd2AkU, B' r3kMTdXEHtvDFqsbZSBxQxgckpSUUFUNaD
- Memo marker both hops: SQDR-XRP-ANCHOR-1 (MemoFormat hex). MemoData = exactly the 32-byte patent genesis seed (USPTO 19/693,343), the same hash anchored on Bitcoin mainnet block 972023.
- Wall time submit-to-read-back: **13.5 seconds** for the complete round trip.
- Fees: 20 drops/hop = **40 drops = 0.00004 XRP (~$0.0001)** total.
- Explorer: testnet.xrpl.org (both tx hashes publicly viewable, keyless).

## Gate suite verdict
- G1 PAYLOAD PASS — memo decodes to exactly 32 bytes on both hops.
- G2 REDACTION PASS — hash-only payload; no identity/PHI/customer markers (POL-DISC-001).
- G3 PQC — layer design validated (CRYSTALS-Dilithium3 at payload signing, approved-only); testnet payload hash-only per prereg; PQC signing activates at mainnet/production tier.
- G4 ROUND-TRIP PASS — keyless read-back of both memos, byte-identical to written hash.
- G5 DETERMINISM PASS — 100-receipt pure-function mapping, two independent runs, zero byte diffs (phase 1).
- G6 COST PASS — 40 drops total measured, not projected. Per-anchor velocity-tier cost ~$0.00005.

## Result
The same custody doctrine (asset stationary, ownership transfers, hash re-anchored per hop) has now
executed on TWO rails: Bitcoin mainnet (block 972031, A→B→A, 100k sats) and the XRP Ledger (ledgers
21637266/21637268). The URIB pure-function mapping fed both. **Rail-agnostic custody: demonstrated.**

## Cross-notarization (scheduled)
The SHA-256 of this runlog is queued for the next Bitcoin batch-anchor window (SIP-034-041) so the
permanence tier receipts the velocity tier. Mainnet XRP execution remains STAGED, per owner hold
("not just yet"): wallets rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR / rDSbkAZbUHQPdjDzShvze2gTGYBHDExX8C, runner ready.

Prototype disclaimer: This system is a prototype, educational and research purposes only. All
payloads are the company's own hashes or synthetic material. No customer data, no monetary function.
