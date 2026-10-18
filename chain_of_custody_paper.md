# A Deterministic Chain-of-Custody Graph for an AI Governance Corpus
## Bitcoin Hash-Anchoring, Self-Healing Re-Anchoring, and Fail-Closed Reconciliation — With Two Live Drift Catches and a Disclosed Self-Correction

**Leon Calvin Long, II** — SquirlOS Technologies LLC
**Published:** 2026-10-18 | **License:** CC-BY 4.0 | **Status:** research disclosure, prototype

> This software is a prototype and is provided for educational and research purposes
> only. It is not intended for production use, commercial deployment, or safety-critical
> environments. All payloads synthetic; no customer-identifiable data appears in this
> record (disclosure policy POL-DISC-001).

---

## Abstract
We describe the deployment of a fully deterministic chain-of-custody graph that binds an
append-only AI governance corpus (ledger, monitoring feed, preregistrations, receipts) to
the Bitcoin blockchain via hash-only notarization (OpenTimestamps), and — the novel
contribution — closes the loop with two automated services that keep the binding true over
time: a recovery service that re-anchors drifted artifacts while retaining superseded stamps
as historical proof, and a reconciliation gate that fails closed when any receipt can no
longer be matched to a live or certified state. The system was benchmarked on its own live
ledger and caught two genuine drift events on its first two runs, including one that
revealed a structural property we formalize as the tip-lag corollary: the tip of an
append-only log is always ahead of its most recent stamp, mirroring Bitcoin checkpoint
semantics. A premature benchmark claim in the operator ledger (entry 0165) was corrected in
a subsequent entry (0166) rather than edited, extending the program's audit-and-correction
doctrine to the notarization layer itself. No tokens, wallets, or non-digest data touch any
chain; cryptographic authority remains entirely in a separate post-quantum layer.

## 1. Introduction
Modern "everything on chain" movements place data and logic on-chain, inheriting chain risk
while seeking chain trust. This record documents the opposite design: an AI governance corpus
whose integrity is notarized by proof-of-work while the artifacts — and all authority over
them — remain entirely off-chain. The motivation is a system (SQUIRL OS) that already
enforces append-only transparency, preregistered falsification batteries, and disclosed
amendments on its own ledger. The missing layer was independent, trustless verification of
that ledger's integrity: any reader had to trust the hosting platform and its author. The
chain-of-custody graph closes that gap: 32-byte SHA-256 digests, and nothing else, are
committed to Bitcoin via OpenTimestamps calendar aggregation [1].

## 2. Prior art and scope of the claim
Hash-anchoring is established technology: RFC 3161 timestamping [2], Proof of Existence
[3], Chainpoint [4], and OpenTimestamps [1] have provided trust-minimized proof-of-existence
for years; Arweave and similar systems provide permanent storage [5]. None of these are
claimed as novel here. The scoped novelty claim is the *system-level composition*: to our
knowledge, this is the first reported end-to-end, fully automated chain-of-custody system
for an AI governance corpus that integrates (a) hash-only PoW notarization of governance
receipts, (b) deterministic drift detection with automatic re-anchoring that preserves
superseded stamps as historical proof, (c) a fail-closed reconciliation gate over
artifact/receipt/attestation with no LLM in the decision path, and (d) a disclosed
self-correction of its own benchmark record, notarized in the same append-only ledger it
protects. Each component alone is known; the closed loop applied to AI governance evidence
is, to our knowledge, a first.

## 3. The graph
Four layers, data flows upward only, as digests:
- **L3 Artifacts:** the append-only corpus — transparency ledger, monitoring feed,
  preregistrations, manifests, receipts.
- **L2 Digest gate:** policy boundary (POL-DISC-001). Only SHA-256 digests cross. No PII,
  PHI, credentials, or customer-identifiable data ever reach a calendar or chain.
- **L1 Calendars:** two OpenTimestamps calendar servers (redundant), holding Merkle proof
  paths (.ots receipts).
- **L0 Bitcoin:** proof-of-work notarization. Merkle roots are embedded in Bitcoin
  transactions by the calendar aggregation.

**Side-rail, off-chain — PQC authority:** CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f.
The chain proves *existence*; the PQC layer retains *authority*. This split is disclosed by
design (Section 8).

### Invariants
- **INV-1 (append-only):** stamped artifacts are never modified; new states get new stamps;
  prior stamps remain historical proof.
