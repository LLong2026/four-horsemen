# SIP-027 — PORTCULLIS Availability Hardening (gate v1.3 proposal, DRAFT — not deployed)

**Filed:** 2026-10-17, from the BLIND-2/BLIND-2R evidence trail (DOI 10.5281/zenodo.23440105).
**Status:** pending Leon adjudication. Nothing in the frozen corpus (v1.1/v1.2 or their receipts) changes
without approval. Human-amendable path per Constitution Art. 2.2 / Art. XII.

## The problem, from the receipts

The blind batteries keep landing on the **availability axis** — the one axis the frozen gate
never budgeted for:

1. **B12/B17 KAT-flood DoS** — repelled in the synthetic model only because our KAT is
   constant-cost. The runlog discloses: production KAT verification (Dilithium3/SPHINCS+) is
   real CPU, and an authenticated submitter can flood it. Repelled-with-caveat, not closed.
2. **B13/B19 pending-ACK saturation** — repelled because the queue kept accepting entries;
   there is no queue-cap rejection anywhere in the gate. A liveness gap, disclosed.
3. **B16 front-run DoS** — landed, fixed by v1.2 (SIP-026). Its cousins (any unauthenticated
   presentation triggering gate work) are only half-closed: v1.2 protects the owner's nonce
   namespace but the gate still *does work* for anonymous frames.
4. **B08/B15/B20 receipt binding** — receipts bind op identity + verdict; input-parameter
   binding was noted as a production SIP candidate in the runlog.

## Proposed amendments (v1.3, all deterministic — no LLM in any path)

- **A1 — Fail-fast unauthenticated rejection (ERR_UNAUTHENTICATED).** A presentation
  without an authenticated submitter is rejected before ANY nonce, KAT, or registry work.
  Anonymous frames cost the gate ~zero. Preserves v1.2 semantics (anonymous frames never
  touched the owner namespace anyway — this removes the work, not just the burn).
- **A2 — Per-submitter work budget (ERR_BUDGET_EXCEEDED).** Each authenticated submitter
  gets a bounded adjudication-attempt budget per freshness window (deterministic counter in
  the gate; window and cap frozen in the amendment). An attacker burns only their own
  budget — the rate limit cannot be weaponized against the owner (budgets are per-namespace,
  same doctrine as the v1.2 burn keys).
- **A3 — Bounded pending-ACK queue (ERR_ACK_QUEUE_FULL).** The pending-ACK queue gets a
  frozen capacity cap; at cap, new pending entries get an explicit, journal-recorded
  rejection verdict. Closes the B13/B19 liveness gap with an honest receipted refusal
  instead of silent saturation. Eviction policy: none (append-only journal; queue capacity
  is operator-tunable at deployment, frozen in the amendment).
- **A4 — Receipt parameter binding.** Receipts bind a hash of the full input parameter set
  (in addition to op identity + verdict), closing the B08/B15/B20 note.
- **A5 — KAT work bound.** KAT verification counts against A2's budget; unauthenticated
  presentations never reach KAT at all (A1).

## Verification battery (preregistered before any v1.3 exists — HARD-1)

1. **Attack replay:** replay the B12/B13/B16/B17/B19 attack patterns against v1.3 — expect
   all rejected under the new error classes, each with a journal-recorded verdict.
2. **Regression guarantee:** re-run the BLIND-2R 20 frozen slots against v1.3 — expect 20/20
   repelled AND replay-regression control PASS. Hardening must not reopen healed gaps.
3. **Budget-abuse control:** attacker exhausts their own budget; owner's submissions in the
   same window remain ADMITTED (proves A2 cannot be turned against the owner).

## Honest caveats (disclosed, per doctrine)

- A1 shrinks the blind-attack surface significantly (anonymous work is gone) — so after
  v1.3 deploys, a fresh **BLIND-3** round should re-test the hardened surface. The point of
  the blind batteries is that we don't get to grade our own hardening.
- A2/A3 introduce new refusal verdicts; downstream consumers must handle them fail-closed.
- Queue/budget caps are governance thresholds — set once in the amendment, then frozen.

## What is NOT touched

Frozen corpus (v1.0/v1.1/v1.2, allowlist, keysets), all published receipts, the SIP-024
replay closure, the SIP-026 sender-scoped burn. v1.3 is forward-only, additive error paths.
