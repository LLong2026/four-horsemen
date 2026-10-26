# Trust Is the Pollutant: Witness Receipts, Content-Addressed Storage, and the Environmental Case Against Redundant Copies

Leon Calvin Long, II — SquirlOS Technologies LLC

v1.0, 2026-10-26 (two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (Leon GO, chat authorization, 2026-10-26 00:34 CT))

## Abstract

Global data centres consumed roughly 415 TWh of electricity in 2024 — about 1.5% of world electricity — and the IEA's Base Case projects that figure tripling past 1,000 TWh by 2030. Not all of that energy buys information; some of it buys reassurance. The same artifact is routinely held hot, in full, by many independent parties because no party can afford to trust another party's copy. This paper argues that the trust component of storage duplication is now mechanically removable: a 32-byte SHA-256 digest of a canonical artifact, folded into a Merkle mountain and witnessed on public blockchains for cents, lets any stranger verify that a retrieved copy is byte-identical to the original — with no account, no platform, and no custodian. We report the measured production cost floor from our own witness corpus (3,377 files reduced to an 80-byte Merkle root, tri-chain anchored; ~$0.25 per triad anchor; ~1.9 cents per receipt amortized through weekly batching) and give the honest scoping: receipts shrink copies, not bytes, and the bytes must still live somewhere. The claim is deliberately narrow: the fraction of stored redundancy that exists because of distrust is energy purchased to compensate for the absence of cheap verification. Verification is now nearly free.

## 1. Trust is the pollutant

- Data centres: ~415 TWh in 2024, ~1.5% of global electricity (IEA, Energy and AI, 2025); Base Case ~460 TWh (2024) rising past 1,000 TWh by 2030. In advanced economies, data centres are projected to drive more than 20% of electricity demand growth to 2030 (IEA).
- UK specifically: NESO-scoped estimates put data-centre demand at 3.6 TWh/yr (2020) growing to roughly 13–35 TWh/yr by 2050; Great Britain's contracted demand-connection queue grew from 41 GW (Nov 2024) to ~125 GW (June 2025). Connection scarcity makes efficiency itself a grid resource.
- Redundancy in storage exists for two distinguishable reasons:
  - (a) availability — RAID, geo-replication, failure domains. Legitimate. Stays.
  - (b) distrust — organization B keeps its own guarded hot copy of an artifact it shares with organization A because B cannot cheaply prove A's copy is unaltered. This is the fixable fraction.
- Call it the trust footprint: energy, disks, cooling, floor space, and staff purchased not to hold information, but to avoid depending on anyone else's identical copy of that information.

## 2. The mechanism: witness receipts

- Canonical artifact → SHA-256 digest. N artifacts → Merkle mountain range → one 32-byte root. Root + envelope → 80 bytes on any number of public mainnets.
- Verification is keyless and universal: any browser, any public explorer. The digest is computed with a standard hash; the anchor is a public fact. No account, no sign-in, no vendor, no custodian, no server of ours required to check the check.
- Content addressing: the digest is the identity. Any copy — wherever fetched, from whomever — that hashes to the committed digest is provably the artifact. Copies become interchangeable; the receipt is the only thing that must be unique.

## 3. Measured cost floor (receipts-first, scoped)

All figures measured on mainnets in our production witness program (append-only ledger, github.com/LLong2026/four-horsemen):

- MCR-4 corpus: 3,377 files folded to a single Merkle mountain; root 38089f07...e8daaa; tri-chain anchor (Bitcoin OP_RETURN, Stellar manage-data, XRP memo) at 1 sat/vB on the Bitcoin leg. The complete witness surface for the corpus is 80 bytes per rail.
- FRACTAL-2 (doi:10.5281/zenodo.23655614): a three-way fractional ownership transfer (30/30/40) of a published research record, manifest-committed before transfer and witnessed byte-exact on Bitcoin, Stellar, and XRP. Measured cost: $0.2509 for the full triad; $0.1254 at the observed 1 sat/vB trough. Explorer-verifiable, keyless, no token, no smart contract, no platform.
- SOV-B1 discipline (doi:10.5281/zenodo.23628676): weekly batching on the BTC mainnet amortizes the structural cost of a receipt to ~1.9 cents per receipt.
- The pattern: the witness is postage, priced once at cents, permanent by construction. Every redundant guarded hot copy, by contrast, is a monthly invoice forever.