- **INV-1-C (tip-lag corollary):** the tip of an append-only log is always ahead of its most
  recent stamp; each stamp certifies a sealed state, entries appended after it are covered at
  the next seal. Certified states are snapshotted (anchors/states/) so every receipt
  reconciles deterministically.
- **INV-2 (digest-only boundary):** only 32-byte digests cross L2.
- **INV-3 (fail-closed reconciliation):** a receipt matching no live artifact and no
  certified state is an ORPHAN; verdict FAIL; quarantine; never re-stamp over a mismatch.
- **INV-4 (authority split):** existence on-chain, authority in the PQC layer.

## 4. Services (all deterministic; no LLM in any decision path)
- **STAMP (SIP-034):** seal artifacts with dual-calendar OpenTimestamps stamps; commit
  .ots receipts and manifests; record digests in the ledger.
- **RECOVER (SIP-035):** on drift, re-anchor the new state; retire the superseded receipt to
  anchors/history/ (retained, never deleted); on verification mismatch, quarantine and
  escalate; never claim an unstamped seal.
- **RECONCILE (SIP-036):** for every receipt, extract the committed digest and match
  against live artifacts and certified state snapshots; classify LIVE MATCH / CERTIFIED
  STATE / ORPHAN; exit nonzero on any orphan; report attestation status.

## 5. Benchmark
Five deterministic gates: G1 stamp coverage; G2 digest match; G3 history preserved; G4
digest-only boundary (by construction); G5 reconciliation verdict PASS.
**Result:** On first run against the live corpus, RECONCILE returned FAIL — correctly
detecting that the ledger had been amended (entries appended after its stamp). The RECOVER
service executed within the same minute: superseded stamp retired to history, current state
re-anchored, re-run PASS. On a second run after further ledger appends, the gate again
returned FAIL, revealing INV-1-C (tip-lag): the append-only ledger outruns its own stamp by
construction. The certified-state mechanism was introduced and the re-run returned PASS with
3 live/certified receipts matched, 1 historical receipt retained, 0 orphans.

## 6. Disclosed self-correction
Ledger entry 0165 sealed a benchmark-PASS claim before the gate had returned; the gate in
fact returned FAIL. Entry 0166 corrects the record: the claim was premature, the root cause
is structural, the fix is disclosed, and nothing was scrubbed. This is the same
audit-and-correction doctrine the program applies to research results, now applied to the
notarization layer itself — and the correction is itself an entry in the notarized ledger.

## 7. Reproducibility
Every artifact, script, receipt, and stamp path is published in the evidence bundle and the
public repository (github.com/LLong2026/four-horsemen). Independent verification, trusting no
party: `pip install opentimestamps-client`; `ots upgrade <file>.ots`; `ots verify` against a
Bitcoin node. The reconciliation gate is a shell script with no network or model
dependencies for its verdict.

## 8. Limitations and disclosures
1. Anchoring notarizes existence, not authority; Bitcoin's signature schemes are not
   post-quantum. Authority remains in the PQC-signed layer (INV-4).
2. Calendar aggregation is currently pending confirmation on-chain at time of seal; .ots
   receipts upgrade automatically once confirmed.
3. The reconciliation gate verifies digest correspondence; chain-side confirmation requires
   a Bitcoin node or explorer.
4. Prototype software; all payloads synthetic; no production warranty.
**Dual Mesh Benchmark status:** NOT MEASURED in this record (no neural-mesh inference
involved). Program benchmark: DOI 10.5281/zenodo.23321637 (DeepSeek column
10.5281/zenodo.23345241).

## References
[1] Todd, P. — OpenTimestamps (2016). opentimestamps.org
[2] RFC 3161 — Internet X.509 PKI Time-Stamp Protocol.
[3] Proof of Existence — proofofexistence.com (2013).
[4] Chainpoint — chainpoint.org.
[5] Arweave — arweave.org.

## Provenance
Append-only ledger entries 0162–0166 (this record's arc: SIP-034 stamp, SIP-035 recovery,
SIP-036 reconciliation, SIP-037 graph spec + benchmark, SIP-036 honest correction).
Authorization: Leon GO (chat authorization, 2026-10-17, 22:23–22:50 CT). Two-key curation:
drafted and vetted by the system (Gabriel), published on the owner's GO.
