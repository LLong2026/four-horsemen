# THE PWR-1 SPEC — The Penta-Write Receipt, Class Definition v1.0

**Author:** Leon Calvin Long, II — SQUIRL OS Technologies LLC
**Date:** 2026-10-19 | **Series:** No. 10 | **Predecessors:** DWR-1 (2 rails), TWR-1 (3), RTWR-1 (3, recursive), QWR-1/QWR-2 (4), XCF-1 (8-hop custody crossfire)

## 1. Definition

A **Penta-Write Receipt (PWR)** is the simultaneous, non-custodial, hash-only storage of one
SHA-256 digest on FIVE independent mainnets in a single ceremony:

| Rail | Mechanism | Value moved |
|------|-----------|-------------|
| Bitcoin | OP_RETURN (SQDR + 0x03 + digest) | none |
| XRP Ledger | AccountSet with memo (SQDR-PWR-1 + digest) | none |
| Stellar | ManageData entry "PWR-1" = digest | none |
| Cardano | transaction metadata, label 1968 | self-transfer only (fee) |
| Ethereum | transaction calldata (SQDR + 0x03 + digest), self-addressed | none |

**No tokens are minted. No custody is taken. No payments are moved.** The document lives in
the vault; only its fingerprint is engraved. This is not tokenomics; it is multi-rail
evidence anchoring.

## 2. Zero-Movement Doctrine

The artifact never moves. Every leg of PWR-1 is an inscription: Bitcoin OP_RETURN carries no
value; XRPL AccountSet changes no balance; Stellar ManageData writes a named ledger entry;
Cardano sends value to its own address (only the fee leaves); Ethereum sends zero to itself.
Wallet view → hash → hash → wallet view: the fee buys permanence and consensus, not motion.

## 3. Why five rails

Each mainnet is an independent failure domain with its own validator set, consensus,
cryptography, and governance. A digest readable across five such domains simultaneously has
no single point of deletion. Five is the declared terminal set for this program phase:
enough to prove the point; the ceremony spec is rail-agnostic and any further rail is a
postage line item, not a capability gap.

## 4. Wallet roster (all keys local, self-custodial, both sides per rail)

- BTC-A bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6
- XRP-A rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR
- STELLAR-A GDIQGGTUC4FTKP7R7CZ57L3ATXVJ2NRLNVGQPLKB6WJQIZA4LQ7KFM63QC
- CARDANO-A addr1vxpwu7fg7qy0u60wjcyx30rf9uzqvpssphhppar2ju45dnqwnrq5q
- ETH-A 0x96d17F38E50A5372b8FEfdD1D121785DABB62C30 (new rail, funded 2026-10-19)

## 5. Gates

G1 spec+prereg frozen and committed pre-broadcast — G2 five legs built and signed offline —
G3 five legs broadcast back-to-back — G4 keyless byte-exact read-backs on all five —
G5 ledger + receipts sealed. All gates deterministic; no LLM in any decision path.

## 6. Cost ceiling

BTC ~700 sats | XRP 10 drops | Stellar 100 stroops + 0.5 XLM data-entry reserve | Cardano
~171,000 lovelace | Ethereum ~22,000 gas at prevailing base fee. Total under $1 equivalent.

This software is a prototype and is provided for educational and research purposes only. It
is not intended for production use, commercial deployment, or safety-critical environments.
All systems are experimental and may contain defects.
