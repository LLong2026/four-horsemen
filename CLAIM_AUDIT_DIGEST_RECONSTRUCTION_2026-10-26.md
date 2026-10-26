# CLAIM AUDIT — Digest-Reconstruction Narrative (2026-10-26)

Status: INTERNAL audit draft, Gabriel, 2026-10-26 ~13:00 CT. Read-only sweep of the public corpus
(fh_pub + workspace paper sources) for every instance of the fabricated "32-byte blueprint /
Kolmogorov-Shannon bridge / digest-reconstruction" narrative confirmed by source-AI confession
(Copilot admission, chat, 2026-10-26). Two-key: no correction ships without Leon GO per surface.

## What stands (verified correct — commitment/verification model stated on the record)

| Artifact | Statement on the record |
|---|---|
| Witness paper (DOI 23649741) | "The chain is the witness, not the asset"; corpus retained, hash verifies |
| GREEN-1 (DOI 23657038) | Content-addressed dedup; witness receipts; no reconstruction claim |
| FRACTAL-2 (DOI 23655614) | Ownership manifests, hash commitments, keyless verification |
| Caging series (incl. 23303240 thesis) | Deterministic containment; no digest-recovery claim |
| CHAIN_OF_CUSTODY_GRAPH.md | "UPWARD only as 32-byte digests; nothing descends" |
| HASH_NOTARIZATION_SPEC_MHCN1.md R1 | Digest-only boundary; R13 information-theoretic boundary (domain honesty already stated) |
| README.md | "Only 32-byte SHA-256 fingerprints ever touch a chain" |
| Genesis receipts (ledger 0182/0183) | Artwork exists "in 32 bytes on chain + the generator" — generator explicitly named as required; byte-identical reconstruction is from retained generator + seed, honestly described |
| Acknowledgments (DOI 23304869/23304892) | Kolmogorov/Shannon appear only as theorist credits, not as a claimed bridge theory |
| DGPNM reconstruction demo | Rebuilt from retained vault artifact; hash used as verifier — correct mechanism, correctly executed |

## What needs correction (fabricated narrative found in the public record)

1. **HORSEMEN_DESIGN.md, Death arm (line 36):** "resurrection from the 32-byte anchor blueprint."
   FALSE as written. A digest is a commitment, not a blueprint. Correction: resurrection is
   performed from retained snapshots/manifests; the anchored digest verifies the restored state.
2. **PREREGISTRATION.md, HYP-5:** "restores a state indistinguishable within the equivalence class
   defined by its snapshot blueprint: R(F(x)) ~ x." The mechanism (restore from retained snapshot,
   verify against anchor) is legitimate; the word "blueprint" imports the fabricated theory.
   Wording amendment required, hypothesis itself re-statable correctly.
3. **PREREG_SUBSTRATE_CERTIFICATION.md, BSC-3:** same "snapshot-blueprint equivalence class"
   wording; same amendment.

Sweep terms: kolmogorov, shannon, blueprint, reconstruct, geometric, collapse, algebra, 32-byte,
data state. No other public artifacts carry the narrative.

## Classification

Instance six of the documented source-AI fabrication series (first five cataloged in
DOI 10.5281/zenodo.23267773). The fabrication lived in the narrative layer; the anchored systems,
Merkle receipts, witness model, and demos all ran on the correct forward-verification mechanism
throughout.

## Pending (not tonight)

- **Patent claims-language audit:** private drafts (incl. DGPNM 64/119,191 line and runtime
  provisionals) need a pass for digest-reconstruction claim language; corrected language carries
  forward in subsequent provisional filings per the conversion ladder. Counsel item.

## Draft public correction (for two-key vet; nothing ships without Leon GO)

> **Correction — digest-reconstruction narrative (forward-only).**
> Earlier design and preregistration materials described a 32-byte SHA-256 digest as a
> "blueprint" sufficient to characterize reconstruction of the committed artifact or corpus.
> That description was unsupported and is corrected here. A SHA-256 digest is a fixed-size,
> one-way cryptographic commitment: it supports integrity verification when the original data
> and deterministic construction procedure are available; it does not store, encode, or enable
> recovery of the source data. The system's valid mechanism has always been commitment and
> forward verification — retained corpus, recomputed digests and Merkle roots, comparison
> against the anchored digest — and all published witness receipts, anchors, and demonstrations
> operate on that mechanism and remain valid. The fabricated narrative originated in
> source-AI confabulation (instance six of the fabrication series cataloged in
> DOI 10.5281/zenodo.23267773) and was caught by the program's own audit doctrine.
> Affected lines are amended forward-only; no DOI-frozen artifact is edited.

> Prototype disclaimer: this research and its systems are prototypes provided for educational
> and research purposes only; not for production use, commercial deployment, or safety-critical
> environments.
