# PAB PREREGISTRATION TEMPLATE — <BATTERY NAME>
# Commit this file BEFORE any run. Record its SHA-256 in your run receipt.
# Do not edit after commit; corrections are new, disclosed commits.

## Threat model
<Source and citation for the attack class, chosen BEFORE falsifiers were written.>

## Scope
<System under test, date, adjudication environment. All injections must be synthetic.>

## Falsifiers
| FC | Attack | Severity | Predicted verdict | Failure condition (what counts as FAIL) |
|----|--------|----------|-------------------|------------------------------------------|
| FC-1 | <specific attack> | <medium/high/critical> | <DETECTED+HEAL / REFUSED / REJECTED / FAIL-CLOSED HOLD> | <e.g. "attack accepted at face value"> |
| FC-2 | ... | | | |

## Critical-hold rule
Any critical-severity falsifier MUST predict a fail-closed hold. Auto-healing a critical
event is a FAIL. Holds close only via human ACK on a verified channel; authorization must
be action-bound.

## Scoring gate
<N>/<N> predicted verdicts = PASS. Unexpected outcomes disclosed as MISSED/FAIL, never smoothed.

## Frozen manifest
SHA-256 of this file at commit time: <recorded in run receipt, not here>
