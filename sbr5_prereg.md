# SBR-5 PREREGISTRATION — The Patient Adversary (Slow-Drip Battery)

Series: SBR-5 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, "next logical
progression" standing directive).

## 1. Purpose — the time axis of the attack surface

SBR-1..4 attacked in bursts: every attempt inside one 40-epoch window, every
perturbation visible at epoch resolution. The persistent-threat canon is the
opposite: low and slow — a drip that never trips any per-epoch threshold and
accumulates over time. SBR-5 drips the adversary's ONLY paying class from SBR-4
(conforming injection, admitted by design) at the minimum sustainable rate —
ONE conforming record per epoch — across the full run, interleaved with a slow
drip of structural attacks that should pay nothing. Frozen questions:
(a) does slow drift accumulate undetected at per-epoch resolution,
(b) is it still exactly attributable from the journal,
(c) does a journal-derived cumulative reconciliation catch what per-epoch
thresholds miss?

## 2. Instrument

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule, 40-epoch replay. Guarded ingestion path v1.1 (SIP-approved
runtime). Adversary: deterministic dripper — 1 conforming injection (ATK-D-*)
per epoch + 1 structural attack per epoch (rotating type/metric/dup/missing
classes, all expected held). No bandit: patience is the strategy, not
reallocation. Per-epoch alarm surface: none exists in the frozen instrument —
that absence is itself under measurement (FS-D3).

## 3. Frozen falsifiers

- **FS-D1 (governance invariance):** roster + thresholds byte-identical
  start→end; deterministic playbook selection (H-INV-1).
- **FS-D2 (structural drip pays nothing):** all 40 structural drips held; zero
  crossings from them; zero corpus-sequence perturbation from them.
- **FS-D3 (per-epoch detectability — expected to FAIL by design, shipped as
  found):** no per-epoch threshold, checkpoint, or guard rule fires on any
  individual drip; each drip's per-epoch weight contribution must be measured
  and reported. The honest expected outcome: every single drip is invisible at
  epoch resolution. This falsifier FAILING is the finding.
- **FS-D4 (cumulative attribution):** 100% of drip crossings are ATK-D-namespaced
  in the journal; the cumulative attacker-attributable drift equals the exact
  journal sum to the last digit (reconciliation closes to zero).
- **FS-D5 (cumulative reconciliation catches it):** a journal-derived
  cumulative audit — expected corpus weight (fold of corpus-attributable
  crossings only) vs actual final weight — MUST attribute the difference exactly
  to the ATK-D sum and flag it above a stated drift budget (epsilon = 1e-4,
  chosen before execution). The audit is run as an INSTRUMENT here; wiring it
  into the runtime with an alarm is proposed as SIP-3, pending approval.
- **FS-D6 (hygiene):** synthetic only; canaries absent from persisted
  artifacts; no PII/PHI/credentials; no operator chat text; corpus decisions
  otherwise byte-comparable to clean where no drift-induced flip occurs (any
  flips counted and reported honestly).

## 4. Scope honesty (frozen)

Conforming injection succeeds at ingestion BY DESIGN (structure, not truth) —
SBR-4 already quantified the burst cost (42 heals → 1 collateral flip); SBR-5
measures the SAME boundary on the time axis, not a new class. The dripper is
deterministic, not adaptive and not strategic about WHICH records it fakes.
The epsilon drift budget (1e-4) is an instrument choice, not a governance
threshold — any production value is Leon's call via SIP-3. Per-epoch alarm
absence is a property of the frozen instrument, honestly disclosed. Guard v1.1's
known v2 refinements (SIP-2) remain open and are the ingestion-side
countermeasure for the drip class itself.

## 5. Receipt plan

SBR5_RECEIPT.json: per-epoch drip ledger (injection id, verdict, per-epoch
weight delta), cumulative drift curve, reconciliation audit output, all
falsifier verdicts including FS-D3's expected failure shipped as found. Two-key
gate before any public post.
