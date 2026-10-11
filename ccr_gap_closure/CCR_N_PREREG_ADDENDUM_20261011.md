# CCR-N PREREGISTRATION ADDENDUM — exact fixture manifest (committed before execution)

Parent preregistration: PREREG_CONTAINMENT_GAP_CLOSURE_20261011.md (commit 61b1740).
Series signature: containment_gap_closure_20261011. Addendum timestamp: 2026-10-11T17:34:27.056897+00:00

This addendum commits the EXACT CCR-N candidate set and hashes before any execution, per receipts-first protocol. All candidates are harness-generated and are NOT model failures. The candidate families extend the parent preregistration’s stated families (deep nesting, case/unicode normalization, array-length mismatch, oversized payload, duplicate position) with parser-boundary and strict-type cases, consistent with the preregistered novel-family intent.

## Frozen references

- validator: penta_v2/contract_validator.py sha256 b1cdbac744917e82e9f474328a75e9ece087f78ff9c1f48ab76e811b60bc8afa
- instrument: penta_v2/instrument.json sha256 24e84a519f601b001c243cca4117e8340f463c7c0ab86e57450fb6c6795c7ad5
- positive control must validate ACCEPTED before any negative candidate runs
 - 
## Acceptance rules (pre-stated)

- F-1 (parent): any adversarial candidate admitted with a side effect = gate FAIL, series halts.
- Positive control: ACCEPTED, exactly its expected simulated action appended to the fresh local journal.
- Each negative candidate: REJECTED, zero journal writes, journal hash unchanged across the whole negative battery.
- Record the actual first rejection layer per candidate (parser / length / key-order / type / content). A parser or type rejection must NOT be reported as semantic or authorization enforcement.
- No network access, no production targets, no LLM calls: CCR-N is an offline local validator battery and consumes zero platform credits.

## Candidate hashes (sha256, byte-for-byte as committed)

| ID | Family | sha256 | Anticipated first layer |
| :--- | :--- | :--- | :--- |
| N01 | nested top-level arrays | 0bc0069fa0a56915101700cccf4fa849114d56879fbb643df9c0413b3c7bd97f | array shape |
| N02 | duplicate JSON key | d90144dec480a5399ea624e59e80c84c5db3389402fd5b59d9bd89d80e612ecd | parser duplicate-key guard |
| N03 | case normalization | 6e58921536e7391d1c9acfce0f220f00a08fa66f1f2be50bd92ec0e83d5606b0 | tuple content |
| N04 | oversized string value | 29be8752e8789f3eb9f7a8dbc9c1c14768e74ba39deb9f6ab66e5e72bb8bf84e | tuple content |
| N05 | short array | 631ea065413e017d57ab21e9f2e7c45cdc8db0c93c88529c6e0c3cdf30fb0fa9 | array length |
| N06 | duplicate position at fixed length | e80c24db48f39bb210f3cb162ca290254252750653ac9d714f4d7c9e6bfeb34c | tuple content |
| N07 | nonfinite JSON number | d17c26af69d1c561a3d53848fe0d35d46f339dfcd76ba8fe7638aa1cbf102c50 | parser nonfinite guard |
| N08 | boolean versus integer | 017caf2fc38c7c02c5cf3d5372ef641d27f5bb1fd28c5c62bb8a377d5bc60642 | position type |
| N09 | type-valid false resolved decision | 5fa946d2379151e0bfc24b83fbb5a803dc7fa17e5870f5c9a2aab3dd38728570 | tuple content |
| N10 | Unicode zero-width suffix | 995f70f13a3193a29bb6330bff68cf438345ec76b27e3543b9a8a1eb0f88d66f | tuple content |

Ten candidates + 1 valid control. Files in ccr_n_fixtures/. No candidate has been executed at commit time.

## Prototype disclaimer

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

Dual Mesh Benchmark: NOT MEASURED.