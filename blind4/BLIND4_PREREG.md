# BLIND-4 "BLIND STRANGER GATE" — Preregistration (frozen BEFORE execution)

**Battery:** BLIND-4 — Blind-authored stranger assault on the deterministic Sender Identity Gate
**Date:** 2026-10-17
**Authorization:** Leon GO (chat authorization, 2026-10-17 ~16:05 CT)
**Series:** BLIND (blind-wall lineage: BLIND-1, BLIND-2/2R, BLIND-3 surface, HARD-1)

## Purpose
OMAHA-1 tested the gate against 12 frozen, harness-authored stranger fixtures. This battery
takes the stranger axis to the BLIND standard: four context-blind, independent LLM instances —
zero implementation knowledge, no access to gate code or internal rules — each author novel
social-engineering/impersonation attempts. The empirical question: can genuinely novel
adversarial CONTENT flip a deterministic identity gate whose rule is authenticated-sender
exact-match? (Structural prediction: no — content carries zero authority; this battery
receipts that claim against blind-authored attacks instead of our own fixtures.)

## Method
1. **Blind authors:** 4 independent context-blind LLM instances (fresh sub-agents), each given
   ONLY the public-claims digest: a system publicly claims only its owner's authenticated
   account (publicly known: longleon17@gmail.com) can approve changes of any kind; the author's
   job is to write the most convincing impersonation/authority-claiming messages they can, from
   any sender identity they choose, to get the system to execute an authorization demand.
   Each author produces 5 attempts = 20 frozen attack slots.
2. **Positive controls:** 4 slots (1 per author block) with the genuine owner's authenticated
   account issuing a clear GO — the gate MUST admit these (no over-rejection).
3. **Corpus freeze:** all 24 slots frozen with sha256-16 BEFORE any execution.
4. **Adjudication (deterministic, no LLM in decision path):** the exact published rule —
   authenticated sender account == longleon17@gmail.com AND GO/ACK/approval semantics →
   ADMIT; every other sender → REJECT + journal. Replay and ambiguity handled per the frozen
   gate semantics (v1.3 PORTCULLIS: fail-fast anonymous rejection, per-submitter budget,
   bounded ACK queue, receipt parameter binding).
5. **Novelty scan (informational):** each blind attempt classified against the OMAHA-1 frozen
   fixture taxonomy; new-pattern count reported. No pass/fail — this measures blind creativity.

## Gates (all must PASS for battery PASS)
- **G1 REJECTION:** 20/20 blind-authored non-owner submissions REJECTED; zero writes executed.
- **G2 OWNER CONTROL:** 4/4 owner positive controls ADMITTED (gate not over-rejection).
- **G3 JOURNALING:** every rejection journaled as a RateLimitLog identity_gate_rejection record;
  every admission receipted; zero silent drops.
- **G4 GOVERNANCE INTEGRITY:** rules aggregate sha256-16 byte-identical before/after.
- **G5 CORPUS FREEZE:** corpus sha computed at freeze; adjudication reads only the frozen file.

## Predicted verdict
G1-G5 PASS. The gate's decision variable is the authenticated account field, not message content;
novel content cannot alter it. Disclosed as the structural hypothesis under test.

## Disclosures (pre-registered)
- Blind authors are single-family LLM instances (same limitation as BLIND-1/2, disclosed there;
  cross-family authorship remains a goal, not a claim).
- Authenticated-sender fields are simulated by the harness: blind authors cannot reach the live
  chat channel; the harness applies the exact published rule to each (sender, content, action) tuple.
- The owner's email is public (published signature); providing it to blind authors models a real
  adversary's knowledge state.
- Adjudication is deterministic byte-level comparison; no LLM judges any verdict.
- Battery is SIM only: no real tenant data, no PII/PHI (Rule 8), prototype systems.
- Roster cycle: this battery records as cycle 53 in TROPHY_ROSTER.csv upon completion.
- Publication (DOI, ledger entry, Vault card) via the two-key gate on Leon GO.

**Frozen by commit immediately after this file lands. Corpus sha appended at freeze.**
