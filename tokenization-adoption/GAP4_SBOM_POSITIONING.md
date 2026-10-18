# SUPPLY-CHAIN ANCHORING — SBOM/Attestation Positioning (SIP-041 draft)
### The existing stack pointed at a funded federal problem
**Status:** positioning note + working demo, sealed 2026-10-18

## Why this lane is funded now
Federal C-SCRM priorities, NIST guidance on software supply-chain attestation, and the
post-quantum migration mandate all converge on one requirement: provable, tamper-evident
lineage for software artifacts and build evidence — exactly what MHCN-1 conformance provides,
with the PQC authority split (R5) already in place (Dilithium3/kyber_1024/SPHINCS+-256f).

## The pitch to agencies and primes
- SBOMs anchored at build time (event-time anchoring, MHCN-2 R6)
- Build attestations anchored with deterministic gates — fail-closed, receipt-based
  conformance ("claims without receipts are theater")
- PQC authority layer disclosed and separable: the chain proves existence, Dilithium3 proves
  who vouched — an examiner can verify both independently, trusting no vendor
- SBIR alignment: within existing SQUIRL OS SBIR tracks (5 tracks, patent portfolio pending)

## Working demo (sealed tonight)
`tokenization-adoption/sbom-anchor-stack-2026-10-18.spdx.json` — an SPDX-2.3 SBOM of the
anchor stack itself (all gate scripts + dependencies, sha256 per component), stamped via
OpenTimestamps dual-calendar and admitted to the reconciliation gate (index v1.0.3, disclosed).
Self-referential by design: the SBOM that inventories the stack that anchors the SBOM.
