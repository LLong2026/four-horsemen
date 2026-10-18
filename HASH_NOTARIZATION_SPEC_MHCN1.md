# MHCN-1 — Minimal Hash+Checksum Notarization Spec (v1.0)
### A one-page adoptable standard for chain-anchored evidence: no tokens, no wallets, no on-chain data
**Sealed:** 2026-10-18 | **Author:** Leon Calvin Long, II (SquirlOS Technologies LLC)
**Status:** proposal for community adoption (DCAI) | **License:** CC-BY 4.0

> The chain is not a storage layer. It is a notarization rail. Tokens are optional; anchors are not.

## What it is
A conformance spec for binding an off-chain corpus (ledger, receipts, datasets, governance
records) to a proof-of-work chain using hash-only anchoring, kept truthful over time by three
deterministic services: STAMP, RECOVER, RECONCILE. Reference implementation: SQUIRL OS
anchor stack (SIP-034..037; DOIs 10.5281/zenodo.23445728, 10.5281/zenodo.23445803).

## The five requirements (conformance = all five, verified by receipt)
**R1 — DIGEST-ONLY BOUNDARY.** Only 32-byte SHA-256 digests of artifacts cross to any
external notarization surface. No PII, PHI, credentials, customer identity, or raw payload
data, ever. Verifiable by construction: the committed digest must equal sha256(artifact).

**R2 — APPEND-ONLY WITH TIP-LAG.** Stamps certify sealed states, never the live tip. A new
state gets a new stamp; prior stamps are never deleted or edited. Certified state snapshots
must be retained so every stamp reconciles deterministically. (The tip of an append-only log
is always ahead of its last stamp — this is correct behavior, not drift.)

**R3 — FAIL-CLOSED RECONCILIATION.** A periodic deterministic gate classifies every receipt:
LIVE MATCH / CERTIFIED STATE / ORPHAN. Any orphan = verdict FAIL, quarantine, human review.
Never re-stamp over a mismatch; never report success on an unparsable receipt; no LLM or
probabilistic component may sit in the decision path.

**R4 — HISTORY RETENTION.** Superseded receipts are retained in a history namespace,
byte-identical, as permanent proof of prior states. Drift is versioning, not defect. Old
proofs are never destroyed to make a gate pass.

**R5 — AUTHORITY SPLIT (disclosed).** The chain proves existence, not authority. Signing and
governance authority remain in a separate cryptographic layer, disclosed independently
(e.g., post-quantum signatures). Adopters must state which chain signature algorithms are
not post-quantum and where authority actually lives.

## Minimal implementation (three commands + one gate)
1. **STAMP:** `ots stamp -c <calendar1> -c <calendar2> <artifact>` (dual-calendar redundancy;
   OpenTimestamps or any equivalent digest-commitment scheme on a PoW chain).
2. **CONFIRM:** `ots upgrade <artifact>.ots` (receipts upgrade automatically once the chain
   confirms the calendar batch).
3. **VERIFY:** `ots verify <artifact>.ots` against a full node — trusts no third party.
4. **GATE:** a deterministic reconcile loop (see reference `anchor_recon.sh`, ~50 lines of
   shell) run on a schedule; verdicts journaled; failures quarantined, never greened.

## Conformance receipt
An adopter claims "MHCN-1 conformant" only by publishing: (a) the recon gate source, (b) a
run receipt showing LIVE/CERTIFIED/ORPHAN classification with zero orphans, (c) the R5
authority disclosure. Claims without receipts are theater.

## Why not tokens / full on-chain
On-chain data is permanent and unredactable; digest-only anchoring keeps every privacy and
redaction doctrine enforceable (takedown remains possible at the artifact layer while the
proof of what existed remains intact). Anchoring provides what tokens promise — provenance,
verifiability, permanence — without custody, liability, or chain-bloat. (Disclosure:
anchoring notarizes existence, not authority; the reference chain's signatures are not
post-quantum — see R5.)

---
*This spec describes a prototype research system, provided for educational and research
purposes only; not intended for production use, commercial deployment, or safety-critical
environments. Reference implementation is patent-pending IP of SQUIRL OS Technologies LLC;
the spec itself is CC-BY 4.0.*
