# QWR-2 — THE QUAD-WRITE RECEIPT SPECIFICATION v1.0

**Class:** Quad-write storage ceremony (second of the class proven in QWR-1).
**Definition:** The simultaneous, non-custodial storage of ONE SHA-256 digest on FOUR mainnets —
Bitcoin, XRPL, Stellar, and Cardano — under a single joint pre-broadcast commitment. Hash-only on
every rail: no tokens minted, no custody taken, no payments moved, no client data (POL-DISC-001).

## Artifact (first non-self-referential quad-write)
DRIFT1_REPORT_v1.0.md — the first real metrics of the 60-day run (drift report, epoch 20261019).
**Artifact digest (sha256):** 5f69e1bf9a35a6fae4dd2adf8fd19f8e8135a8acb1980279caba2a377efc275e

## Rails and payload doctrine
1. **Bitcoin mainnet** — OP_RETURN, payload SQDR + 0x01 + digest (37 bytes). IDENTIFIER OF RECORD:
   canonical txid computed locally over the non-witness serialization (ledger 0228 doctrine).
2. **XRPL mainnet** — AccountSet non-payment storage write, memo type SQDR-XRP-STORE-5 + digest.
   IDENTIFIER OF RECORD: transaction hash.
3. **Stellar mainnet** — ManageData (SQDR-STORE-4 = 32-byte digest, zero transfer) + memo_hash.
   IDENTIFIER OF RECORD: the NETWORK transaction hash.
4. **Cardano mainnet** — transaction metadata, label 1967, keys "SQDR" = "QWR-2" and "DIGEST".
   IDENTIFIER OF RECORD: the transaction hash = **blake2b256 over the tx body CBOR** (correction of
   the QWR-1 prereg's imprecise "sha256" prose label; the QWR-1 on-chain identifier was always the
   correct blake2b256 value and is byte-exact on-chain — disclosed in DRIFT-1 section 2.3).
   Wire form: plain 4-element CBOR array [body, witness_set, valid, aux] (the QWR-1 working form).

## Gates
- G1 BUILD: all four legs signed offline; all identifiers computed and committed pre-broadcast.
- G2 BROADCAST: back-to-back, ceiling 90s per leg; retries disclosed.
- G3 READ-BACK: keyless, byte-exact on all four rails.
- G4: identifier forms correct per rail (ledger 0228 doctrine).
- G5 DOI: Zenodo record minted with receipts after verification.

## Planned costs (ceiling)
700 sats + 10 drops + 200 stroops + 0.17 ADA.

MEASURED (scoped): all gates deterministic; no neural-mesh or LLM inference in any decision path
(program benchmark: DOI 10.5281/zenodo.23321637).

Prototype disclaimer: this system is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
