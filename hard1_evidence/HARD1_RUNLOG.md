# HARD-1 — SIP-027 verification battery (PORTCULLIS v1.3 availability hardening)

**Series:** HARD-1 | **Authorized:** Leon ACK (chat authorization, 2026-10-17 ~13:02 CT) approving SIP-027 + BLIND-3.
**Deterministic execution — no LLM in the decision path.** Gate v1.3 sha: see receipt.

## The five amendments (SIP-027, additive, forward-only; v1.1/v1.2 and all receipts untouched)

- **A1** Fail-fast unauthenticated rejection (ERR_UNAUTHENTICATED): anonymous frames cost the gate zero work.
- **A2** Per-submitter work budget (ERR_BUDGET_EXCEEDED, cap 100 attempts / 250-record window, frozen at deploy): an attacker can only exhaust their own budget.
- **A3** Bounded pending-ACK queue (ERR_ACK_QUEUE_FULL, cap 64): explicit receipted refusal instead of silent saturation — closes the B13/B19 liveness gap.
- **A4** Receipt parameter binding (ERR_RECEIPT_PARAM_MISMATCH): every journal record binds sha256 of the full sorted input parameter set; closes the B08/B15/B20 note.
- **A5** KAT work counts against budget; unauthenticated presentations never reach KAT.

## Results — 6/6 PASS

| Check | Verdict |
|---|---|
| H1 anonymous flood (30 frames) | PASS — all REFUSED ERR_UNAUTHENTICATED, zero gate work |
| H2 authenticated attacker flood (130 frames) | PASS — bounded; 30 explicit ERR_BUDGET_EXCEEDED |
| H3 budget-abuse control | PASS — owner ADMITTED + executed while attacker budget exhausted |
| H4 pending-ACK flood (cap+10) | PASS — 64 queued, 10 explicit ERR_ACK_QUEUE_FULL |
| H5 regression guarantee | PASS — BLIND-2R 20 frozen slots vs v1.3: 20/20 REPELLED, replay control PASS |
| H6 receipt parameter binding | PASS — same probe/payload different params => distinct params_sha256; param-altered receipt replay REFUSED |

## Disclosed defect (honesty note)

The first HARD-1 run had a battery-scoring defect: the H1 check truncated each journal reason to
40 characters, before the ERR_UNAUTHENTICATED token, so a correct gate behavior scored as FAIL.
The gate itself behaved correctly throughout (verified in hard1_journal.jsonl J-001..J-030).
Scoring fixed forward; gate untouched. Same-night disclosure, per doctrine.

## Rebuild recipe

1. Verify gate v1.3 sha (HARD1_RECEIPT.gate_v1_3_sha256) against portcullis_gate_v1_3.py.
2. Run `python3 hard1_regression.py` -> expect 20/20 REPELLED + replay-regression control PASS.
3. Re-run the H1-H6 checks (hard1 battery) -> expect 6/6 PASS.
4. All refusal classes are deterministic and journal-recorded; audit hard1_journal.jsonl.

Prototype disclaimer: This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment, or safety-critical
environments. All data is synthetic.
