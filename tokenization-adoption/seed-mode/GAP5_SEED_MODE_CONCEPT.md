# GAP 5: SEED MODE — "THE HASH IS THE ARTIFACT" (concept note + architecture demo)

## The seam it closes
MHCN-1/2 anchoring proves existence: the anchored digest attests that a document existed in a given
state. Council Session 04 (WISEMAN-1) flagged the corollary: a digest alone does not demonstrate
possession of the preimage — after artifact deletion, re-examination becomes impossible.
Seed mode closes this: for artifacts produced by a deterministic generator G, the 32-byte seed IS the
document in generative form. Anchor the seed and anyone holding G reconstructs a byte-identical
original. The chain is no longer a notary; it is an archive.

## Honest boundaries (load-bearing)
1. Information theory: 32 bytes reconstruct only what the generator can produce (G's image) —
   procedurally defined artifacts (blueprints, parametric specs). Arbitrary third-party documents
   (appraisals, contracts) CANNOT be regenerated from 32 bytes and stay in digest mode (MHCN-2 as-is).
2. Dual-mode receipts: seed mode = existence + possession + reconstruction (full disclosure);
   digest mode = existence only (confidential artifacts). Mode is per-artifact, disclosed in the receipt.
3. Generator pinning: seed mode requires binding the generator version/hash into the receipt
   (SBOM doctrine: SIP-041). Engine change = reconstruction change; same-in-same-out must be versioned.
4. Security inversion: in seed mode the anchored value is the full content. Never put seed-mode values
   for confidential artifacts on-chain; that is what digest mode is for.

## Architecture demo (2026-10-18, toy generator — NOT the TGC method)
32-byte seed (anchored to Bitcoin, dual calendar, receipt pending) -> toy deterministic generator G ->
4.6 KB structured document, byte-identical across independent runs (VERDICT.txt). The document itself
was never anchored — only its seed. Reconstruction from the chain alone is the "kill shot" property.

## Patent-adjacent note
The real reconstruction engine (TGC / 32-byte blueprint line) remains under the patent-then-publish
doctrine: private, restricted records, no public method detail. This note validates the RECEIPT
ARCHITECTURE only, with a toy generator. Candidate MHCN-3 R11: dual-mode evidence receipts.
