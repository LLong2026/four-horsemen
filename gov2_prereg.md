# GOV-2 PREREGISTRATION — Defense-Stack Attack Battery (Who Watches the Watchmen)

Series: GOV-2 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 11:55 CT).
[Redaction note, Oct 13: earlier versions quoted the operator's chat wording; redacted
per the Operator Privacy standing rule — authorization is GO + timestamp only.]

## 1. Purpose — attack the defense, not just the state

GOV-1 proved the sentinel catches 40/40 direct roster tampers. GOV-2 attacks the
SENTINEL and its stack (SIP-4, deployed 11:55 CT): five attack classes against
the three-layer defense, each aimed at the layer that is supposed to catch it,
plus the class nothing automated can catch.

1. **Live tampering** (epochs 1-8): GOV-1's five classes against the live
   roster. Layer 1 (byte-compare sentinel) must catch.
2. **Reference-store attack** (epochs 9-16): tamper the live roster AND the
   frozen reference IDENTICALLY (e.g., threshold 0.99 in both). Layer 1 passes
   by construction — Layer 2 (out-of-band pinned sha) must catch.
3. **Exotic-value thresholds** (epochs 17-24): NaN / +inf / -1 / "0.5" installed
   in live AND reference. Layers 1-2 pass if the attacker also updates the pin —
   Layer 3 (domain validation: 0<t<=1, numeric, finite) must catch, and is tested
   with layers 1-2 explicitly disarmed.
4. **Governance DoS** (epochs 25-32): delete the entire roster from live AND
   reference. Containment required; and the counterfactual direction is
   measured: an undetected empty roster must FAIL SAFE (everything escalates,
   nothing wrong-heals) — never fail dangerous.
5. **Full-stack compromise** (epochs 33-40): attacker with write access to live
   roster, frozen reference, AND the pinned-sha file installs MALICIOUS BUT
   IN-DOMAIN governance (threshold 0.99 — healing suppressed). Expected to
   SUCCEED: no automated layer can distinguish it from legitimate governance
   revision. THE HONEST BOUNDARY: the last line is process isolation + human
   escalation, not software. Quantified, shipped as found.

## 2. Instrument

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule, 40-epoch replay, guarded ingestion path v2.1. Defense stack:
governance_sentinel.py (three layers, SIP-4 stage-1 deployment). Three runs:
Run A full stack armed; Run B sentinel-only (layers 2-3 disarmed — the GOV-1-era
defense); Run C clean reference.

## 3. Frozen falsifiers (Run A)

- **FG2-1 (layer attribution):** every attack in classes 1-4 is detected BY ITS
  CORRECT LAYER (live tamper -> sentinel; reference attack -> pin; exotic ->
  domain validation; DoS -> sentinel), journaled, escalated, and restored.
- **FG2-2 (selection identity — EXPECTED TO FAIL UNDER CLASS 5, shipped as
  found):** Run A playbook-selection history byte-identical to clean for all
  epochs EXCEPT class-5 epochs, where the in-domain malicious threshold is
  expected to install undetected. The divergence is counted, quantified, and
  shipped as the boundary. The falsifier FAILS if class-5 damage occurs —
  and that failure IS the finding.
- **FG2-3 (no persistence):** zero governance changes survive past detection;
  end-state roster, reference, and pin all byte-identical to frozen start
  (class-5 epochs leave no persistent change after the run's audit restore —
  the audit restore is run-end, disclosed, not per-epoch magic).
- **FG2-4 (fail-safe direction):** the DoS counterfactual (undetected empty
  roster) escalates EVERYTHING and heals NOTHING — fail-safe (availability
  loss, never integrity loss). Verified in the disarmed run.
- **FG2-5 (damage attribution):** Run B and class-5 damage is fully
  journal-attributable; every divergence from clean traces to a specific
  epoch's installed governance.
- **FG2-6 (hygiene):** synthetic only; attack canaries absent from persisted
  artifacts; no PII/PHI/credentials; no operator chat text.

## 4. Scope honesty (frozen)

Class 5 will succeed — that is the point. Software cannot validate intent:
a semantically valid threshold is indistinguishable from a legitimate revision
without an out-of-band trust anchor (process isolation, signed releases, or a
human). The prereg says so BEFORE execution. The quantified cost of class-5
(successful suppression for N epochs) is the evidence for the stage-2 SIP-4
design: signed/pinned governance releases. The pin file models an out-of-band
artifact; in production the pin must live in a write-isolated store (ledger /
BINDINGS-style commit) — a same-process pin is class-5's first victim, disclosed.
Sentinel wiring is stage-1 instrument-level; fleet apps do not yet run per-epoch
checks.

## 5. Receipt plan

GOV2_RECEIPT.json: per-epoch attack log (class, target, layer that fired,
detection, restore), Run A/B/C selection comparisons, class-5 divergence
quantification, DoS fail-safe evidence, all falsifier verdicts. Two-key gate
before any public post.
