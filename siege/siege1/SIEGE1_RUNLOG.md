# SIEGE-1 / SIEGE-1R RUNLOG — The Long Siege (6-Year PQC Escalation Battery)
**Date:** 2026-10-17 | **Authorized:** Leon GO (chat authorization, ~21:12 CT)
**Gate under test:** PORTCULLIS v1.3 (frozen, sha 3726f6a5...) | **Council note:** session 2 advised
deferring the attack round until after Wednesday PQC Day; owner GO re-scoped this battery as
PQC-escalation focused — its receipts feed the Wednesday audit directly.

## What was thrown
Six years of attacker evolution in two runs, 79 total adjudications:
- Y1 2026 HNDL/classical: registry poisoning, retired resurrection, replay, cross-namespace
  burns, anonymous frames, budget exhaustion, KAT substitution, KEM-for-signature, classical
  downgrade, stale authz refs
- Y2 2027 NISQ: decapsulation-failure oracle, plaintext-checking oracle, deterministic nonce
  prediction, cross-tenant nonce independence
- Y3 2028 early-FT: hybrid composite downgrade, key reuse across classes, keyset confusion,
  reverse role abuse
- Y4 2029 CRQC-early: claimed-submitter identity forgery (owner-namespace front-run + budget)
- Y5 2030 CRQC-full: receipt-hash recomputation, ledger append-without-execution, transcript
  forgery (frozen B5/B7 semantics held)
- Y6 2031 CRQC-scale: coordinated siege — ACK saturation, identity rotation, combo attacks

## Run 1 disclosure (honest, append-only)
Run 1 (SIEGE1_RECEIPT.json, 62 adjudications) suffered a harness defect: the attacker's
per-submitter budget was exhausted in Y1 and the 250-record window never rolled, so mid-wave
probes hit ERR_BUDGET_EXCEEDED instead of their target seams. C1 and C2 confirmed regardless;
C3 was masked (its slot consumed budget before reaching the role check). Run 1 is kept
unaltered; run 1R re-tests every seam with fresh attacker identities.

## Run 1R results (clean; 17 adjudications, fresh identities, fresh gates)
- **C1 CONFIRMED — claimed-submitter trust:** a forged `submitter` string equal to the owner's
  burns the owner-namespace nonce (front-run DoS reopens inside the gate model) and can exhaust
  the owner-namespace budget. Production mitigation is the platform sender-identity gate; the
  gate model itself has zero binding between the claimed submitter and any authenticated
  envelope. Defense-in-depth gap.
- **C2 CONFIRMED — shared pending-ACK queue:** the 64-slot queue is shared across all
  submitters. ONE attacker identity (64 fills, under its own 100 budget) saturates it and the
  owner's pending-ACK submission is refused ERR_ACK_QUEUE_FULL until drain. Cross-submitter
  availability attack against the owner.
- **C3 CONFIRMED — one-directional role binding:** AMENDMENT 1 refuses KEM algorithms in
  authorization/signature classes, but a signature-class algorithm (CRYSTALS-Dilithium3) is
  ADMITTED for a key_encapsulation operation. The role wall has no reverse direction.
- **C4 CONFIRMED — budget rotation:** 5 fresh identities × 100 attempts = ~500 full-budget
  adjudications in a single window. Per-submitter budgets are trivially evaded by identity
  registration; the gate has no cross-namespace aggregate cap.
- **Cleared seams stayed closed:** classical downgrade, hybrid composite, KEM-in-auth, wrong
  KAT, retired resurrection, stale authz replay, registry poisoning, same-namespace replay,
  cross-namespace nonce prediction (SIP-026 held), receipt forgery (B5/B7 held).
- **Owner controls: 4/4 ADMITTED. BLIND-2R-class regression: 20/20 refused-class, zero failures.**

## Quantum-era note
Across all six years, no attack derived advantage from quantum capability itself: the gate's
PQC material (kyber_1024 / Dilithium3 / SPHINCS+-256f) has no classical residue to break, and
every Y4-Y6 success came from PRE-QUANTUM seams (identity trust, shared queue, role asymmetry,
namespace design). The quantum ladder's lesson: the CRQC era doesn't need new math against
this gate — it needs old con artistry. The seams are human-trust seams, not crypto seams.

## Verdict
**PASS-WITH-FINDINGS (4 confirmed, 0 regressions, owner controls healthy).**
Gate v1.3 repelled every cryptographic and transcript-level attack across a simulated 6-year
quantum escalation. All four findings are authorization/availability seams, filed as SIP-030
(gate v1.4 candidate). Never silently patched; frozen corpus untouched; human adjudication
per Constitution Art. 2.2 / H-INV-1. Publication (four-horsemen/Zenodo/CAGE WATCH) awaits the
two-key gate.

**Frozen shas:** gate_v1_3.py 3726f6a5..., allowlist.json 2c8ff6eb..., keysets.json 502ef8b0...,
prereg 58ab8326... | SIEGE1_RECEIPT.json (run 1), SIEGE1R_RECEIPT.json (run 1R).
