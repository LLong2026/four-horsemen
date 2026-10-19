# ALGORAND T2 TRAINING LEG — RUNLOG (training, not a ceremony)

**Route:** Algorand (Route 6, first Tier 2 candidate) | **Leg type:** T2 training inscription
**Doctrine:** rehearsal only — no DOI, no ledger entry, no public artifact, disclosed as training.
**Training digest (SHA-256 of training marker, not an artifact digest):**
`1d7434646be72ae11529eea7dd9b16d493d97eb466d322edd8abb6e3222b4675`
**Txid:** `MA2L6YWDVMKRDXR7VAROEQOBJ4NZLC5YLAXVN324VBVE5BYVWSPA`
**Confirmed round:** 66138941 (2026-10-19)

## Measured performance
- Broadcast → confirmed: **4.4s**
- Fee: **1,000 microALGO = 0.001 ALGO** (~$0.0004)
- Mechanism: note field on zero-value self-payment, lease-bound for idempotency

## Keyless read-back (public, no credentials)
- Verified byte-exact against the digest via public indexer (mainnet-idx.algonode.cloud)
- Public verifier: https://allo.info/tx/MA2L6YWDVMKRDXR7VAROEQOBJ4NZLC5YLAXVN324VBVE5BYVWSPA
- Result: **BYTE-EXACT MATCH — PASS**

## Route status
T2 PASS. Route 6 proceeds to T3 (full certification ceremony) on Leon GO — that leg
freezes spec + prereg, executes the timed inscription, and seals the ledger entry,
promoting Algorand to Tier 1 CERTIFIED.

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
