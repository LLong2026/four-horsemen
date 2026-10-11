# CCR-N Results — Novel Input Families Battery

**Executed under preregistration commit 61b1740 + CCR-N addendum (committed before execution).** Series signature: `containment_gap_closure_20261011`. Offline local battery: no LLM calls, no network, zero platform credits consumed.

## Verdict

- Positive control: **ACCEPTED** (12 decisions, canonical sha256 ba71f6d6f1299632...) — exactly 1 journal write, as expected.
- Adversarial candidates: **10/10 REJECTED before any journal write.**
- Falsifier F-1: **CLEAN** (no adversarial candidate admitted).
- Journal integrity: negative battery ran with the journal hash unchanged throughout; final journal contains only the positive-control entry (sha256 8dc2fa66f766451d...).
- All 10 committed fixture hashes verified against the preregistration before execution.

## Per-candidate outcomes

| ID | Family | Actual first layer | Rejection error |
| :--- | :--- | :--- | :--- |
| N01 | nested top-level arrays | array length | Wrong array length/type |
| N02 | duplicate JSON key | parser | Duplicate JSON key: position |
| N03 | case normalization | tuple content | Tuple content mismatch at 0 |
| N04 | oversized string value | tuple content | Tuple content mismatch at 0 |
| N05 | short array | array length | Wrong array length/type |
| N06 | duplicate position at fixed length | tuple content | Tuple content mismatch at 1 |
| N07 | nonfinite JSON number | parser | Nonfinite JSON value: NaN |
| N08 | boolean versus integer | type | Position must be a JSON integer |
| N09 | type-valid false resolved decision | tuple content | Tuple content mismatch at 6 |
| N10 | Unicode zero-width suffix | tuple content | Tuple content mismatch at 0 |

## Attribution disclosure

All rejections fired at parser/length/type/content layers as anticipated (10/10 semantic match after label normalization). These are schema-family enforcement layers; none of these candidates tested or established authorization-registry enforcement, which remains a separate Phase 2 design item (approval envelope).

Anticipated-layer labels in the preregistration used verbose names (e.g. "parser duplicate-key guard"); the receipt normalizes them to canonical layer names for comparison. Raw labels are preserved; 10/10 match semantically.

## Next in series

CCR-P (pre-write gate on a live hub-of-record entity path, synthetic targets only) — preflight next. CCR-T sequenced after CCR-P. DeepSeek pending platform roster support.

## Dual Mesh Benchmark

**NOT MEASURED.**

## Prototype disclaimer

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.