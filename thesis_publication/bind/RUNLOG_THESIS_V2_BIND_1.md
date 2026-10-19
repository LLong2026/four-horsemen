# RUNLOG — THESIS-V2-BIND-1
## Dual-Rail Bind of Master Thesis Volume II (BTC + XRP, DWR-class)
**Date:** 2026-10-19 (owner GO, chat authorization ~14:25 CT)
**Prereg:** sha256 c1db2f4eac407b471ebd73b55f644ed9bd303f22778656e5118623807b973c9 (frozen pre-broadcast, identifiers committed)

### Artifact
Master Thesis Volume II PDF (DOI 10.5281/zenodo.23482711), sha256
d676902dd34934c137793910632e02b717e3e17098303348585a5004459c827e.

### Build (offline, both legs signed before broadcast)
- BTC: segwit writer (bc1qf4zs...harzw6), OP_RETURN postage-only, payload SQDR+0x01+digest (37 bytes),
  spending 266b1780...:1 (79,815 sats confirmed), adaptive fee 790 sats @ ~5 sat/vB (vsize 158).
  Canonical txid computed over the witness-stripped serialization (ledger-0228 doctrine); an in-build
  assert caught a wtxid-instability hazard before any broadcast — the identifier doctrine was enforced
  at build time this session, versus DWR-1's post-hoc correction.
- XRP: writer rBbxYuBk... (seq 107745089), AccountSet non-payment storage write, fee 10 drops,
  memo_type SQDR-XRP-THESIS-V2, memo_data = digest.

### Broadcast
- BTC: broadcast via blockstream.info — returned txid 1fb243ab8460c97ad2eb1d7ab5847ba8c4b003d1e0b366113195ed5ebf3be2d9,
  exact match to the committed canonical txid.
- XRP: tesSUCCESS, hash 7ABEF6066CAB61076E6A4E20966121FB9B5EF881A3FD2CDBDF414CFBB470043B, exact match to committed.
- **DEFECT DISCLOSED (G4 FAIL):** the BTC->XRP broadcast interval exceeded the 60-second target. Two xrpl-py
  Submit kwarg rejections (tx_blob, then tx) preceded a raw JSON-RPC fallback. The joint commitment was
  unaffected — both identifiers remained frozen before either broadcast — but the interval gate is scored
  FAIL and disclosed, not smoothed.

### Keyless read-backs (zero credentials)
- BTC: blockstream.info + mempool.space — OP_RETURN script 6a25 5351445201+digest BYTE-EXACT MATCH on both
  independent explorers. Fee 790 sats. Block confirmation pending at seal (standard ~10-min cadence).
- XRP: rippled tx — validated, ledger 107768211, MemoType SQDR-XRP-THESIS-V2, MemoData digest
  BYTE-EXACT MATCH. Fee 10 drops.

### Gates
G1 joint commitment PASS | G2 BTC payload PASS | G3 XRP memo PASS | G4 interval FAIL (disclosed above) |
G5 identifier doctrine PASS (both committed identifiers match chain data) | G6 purity PASS
(no keys, no PII/PHI, no customer data; no token, no contract, no monetary output; ledger-0244 terminology).

Predictions: 4 PASS + 1 FAIL (G4 interval), all disclosed. MEASURED (scoped): all gates deterministic,
no LLM or neural-mesh component in any decision path (program benchmark DOI 10.5281/zenodo.23321637).
Dual Mesh Benchmark: NOT MEASURED (not applicable to ledger ceremonies).
