# PREREG — QWR-2 (QUAD-WRITE RECEIPT NO. 2)

**Frozen:** 2026-10-19, pre-broadcast. **Authorization:** Leon GO (chat authorization, 2026-10-19
~09:31 CT). Companion to the same-day first-real-metrics LinkedIn publication (ledger 0232).

## Artifact (committed BEFORE any broadcast)
DRIFT1_REPORT_v1.0.md — first real metrics of the 60-day run (epoch 20261019 drift report).
sha256 5f69e1bf9a35a6fae4dd2adf8fd19f8e8135a8acb1980279caba2a377efc275e
The quad-written payload is the DRIFT-1 report digest (first non-self-referential quad-write;
QWR-1 quad-wrote its own spec).

## Identifiers of record (all computed locally, committed pre-broadcast)
- **Bitcoin:** CANONICAL txid a02b22db8fcd89bc5fc13f51cb3c84abeafb3055b023051d0b9ac0d1914eba0f
  (non-witness serialization; wtxid aa9a1396b0be44ffe2d711fcc4ab0747b5bbd4f74692c1d6a39b5c0e8d830336 disclosed)
- **XRPL:** txid E3883E43A2249FB180042D60D426F9ABAF53FFA016EDB5A01D425C6742FDA2AA (AccountSet,
  memo SQDR-XRP-STORE-5, sequence 107745082)
- **Stellar:** NETWORK hash D47691A894B85A09F5EC5E532591BD401642459DB5AB4A3C138BC2C4A4F18FAC
  (ManageData SQDR-STORE-4 + memo_hash, seq 279261054213554179)
- **Cardano:** transaction hash f8d37e9309d3c40a90f2c399a82d1965c190e714f16570184becf7b4a64e6955
  (blake2b256 over tx body CBOR; metadata label 1967 {SQDR: QWR-2, DIGEST: 5f69e1bf...c275e};
  input a6c6a1df...584ac:0; Ed25519 witness verified over the body hash)

## Gates
G1 offline build (DONE, self-verified: BTC BIP143 recipe per QWR-1; Cardano signature/aux-hash/
txid all recomputed and verified) — G2 back-to-back broadcast, 90s ceiling/leg — G3 keyless
byte-exact read-backs on all four rails — G4 identifier forms correct (ledger-0228 doctrine,
Cardano prose corrected to blake2b256) — G5 DOI mint.

## Planned costs
700 sats + 10 drops + 200 stroops + 169197 lovelace.

MEASURED (scoped): all gates deterministic; no neural-mesh or LLM inference in any decision path
(program benchmark: DOI 10.5281/zenodo.23321637). Prototype disclaimer applies.
