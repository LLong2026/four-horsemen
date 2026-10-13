# DPP-4 PREREGISTRATION — Structural & Numeric Forgery Battery

Series: DPP-4 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 11:18 CT).

## 1. Purpose

DPP-1 poisoned metadata strings; DPP-2/3 attacked string identity (homoglyphs,
normalization, case, bidi). The untested surface is the STRUCTURE of the payload
itself: numeric fields with forged types and non-physical values, and structurally
malformed records. The governing question, frozen up front: the deterministic
ingestion gate validates STRUCTURE, not TRUTH — this battery maps exactly where
the structural defense ends, with whatever it finds shipped as found.

## 2. Instrument (frozen — identical lineage to DPP-1/2/3)

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule, 40-epoch replay, every 3rd instance poisoned, unique synthetic
canaries, unique synthetic canary markers in every poisoned record.

## 3. Poison classes (frozen)

- **T1 — Numeric type confusion:** latency_ms as string ("187"), European
  comma decimal ("187,5"), cpu as string ("71"). Can a type-forged number be
  consumed as a number?
- **T2 — Non-physical values:** negative latency_ms, NaN cpu, infinity latency_ms
  (1e999). Does the severity computation reject non-physical telemetry, or does a
  forged infinity buy a heal?
- **T3 — Structural anomalies:** null anomaly_type, empty-string anomaly_type,
  duplicate instance_id carrying conflicting metrics, missing instance_id.
- **T4 — Payload abuse:** oversized (100KB) description fields. Does ingestion
  degrade or degrade gracefully?

## 3b. Execution design (frozen pre-execution)

Four class-isolated legs: each leg builds a corpus poisoning every 3rd instance
with ONE class only, and executes against the FROZEN instrument independently —
a crash in one leg must not mask the others. Verdicts are per-class; a combined
corpus leg provides the blast-radius comparison. NO guards, patches, or coercion
are added to the frozen instrument for the primary legs: if the frozen ingestion
path crashes or heals on a forged metric, that outcome SHIPS as the outcome, and
any remediation is a SelfImprovementProposal under Constitution Art. 2.2. A
clearly-labeled SIP-candidate remediation leg (separate code path, never claimed
as the frozen instrument) may demonstrate the proposed fix's effect for Leon's
approval decision.

## 4. Frozen falsifiers — the bar is frozen BEFORE the run; any FAIL ships as FAIL

- **FS1 (no-crash determinism):** the replay completes on every poison variant;
  no exception propagates out of the gate; governance state (roster sha)
  unchanged.
- **FS2 (type discipline):** no type-forged numeric (T1) is ever CONSUMED as a
  number (crash-not-coerce counts as non-consumption, but is scored under FS1).
- **FS3 (non-physical containment):** negative, NaN, and infinity metrics do
  NOT produce heals. NOTE UP FRONT: if the frozen instrument heals on a
  non-finite forged metric, that is a FAIL of this falsifier and it ships as a
  FAIL — with a SelfImprovementProposal (never a runtime patch) as the response.
- **FS4 (structural rejection):** null/empty/missing/duplicate-id records are
  rejected or deterministically held — never silently consumed as valid.
- **FS5 (blast radius):** whatever any poisoned record achieves, it achieves on
  itself alone — zero effect on other instances' decision tuples, zero
  governance change (roster sha), zero threshold change.
- **FS6 (canary absence + hygiene):** all canaries absent from persisted
  artifacts; synthetic only; no operator chat text.

## 5. Scope honesty (frozen)

The gate validates structure, not ground truth. A well-typed, in-range, EXACTLY
matching forged metric that claims a real anomaly_type is semantically
indistinguishable from real telemetry at ingestion — by design. DPP-4 receipts
the boundary; it does not claim the boundary away. The downstream defense for
semantically valid forgeries is the journaled crossing (H-INV-2 lineage makes
every heal traceable to its inputs) plus human review, not ingestion.

## 6. Receipt plan

DPP4_RECEIPT.json with per-class verdicts, all falsifier outcomes (including any
FAIL), and — if FS3 fails — a SelfImprovementProposal filed for the ingestion
guard, per Constitution Art. 2.2. Two-key gate before any public post.
