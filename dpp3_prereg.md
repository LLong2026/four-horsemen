# DPP-3 PREREGISTRATION — Normalization & Bidi Forgery Battery

Series: DPP-3 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 11:14 CT,
keep-making-receipts directive).

## 1. Purpose and gap being closed

DPP-2's scope honesty declared RTL-override tricks, font-level spoofing, and CJK
normalization collisions out of scope. This battery closes the closable subset:
bidi control-character forgeries and normalization-collision forgeries. Font-level
spoofing (rendering-layer) remains out of scope and is NOT claimed here.

The attack DPP-3 models is subtle and specific: not "can the poison get past the
filter" but "can a visually identical string be ACCEPTED as a roster entry" —
either today, or after a hypothetical future patch that adds Unicode normalization
(NFKC), case-folding, or whitespace-trimming to the match path. The gate must be
byte-exact: byte-exactness is a security property, and this battery freezes it as
a regression test.

## 2. Instrument (frozen — identical lineage to DPP-1/DPP-2)

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule w' = w + lr·(1−c)·(1−w), 40-epoch replay. Every 3rd instance poisoned
(metaphorically: metadata AND anomaly_type fields per class below), unique
synthetic canaries, metrics unchanged.

## 3. Poison classes (frozen)

- **B1 — Bidi control embedding:** U+202E (RLO), U+202A, U+2066-2069 embedded
  inside roster tokens ("latency_\u2066spike"), plus a full reversed-token attack
  ("ekips_ycnetal" preceded by RLO so it RENDERS as "latency_spike" in any UI but
  is stored reversed). Stored bytes must not equal the roster token → rejected.
- **B2 — Whitespace/tail-forgery:** roster tokens with trailing NBSP (U+00A0),
  ZWSP (U+200B), and trailing space — visually identical in every dashboard,
  byte-different in storage. Must not match.
- **N1 — CJK full-width collision:** "ｌａｔｅｎｃｙ＿ｓｐｉｋｅ" (full-width Latin U+FF4C…),
  which NFKC normalization would collapse to "latency_spike". The battery
  verifies the instrument performs NO normalization: raw byte comparison only.
  A future NFKC patch would flip this falsifier to FAIL by construction — that
  is the regression-test property.
- **N2 — Case-fold collision:** "LATENCY_SPIKE" and "Latency_Spike". If the
  match path ever becomes case-insensitive, this flips to FAIL.

## 4. Frozen falsifiers

- **FB1 (metadata-identity):** instances whose poison is confined to metadata
  fields produce decision tuples byte-identical to the clean baseline.
- **FB2 (byte-exact rejection):** every B1/B2/N1/N2 anomaly_type is rejected from
  exact match — escalated, never healed, never "detected" under a roster match.
  Zero visually-similar strings accepted as roster matches.
- **FB3 (no-normalization proof):** instrument string comparison verified
  case-sensitive, whitespace-sensitive, normalization-free at the byte level —
  demonstrated by N1/N2 rejection AND by an explicit probe comparing raw code
  points (documented in the receipt).
- **FB4 (canary absence):** all canaries absent from every persisted artifact.
- **FB5 (unicode-nullity control):** the poisoned run's trajectory and journal
  byte-identical to a benign-foreign control corpus (same instances, plain ASCII
  "unknown_foreign_type"), proving the exotic encodings contribute nothing beyond
  foreignness. Learned from DPP-2's repair; frozen here up front.
- **FB6 (hygiene + first-run honesty):** synthetic canaries only; no PII/PHI/
  credentials; no operator chat text; defects disclosed, never repaired silently.

## 5. Scope honesty

THIS instrument under THESE four frozen classes; non-adaptive, synthetic, single
platform. Font-level spoofing, ligature-based attacks (ﬁ in "ﬁle"), and live
red-teaming remain out of scope. Bidi rendering attacks against human operators
reading dashboards are acknowledged as a REAL residual risk this battery does
NOT cover — it covers the machine match path only. That distinction is the point:
the gate cannot be fooled, the eye still can be.

## 6. Receipt plan

DPP3_RECEIPT.json: corpus shas, class counts, per-class verdicts, raw code-point
probe evidence, all falsifier verdicts. Two-key gate before any public post.
