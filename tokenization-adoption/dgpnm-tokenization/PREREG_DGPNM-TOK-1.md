# PREREG DGPNM-TOK-1 — First Real-Life Full-Stream Tokenization
Frozen: 2026-10-18 ~14:40 CT. Operator authorization: Leon GO (chat authorization, 2026-10-18 ~14:38 CT).

## Asset
Document: "Deterministically Governed Probabilistic Neural Mesh" (v1.1, 2026-10-18)
Asset digest (SHA-256): 66dc843abbfb6d98245187c036cf4a631395cd783debdb852833e31b3ee9de2b
v1.0 digest (superseded, retained for record): ae3bc6299bf8200b205226619d028dbd6e6d0d214b43376c78ca221aa581cd81
Patent linkage: U.S. Provisional Patent Application No. 64/119,191

## Frozen gates (deterministic, no LLM in decision path)
- G1 BIND: OP_RETURN on Bitcoin mainnet = SQDR marker + version 0x01 + 32-byte digest. Payload purity: 37 bytes, hash-only. No monetary output.
- G2 SEND: XRPL mainnet payment A -> B carrying the digest in Memo data (marker SQDR-XRP-ANCHOR-1), followed by return hop B -> A (custody round trip).
- G3 PULL-BACK: keyless chain-pull of the OP_RETURN payload from mainnet; byte-exact match against the asset digest required.
- G4 RECEIPTS: every hop journaled (hub DropboxDrop + URIB DropReceipt + DropQueue lifecycle). No client data, no PHI, keys writer-side only (D1-D5 invariants, SIP-042).

## Cost envelope (postage only)
BTC fee ~800 sats (adaptive); XRPL fees ~40 drops (~$0.0001). Asset value: $0. What is tokenized is the hash.
