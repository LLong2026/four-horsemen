# RETROFIT SPEC — URIB -> XRP RAIL (DETERMINISTIC)
**Spec:** RETROFIT-URIB-XRP-1 | **Companion to:** PREREG-XRP-RAIL-1 | **Status:** DRAFT v1.0 (frozen at first execution)

The ISO 20022 Universal Bridge (URIB) already models the receipt/settlement shape: message in, canonical receipt out. This retrofit re-uses that spine and replaces the transport with a deterministic XRPL memo writer. No probabilistic component enters the decision path: URIB's template layer is static, the mapping is a pure function.

## 1. Mapping (pure function, ISO 20022 -> XRPL Memo)
An anchored receipt R (canonical, from the receipts ledger) maps to exactly one XRPL Payment:
- `Amount`: 1 drop (minimum; the tx is a notary act, not a value transfer).
- `Destination`: the anchor account (writer-controlled, single-account doctrine).
- `Memos[0].MemoData`: hex(SHA-256(R_canonical)) — exactly 64 hex chars.
- `Memos[0].MemoFormat`: "hex" | `Memos[0].MemoType`: "SQDR-XRP-ANCHOR-1".
- No other fields carry data. Identical input receipt -> byte-identical memo payload (determinism contract, G5).

## 2. Rail placement
- VELOCITY TIER (XRPL): high-frequency per-item anchors, immediate finality, negligible fee.
- PERMANENCE TIER (Bitcoin): batched Merkle anchors (SIP-034-041 OTS), one commit per batch window.
- CROSS-NOTARIZATION: the digest of every XRP runlog is batch-anchored on Bitcoin; the Bitcoin tip is memo-anchored on XRP. Each rail receipts the other; neither is trusted alone.

## 3. Custody representation (H4, mirrors the Bitcoin A->B->A demo)
- The satoshi-custody representation moves via XRPL account sequence/control transfer (issuance-free, trustline-free), with the asset hash re-anchored per hop — same doctrine, different rail: asset stationary, custody transferable.

## 4. Security layer
- Payload PQC-signed (approved algorithms only) before broadcast; reader verifies PQC signature plus digest equality (G3/G4). Fail-closed everywhere.

## 5. Explicitly out of scope
- Tokens, issuances, trustlines, DEX, AMM, monetary value transfer of any kind. Customer data of any kind. Non-PQC schemes. The TGC engine (licensed product, not distributed).
