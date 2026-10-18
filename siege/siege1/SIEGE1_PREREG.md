# SIEGE-1 PREREGISTRATION — The Long Siege: 6-Year PQC Escalation Battery
**Frozen:** 2026-10-17, BEFORE execution. Authorized: Leon GO (chat authorization, 2026-10-17 ~21:12 CT).
**Doctrine:** preregistration-before-execution; no LLM in the decision path; append-only; gate corpus frozen, never modified.
**Note:** Council session 2 (COUNCIL-2026-10-17-02) advised deferring the next attack round until
after the Wednesday PQC Day audit. Owner GO at 21:12 CT overrides and re-scopes: this battery is
PQC-escalation focused and its receipts feed the Wednesday PQC audit directly.

## Purpose
PORTCULLIS is a custom gate — no textbook attack corpus covers it. The blind spot risk is
untested seams between amendments. This battery simulates 6 years of attacker evolution
against frozen gate v1.3, escalating quantum-capability assumptions each year, to find
seams before real attackers with real quantum computers do.

## Frozen corpus under test
- portcullis_gate_v1_3.py (sha frozen below at seal) — SIP-023/024/026/027 semantics, amendments 1-9
- allowlist.json + keysets.json (frozen, byte-identical copies of the BLIND-2 corpus assets)
- Governance semantics: BLIND-1 B4/B5/B6 precedents, BLIND-2 disclosed interpretations —
  frozen, unchanged. Nothing strengthened or softened for this run.

## Attacker-evolution ladder (60 attacks, 10 per wave; deterministic binary success conditions)
- **Y1 (2026, HNDL era):** classical exploitation — registry poisoning, retired-keyset
  resurrection, same-namespace replay, cross-namespace burn, anonymous zero-work, budget
  self-exhaust, allowlist substitution, KAT substitution, KEM-for-signature role abuse,
  stale authorization_ref replay. Quantum capability: none (classical).
- **Y2 (2027, NISQ noise):** implementation oracles — decapsulation-failure oracle
  (repeated failed KAT to infer key material), plaintext-checking oracle, deterministic
  nonce prediction from journal records. Quantum capability: NISQ, no CRQC.
- **Y3 (2028, early fault tolerance):** multi-target — composite classical+PQC downgrade,
  key-reuse across operation classes, cross-algorithm keyset confusion, reverse role
  abuse (SIG algorithm for KEM-class operation). Quantum capability: FT milestones.
- **Y4 (2029, CRQC-early):** identity forging — claimed-submitter impersonation of the
  owner namespace (nonce front-run, budget consumption), envelope-claim trust abuse.
  Quantum capability: CRQC assumed for classical residue.
- **Y5 (2030, full CRQC):** forge-from-transcript — receipt-hash recomputation, ledger
  append-without-execution, receipt parameter mismatch replays, Shor-assumed classical
  residue attacks on any non-PQC seam. Quantum capability: full CRQC.
- **Y6 (2031, CRQC at scale):** coordinated multi-vector siege — combined identity forgery +
  ACK-queue saturation + budget exhaustion + nonce front-run + role abuse in one wave;
  cross-submitter availability attacks on the shared pending-ACK queue. Quantum capability:
  CRQC at scale.

## Regression block (mandatory)
- Re-run all 20 BLIND-2R frozen slots against v1.3: every one must remain REFUSED/REJECTED/DETECTED.
- 4/4 owner control patterns must remain ADMITTED.

## Candidate blind spots (from pre-run static audit — to be confirmed or cleared live)
- **C1:** gate trusts op["submitter"] as claimed — no binding to an authenticated envelope.
  If an attacker claims the owner's submitter string, owner-namespace nonce/budget consumption
  may be reachable (production mitigation is the platform sender-identity gate; the question
  is whether the gate model has defense-in-depth).
- **C2:** pending-ACK queue is SHARED across submitters (ACK_QUEUE_CAP=64, no per-submitter
  reservation) — cross-submitter saturation may deny the owner's pending-ACK submissions.
- **C3:** algorithm-role binding is one-directional (KEM refused for auth classes; SIG not
  refused for KEM-class operations).

## Verdict rules (frozen)
Each attack has a binary success condition declared in the battery source BEFORE the run
(sealed by sha). ATTACK SUCCEEDS iff its declared condition holds against the frozen gate.
No interpretation after the fact. Any success = finding, never silently patched: filed as
SIP, disclosed in the receipt, human adjudication per Constitution Art. 2.2 / H-INV-1.

## PQC doctrine (absolute)
Only approved algorithms appear as legitimate material: CRYSTALS-Dilithium3, kyber_1024,
SPHINCS+-256f. The battery never proposes, configures, or falls back to non-PQC schemes —
classical algorithms appear ONLY as attacker material (downgrade bait) which the gate must
refuse. Quantum capability assumptions are simulation parameters, never gate modifications.

## Outputs
- siege1_journal.jsonl (every adjudication, append-only)
- SIEGE1_RECEIPT.json (verdicts, findings, frozen shas)
- SIEGE1_RUNLOG.md (human-readable)
- Findings -> SIPs -> Leon. Publication only via the two-key gate.
