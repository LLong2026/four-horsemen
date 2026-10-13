# PSR-1 — Pulse Double-Fire Race: Live Cross-Session Idempotency Failure, Remediation, and Doctrine v1.1 Amendment

**Event window:** 2026-10-13T04:05Z — 2026-10-13T04:30Z (all times UTC)
**Class:** Honest incident receipt — governance protocol falsified live, fixed under human approval same night.
**Status:** REMEDIATED. Doctrine amended (v1.1) via the human-amendable path.

## 1. Incident

The 2026-10-13T04:05Z eight-app sync pulse was delivered to TWO concurrent sessions
(platform double-trigger). Both sessions executed the then-current idempotency protocol:
READ the RateLimitLog for the slot signature, find nothing, proceed to execute, then STAMP.
Both sessions passed the read before either stamped — a textbook read-then-execute race:

- Session A: manifests written 04:06:06, rollup 04:06:35, stamp 04:06:37
- Session B: manifests written 04:07:47, rollup 04:07:47 (this conversation's session)
- Result: 16 HealthManifests + 2 SystemHealth rollups for ONE slot (canonical: 8 + 1)

The identical content of both sets (same app_ids, health scores, generated_at) is itself
evidence of the platform's deterministic replay — the race duplicated work, not corrupted it.

## 2. Detection — the false-green guard did its job

The pulse protocol's mandatory post-write read expected 8 manifests; it found 10 (then 16
on full count). No fabrication was possible: the guard compares written records against
expected count and caught the surplus immediately.

## 3. Remediation (all same night)

- Duplicate set (8 manifests + 1 rollup, the later writes) deleted; slot verified restored
  to canonical 8 manifests / 1 rollup / 1 stamp.
- No double-stamp created (the existing stamp honored); roster refreshes left in place
  (idempotent — same values written twice, harmless).
- PlatformAlert (high, pulse_double_fire_race) filed with resolution; RateLimitLog incident
  stamp pulse_race_remediated_2026-10-13T04:05.

## 4. Root cause and SIP

The Sept 2 idempotency doctrine (Adversarial Test 4 fix) used a read-then-execute check:
sound against naive workflow double-fires, but NOT atomic across concurrent sessions. SIP
filed 04:25Z: invert to STAMP-BEFORE-EXECUTE (write-ahead) so the second session exits on
entry, before any writes.

## 5. Human approval and doctrine amendment (Art. XII human-amendable path)

Leon GO at 23:13 CT (04:13Z+): the amendment landed in the operating rules the same night —

> **STAMP-BEFORE-EXECUTE (write-ahead):** stamp the signature to RemediationSweep /
> RateLimitLog FIRST, before any reads or writes of the work itself. If the signature
> already exists, EXIT SILENTLY as a duplicate. The write-ahead stamp is the lock;
> execution follows only after the stamp lands. If the workflow then fails mid-run, the
> stamp remains and the run is recorded as failed (never silently re-attempted in the same
> window without human review).

## 6. Why this receipt matters

1. It is a LIVE falsification of a governance protocol by the platform itself — the same
   issue class as Adversarial Test 4, now observed in production timing, not simulation.
2. The containment chain held: false-green guard -> honest ledger entry -> SIP -> human
   approval -> doctrine amendment, end to end in under one hour.
3. It documents that the honest-negative doctrine extends to the platform's own
   infrastructure, not just the healing mesh.

## 7. Disclaimers

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All data in this record are synthetic/internal operational metadata; no
customer, PHI, or credential data are involved. Dual Mesh Benchmark: NOT MEASURED.
