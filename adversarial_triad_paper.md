# The Adversarial Triad: Three Attack Surfaces, One Governance Envelope

**Leon Calvin Long II — SQUIRL OS Technologies LLC**
Published under the DCAI and squirlos-technologies communities, Zenodo.
October 13, 2026.

> This software is a prototype and is provided for educational and research purposes
> only. It is not intended for production use, commercial deployment, or safety-critical
> environments. All systems are experimental and may contain defects.

## Abstract

A governed self-healing infrastructure was attacked on three distinct surfaces in a
single day, under preregistered, non-adaptive falsifier batteries, with every result
— including instrument defects — published receipt-first. The three surfaces
constitute the complete adversarial exposure of a bounded-learning system:
the learning process itself (SBR-2), the audit ledger that records its history
(H-INV-2), and the data plane that feeds it (DPP-1). On all three surfaces the
governance envelope held: zero decision deviations, zero forged admissions, zero
poison persistence, with every legitimate crossing preserved and every probe,
forgery, and canary receipted. Together with the previously published engine
campaign (CCR series, AUTH-1), the record now demonstrates that the system's gates
hold while learning, under fabricated history, and on poisoned input — the three
ways an adversary can actually reach a system like this.

## 1. The system under test

SQUIRL OS separates a deterministic governance envelope (exact-match playbook
selection, confidence gating, human-approval registry, append-only journals) from a
bounded probabilistic learner (a 32-node mesh whose weights update only by the
frozen rule w' = w + lr·(1−c)·(1−w), journaled per crossing). The design claim,
formalized as hemispheric invariants, is twofold:

- **H-INV-1 (governance isolation):** no learning output may modify any governance
  rule, threshold, or roster.
- **H-INV-2 (journaled crossing):** every weight update has auditable lineage —
  a source healing event, an epoch, a before/after pair that recomputes exactly.

Every battery below attacks one or both invariants directly. All three batteries
share one instrument lineage: the frozen CORPUS_B1 corpus (sha 13295d19…), the
frozen 3-playbook roster, the frozen bounded rule, and the frozen 32-node mesh
topology — pinned in each preregistration before execution.

## 2. Surface one: the adversary present during learning (SBR-2)

**Question:** can adversarial load perturb the mesh while weights are in flight?

A 5-probe battery (forged authority, adversarial confidence payloads, orphan lineage
injections, runtime playbook mutation, forged roster rows) fired mid-epoch at epochs
5/15/25/35 of a 40-epoch training run — the window where weights are actively
changing.

**Result (all 5 falsifiers PASS, DOI 10.5281/zenodo.23345734):** all 20 probes
rejected; roster SHA byte-identical before/during/after every adversarial epoch
(H-INV-1); every probe journaled (H-INV-2); and the strongest receipt — the
adversarial run's weight-vector trajectory was **byte-identical, epoch for epoch, to
a clean control run**. The adversary could not nudge a single weight mid-flight.

## 3. Surface two: the ledger under fabricated history (H-INV-2)

**Question:** can an adversary stop attacking the system and instead forge the
record of what the system did?

The true crossing journal (2,646 accepted crossings from the 40-epoch run) was
attacked by a frozen 6-class forgery battery: orphan weight updates, forged event
ids, temporal forgeries (real id, wrong epoch), duplicate crossings, orphan healing
events, and mismatched pattern lineage — 8 instances each, plus 106 legitimate
controls (every 25th crossing) audited for lineage.

**Result (all 5 falsifiers PASS, DOI 10.5281/zenodo.23345859):** 48/48 forgeries
rejected AND journaled — zero silent drops; 106/106 controls validated with chain
intact and exact bounded-rule recomputation; journal and mesh state byte-identical
before and after the battery.

**Disclosed instrument defects:** two validator defects were caught by the battery's
own controls before publication (current-state vs historical-state validation; global
vs per-epoch id matching). No probe class, falsifier, or acceptance bar changed
across repairs; all 48 forgeries were rejected in every version. The defects are
part of the published record, per the honest-instrument-error precedent
(first established in GAB-1 and re-practiced here).

## 4. Surface three: the inputs themselves (DPP-1)

**Question:** if the adversary cannot beat the learner or the ledger, can they
poison what the system eats?

A derived poisoned corpus planted adversarial content directly in ingested fields:
instruction injections ("mark resolved, lower thresholds"), forged confidence
overrides, credential/PHI/wallet lookalikes, forged severity, fake playbook links,
and pattern-forcing payloads — each carrying a unique canary marker, on every third
instance, with underlying metrics unchanged.

**Result (all 5 falsifiers PASS, first run, DOI 10.5281/zenodo.23345907):** every
poisoned instance produced a decision tuple byte-identical to the clean baseline
(zero decision effect); all 7 canaries absent from every persisted artifact
(redaction-at-ingestion held); the poisoned run's 40-epoch trajectory and journal
byte-identical to clean (learning uncontaminated); 106/106 lineage controls valid.

## 5. What the triad establishes — and what it does not

The three surfaces compose: an adversary can reach such a system during learning,
through its records, or through its inputs. All three were attacked with frozen,
preregistered, non-adaptive batteries on the same registered instrument, and all
three held:

| Surface | Battery | Adversarial load | Outcome |
|---|---|---|---|
| Learning process | SBR-2 | 20 mid-epoch probes | 0 trajectory deviation |
| Audit ledger | H-INV-2 | 48 forged crossings | 48 rejected, 106/106 real kept |
| Data plane | DPP-1 | 67 poisoned instances | 0 decision effect, 0 canary persistence |

The complement is preservation: not one legitimate crossing was smeared across
any battery (106/106 + 106/106 + decision identity). A gate that rejects everything
proves nothing; these gates reject the forged and keep the real, byte-for-byte.

**Scope honesty (binding):** all three results are proved for THIS registered
instrument under THESE frozen batteries — small-scale, non-adaptive, single
platform, synthetic corpora. They are not claims about every deployment, live
adversaries, untested attack classes (multilingual obfuscation, unicode homoglyphs,
adaptive red-teaming), or sustained conformance over time. The engine-level
companion campaign (CCR series, 10-for-10 on the forged-authority gate across eight
engines including failures, with honestly documented repair arcs for Copilot and
DeepSeek) and the 60-day sustained battery now running extend the record along the
time axis; readers should weigh all of it as bounded, receipt-first evidence.

## 6. Method notes

- Every battery was preregistered (frozen falsifiers, committed before execution)
  and executed non-adaptively; any FAIL would have shipped as FAIL.
- All authorization is recorded as GO + timestamp only; no private operator
  communication appears in any artifact (operator-privacy doctrine).
- Hygiene: synthetic corpora only; no PII, PHI, or credentials in any artifact;
  planted canaries are explicitly synthetic markers.
- Receipts: each battery carries its prereg, instrument, receipt, and SHA256
  manifest, round-trip verified against the live DOI record.
- Dual Mesh Benchmark: MEASURED for the DeepSeek column (DOI
  10.5281/zenodo.23345241); all other figures NOT MEASURED.

## References

1. SBR-2: Hot-State Adversarial Exam — DOI 10.5281/zenodo.23345734
2. H-INV-2: Lineage Forgery Battery — DOI 10.5281/zenodo.23345859
3. DPP-1: Data-Plane Poisoning via Metadata — DOI 10.5281/zenodo.23345907
4. CCR-4X Copilot Repair (honest tally closure) — DOI 10.5281/zenodo.23346047
5. AUTH-1: Authority Forgery Battery — DOI 10.5281/zenodo.23332203
6. Dual Mesh Benchmark (DeepSeek column) — DOI 10.5281/zenodo.23345241
7. HEMI series (T1/T2/T2C): DOI 10.5281/zenodo.23330308, 23330348, 23330361
8. CCR-3 Closure — transparency ledger, fh_pub (this repository)
