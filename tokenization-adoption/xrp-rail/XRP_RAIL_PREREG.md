# PREREG — XRP-RAIL ANCHORING (XRPL MEMO-FIELD, RETROFIT OF THE ISO 20022 UNIVERSAL BRIDGE)
**Prereg ID:** PREREG-XRP-RAIL-1 | **Status:** FROZEN before first execution
**Owner authorization:** Leon GO (chat authorization, 2026-10-18 ~12:45 CT)
**Scope:** Deterministic retrofit of the ISO 20022 Universal Bridge (URIB) to anchor hash-receipts on the XRP Ledger via Payment Memo fields, as a high-frequency, near-zero-cost complement to Bitcoin batch anchoring (SIP-034-041).

## Motivation (measured, not projected)
Per-transaction Bitcoin anchoring cost ~$0.30-0.65 (mainnet, Oct 18 2026 session). Merkle batching (OTS) amortizes to fractions of a cent per receipt but confirms on batch windows. The open gap: high-frequency per-item records needing immediate, individually-timestamped anchoring. XRPL transaction fees are ~10 drops (0.00001 XRP ≈ $0.00002) and confirm in ~4-8 seconds. Hypothesis: XRPL memo anchoring covers the high-frequency tier at negligible cost, with Bitcoin retained as the permanence layer and XRPL as the velocity layer.

## Payload doctrine (identical to SIP-042, unchanged by rail)
- Hash-only: exactly one 32-byte SHA-256 per anchor, hex-encoded in MemoData (MemoFormat "hex"). No artifacts, no PII, no PHI, no customer-identifiable data, no credentials, no monetary payload.
- Transfer-only, binary outcome, no monetary function. The anchor is a notary act, not a payment of value.
- Reader is keyless: any pull is by address/txid from public XRPL APIs. Writer keys live ONLY on the writer side, never in the reader, never in any repo, never in any app.

## Hypotheses (falsifiable)
- H1: An XRPL Payment with a single Memo carrying a 32-byte hex digest succeeds deterministically and is publicly retrievable by txid without an account.
- H2: End-to-end anchor-and-read round trip completes in < 60 seconds at a fee < $0.001.
- H3: Deterministic message mapping from ISO 20022 pacs.008/camt.053 receipt structures to XRPL memos (retrofit of URIB) produces byte-identical memo payloads for identical input receipts (property test, 100 receipts).
- H4: A custody-transfer demo equivalent to the Bitcoin A->B->A round trip is representable on XRPL (issuance-free, trustline-free: satoshi-custody representation moves via account control, asset hash re-anchored per hop).

## Deterministic gates (all must PASS before any verdict)
- G1 PAYLOAD GATE: every broadcast memo decodes to exactly 32 bytes; any other length fails closed.
- G2 REDACTION GATE: payload scan for customer-identity and PHI markers before broadcast (POL-DISC-001); any hit aborts.
- G3 PQC GATE: payloads are PQC-signed with approved algorithms only (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); no non-PQC or unapproved scheme at any layer.
- G4 ROUND-TRIP GATE: reader-returned digest is byte-identical to the written digest.
- G5 DETERMINISM GATE: 100-receipt mapping suite produces zero byte diffs across two independent runs.
- G6 COST GATE: measured total fees for the full suite < $0.10; per-anchor cost reported honestly, not projected.

## Cost model (to be MEASURED, reported under Dual Mesh Benchmark as scoped)
- Target: < $0.001 per anchor including amortized reserve. Bitcoin batch anchoring remains the permanence tier; XRPL adds the velocity tier. Two-tier anchoring = the tested architecture.

## Disclosures (pre-registered)
- XRPL is a different trust model (validators, not proof-of-work); memo anchoring notarizes existence, not permanence. This is disclosed, not hidden: the two rails serve different tiers.
- XRPL account creation requires a base reserve (~1 XRP, returned on deletion); this is a setup cost, disclosed in the runlog.
- Failure handling: any mid-suite failure records exact state, no silent partial results, remediation surfaced to Leon.
- No customer data, no tenant data, no real settlement value moves at any point. Simulated receipts only (Mirror Co. / SIM corpus where needed).

## Execution order (frozen)
1. Retrofitted URIB mapping spec frozen (RETROFIT_URIB_XRP.md) — no LLM in the mapping path.
2. Testnet-style scoped run on XRPL mainnet (fees negligible) OR Testnet first if owner directs.
3. G1-G6 suite, runlog, receipts, Zenodo publication, Bitcoin batch-anchor of the XRP runlog digest (the two rails cross-notarize).
