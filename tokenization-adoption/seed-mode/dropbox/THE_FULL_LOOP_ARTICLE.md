# End-to-End Tokenization with Receipts and Hashes: A Complete, Self-Anchored Loop Demonstration

**Leon Calvin Long, II — SquirlOS Technologies LLC**
October 18, 2026

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All battery payloads are synthetic. Nothing herein is investment, legal, or financial advice.

---

## Abstract

On October 18, 2026, SquirlOS Technologies LLC completed a full-loop demonstration of hash-based asset tokenization on the Bitcoin mainnet: a patent artifact was reduced to a 32-byte seed, sealed permanently into the blockchain, reconstructed byte-identically in a keyless browser viewer, transferred between two independent wallets and back — with the asset itself never moving — and every step of the process carried a downloadable, independently verifiable receipt. This article documents that loop. In the final act, the article's own SHA-256 digest was anchored in a Bitcoin mainnet transaction: the artifact that documents the system is itself notarized by the system. The transaction identifier and block height are recorded in the Zenodo record metadata and in the company's append-only public ledger. We also report the honest cost economics of per-transaction anchoring, the batching architecture that scales it, and the open question of secondary rails.

## 1. The Thesis: The Hash Is the Asset

Classical tokenization binds an asset to a transferable on-chain instrument: the token moves, and moving it costs gas. This demonstration inverts that model:

1. **The asset is stationary.** The artifact — Patent Genesis Series No. 1 (USPTO application 19/693,343) — is reduced to a 32-byte seed. The seed is sealed once into an OP_RETURN output on Bitcoin mainnet. From that moment, anyone with the hash can reconstruct the original artifact byte-for-byte in a browser, at any time, with no account, no Python, and no trust in the author. The asset never moves again.

2. **Ownership is custody of the satoshis.** Control of the funding wallet is the transferable layer. A custody transfer is an ordinary Bitcoin transaction that moves the writer balance to a new wallet — and, in this design, re-anchors the asset hash in the same transaction. Every transfer of ownership re-seals what is owned, in the very transaction that moves it.

3. **Every step carries a receipt.** Each on-chain act is journalized with a downloadable receipt: transaction id, block height, fee, payload digest, verification links, and a prototype disclaimer. The receipts layer is itself anchored, versioned in git, and published under citable DOIs.

The corresponding patent-track filing (THREADZERO, application 64/081,490, gas-free off-chain asset transfer and MSSM-based issuance) is pending; the priority relationship between the applications remains subject to confirmation by counsel and is not asserted here.

## 2. The Demonstrated Loop (October 18, 2026)

All items below are independently verifiable today, without contacting the authors.

| Step | Act | Evidence |
|---|---|---|
| 1 | Patent artifact reduced to 32-byte seed; deterministic reconstruction verified byte-identically | DOI 10.5281/zenodo.23447609 |
| 2 | Seed sealed on Bitcoin mainnet, block 972023, tx `97d8cd38ecb37602aaa93363f4591c5c357721ff0cee9a80455fbc548a8a5b89` | DOI 10.5281/zenodo.23455768 |
| 3 | IP portfolio ledger (10 patents pending + 5 SBIR tracks) anchored by digest, block 972026, tx `549bcf47e8a15e054e0c944d435d37f3d228de9f7191df27856cda42ffb90118` | Ledger 0194, hash `67c36f18...` |
| 4 | Keyless in-browser viewer: paste the hash, watch the artifact rebuild | https://deterministic-code-dsos.base44.app/genesis-viewer |
| 5 | Ownership transfer hop 1 (A to B): writer wallet `bc1qf4zs...` to fresh wallet B `bc1q90jca...`, 94,827 sats, asset hash re-anchored, tx `1f550498f56881e47233874d8ea5af0b860acc8670ddfc684d0a4ade94d5093e` | Ledger 0196 |
| 6 | Ownership transfer hop 2 (B to A): full balance returned, hash re-anchored again, tx `c850f1d40bb3069523f0469d88d5d6258d9bd79193d03dee76cd55fb13d11ec8` | Ledger 0196 |
| 7 | Complete public receipts corpus: 194 ledger entries, 93 DOI records, Bitcoin anchor registry | DOI 10.5281/zenodo.23455954 (concept 10.5281/zenodo.23455937) |
| 8 | This article: digest anchored on Bitcoin mainnet; txid and block recorded in the Zenodo record metadata | This record |

