# PREREG — XCF-1 (THE WALLET CROSSFIRE)

**Frozen:** 2026-10-19, pre-broadcast. **Authorization:** Leon GO (chat authorization,
2026-10-19 ~10:34 CT, "do a wallet crossfire... exchanging ownership").

## What this ceremony proves
Simultaneous ownership exchange of one 32-byte digest across FOUR mainnets, back and forth,
between two self-custodial writer wallets per rail (both keypairs held locally, non-custodial,
no third party). The riding payload is the DRIFT-1 report digest — the first real metrics of
the 60-day run — owned alternately by wallet A and wallet B on every rail.

**Riding digest (sha256, DRIFT1_REPORT_v1.0.md):** 5f69e1bf9a35a6fae4dd2adf8fd19f8e8135a8acb1980279caba2a377efc275e

## Wallet roster (all keys local, both sides per rail)
- BTC-A bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6 | BTC-B bc1q90jca35yjzup30nlqq8duwqzld43au0n88ege3
- XRP-A rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR (seq 107745083 after QWR-2) | XRP-B rDSbkAZbUHQPdjDzShvze2gTGYBHDExX8C (seq 107745085)
- STELLAR-A GDIQGGTUC4FT... (seq next 279261054213554180) | STELLAR-B GC6VZWZXARDOCAJP7WGQUHRPNKCVLTCSO7XTEG5YDGZR6ATGEIMDL6JD (NEW key, generated 2026-10-19)
- CARDANO-A addr1vxpwu7fg7qy0u60wjcyx30rf9uzqvpssphhppar2ju45dnqwnrq5q | CARDANO-B addr1v9vqnqx7d8puzv0tk5dt3up2r7lcdel7dt0fr3nhayjwrdql52lja (NEW key)

## Hop plan — two synchronized bursts
BURST 1 (outbound, back-to-back):
- BTC A→B: 82,000 sats + OP_RETURN (SQDR + 0x02 + digest), fee 700 sats
- XRP B→A: 700,000 drops + memo SQDR-XCF-1 + digest, fee 10 drops
- STELLAR A→B: create_account 20 XLM + memo_hash digest, fee 100 stroops
- CARDANO A→B: 50,000,000 lovelace + metadata label 1968 {XCF: XCF-1, HOP: 1, DIGEST}, fee ~0.17 ADA

BURST 2 (return, after burst-1 settlement):
- BTC B→A: received minus 700 sats fee + same OP_RETURN payload
- XRP A→B: 700,000 drops back + same memo
- STELLAR B→A: payment 19.5 XLM + memo_hash digest, fee 100 stroops
- CARDANO B→A: ~49,500,000 lovelace + metadata HOP: 2, fee ~0.17 ADA

Crossfire doctrine: BTC and Stellar carry ownership A→B→A; XRP carries B→A→B (ownership moves
in OPPOSITE directions simultaneously — the crossfire). Cardano A→B→A.

## Gates
G1 prereg frozen + committed pre-broadcast — G2 burst-1 broadcast back-to-back — G3 burst-1
settlement verified — G4 burst-2 broadcast — G5 keyless byte-exact read-backs on all 8 hops —
G6 ledger + receipts sealed. Burst-2 identifiers depend on burst-1 settlement (declared).

## Planned cost ceiling
2,800 sats + 20 drops + 200 stroops + ~0.4 ADA.

MEASURED (scoped): all gates deterministic; no LLM in any decision path (program benchmark DOI
10.5281/zenodo.23321637). Payload is a report digest; no production, customer, or personal data
(POL-DISC-001). Prototype disclaimer applies.
