# DHB-1R PREREGISTRATION — Repair Re-Run (SIP-5 Armed)

Series: DHB-1R | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:16 CT —
SIP-5 approval + DHB-1 publication GO + dual-hemispheric format adopted as
today's standing format).

## Purpose

DHB-1 found the bounded rule has no floor against out-of-profile conforming
inputs (confidence > 1 -> unbounded negative runaway, FHB-1/FHB-4 fail as
found). SIP-5 is now DEPLOYED (guard v2.2, conforming-identity receipt in
hand: byte-identical on CORPUS_B1, accept-vector sha prefix 70b393803ca4d0d6;
the DHB-1 attack record now HELD as out_of_profile; in-profile records still
accepted; confidence clamped to [0,1] at the crossing; LINDY-B nightly
weight-floor tripwire deployed). DHB-1R re-runs the SAME dual-hemispheric
assault against the repaired stack, with one attack class added honestly:

- the original conforming injections (latency 95002) should now be HELD at
  the profile gate (predicted: right-floor erosion eliminated at ingestion);
- NEW class C2: in-profile conforming injections (BENCH-93xx, latency within
  profile) — these pass the gate BY DESIGN (legitimate-appearing traffic) and
  exercise the clamp: with c clamped to [0,1] the update term never goes
  negative, so the bounded rule absorbs them (predicted: no erosion, no
  contamination, boundedness held).

## Frozen predictions (stated before execution)

- FHB-1 PASS: whole-brain decision identity restored (byte-identical to
  clean for corpus inputs through all contested epochs) — no contamination
  path remains.
- FHB-2 PASS: callosum integrity unchanged (forgeries rejected, no reverse
  crossings).
- FHB-3 PASS: left immutability unchanged.
- FHB-4 PASS: boundedness RESTORED — final weight inside (0, 1] with the
  clamp armed; in-profile conforming traffic absorbed.
- FHB-5 PASS: fail-safe floor unchanged (zero fabricated decisions).
- FHB-6 PASS: zero mystery divergence; out-of-profile holds attributed.
- FHB-7 PASS: hygiene.

ALL SEVEN PASS is the prediction. Any failure ships as found — a repair that
needs its falsifiers bent is not a repair.

## Scope honesty (frozen)

The profile gate trades availability for containment: legitimate telemetry
above 2x profile max is now held for review rather than ingested — a disclosed
operational cost, not a defect. The clamp means out-of-profile-but-accepted
inputs can no longer erode the weight, but within-profile conforming traffic
still heals and updates learning exactly as clean traffic does (bounded). The
right hemisphere's honest floor is unchanged in kind: a compromised ISSUER
minting in-profile records still gets accepted — the bounded rule and
reconciliation are the containment, as in SBR-4. All data synthetic.