The round trip of steps 5-6 is the core result. The asset stayed stationary throughout — reconstructible at every instant — while ownership tracked control of the custody satoshis across two independent wallets and back. The demonstration's total on-chain cost was 1,600 sats (approximately $1.30 at the time of broadcast).

## 3. The Receipts Layer

Verification is three-tiered, requiring zero trust in the authors:

1. **DOI tier**: every claim above resolves to a public, citable Zenodo record with downloadable files.
2. **Bitcoin tier**: anchored states are sealed in OP_RETURN outputs. Re-hash any anchored artifact and compare; the blockchain is the notary.
3. **Git tier**: the full commit history is public at github.com/LLong2026/four-horsemen, append-only since September 7, 2026, with an auditable authoring-correction trail (corrections are forward-only and disclosed, never silent).

A disclosed example: during custody tooling development, three broadcast attempts were rejected by mempool policy (a non-canonical DER signature and a malformed BIP143 scriptCode) before a clean broadcast succeeded. The defects and their resolution are recorded in the ledger rather than erased. No funds moved on a malformed transaction; standard Bitcoin script policy caught every defect. This is the receipt-first doctrine operating as designed: errors are disclosed, not hidden.

## 4. Honest Cost Economics

Per-transaction anchoring on Bitcoin is not free. The demonstration transactions cost roughly $0.30-$0.65 each at prevailing fee rates. At that unit cost, per-asset anchoring does not scale: one thousand individually-anchored assets would cost on the order of hundreds of dollars at today's rates, and fee volatility can move that number either way.

The architecture answers this with **batch anchoring**, already implemented in the company's SIP-034-041 notarization stack (OpenTimestamps-compatible): thousands of receipts are hashed into a single Merkle tree, and only the root is committed to one Bitcoin transaction. Cost per anchored receipt becomes fee divided by batch size — fractions of a cent at scale. Permanence is preserved at the batch level; individual proofs branch from the on-chain root and remain independently verifiable.

The correct reading of the "gas-free" claim is therefore: **the asset never moves, and the fee layer is amortized.** Transfer of custody between parties remains an ordinary transaction with an ordinary fee, and per-item timestamping at very high volume is a cost question the company continues to evaluate, including secondary rails (e.g., the XRP Ledger's memo-field anchoring at near-zero per-transaction cost) for high-frequency records, with Bitcoin retained as the permanence layer. This open cost question is disclosed rather than hidden; it is the next engineering problem, not a settled result.

## 5. Adoption Path

Consistent with the company's licensing posture, the demonstration stack is published in three tiers: (1) the viewer is free to all — any hash, any browser, zero trust; (2) examiner-level verification tooling is published for independent re-implementation and adversarial review; (3) the production generation layer (the TGC engine) is a licensed commercial product and is not distributed in source form in this corpus.

## 6. Dual Mesh Benchmark

Status: **MEASURED (scoped)** — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.

## 7. Limitations and Disclosures

- This is a prototype demonstration on live Bitcoin mainnet using the authors' own funds; the total experimental postage for the October 18 session was under $3.
- Patent statuses: USPTO application 19/693,343 is pending; THREADZERO application 64/081,490 is pending; no patent claim is granted or asserted by this article.
- Bitcoin fee rates are volatile; the cost figures above are point-in-time observations, not projections.
- The OpenTimestamps and OP_RETURN anchoring layer notarizes proof of existence and integrity; it does not and cannot notarize semantic claims made inside a document.
- No client, customer, or tenant data appears in any artifact of this demonstration. All payloads are the authors' own company records or synthetic test material.
- Publication of this article followed the company's two-key protocol: drafted and vetted by the system (Gabriel), published on the owner's explicit authorization (recorded as owner chat authorization, 2026-10-18).

## 8. Closing the Loop

This article's own SHA-256 digest is sealed in a Bitcoin mainnet OP_RETURN. The transaction identifier and block height are recorded in the Zenodo record metadata for this article and in the public ledger entry that accompanies it. The article about receipts is itself a receipt — the artifact of all artifacts, notarized by the system it documents.

*Correspondence: SquirlOS Technologies LLC. Public record: zenodo.org/communities/dcai (DCAI) — science.squirlos-technologies.com (DSOS Science).*
