# The Hash Is the Artifact: Dual-Mode Evidence Receipts with Seed-Reconstructed Originals, Notarized on the Bitcoin Blockchain

**Leon Calvin Long, II** (SquirlOS Technologies LLC) — SQUIRL OS Technical Report, 2026-10-18
Author ORCID: 0000-0002-8893-7854

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

## Abstract

Blockchain notarization of documents conventionally proves only *existence*: a 32-byte digest attests that an artifact existed in a given state at a given time, but — as an adversarial review of our own standard observed — a digest alone does not demonstrate possession of its preimage, and once the artifact is deleted it cannot be re-examined. We introduce **seed mode**, an extension of our Merkle-hash chain-of-notarization standard (MHCN) in which the notarized value is not a digest of the artifact but a *generative seed* from which the artifact can be reconstructed byte-identically at any time by any party holding the pinned generator. For artifacts within the generator's image, this collapses the distinction between notarization and archival: the hash is the artifact. We formalize dual-mode receipts (R11), generator pinning (R12), an information-theoretic domain rule (R13), a security inversion rule (R14), and a pilot gate (R15); we demonstrate the architecture with two Bitcoin-anchored originals — a structured document and a 51,560-byte patent-citation artwork — each reconstructed byte-identically from independent runs; and we deploy a public zero-trust examiner station in which any visitor can reconstruct the artifact from its published fingerprint and verify the canonical hash in-browser. We further report a disclosed rendering defect in the first-minted artwork as a case study of preregistration discipline applied to generative artifacts.

## 1. Introduction

The MHCN standard family (MHCN-1, DOI 10.5281/zenodo.23445938; MHCN-2 v0.2, DOI 10.5281/zenodo.23445938 as amended by Council Session 04, DOI 10.5281/zenodo.23446655) anchors evidence for real-world-asset workflows — deeds, appraisals, bond issuance records — on the Bitcoin blockchain via OpenTimestamps (OTS). The design is deliberately digest-only: no artifact content, no personally identifiable information, and no customer-identifiable data ever touch the chain (compliance policy POL-DISC-001). The cost of that conservatism is the preimage gap: a receipt proves that *something* existed, not that the examining party can ever see it again.

This report closes the gap for a defined and honest domain. For artifacts that are *produced by a deterministic generator* — blueprints, parametric specifications, procedural artworks, and, in general, any artifact in the image of a generator G — the artifact can be represented by a 32-byte seed s such that G(s) equals the artifact, byte for byte, on every execution. Anchoring s (or its fingerprint) on the Bitcoin chain then provides not only existence but possession and reconstruction: any party, at any future time, with no permission from anyone, can regenerate the original and verify its identity by hash comparison.

## 2. Architecture

The stack (SIP-034 through SIP-041; DOI 10.5281/zenodo.23446098) is a three-layer deterministic notarization pipeline:

1. **Stamp layer** — SHA-256 fingerprints are submitted to dual OTS calendars (alice/bob.btc.calendar.opentimestamps.org) and embedded in Bitcoin blocks. No tokens, wallets, or crypto-assets are involved.
2. **Recovery layer** — `anchor_recover.sh` re-stamps artifacts that drift (with disclosed reason); `anchor_recon.sh` reconciles live digests against stamps; a tip-lag corollary archives certified historical ledger states so that every stamp remains verifiable after the tip advances.
3. **Examiner layer (SIP-041)** — a zero-trust verification protocol plus, as of this report, a public browser-based examiner station (the Genesis Viewer) described in §4.

Seed mode adds a fourth property: reconstruction. The receipt schema (v0.3) gains `mode` (digest | seed), `generator_ref` (required for seed mode: SHA-256 and semantic version of the pinned generator), `seed_ref` (fingerprint of the anchored seed), and a human-readable `reconstruction_note`.

### 2.1 Rules (MHCN-3, pilot-ready)

- **R11 Dual-mode receipts.** Digest mode proves existence (MHCN-2 semantics). Seed mode proves existence, possession, and reconstruction. Mode is explicit per artifact.
- **R12 Generator pinning.** Seed-mode receipts bind the generator's hash and version (SBOM doctrine). A generator change is a receipt invalidation event, not a silent edit.
- **R13 Domain honesty.** Seed mode applies only to artifacts in the generator's image. No 32-byte seed regenerates data outside that image; this is an information-theoretic theorem, not an implementation limit. Third-party documents (appraisals, contracts, title records) remain in digest mode. The standard never overclaims.
- **R14 Security inversion.** In seed mode the anchored value *is* the full content. Confidential artifacts must never be seed-anchored; disclosure is the feature, and digest mode is the confidentiality boundary.
- **R15 Pilot gate.** PQC authority-key registry (CRYSTALS-Dilithium3) and revocation procedure; counsel review of legal non-assertion language; asset-reference namespace registry; per-artifact-class generator SBOM; council certification; one pilot asset class with a consenting issuer.

## 3. Method

**Deterministic byte stream.** All generators consume a DRBG defined as SHA-256(seed || counter32-BE) blocks, consumed in documented call order. No wall-clock, no randomness source, no environment inputs: the same seed produces identical output bytes on any conforming implementation, forever.

