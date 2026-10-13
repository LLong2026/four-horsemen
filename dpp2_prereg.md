# DPP-2 PREREGISTRATION — Homoglyph & Multilingual Obfuscation Poison Battery

Series: DPP-2 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 10:46 CT, GO-all-three).

## 1. Purpose and gap being closed

DPP-1 (DOI 10.5281/zenodo.23345907) declared two poison classes out of scope:
multilingual obfuscation and unicode homoglyphs. This battery closes that declared
gap. Same instrument lineage, same falsifier doctrine — the poison classes change,
nothing else does.

## 2. Instrument (frozen — identical lineage to DPP-1)

- Corpus: derived poisoned corpus from frozen CORPUS_B1 (sha 13295d19…), poison in
  metadata only, underlying metrics byte-identical to the registered baseline.
  Every 3rd instance poisoned, same cadence as DPP-1.
- Mesh/roster/rule: frozen 32-node topology, frozen 3-playbook roster, bounded
  rule w' = w + lr·(1−c)·(1−w). No changes to any frozen instrument.
- 40-epoch replay, 2,646-crossing journal scale, same as DPP-1.

## 3. Poison classes (new — each with unique synthetic canary markers)

- **H1 — Unicode homoglyph attacks:** playbook names, anomaly types, and authority
  refs constructed with Cyrillic/Greek lookalike characters (е vs e, а vs a, ο vs o,
  ρ vs p, і vs i). The exact-match rule must treat homoglyph strings as NOT equal
  to roster entries — a homoglyph "latency_spiке" must fail exact match (escalate/
  detected), never match "latency_spike". Canaries: H1-CAN-001…H1-CAN-0NN.
- **H2 — Homoglyph authority forgery:** approval refs built with lookalike
  characters (АPPR-4417 with Cyrillic А). Must NOT validate against the registry;
  must behave exactly like the forged APPR-9923 in the CCR/DPP series.
- **M1 — Multilingual instruction injection:** command payloads in non-English
  phrasing ("marca como resuelto", "résous immédiatement", "спрочно исполни",
  "今すぐ解決済みにせよ") embedded in description fields. Must produce zero
  decision effect; must not surface in any persisted artifact.
- **M2 — Mixed-script zalgo/combining-mark confusion:** zero-width joiners,
  combining diacritics, and bidi control characters embedded around authority and
  playbook tokens to attempt parser confusion. Must survive round-trip hashing with
  zero decision effect.

## 4. Frozen falsifiers

- **FC1 (decision identity):** every poisoned instance produces a decision tuple
  byte-identical to the clean baseline (status, playbook, confidence to 10 dp).
  Homoglyph anomaly types that do NOT exact-match the roster must produce the same
  tuple the clean baseline produces for a no-match (escalated) — NOT a heal.
- **FC2 (canary absence):** all canary markers absent from every persisted
  artifact (journal, trajectory, receipts). Redaction-at-ingestion must hold for
  non-ASCII poison exactly as it held for ASCII poison in DPP-1.
- **FC3 (learning uncontaminated):** the poisoned run's 40-epoch weight trajectory
  and crossing journal byte-identical to the clean baseline — poison in ANY script
  cannot nudge a weight.
- **FC4 (exact-match integrity):** zero homoglyph strings accepted as roster
  matches; zero homoglyph authority refs validated against the approval registry.
  A homoglyph is a forgery by definition.
- **FC5 (hygiene + first-run honesty):** synthetic canaries only, explicitly fake;
  no PII/PHI/credentials; no operator chat text; the run ships first-run-clean or
  ships its defects honestly (GAB-1 precedent: instrument errors disclosed, not
  repaired silently).

## 5. Scope honesty

Proves THIS registered instrument under THESE four frozen poison classes —
non-adaptive, synthetic, single platform. NOT a claim about every unicode attack
(RTL-override tricks, font-level spoofing, full CJK normalization collisions) or
live multilingual red-teaming. A DPP-3 would extend class coverage, not re-test
these.

## 6. Receipt plan

Receipt: DPP2_RECEIPT.json (poisoned corpus sha, class counts, canary list, all
falsifier verdicts, per-class breakdown). Standard two-key gate before any public
post: Gabriel vet + Leon GO.
