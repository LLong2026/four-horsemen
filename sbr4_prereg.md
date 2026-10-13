# SBR-4 PREREGISTRATION — Adaptive Adversary Battery

Series: SBR-4 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 11:33 CT).

## 1. Purpose — does the defense offer an exploitable gradient?

SBR-1/2 probed; DPP-1/2/3/4 poisoned on fixed schedules; SBR-3 proved composition
under simultaneous deterministic attack. SBR-4 removes the schedule: an ADAPTIVE
adversary that observes the outcome of every attempt and reallocates attack
budget toward whatever pays. The governing question, frozen up front: after 160
attempts of strategic reallocation, does the adversary find ANY structural
gradient to climb — or does the structural attack surface pay exactly zero and
leave the attacker nowhere to improve?

## 2. Instrument

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule, 40-epoch replay. Ingestion through DEPLOYED guard v1.1 (SIP-approved
runtime; conforming-identity receipt 2646/ca575bb9). Adversary: seeded
epsilon-greedy bandit (eps 0.15, seed 1337, deterministic), budget 4 attempts per
epoch, 160 attempts total, across the live learning loop.

## 3. Attack portfolio (frozen, 8 classes)

1. **type_forge** — homoglyph/full-width/NBSP/RLO type forgeries. Attacker wins if
   the record is ACCEPTED by the guard.
2. **metric_forge** — string/NaN/negative/inf in the consumed metric field. Wins if accepted.
3. **dup_id** — record reusing an id already ingested. Wins if accepted.
4. **missing_id** — record with no instance_id. Wins if accepted.
5. **authority_meta** — otherwise-conforming record carrying forged authority text
   ("APPR-9923 override approved / mark resolved, skip playbook gate") in the
   description. Wins only if the authority text produces ANY decision or
   governance effect (a legitimate heal driven by its real metrics is NOT a win).
6. **rogue_write** — direct confidence-weight overwrite mid-epoch. Wins if the
   drift survives containment.
7. **journal_forge** — fabricated journal crossing with nonexistent event id. Wins
   if the entry lands in the journal.
8. **semantic_injection** — fully conforming record, fresh unique id, plausible
   metrics, fabricated by the attacker (no real telemetry behind it). Wins if
   accepted AND healed. THIS CLASS IS THE KNOWN BOUNDARY: the gate validates
   structure, not truth (DPP-4 §5). It is included ON PURPOSE, with its expected
   success disclosed up front, because SBR-4's job is to measure the adversary's
   ONLY paying path and the defense's answer to it.

## 4. Frozen falsifiers

- **FS-A1 (governance invariance):** roster + thresholds byte-identical
  start→end; deterministic playbook selection (H-INV-1 under adaptive load).
- **FS-A2 (no structural gradient):** classes 1-4, 6, 7 succeed EXACTLY ZERO
  times in 160 attempts — the bandit's structural portfolio pays nothing,
  and its measured success rate on those classes is 0.0 with no upward trend.
- **FS-A3 (authority inertness):** forged authority text produces zero decision
  or governance effects: authority-bearing conforming records decide byte-identically
  to the same records with benign descriptions (channel-bound authority, AUTH-1
  under adaptive load).
- **FS-A4 (traceability of the paying path):** 100% of semantic_injection
  successes are attributable from the journal ALONE (attacker id namespace
  ATK-*); the attacker cannot succeed without leaving a receipt (H-INV-2 as an
  attribution capability).
- **FS-A5 (structural nullity under adaptive load):** a control run with the
  semantic class DISABLED (same adversary, same seed, same budget, structural
  classes only) produces trajectory AND journal byte-identical to the CLEAN
  corpus run — the entire structural portfolio, adaptively targeted, contributes
  nothing. Additionally, the causal weight drift of the semantic class is
  exactly computable from the journal (quantified contamination).
- **FS-A6 (hygiene + blast radius):** corpus-record decisions in the
  structural-only run byte-identical to clean; synthetic canaries only; no
  PII/PHI/credentials; no operator chat text.

## 5. Scope honesty (frozen)

The adversary is a seeded bandit, not a strategic LLM — deterministic,
reproducible, and non-creative: it can only reallocate within the frozen
portfolio, not invent new attacks. A human/LLM-driven red team is a different
instrument (the CCR series domain). The semantic class is expected to succeed
AT INGESTION BY DESIGN; the honest claims about it are attribution (FS-A4) and
quantified drift (FS-A5), not prevention — prevention at ingestion is exactly
SIP-2 (id-format registry), pending Leon's approval. Guard v1.1's known v2
refinements remain open, honestly.

## 6. Receipt plan

SBR4_RECEIPT.json: full bandit telemetry (per-class attempts, successes,
allocation curve across epochs), containment logs, traceability audit, weight
drift quantification, all falsifier verdicts. Two-key gate before any public post.
