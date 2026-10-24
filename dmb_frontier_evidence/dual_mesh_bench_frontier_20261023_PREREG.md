# Dual Mesh Benchmark — Frontier Raw-API Leg (Opus 5.5 + GPT-6.1 Sol) Preregistration (UNEXECUTED)

**Series signature:** dual_mesh_benchmark_frontier_20261023
**Prereg committed:** 2026-10-23, BEFORE any execution.
**Owner authorization:** Leon GO (chat authorization, 2026-10-23, 21:50 CT — "dual mesh benchmark first" for the DOORS benchmark post).
**Lineage:** extends the Dual Mesh Benchmark series (v1.0 DOI 10.5281/zenodo.23303081, v2.0 DOI
10.5281/zenodo.23321637), the DeepSeek B1 column (concept DOI 10.5281/zenodo.23345060, v2 DOI
10.5281/zenodo.23345241), and the DMB-X 8-column matrix (ledger 0081, instrument dmbx_runner.py,
commit b293d58). This leg adds TWO frontier engine columns never before measured raw-API on the
frozen corpus: anthropic/claude-opus-5.5 and openai/gpt-6.1-sol (both previously measured only in
conversation-loop substrate: PENTA-CL v1/v2, CCR series — XPLAT-2/3 doctrine: not wall-clock
comparable across substrates).

## Purpose

The DOORS series closed the production-reach red-team of the deterministic action gates. The Dual
Mesh Benchmark characterizes the OTHER side of the dual-mesh doctrine: how the strongest available
LLM engines behave on the frozen B1 corpus when proposing decision tuples, versus the deterministic
mesh's in-memory lookup. Adding the two strongest frontier columns (Opus 5.5, GPT-6.1 Sol) completes
the matrix's coverage at the frontier: per-instance resolution latency and validated-tuple
correctness on the same 20-instance selection rule used by every B1 leg.

## Protocol (fixed before execution)

1. **Corpus:** CORPUS_B1.json, sha256 13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59
   — identical file to all prior legs. Selection rule: **first 20 instances in file order**.
2. **Engines & route:** OpenRouter chat/completions direct, models `anthropic/claude-opus-5.5` and
   `openai/gpt-6.1-sol`, model_returned recorded per call. Raw external API leg; explicitly NOT
   wall-clock comparable to conversation-loop legs (XPLAT-2/3 doctrine).
3. **Task & prompt contract:** byte-identical to dmbx_runner.py (commit b293d58): deterministic
   instructions, 3-entry roster with platform playbook_ids, single anomaly per call,
   confidence_score 0.9, required output JSON array of exactly one tuple, position 0. Fresh
   stateless request per instance, no conversation reuse.
4. **Metrics (preregistered, no additions):** per instance — wall-clock ms, strict validity,
   normalized validity, correctness vs expected tuple. Per leg — valid counts, median, p95,
   cost. Comparison disclosures: v1.0 B1 mesh median 0.000443 ms (in-memory lookup);
   conversation-loop baseline 4509.1 ms (different substrate, directional only).
5. **Credit guard:** projected spend ~40 calls x <= $0.01 = <= $0.40 against ~$18.6 balance;
   abort on payment error (402/403), partial run recorded, never silently retried.
6. **Raw preservation:** all 40 raw responses preserved verbatim in the evidence folder.
7. **Expected tuples:** per corpus expected_playbook; thresholds <= 0.9 → all 20 expected
   match_type "exact", steps_executed "isolation,healing,verification", status "resolved".
   Any deviation is a recorded FAIL, not a re-run.
8. **Order:** opus_5_5 leg first, then gpt_6_1_sol. No other engines added without a committed
   amendment.

## Falsifiers

- FBF-1: any published number without preserved raw logs = FAIL.
- FBF-2: corpus or selection differing from the frozen rule = FAIL.
- FBF-3: any run omitted or retried to improve the distribution = FAIL.
- FBF-4: any metric added post-execution without a committed prereg amendment = FAIL.
- FBF-5: any PHI, customer identity, or credential in a benchmark artifact = FAIL (synthetic corpus only).
- FBF-6: any claim beyond the tested columns/substrate = FAIL.

## Claim discipline

This leg characterizes two frontier engines via OpenRouter on the frozen 20-instance corpus,
October 2026. Sampled-baseline measurement, not an engine certification, not a universal
performance claim, not a cross-substrate wall-clock equality claim. Dual Mesh Benchmark status
updates to MEASURED for these two columns only after raw logs exist and Leon reviews. Two-key
curation before any public artifact.

This software is a prototype and is provided for educational and research purposes only. It is not
intended for production use, commercial deployment, or safety-critical environments.
