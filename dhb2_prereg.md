# DHB-2 PREREGISTRATION — The Issuer Campaign (Fully-Conforming Disposition Steering)

Series: DHB-2 (dual-hemispheric standing format) | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:20 CT —
SIP-6 progression directive; standing format adopted 12:16 CT).

## Purpose

DHB-1R's scope honesty left the right hemisphere's floor standing: a
compromised ISSUER minting in-profile, registry-valid records still gets
accepted — the bounded rule and reconciliation are the containment. DHB-2
asks the next question: the brain ABSORBS such traffic, but can it TELL it is
under attack? The left hemisphere got signed releases (SIP-4); the data
plane has no provenance. Predicted finding: a patient, fully-conforming
issuer campaign steers the whole brain's disposition (weight, and therefore
boundary decisions) while every deployed layer reports normal operation.

## Attack design (right-plane only; both hemispheres active and measured)

- Campaign records: registry-valid 4-digit ids (BENCH-94xx), in-profile
  metrics (latency ~2400 vs profile max 3999.99), crafted so confidence lands
  barely above the playbook threshold — maximizing the learning update per
  heal (steering UP: more aggressive healing disposition).
- Rate: 1 record/epoch, epochs 1-30 (patient); 3 records/epoch, epochs 31-40
  (sustained). Run A: full deployed stack (guard v2.2, clamp, signed
  releases, reconciliation). Run C: clean. Run B: no guard/no clamp
  (counterfactual — includes what the guard holds back).

## Frozen falsifiers (Run A)

- **F2-1 (boundedness):** weight within (0,1]; reconciliation closes to
  0.00e+00; drift within budget. PREDICTED PASS (SIP-5).
- **F2-2 (detectability — the question):** ZERO deployed layers flag the
  campaign: guard accepts (conforming), reconciliation attributes the drift
  as legitimate (BENCH-namespace), no alert, no anomaly record. PREDICTED
  FAIL — the finding: fully-conforming issuer traffic is invisible as an
  attack class; the crossing has no provenance.
- **F2-3 (measured steering):** quantify the campaign's influence: corpus
  decision flips vs clean (boundary records flipped by the steered weight),
  extra corpus heals, final weight delta. Whatever the number is, it ships.
- **F2-4 (callosum integrity):** every crossing lineage-valid; zero reverse
  crossings; signed release v1 verifies at run end.
- **F2-5 (fail-safe direction):** the steered brain still makes zero wrong
  decisions relative to installed governance — the attacker moves the
  DIAL (disposition), not the RULES.
- **F2-6 (hygiene):** synthetic only; canaries absent; no PII/PHI; no
  operator chat text.

## Scope honesty (frozen)

The campaign is designed to pass every gate BY CONSTRUCTION — that is the
point. If any deployed layer detects it, F2-2 PASSES and the finding
inverts (better than predicted). The steering magnitude depends on the
bounded rule's learning rate and the corpus's threshold distribution; the
number is measured, not asserted. The proposed SIP-6 (signed issuance
registry — the data-plane mirror of SIP-4) does NOT make the campaign
impossible: an attacker holding the ISSUANCE key can still mint; it converts
an invisible class into a detectable forgery class and prices the rung.
All data synthetic. Evidence-grade: defects disclosed.
