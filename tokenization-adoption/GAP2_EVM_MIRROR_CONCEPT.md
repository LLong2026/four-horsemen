# EVM MIRROR — Read-Only Root Bridge (concept, SIP-040 draft)
### Making Bitcoin-anchored receipts verifiable by smart contracts, without becoming a token
**Status:** concept architecture, sealed 2026-10-18 | **Author:** L.C. Long II

## The problem
MHCN-1 proofs live on Bitcoin. The tokenization world lives on EVM chains. A smart contract
cannot verify a Bitcoin anchor. Without a bridge, our receipts are invisible to the exact
market that needs them.

## The architecture (no tokens, no custody, no data on-chain)
1. **WATCHER** (deterministic): reads ANCHOR-BLOCK-REGISTRY.json; when a receipt confirms,
   extracts the confirmed Merkle root for that calendar batch.
2. **ROOT REGISTRY CONTRACT** (EVM, read-mostly): a single on-chain mapping
   `batchIndex => merkleRoot` plus a timestamp and the Bitcoin block hash (32 bytes).
   Deployment target: a public EVM chain TBD by owner decision. Contract holds no assets,
   has no upgrade keys beyond the poster, and posts roots only — never digests of payloads,
   never PII (MHCN-1 R1 heritage preserved).
3. **POSTER**: a scheduled, receipted job (MHCN-1 conformance receipts required for each post).
4. **CONSUMER VERIFY**: an on-chain MerkleProof.verify(leaf=digest, proof, root) — any dApp
   can prove a document's digest was anchored by us, trust-minimized, without a Bitcoin node.

## Trust model (disclosed, not hidden)
- The bridge adds ONE new trust seam: the poster. Mitigation: every root post is itself
  anchored (recursive MHCN-1 receipt) and the watcher can cross-verify poster claims against
  the Bitcoin chain; divergence = ORPHAN-class failure, quarantine per R3.
- The EVM chain's own consensus is NOT post-quantum; the PQC authority split (R5) is unchanged
  — EVM mirroring is a READ surface, never an authority surface.

## What deployment requires (owner decisions, NOT taken tonight)
- Choice of chain + a funded signer for gas (a custody decision under the no-wallet doctrine;
  requires Leon's explicit authorization per deployment policy).
- Contract audit before any third-party reliance; prototype disclaimer remains in force.
This document is the sealed architecture; no contract code is deployed as of this seal.
