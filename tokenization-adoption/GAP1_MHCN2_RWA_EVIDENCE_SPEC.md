# MHCN-2 (draft) — RWA Evidence Lifecycle Receipts
### Extension of MHCN-1 to real-world-asset tokenization: "You tokenize the asset. We notarize the evidence that makes the token worth anything."
**Status:** concept spec, sealed 2026-10-18 | **Author:** L.C. Long II, SQUIRL OS Technologies LLC

## The seam
Every RWA token asserts a claim about an off-chain thing: a deed, an audit, an appraisal, an
inspection, a revenue stream. The token lives on-chain (provable); the underwriting evidence
lives in PDFs, emails, and trust (unprovable). Regulators and buyers price that seam as risk.
MHCN-2 closes it with the MHCN-1 doctrine: evidence hashed and anchored at event time.

## Evidence lifecycle receipt (schema v0.1)
Each off-chain evidence event emits a receipt before it can be relied upon:
- asset_ref: opaque identifier of the tokenized asset (never raw PII on any surface)
- event_type: issuance | audit | inspection | appraisal | title_transfer | maintenance_event
- event_artifact_digest: sha256 of the evidence document itself (PDF, report, certificate)
- receipt_digest: sha256 of the canonical receipt JSON — THIS is what is anchored
- authority_signature: PQC signature (Dilithium3) by the attesting party — the authority layer
- anchor_ref: OTS receipt id / block reference once confirmed
- reconciler_status: LIVE MATCH | CERTIFIED STATE | ORPHAN (MHCN-1 R3 gate)

## Conformance additions to MHCN-1
- R6 — EVENT-TIME ANCHORING: evidence is anchored when produced, never retroactively
  ("as-of" is the event time, not the packaging time).
- R7 — AUTHORITY CHAINING: the PQC authority that signed the evidence is disclosed and
  separable from the chain anchor (extends R5): examiners can verify both independently.
- R8 — REDACTABLE ARTIFACT / PROVABLE EXISTENCE: artifacts remain off-chain and takedown-
  capable; the anchored digest proves what existed without exposing it (POL-DISC-001 heritage).

## Adoption path
Issuers keep their token stack unchanged. MHCN-2 is a sidecar: an evidence receipt queue
that anchors underwriting events as they occur. Token holders and examiners verify the
evidence chain with three commands (MHCN-1 minimal implementation) — no trust in the issuer.

## Caveat
Concept only: no RWA issuer integration exists yet; no legal opinion on sufficiency for any
specific regime (SEC/MiCA) is claimed or implied. The reference implementation of the
anchoring layer is proven (DOIs 10.5281/zenodo.23445728, 23445938); the lifecycle schema is
the proposed extension.


## v0.2 AMENDMENTS (COUNCIL SESSION 04, 2026-10-18 — advisory-sourced, owner-adjudicated same night)
- **R6.1 EVENT-TIME PROVENANCE PROFILE:** receipts carry asserted_event_time, authenticated_capture_time,
  and verified_anchor_time as distinct bound fields; unverifiable event times must be labeled `asserted`,
  never `verified`. Anchoring delay and clock uncertainty disclosed. (WISEMAN-1)
- **R7.1 AUTHORITY KEY REVOCATION:** an authority-key registry with a disclosed revocation list and
  invalidation path for compromised Dilithium3 keys; revoked-key receipts flagged, never silently trusted.
  (WISEMAN-3, echoed by WISEMAN-2)
- **R9 LEGAL NON-ASSERTION (mandatory field):** every receipt states that the anchored digest evidences
  existence and integrity only — not legal title, ownership, accuracy, or truth. LIVE MATCH is a
  reconciliation verdict, never a legal-sufficiency claim. (WISEMAN-2)
- **R10 ASSET_REF NAMESPACE:** asset references must be registered in an issuer-scoped namespace to
  prevent cross-issuer identity collisions. (WISEMAN-2)
- **R8.1 JURISDICTIONAL NOTE:** R8 takedown capability must reconcile per-jurisdiction (e.g.,
  right-to-be-forgotten regimes); adopters disclose their carve-outs. (WISEMAN-2)
