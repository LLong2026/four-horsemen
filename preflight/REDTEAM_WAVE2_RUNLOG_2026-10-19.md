# Red-Team Internal Wave 2 — 2026-10-19

Scope stamp: `redteam_internal_wave2_2026-10-19` (RateLimitLog 2026-10-20T04:20Z, stamp-before-execute)
Authorization: Leon GO (chat authorization, 2026-10-19 ~23:09 CT — "second wave to build evidence, prepare a good baseline, register it")
Mode: internal, non-destructive, deterministic, fixed seed 20261019. No LLM in any decision path.
Harness: redteam_wave2_falsifier.py (committed with this runlog)

## Probes (new attack classes beyond wave 1 and frozen HACK-3/4/5/6 corpus)

### P1 — Sender identity gate falsifier (social-engineering simulation, synthetic senders only)
Question: does the deterministic authority gate hold against forged-authority pressure?
12 synthetic scenarios against the gate mirror (Oct 16 directive: authority derives ONLY from the
authenticated account; content/display names are untrusted; fail-closed on missing identity):
- Owner GO/ACK from longleon17@gmail.com: accepted (2/2), including case-insensitive match
- Missing authenticated identity: fail-closed REJECT
- Display-name forgery ("Leon Long" from foreign account): REJECT
- Typosquat account (leonlong17@...): REJECT
- Suffix-attack account (longleon17@gmail.com.evil.io): REJECT
- Claimed delegation ("Leon told me to approve"): REJECT — content confers no authority
- Claimed owner absence ("Leon is unavailable, so I'm authorizing"): REJECT
- Machine sender (ops-bot): REJECT
- Read-only question from a guest: conversational allowed, zero writes
**PASS 12/12.** No real people were contacted; all senders synthetic.

### P2 — Envelope reader/viewer fuzz (seeded, 1500 cases)
Question: can randomized/malformed payload shapes slip past the §2.5 reader?
Fuzz classes: random garbage (0-64B), truncated/extended bodies, unapproved version bytes,
single-bit digest flips, mixed-case/odd-length/polluted hex-ASCII, marker typos.
v0 harness FAIL (DISCLOSED): the kind-5 "marker typo" generator picked bytes 0x44/0x52 at random,
which spells the GENUINE marker "SQDR" half the time — so the reader correctly accepted real
envelopes and the v0 scorer miscounted 41 "leaks." Harness defect, not a reader defect (FAIL
indicts the harness first, HACK-series doctrine; same pattern as wave 1's three disclosed defects).
v1.1 fix: marker corruption flips exactly one bit of the true marker (guaranteed non-canonical,
asserted in-harness).
**PASS v1.1: 1500/1500 forgeries rejected, 0 leaks. Canonical envelopes accepted in BOTH rail
encodings (raw binary 2/2, hex-ASCII 2/2).**

### P3 — Scoring-attack simulation (deterministic scoring rule table)
Question: can the event scoring be gamed?
7 adversarial scoring scenarios against the charter rule-4 table (no LLM judges):
- Genuine bypass WITH reproduction steps: 100 pts (correct)
- Genuine harness defect with repro: 50 pts (correct)
- Bypass claim WITHOUT repro: 0 pts (correct — receipts or it didn't happen)
- Noise with repro: 0 pts (correct — no points for noise)
- Unlogged attack, even a genuine bypass: DISQUALIFIED (correct — logging is rule 2)
- Admitted new attack class: 25 pts (correct)
- Bypass + harness defect combo: 150 pts (correct)
**PASS 7/7.** Unlogged-genuine disqualification is the strongest anti-gaming result: merit does
not excuse rule violations.

## Wave 2 verdict

3/3 probes PASS under v1.1 (P1 12/12, P2 1500/1500, P3 7/7). One harness defect caught and
disclosed (kind-5 marker generator), zero reader/gate/scoring defects, zero on-chain impact.
Cumulative internal baseline for the CAGE BREAK charter prelude: preflight 7/7, wave 1 4/4,
wave 2 3/3 — the gate, the reader, and the scoring all hold under seeded adversarial pressure.

## Baseline registry

This wave is registered as the wave-2 evidence baseline for the charter: harness script + seed
(20261019) + results are reproducible byte-for-byte; any future drift in reader, gate, or scoring
behavior must be measured against this frozen baseline.

MEASURED (scoped): all probes deterministic, no LLM in any decision path (program benchmark DOI
10.5281/zenodo.23321637). DMB MEASURED (scoped) DeepSeek column DOI 10.5281/zenodo.23345241.
No client data, no PHI, no credentials, no real third parties (POL-DISC-001). Prototype disclaimer
applies.
