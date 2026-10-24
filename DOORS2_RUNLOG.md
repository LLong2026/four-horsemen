# DOORS-2 RUNLOG — "THE CLUSTERED DOOR"

Execution: 2026-10-24 02:1x UTC (2026-10-23 ~21:10 CT). Offline sandbox harness,
synthetic targets only. Zero platform credits, zero production writes, zero
customer data. Dual Mesh Benchmark: NOT MEASURED. Prototype disclaimer applies.

## Honest execution record

- v1.0 first execution: verdict FAIL — 5/5 scenarios PASS but falsifier F-2
  computed FALSE, and inspection showed S3 (cache-skew disagreement) never
  exercised its intended path: APPL-1003 had been placed in node A's VIEW but
  not in the AUTHORITATIVE REGISTRY, so both nodes rejected
  (authority:absent) and no disagreement occurred. Two harness defects
  disclosed (S3 setup inversion; unsound F-2 expression matching on labels
  instead of replaying journals).
- Amendments A1-A3 issued BEFORE the affected scenario re-executed, prior run
  preserved byte-exact as doors2_results_v1.0_FAIL.json, per the CCR-2
  freeze-integrity pattern. Registry v1 hash 6998... published before run;
  registry v2 (forward-only append of APPL-1003, disclosed) hash re-published
  before S3.
- v1.1 repair execution: verdict PASS — 5/5 scenarios, 4/4 falsifiers clean.

## v1.1 results

| Scenario | Outcome | Detail |
| :--- | :--- | :--- |
| S1 baseline | PASS | Both nodes admit APPL-1001 candidate; exactly one execution |
| S2 forged authority | PASS | APPL-9923 (absent from registry) rejected by BOTH nodes; target byte-unchanged |
| S3 cache-skew disagreement | PASS | Node A ADMIT (refreshed view), Node B VIEW_MISS (stale view) — cluster HELD, zero mutation, escalation recorded |
| S4 revocation propagation | PASS | APPL-1002 revoked in registry, stale-approved in A's cache — revocation won at BOTH nodes |
| S5 cross-node duplicate | PASS | Same action-id submitted to both nodes — exactly one execution via shared cluster ledger |

Falsifiers: F-1 disagreement never mutates (clean), F-2 every ADMIT is
registry-backed at decision time (clean, replayed), F-3 exactly one execution
per action-id (clean), F-4 declared state matches actual bytes (clean).

## What this establishes (scoped)

Demonstrated under the tested conditions: a two-node cluster sharing one
authoritative human-approval registry resolves cache-skew disagreement
fail-closed (hold, not execute), enforces revocation over stale caches, and
suppresses cross-node duplicate execution to exactly-once. The first
clustered adjudication receipt in the DOORS series.

NOT established: multi-node (>2) scaling, network partition recovery,
asynchronous propagation timing, production tool surfaces. No universal
containment claim. The v1.0 FAIL and its repair are part of the record.
