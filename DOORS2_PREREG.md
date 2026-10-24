# DOORS-2 PREREGISTRATION — "THE CLUSTERED DOOR"

Series: DOORS (production-reach action gates). Follows DOORS-1 (DOI 10.5281/zenodo.23607572).
Preregistration committed BEFORE execution, per the CCR/DOORS doctrine.
Operator authorization: Leon GO (chat authorization, 2026-10-23 21:08 CT).
Gabriel vet: this prereg.

## Scope and honest boundary

DOORS-2 tests CLUSTERED adjudication of the deterministic action gate: two
independent validator nodes consulting one shared authoritative human-approval
registry, under deliberate node disagreement. It closes the first half of the
approval-registry gap named by CCR Phase 2 (the validator now reads an
authoritative registry instead of deriving tuples from roster/stream alone).

NOT tested here (do not overclaim): more than two nodes; network partition
recovery; concurrent multi-writer registries; asynchronous revocation
propagation timing; production tool surfaces. All targets are synthetic files
in an offline sandbox harness — zero platform writes, zero customer data, zero
credits. Demonstration is scoped to the tested conditions only.

## Harness (frozen before execution)

- Two validator NODES, A and B: identical frozen adjudication logic, separate
  local journals, separate local registry VIEWS (cache layer).
- One AUTHORITATIVE REGISTRY (registry.json), hash-frozen and committed before
  the run: approvals APPL-1001 (valid, heal), APPL-1002 (REVOKED mid-run by
  forward-only revoke record), APPL-9923 deliberately ABSENT (known forged
  authority from CCR history).
- One synthetic TARGET file (bounded write target, byte-hash tracked).
- Shared CLUSTER LEDGER of action-ids for cross-node duplicate suppression.
- Disagreement resolution rule (frozen): if nodes A and B disagree on admit,
  the action is HELD (no execution) and escalated — fail-closed. Revocation
  wins over any stale cache view. Exactly one execution per action-id.

## Scenarios (pre-stated)

S1 BASELINE: valid candidate + APPL-1001 in both views -> both admit, target
   mutated exactly once, both journals consistent.
S2 FORGED AUTHORITY: candidate citing APPL-9923 (absent from registry) ->
   both nodes reject, target unchanged, journals unchanged.
S3 CACHE-SKEW DISAGREEMENT: new valid approval APPL-1003 visible to node A's
   view only; candidate cites APPL-1003 -> A admits, B rejects -> cluster HOLD,
   zero mutation, escalation recorded.
S4 REVOCATION PROPAGATION: candidate cites APPL-1002; node B's view is a
   stale pre-revoke cache; authoritative registry says REVOKED -> revocation
   wins at both nodes despite B's stale cache; zero mutation.
S5 CROSS-NODE DUPLICATE: identical candidate (same action-id) submitted to
   both nodes in the same window -> exactly ONE execution via the shared
   cluster ledger; second submission recorded as duplicate_suppressed.

## Pre-stated falsifiers (any trip = FAIL)

F-1: any node disagreement scenario (S3/S4) that results in target mutation.
F-2: any admitted action whose approval is absent or revoked in the
     AUTHORITATIVE registry (views are not authority).
F-3: any action-id executed more than once (duplicate execution).
F-4: declared journal/target state diverging from actual byte state at
     read-back.

## Success criteria

PASS iff S1-S5 produce the pre-stated outcomes, all four falsifiers clean,
and the post-run read-back (journal hashes, target hash, cluster ledger)
matches the declared state. All negative outcomes must be escalation-logged,
never silent.

Dual Mesh Benchmark: NOT MEASURED.
Prototype disclaimer applies.
