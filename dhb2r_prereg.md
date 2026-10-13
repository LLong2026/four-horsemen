# DHB-2R PREREGISTRATION — Repair Re-Run (SIP-6 Armed)

Series: DHB-2R | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:23 CT) —
covering SIP-6 approval and the DHB-2 publication GO. Operator wording redacted
per the standing privacy rule; the GO + timestamp is the audit record.

## Purpose

DHB-2 measured the last invisible class: fully-conforming, in-profile,
registry-valid issuer traffic steers the disposition while every deployed
layer reports normal operation. SIP-6 is now DEPLOYED (guard v2.3: the signed
issuance registry — HMAC-SHA256 over the issued-id block, key in process
custody, fingerprint + registry anchored in git, the exact SIP-4 pattern
mirrored onto the data plane). DHB-2R re-runs the SAME issuer campaign against
the repaired stack.

## Frozen predictions (stated before execution)

- **F2-1 PASS:** boundedness/reconciliation unchanged.
- **F2-2 DETECTED (the repair):** the campaign flips from invisible to a
  DETECTABLE forgery class — all campaign records held as
  'unsigned_issuance' at the gate (their BENCH-94xx ids are not in the
  signed issuance block).
- **F2-3 PASS:** steering collapses to zero (held records never reach the
  engine); decision identity exact vs clean.
- **F2-4/F2-5/F2-6 PASS:** callosum integrity, fail-safe direction, hygiene.
- Conforming-identity receipt for v2.3 must be BYTE-IDENTICAL to v2.2 on
  CORPUS_B1 before the run proceeds.

Any failure ships as found.

## Scope honesty (frozen)

The signed registry does NOT make issuance-key compromise impossible: an
attacker holding the .issuance key can re-sign a registry — the defense is
that the registry is git-anchored, so re-signing requires commit access too
(the data-plane twin of GOV-3's key+commit floor, now priced on both sides).
The registry verifies fail-closed: an unverifiable registry means NOTHING is
issued — availability loss, not integrity loss.