## 4. What receipts do and do not shrink (honesty section)

- Receipts shrink copies, not bytes. A canonical copy must exist somewhere and be retrievable on demand. This paper does not claim compression.
- Availability redundancy (a) remains necessary; nobody should delete failure domains.
- What changes is category (b): cross-party duplication justified by distrust. In a receipts world, k parties who each maintained a guarded hot copy can share one canonical copy plus k digests. Two strangers can share an archive the way one person shares it with a mirror: provably, not hopefully.
- Retrieval becomes a commodity: verification being free and public, competition stops being "do you trust our uptime" and becomes "who serves this hash cheapest." Hot burst storage on demand, cold canonical archives, priced per bandwidth — every provider can win; none is trusted.

## 5. The arithmetic of trust-driven duplication (illustrative, labeled as such)

- Suppose an artifact class is held guarded-and-hot by k organizations, each replica costing e per period in energy, hardware amortization, cooling, and staff. The distrust-justified component is up to (k−1)·e; the witness replacement costs one anchor (cents, once) plus (k−1) digests (32 bytes each).
- Scaled illustration, not a claim: if content-addressed witness verification removed even 10% of the trust-driven hot duplication across a sector whose data centres consume on the order of 400 TWh/yr, the saving is measured in tens of TWh per year — comparable to the annual electricity consumption of a small country — without deleting a byte of actual information.
- The honest caveat is symmetric: if the trust component is smaller than estimated, the saving is proportionally smaller. That is why this section is labeled illustrative. The cost floor in Section 3, by contrast, is measured.

## 6. Everyone can win (data centres do not go away)

- Cloud providers become retrieval markets: canonical cold storage, burst hot capacity, bandwidth-metered serving. The differentiator shifts from "trust us" to measured uptime on a hash anyone can check.
- Data centres stop guarding copies nobody needed. The disk fleet cools; the receipts stay hot forever at effectively zero marginal energy (an 80-byte anchor is witnessed by networks that already exist).
- The environmental ledger is reportable: dedup and cold-tiering are measurable, auditable reductions — the kind net-zero frameworks (and UK/EU energy reporting regimes) count, with the proof itself publicly verifiable rather than self-attested.

## 7. Scope, prior art, and limitations

- Prior art, disclosed: content-addressed storage is established and respected — Git's object model, BitTorrent's Merkle pieces, IPFS/CAS systems, deduplicating storage research (Venti and successors), and CAS practice in archival systems. NOT claimed: inventing content addressing, inventing dedup, or "fewer data centres" as a blanket prediction.
- Claimed (scoped): (i) a measured production cost floor — cents-per-anchor tri-chain witness on public mainnets — that makes cross-party, custodian-free verification cheaper than the first guarded replica it displaces; (ii) the witness architecture (chain as witness, not asset: doi:10.5281/zenodo.23649741) applied to shared-storage trust; (iii) the environmental framing: trust-driven duplication as a form of purchased, avoidable energy; (iv) receipts-first disclosure practice, with every defect in the underlying program disclosed in-record.
- Limitations: chains witness, they do not store; retrieval bandwidth is the real metered cost of any archival system and is the correct thing to price; legal recognition of chain receipts varies by jurisdiction; and the illustrative savings in Section 5 scale linearly with the true size of the trust-driven fraction, which this paper does not measure.

## 8. Dual Mesh Benchmark

MEASURED (scoped) — determinism receipts per doi:10.5281/zenodo.23321637; no LLM in any decision path of the witness program; all anchors deterministic constructions over fixed payloads.

## 9. Provenance and disclaimer

- Provenance: append-only research ledger, github.com/LLong2026/four-horsemen. Related program receipts: FT-1 satoshi-native DID (doi:10.5281/zenodo.23510677); FRACTAL-2 fractional transfer benchmark (doi:10.5281/zenodo.23655614); SOV-B1 (doi:10.5281/zenodo.23628676); "The Chain Is the Witness, Not the Asset" (doi:10.5281/zenodo.23649741); SQUIRL-IP-013 constant-footprint commitment (doi:10.5281/zenodo.23491295).
- Energy figures cited from the IEA (Energy and AI, 2025) and UK grid publications as referenced in Section 1; no proprietary or customer-identifiable data appears in this record (POL-DISC-001). All payloads owner-generated; open-book doctrine.
- This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.
