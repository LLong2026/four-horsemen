# TL-1 — THE TRUSTABLE LOCK: A TOKENIZED LUMEN SESSION RECEIPT
## SQUIRL OS Tokenization Demo — 2026-10-20

**Asset:** one Stellar lumen (XLM), tokenized in place — the vessel account holds the
lumens AND the ownership record in the same place, on the same chain.

**Artifact:** FL-1 Breakthrough Note — the fractal lease session.
Original (DOI, where the canonical record lives): https://doi.org/10.5281/zenodo.23515307
Artifact sha256: 61de4811d3712b02147ec2dd45e663dd3f5dabe863484b3602ce0a702d35b733

**The lock — three receipts, one digest, three consensus domains:**
1. XLM data entry (the token: asset + record in one account, browser-readable)
2. XRP memo (the attestation: rail of record, 4s finality)
3. BTC OP_RETURN (the mark: tamper-proof, most conservative ledger)

**Redundancy doctrine:** the original lives at the DOI; the chains carry
mutually-verifiable receipts pointing at it. No single ledger is trusted alone.

Envelope: SQDR + 0x0E (TL receipt) + SHA256 digest.
