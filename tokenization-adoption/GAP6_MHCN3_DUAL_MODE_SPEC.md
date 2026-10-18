# GAP 6 / MHCN-3: DUAL-MODE EVIDENCE RECEIPTS — SPEC v0.3 (pilot-ready)

Extends MHCN-2 v0.2 (DOI 10.5281/zenodo.23446655 review, DOI 10.5281/zenodo.23445938 base standard).
Status: pilot-ready spec. Proven by the Genesis Artifact (ledger 0182) and Patent Genesis Series No. 1.

## R11 DUAL-MODE RECEIPTS
Every MHCN-3 receipt carries `mode`:
- `digest` — existence only (MHCN-2 semantics): anchored digest attests an artifact's state at anchor
  time; possession of the preimage is NOT proven (per WISEMAN-1, Council Session 04).
- `seed` — existence + possession + reconstruction: the anchored value IS the artifact in generative
  form; any party holding the pinned generator reconstructs a byte-identical original.
Mode is chosen per artifact, disclosed in the receipt, never implied.

## R12 GENERATOR PINNING (SBOM doctrine, SIP-041)
Seed-mode receipts MUST bind `generator_ref` = sha256(generator) + semantic version. Same-in-same-out
holds only for the pinned generator; a generator change is a receipt invalidation event (ORPHAN).

## R13 DOMAIN HONESTY (information-theoretic boundary)
Seed mode applies ONLY to generator-produced artifacts (the generator's image): blueprints, parametric
specs, procedural works. Arbitrary third-party documents (appraisals, contracts, title records) stay
digest mode. No 32-byte seed regenerates data outside the generator's image — this is a theorem, not an
implementation limit, and it is a selling point: the spec never overclaims.

## R14 SECURITY INVERSION
In seed mode the anchored value IS the full content. Confidential artifacts must NEVER be anchored in
seed mode — that is what digest mode exists for. Seed mode is for works whose disclosure is intended.

## R15 PILOT GATE (requirements to declare pilot-ready)
1. PQC authority-key registry + revocation procedure live (R7.1, Dilithium3).
2. Legal non-assertion language reviewed by counsel (R9).
3. asset_ref namespace registry operational (R10).
4. Generator SBOM pinned per artifact class (R12).
5. Council certification complete (WISBR-1R re-run PASS).
6. One pilot asset class + one consenting issuer, digest-mode receipts first; seed-mode for
   issuer-produced parametric artifacts only.
7. Anchor key hygiene: authority signing (PQC key) is SEPARATE from anchoring (OpenTimestamps
   calendars; no wallet required). Optional sovereign self-anchoring (direct OP_RETURN) is a
   separate, funded-wallet path — not required for pilot.

## Receipt schema v0.3 additions
`mode` (digest | seed), `generator_ref` (required iff mode=seed), `seed_ref` (sha256 of the anchored
seed, iff mode=seed), `reconstruction_note` (human statement of what reconstruction proves).
