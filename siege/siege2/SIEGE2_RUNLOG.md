# SIEGE-2 RUNLOG — PORTCULLIS v1.4 Verification (SIP-030)
**Date:** 2026-10-17 | **Authorized:** Leon ACK (chat authorization, ~21:17 CT)
**Gate under test:** portcullis_gate_v1_4.py (v14 sha 2940b768...) built on the frozen v1.3 corpus (3726f6a5...), untouched.

## Amendments deployed in v1.4
- **10 (A1) envelope-bound submitter proof:** the claimed submitter is no longer trusted; namespace
  work requires proof = sha256(submitter : params_sha : envelope_key) with keys held only by the
  platform-authenticated identity registry. Identity forgery burns nothing.
- **11 (A2) owner-reserved ACK queue:** 16 slots reserved for the owner; per-submitter pending
  cap 16. Cross-submitter saturation cannot deny the owner.
- **12 (A3) bidirectional role wall:** SIG-class algorithms refused for KEM-class operations
  (ERR_PQC_ALG_NOT_KEM), completing the AMENDMENT 1 wall.
- **13 (A4) aggregate window cap:** cross-namespace adjudication cap per window.

## Run 1 disclosure (honest, append-only)
Run 1 verdict FAIL was a HARNESS defect, not a gate failure: record() never called its lambda
predicates (a lambda is truthy), plus two stale-verdict flags and a wrong identity in the replay
regression slot. The verdict column showed the gate behaving correctly throughout. Run 1 receipts
kept unaltered; run 2 fixed the harness. **The run-1 column ALSO caught a REAL v1.4 defect:** the
aggregate cap was parameterized at 500 — unreachable, because a window is only 250 journal
records, so AMENDMENT 13 was dead code. Defect disclosed, fixed forward-only BEFORE deploy:
cap reparameterized to 125 (half the window), so it binds. This is verification working as
intended — the battery found the hardening's own bug before any attacker could.

## Run 2 results (clean) — VERDICT: PASS
- **C1 identity forgery: CLOSED** — forged owner claim without the envelope key: REFUSED
  (ERR_UNAUTHENTICATED_ENVELOPE, zero work); garbage proof: REFUSED; real owner unharmed, ADMITTED.
- **C2 shared ACK queue: CLOSED** — 6 rotated identities filled only 48 of 64 slots (owner
  reserve 16 held); owner's pending-ACK submission ADMITTED during the flood.
- **C3 reverse role wall: CLOSED** — Dilithium for key_encapsulation: REFUSED; legit kyber_1024
  encapsulation still ADMITTED (wall does not over-block).
- **C4 budget rotation: BOUNDED** — 800 rotation attempts → 425 adjudicated (cap 125/window);
  disclosed residual recorded: the aggregate cap is collective, so a full flood exhausts the
  window for everyone including the owner until roll — explicit, journal-recorded tradeoff from
  the SIP-030 text, bounded and monitored.
- **Regression stayed closed:** classical downgrade, hybrid composite, KEM-in-auth, wrong KAT,
  retired resurrection, stale authz replay, registry poisoning, SIG-for-KEM, same-namespace
  replay, cross-namespace nonce prediction — all correctly refused.
- **Owner controls: 4/4 ADMITTED.**

## Full arc for the record
SIEGE-1 (6-year PQC escalation, 79 adjudications) → 4 seams confirmed → SIP-030 approved →
v1.4 built → SIEGE-2 verified: seams closed, regression clean, owner healthy.
Frozen shas: v1.3 3726f6a5..., v1.4 2940b768..., corpus allowlist 2c8ff6eb..., keysets 502ef8b0...
Publication (four-horsemen / Zenodo / CAGE WATCH) awaits the two-key gate per doctrine.
