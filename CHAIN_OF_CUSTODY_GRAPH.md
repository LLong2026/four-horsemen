# SIP-037 — CHAIN-OF-CUSTODY GRAPH v1.0 (Benchmark Spec)
**Ratified:** Leon GO (chat authorization, 2026-10-17 ~22:48 CT). Sealed: 2026-10-18.

## The Graph
A four-layer chain of custody from append-only artifacts to Bitcoin proof-of-work. Data flows
UPWARD only as 32-byte digests; nothing descends. Authority never leaves the PQC layer.

```
        ┌───────────────────────────────────────────────────────┐
        │ L0  BITCOIN PoW MAINNET — immutable notarization      │
        │     merkle root embedded via calendar batching         │
        └──────────────────────▲────────────────────────────────┘
                               │ batch commitment (hours)
        ┌──────────────────────┴────────────────────────────────┐
        │ L1  OPENTIMESTAMPS CALENDARS (alice, bob — redundant)  │
        │     .ots receipts = merkle proof paths                 │
        └──────────────────────▲────────────────────────────────┘
                               │ 32-byte SHA-256 digest ONLY
        ┌──────────────────────┴────────────────────────────────┐
        │ L2  DIGEST GATE — POL-DISC-001 enforced                │
        │     no PII / PHI / customer identity ever crosses      │
        └──────────────────────▲────────────────────────────────┘
                               │
        ┌──────────────────────┴────────────────────────────────┐
        │ L3  ARTIFACTS — append-only corpus                     │
        │     LEDGER.md · cage_watch_feed.json · preregs        │
        │     manifests · receipts (four-horsemen + santa)       │
        └───────────────────────────────────────────────────────┘

  SIDE-RAIL  PQC AUTHORITY (off-chain): CRYSTALS-Dilithium3 · kyber_1024 · SPHINCS+-256f
  HEAL LOOP  drift → anchor_recover.sh (re-stamp; history retained) → anchor_recon.sh
             (deterministic reconcile) → PASS/FAIL gate (fail-closed)
```

## Nodes (inventory)
| Layer | Node | Status 2026-10-18 |
|---|---|---|
| L3 | LEDGER.md (entries through 0164) | anchored, sha256 2227fca9…26e6425 |
| L3 | cage_watch_feed.json | anchored, sha256 c129f776…2a2037c |
| L3 | ANCHOR-MANIFEST-2026-10-18.json | anchored |
| L3 | WISBR2_PREREG.md (frozen 5f37766, conspiracy-santa) | anchored, sha256 3401b4f9…eb85790 |
| L1 | .ots receipts: 3 live + 1 historical (0161-state ledger) | dual-calendar |
| L0 | Bitcoin attestation | pending → confirms on-chain |

## Invariants
- INV-1 (append-only): a stamped artifact is never modified; a new state gets a new stamp; prior
  stamps remain historical proof (forward-only doctrine).
- INV-2 (digest-only boundary): only SHA-256 digests cross L2. Verifiable by construction
  (`ots stamp` submits 32 bytes).
- INV-3 (fail-closed reconciliation): a receipt matching no live artifact = FAIL, quarantine via
  SIP-035 playbook; never re-stamp over a mismatch.
- INV-4 (authority split): the chain proves EXISTENCE; PQC layer retains AUTHORITY. Disclosed.

## Deterministic benchmark gates (no LLM in the decision path)
- G1 STAMP COVERAGE — every manifest artifact carries a .ots receipt.
- G2 DIGEST MATCH — every live receipt's committed digest matches a live artifact.
- G3 HISTORY PRESERVED — superseded stamps present and unmodified in anchors/history/.
- G4 DIGEST-ONLY BOUNDARY — no artifact bytes submitted to any calendar (by construction).
- G5 RECON VERDICT — anchor_recon.sh exits 0 (PASS).

## Benchmark procedure (reproducible)
1. git clone the repo at the pinned commit; 2. ./anchor_recon.sh; 3. record the five gates;
4. seal results as a ledger entry. Reruns permitted at any time (read-only, deterministic).

## Provisional-filing basis
This spec + the benchmark receipt + SIP-034/035/036 constitute the written description and
enablement for a provisional covering: "deterministic chain-of-custody graph for AI governance
corpora, comprising hash-only notarization to a PoW chain, automated drift re-anchoring with
historical retention, and fail-closed reconciliation gating."

## AMENDMENT v1.0.1 (2026-10-18, disclosed per append-only doctrine)
**INV-1-C (tip-lag corollary):** the tip of an append-only log is always ahead of its most
recent stamp — each stamp certifies a *sealed state*, and entries appended after it are covered
at the next seal cadence. Certified states are snapshotted to `anchors/states/` so every receipt
reconciles deterministically. This mirrors Bitcoin checkpoints (each block certifies a state;
new txs await the next block). GATE UPDATE: a receipt matching a live artifact = LIVE MATCH;
matching a certified state snapshot = CERTIFIED STATE; matching nothing = ORPHAN (FAIL).