**Reconstruction verification protocol.** For each artifact: (i) generate the artifact from the seed; (ii) regenerate from a cold independent process; (iii) compare SHA-256 digests; (iv) anchor the seed (and, in digest mode, the artifact digest) via OTS; (v) pin the generator reference in the receipt; (vi) publish seed, generator, artifact, and verdict in an open bundle.

**Legal posture (R9).** Receipts prove what existed, when, and who attested. They do not assert legal title, ownership, or truth. This non-assertion is an adoption feature: the evidence rail carries courts' inputs, not their verdicts.

## 4. Results

**4.1 Genesis 0182 (first seed-mode artifact).** A 32-byte seed (fingerprint 4f539b5f0790390ef142b402c409a37d61b681e6a9dc574a7c273aee8d939859) generated an 8,858-byte structured document; two independent runs produced identical SHA-256 digests (e5aa25e98ab36448f9ba61dcd7e430ff613f18be9ddae5acd6cf58fd051e845b). The seed was anchored to Bitcoin; the document was not anchored and is not stored — it exists in the seed and the generator alone.

**4.2 Patent Genesis Series No. 1.** An original 51,560-byte blueprint artwork citing U.S. Patent Application No. 19/693,343 (programmable satoshi tokenization; public citation only) was generated from a 32-byte seed (fingerprint 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c). The artwork and both generator versions are published (DOI 10.5281/zenodo.23447609). Reconstruction determinism held in every run.

**4.3 Disclosed-defect case study.** The first-minted artwork (v1.0, artifact digest 4b4fbf0e...) exhibited a layout defect: title-block text overflow and graphic collisions, identified by the owner at minting. Per the program's append-only doctrine the defect was disclosed in the artwork itself, in the bundle (DEFECT_DISCLOSURE_PGS1.md), and in the public ledger (entry 0184); v1.0 files were retained; a corrected generator (v1.1, canonical artifact digest 3c130d6626fb78956a35dd177a7be2bd34d80be66104d94dee37ce7d5bd2de69) was pinned as the canonical reference. The seed and its Bitcoin anchor were unaffected — demonstrating that R12 pinning cleanly separates generator evolution from artifact identity.

**4.4 Zero-trust examiner station.** A public browser page (the Genesis Viewer, on the Deterministic Coding public site; linked from the Squirl OS Vault Public Links page) implements: (i) a hash-drop input accepting a registry fingerprint or a raw 32-byte seed; (ii) deterministic in-browser reconstruction (a faithful JavaScript port of the pinned generator, same DRBG and derived parameters); (iii) byte-canonical verification — the browser fetches the published canonical artifact, computes SHA-256 locally, and compares against the pinned digest; (iv) anchor and publication links (OTS proof, DOI, public ledger). Verification requires no account, no installation, and no trust in the authors: every claim is checked by computation in the examiner's own browser. Try it: paste the Series No. 1 fingerprint 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c into the hash drop.

## 5. Honest boundaries

1. *Domain (R13):* seed mode cannot reconstruct arbitrary third-party documents; the 32-byte representation is available only for generator-produced artifacts. The standard states this in the receipt itself.
2. *Security (R14):* the seed is the content; seed mode is full disclosure by construction.
3. *Law (R9):* reconstruction proves existence, possession, and byte-parity — not title, ownership, or truth.
4. *Generator availability:* long-term reconstruction requires the pinned generator to remain published (the DOI bundle and public repository provide replication; independent reimplementation from the published algorithm is encouraged and is itself a verification path).

## 6. Dual Mesh Benchmark

**MEASURED (scoped).** This report documents deterministic generators, hashes, and a browser verification station; no neural-mesh inference is involved in any result. Program benchmark: DOI 10.5281/zenodo.23321637 (DeepSeek column: DOI 10.5281/zenodo.23345241). Governance review of the underlying standard: Council Session 04 (DOI 10.5281/zenodo.23446655).

## 7. Conclusions

Dual-mode receipts close the preimage gap for generator-produced artifacts while preserving the conservative digest-only posture for third-party evidence. The three-tier adoption path — public browser reconstruction, examiner-level generator verification, skeptic-level reimplementation — gives every degree of doubt a door. The producing engine (the generative writer) is licensable IP; the reading standard is open by design: control the writer, give away the reader.

## References

- MHCN-1 base standard and evidence stack: DOI 10.5281/zenodo.23445938; DOI 10.5281/zenodo.23446098
- Council Session 04 (adversarial review, MHCN-2 v0.2 amendments): DOI 10.5281/zenodo.23446655
- Patent Genesis Series No. 1 (seed, generators, artifacts, defect disclosure): DOI 10.5281/zenodo.23447609
- Append-only transparency ledger: github.com/LLong2026/four-horsemen (entries 0182–0185)
- OpenTimestamps: opentimestamps.org

## Disclosures

SQUIRL OS RESEARCH DISCLOSURE: AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. All payloads synthetic or owner-authored; no customer-identifiable data appears in this record (POL-DISC-001). U.S. Patent Application No. 19/693,343 is cited by public reference only; no invention method detail is disclosed (patent-then-publish doctrine). Authorization recorded as owner GO (chat authorization, 2026-10-18).
