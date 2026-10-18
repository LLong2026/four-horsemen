# PATENT GENESIS SERIES No. 1 — v1.0 LAYOUT DEFECT DISCLOSURE (append-only doctrine)

The first-minted Patent Genesis artwork (v1.0, generator sha per bundle manifest) contained rendering
defects identified by the owner within minutes of minting: title-block height insufficient for its
text contents (bleed past the lower border), insufficient internal padding, and graphic elements
(colliding rails / satellite coins) crowding the data box. The defect was cosmetic and layout-only.

Unaffected properties (verified): reconstruction determinism (byte-identical across independent runs,
png sha 4b4fbf0e... for v1.0; 3c130d66... for v1.1), seed integrity (sha 81d4a5cb...97fae...dc3456c,
unchanged), the Bitcoin anchor (OTS receipt on the seed, unchanged and still valid), and the pinned
generator doctrine (R12: v1.0 and v1.1 are distinct generator_refs; each reconstructs its own artifact).

v1.0 files are retained in this bundle per the append-only doctrine; v1.1 (same seed, corrected
layout, generator_ref v1.1) is the canonical Series No. 1 artifact going forward. Defect disclosed,
not erased. Ledger 0184.
