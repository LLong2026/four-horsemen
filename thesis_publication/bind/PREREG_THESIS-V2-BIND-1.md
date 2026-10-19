# PREREGISTRATION — THESIS-V2-BIND-1
## Dual-Rail Bind of Master Thesis Volume II (DWR-class, owner GO 2026-10-19 ~14:25 CT)

**Ceremony type:** Dual-write evidence bind (ledger-0224 doctrine, no custody transfer on either leg).
**Joint prior commitment:** this prereg is frozen (sha256 below) BEFORE any broadcast.

### Artifact
- Master Thesis Volume II (published PDF), Zenodo DOI 10.5281/zenodo.23482711
- PDF sha256: d676902dd34934c137793910632e02b717e3e17098303348585a5004459c827e
- MD sha256: 1efb8f5eaf9304c2207c6d905eeca3cb73a9a3e5739152bcedae76eaa116f77d

### Rails and committed identifiers (frozen pre-broadcast)
1. **Bitcoin mainnet** — OP_RETURN postage-only write, payload `SQDR` + 0x01 + digest (37 bytes, purity: no keys, no PII, no client data).
   - Canonical txid (ledger-0228 doctrine, non-witness): `1fb243ab8460c97ad2eb1d7ab5847ba8c4b003d1e0b366113195ed5ebf3be2d9`
   - Spending UTXO: 266b17804fd3631b16eaa66b9992e8b177b1c2814f61e98abee9486ea5384dc6:1 (79815 sats, confirmed)
   - Predicted fee: 790 sats (~5 sat/vB, vsize 158) — PREDICTION: fee <= 1,500 sats
2. **XRP Ledger mainnet** — AccountSet non-payment storage write, memo_type `SQDR-XRP-THESIS-V2`, memo_data = digest.
   - Tx hash: `7ABEF6066CAB61076E6A4E20966121FB9B5EF881A3FD2CDBDF414CFBB470043B`
   - Sequence: 107745089, fee: 10 drops — PREDICTION: fee <= 20 drops

### Gates
- G1: both transactions broadcast under this single frozen commitment.
- G2: BTC OP_RETURN payload byte-exact on keyless read-back (blockstream.info + mempool.space).
- G3: XRP memo digest byte-exact on keyless read-back (xrpscan / xrplcluster).
- G4: broadcast interval < 60 seconds (target: < 5 seconds).
- G5: canonical identifier doctrine — BTC txid committed as canonical (non-witness), XRP standard hash; committed identifiers MUST match post-broadcast chain data.
- G6: payload purity audit — 37 bytes BTC / memo-only XRP; no credentials, no PII/PHI, no customer data (POL-DISC-001).

Predictions: 5 total. All gates deterministic; no LLM or neural-mesh component in any decision path (MEASURED (scoped); program benchmark DOI 10.5281/zenodo.23321637).
No token, no contract, no monetary output created (terminology doctrine, ledger 0244).
