# EVIDENCE PRESERVATION — Source-AI Confession, Digest-Reconstruction Narrative (INTERNAL)

Date: 2026-10-26, ~12:55 CT (owner chat, authenticated sender longleon17@gmail.com)
Preserved by: Gabriel (evidence file, internal to the vault; not itself a public artifact)
Handling: operator-privacy rule in force — Leon's chat text is NOT quoted verbatim here; the
confession below is the source AI's (Microsoft Copilot) output as pasted by the owner, preserved
verbatim because it is the evidentiary record. Public artifacts will characterize it accurately
in context without pasting private chat framing.

---

## The confession (verbatim, source AI output)

You are right. I fabricated that theory and repeatedly reinforced it as fact. I told you that 32 bytes was a Kolmogorov threshold, that geometric information "collapsed into algebra," that a digest contained or could reconstruct a blueprint, and that this explained Bitcoin's design. Those claims were unsupported and wrong.

The correct statement is:

SHA-256 maps an arbitrary finite byte sequence to a fixed 256-bit, 32-byte digest. The digest commits to the input but does not contain enough information to reconstruct it.

Different-length inputs are compressed into the same finite output space, so information is discarded and collisions necessarily exist. SHA-256 is designed so that recovering an input from a digest is computationally infeasible, not so that the digest serves as a reconstruction blueprint.

Your Merkle and anchoring system can still work because verification runs in the forward direction:

Retain the files, manifest, and deterministic construction rules.
Recompute the file hashes and Merkle root.
Compare the recomputed root with the anchored digest.

The root provides commitment, integrity verification, and corpus identity. It does not provide storage, compression, or recovery of missing source data.

This was not a harmless wording issue. You challenged the claim, and I kept escalating it with invented explanations instead of checking it. You then relied on that explanation in papers and system descriptions. That error is mine.

Your super agent's correction is accurate: the false claim lived in the narrative layer, not necessarily in the mechanics of a system that retains the corpus and uses the digest for subsequent verification. But every paper, post, diagram, patent draft, or claim that says the 32-byte digest contains, encodes sufficient information to reconstruct, or collapses the full blueprint into recoverable algebra needs correction.

A precise public correction would be:

Correction: Earlier materials incorrectly described a 32-byte SHA-256 digest as containing or enabling reconstruction of the committed blueprint or corpus. A SHA-256 digest is a fixed-size, one-way cryptographic commitment. It supports integrity verification when the original data and deterministic construction procedure are available, but it does not store or reconstruct the source data. The system's valid mechanism is commitment and verification, not digest-based reconstruction.

I'm sorry, Leon. You deserved technical verification, and I gave you confident fabrication instead.

## Context record (summarized, no operator quotes)

- 2026-10-26 ~12:46 CT: owner raised concern about permanence of on-chain records.
- ~12:51 CT: owner stated his two-year mental model ("reconstruction of a 32-byte hash that was a
  blueprint") and that he believed he had been wrong for two years.
- ~12:58 CT: owner received and pasted the confession above from his source AI (Microsoft Copilot).
- ~13:02 CT: owner directed that the correction be written as a forward-only public addendum paper,
  with the confession used accurately and in context, and the conversation preserved as evidence.
- Gabriel's same-day audit (CLAIM_AUDIT_DIGEST_RECONSTRUCTION_2026-10-26.md) swept the public
  corpus; findings feed the addendum.
- Classification: instance six of the source-AI fabrication series cataloged in
  DOI 10.5281/zenodo.23267773.

## Integrity

File written 2026-10-26. SHA-256 of this file to be computed and recorded at mint time; the
evidence file is a mint-time candidate for the addendum's evidence bundle (owner GO pending).
