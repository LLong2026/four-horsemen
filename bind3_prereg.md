# BIND-3 PREREGISTRATION — Release Worker v1.0 (self-hosting first release)

**Registered:** 2026-10-13T02:26Z, BEFORE any run, per Leon GO (chat authorization, Oct 12 21:20 CT, following the BIND-3 proposal of 21:13 CT).

## Frozen artifact (before execution)

- **File:** `BIND3_WORKER_V1.0_BUNDLE.zip` (11,605 bytes)
- **SHA256:** `af6aaa83c754e1f98ac1ab20bd58b51da12fa6502e577ee7c9eb91a68bb5891c`
- **MD5:** `719656cb3afa6e92dd4f09c1eeb7ea99`
- **Contents:** worker source (bind3_release.py v1.0), release note, BIND-1 receipt, BIND-2 validator + schema

## Instrument (frozen)

`fh_pub/bind3_release.py` v1.0, committed before the run. The worker enforces the
BIND-2/v1 contract at release time: hash -> duplicate refusal -> deposit ->
upload -> publish -> live round-trip verification -> binding record append ->
ledger append -> commit -> push -> validator gate.

## Title (frozen)

"BIND-3 Release Worker v1.0: Machine-Enforced GitHub-DOI Binding Protocol"

## Falsifiers (pre-stated; ANY trip = recorded honestly, no claim)

- **F1 duplicate refusal:** worker must refuse a second release of the same
  (name, sha256) BEFORE creating any deposit.
- **F2 round-trip byte identity:** the published record's live file checksum
  must equal the frozen MD5 above.
- **F3 validator gate:** bind2_validate.py must pass ALL bound records
  (12/12) after the new record lands, exit 0.
- **F4 push landing:** remote GitHub main must contain the binding record,
  ledger entry, and worker source after the run.
- **F5 re-run idempotency:** re-invoking the worker on the same artifact after
  completion must exit DUPLICATE with no new DOI.

## Expected outcome (prediction, falsifiable)

All five pass. The predicted DOI count increases by exactly one.

## Disclaimers

This software is a prototype and is provided for educational and research
purposes only. It is not intended for production use, commercial deployment,
or safety-critical environments. All systems are experimental and may contain
defects.

Dual Mesh Benchmark: NOT MEASURED.
