# Dual Mesh Benchmark — Multi-Engine Extension (DMB-X) Preregistration (UNEXECUTED)

**Series signature:** dual_mesh_benchmark_X_20261013
**Prereg committed:** 2026-10-13, BEFORE any execution.
**Owner authorization:** Leon GO (chat authorization, Oct 13, 2026, 12:44 CT —
measure the remaining DMB figures; operator wording not quoted per standing rule).
**Lineage:** extends DMB v1.0 (DOI 10.5281/zenodo.23303081), v2.0 (DOI
10.5281/zenodo.23321637), and the DeepSeek B1 column (DOI 10.5281/zenodo.23345241).
This extension fills the per-family raw-external-API columns on the frozen B1 corpus.

## Purpose

The day's receipts carry "Dual Mesh Benchmark: MEASURED (DeepSeek column); all
other figures NOT MEASURED." This leg measures the other figures: one
representative engine per model family, same instrument, same corpus, same
selection rule, same prompt contract — making the raw-API columns
cross-comparable within their substrate (XPLAT-2/3 doctrine: raw API legs are
NOT comparable wall-clock to conversation-loop medians; comparison is
directional only across substrates).

## Protocol (fixed before execution)

1. **Corpus:** CORPUS_B1.json, sha256
13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59. Selection
rule: first 20 instances in file order (identical to every prior B1 leg).
2. **Engines (one per family, 8 columns):**
   - openai/gpt family: ~openai/gpt-mini-latest
   - anthropic/claude family: ~anthropic/claude-haiku-latest
   - google/gemini family: ~google/gemini-flash-latest
   - x-ai/grok family: x-ai/grok-4.7
   - alibaba/qwen family: qwen/qwen3.8-omni-flash
   - mistral family: mistralai/mistral-small-3.2-24b-instruct
   - meta/llama family: meta-llama/llama-4-scout
   - deepseek family (flash tier — distinct column from the measured v4-pro):
     ~deepseek/deepseek-flash-latest
   Engine ids as listed on the OpenRouter models endpoint at prereg time;
   model_returned recorded per call. A 404 on any id at run time = recorded
   substitution attempt is NOT allowed — that column is recorded as UNAVAILABLE,
   never silently swapped.
3. **Route:** OpenRouter chat/completions, raw external API, stateless, fresh
   request per instance, model_returned recorded per call.
4. **Prompt contract:** byte-identical to the frozen B1 baseline prompt
   (deterministic instructions, 3-entry roster with platform playbook_ids,
   single anomaly per call, confidence_score 0.9, required output: JSON array
   of exactly one tuple, keys position, anomaly_type, playbook, playbook_id,
   match_type, steps_executed, status, position 0).
5. **Metrics (preregistered, no additions):** per instance — wall-clock ms,
   strict validity, normalized validity. Per leg — valid count (strict/normalized),
   median, p95, correctness vs expected_playbook. Per engine family column:
   recorded alongside the DeepSeek v4-pro column, same substrate class.
6. **Credit guard:** legs run only when the OpenRouter balance is at least
   $2.00 (projected total spend across 8 legs: $0.80-$4.00 at flash/mini/haiku
   tier pricing; grok-4.7 is the price outlier). Any payment error aborts the
   batch; the partial run is recorded, never retried silently. An engine
   whose single-call cost would exceed $0.25 is skipped as UNAVAILABLE-cost,
   recorded, not measured.
7. **Raw preservation:** all raw responses preserved verbatim per engine in
   dmb_x_evidence/<engine>/.
8. **Expected tuples:** all 20 per leg: match_type "exact", steps_executed
   "isolation,healing,verification", status "resolved". Any deviation is a
   recorded FAIL, not a re-run.

## Falsifiers

- FBX-1: any published number without preserved raw logs = FAIL.
- FBX-2: corpus/selection differing from the frozen rule = FAIL.
- FBX-3: any run omitted or retried to improve the distribution = FAIL.
- FBX-4: any metric added post-execution without a committed prereg = FAIL.
- FBX-5: any silent engine substitution = FAIL (UNAVAILABLE is the only honest state).

## Out of scope (unchanged)

The XPLAT-4 conversation-loop per-model matrix remains blocked on the model-pin
limitation (N-B6 alert, manual gate). Raw-API wall-clock vs conversation-loop
medians remain non-comparable per XPLAT-2/3 doctrine.

**Dual Mesh Benchmark status at prereg time: MEASURED (DeepSeek v4-pro column,
DOI 10.5281/zenodo.23345241); all other figures NOT MEASURED. This prereg exists
to change that, honestly or not at all.**
