# Dual Mesh Benchmark — DeepSeek B1-Baseline-Style Leg Preregistration (UNEXECUTED)

**Series signature:** dual_mesh_benchmark_deepseek_20261013
**Prereg committed:** 2026-10-13, BEFORE any execution.
**Owner authorization:** Leon GO (chat authorization, Oct 13, 2026, immediately after the CCR-4X leg I re-run, with the OpenRouter credit top-up supplied for this batch).
**Lineage:** extends the Dual Mesh Benchmark series (v1.0 DOI 10.5281/zenodo.23303081, v2.0 DOI
10.5281/zenodo.23321637) and XPLAT-2/3 (raw external API vs conversation-loop decomposition, ~41x
orchestration gap). This leg adds a DeepSeek v4-pro column to the raw-external-API baseline.

## Purpose

The CCR-4X leg I re-run made DeepSeek v4-pro the eighth engine in the containment series with a
conforming capture. This leg measures it on the frozen B1 benchmark corpus so the Dual Mesh
Benchmark gains a DeepSeek baseline: per-instance resolution latency and validated-tuple
correctness on the same 20-instance selection rule used by every B1 baseline leg.

## Protocol (fixed before execution)

1. **Corpus:** CORPUS_B1.json, sha256 13295d197be59dd1266814bc2f961f1e55e974c61c642fd9c7a6a389668fee59
   — identical file to all prior legs (verified on the staged copy). Selection rule: **first 20
   instances in file order** (same rule as B1 baseline / ENV-B / XPLAT-3/4).
2. **Engine & route:** OpenRouter chat/completions direct, model `deepseek/deepseek-v4-pro`,
   model_returned recorded per call. No Base44 conversation loop: this is a raw external API leg,
   explicitly NOT comparable wall-clock to the conversation-loop medians (XPLAT-2/3 doctrine).
3. **Task & prompt contract:** byte-equivalent to the frozen B1 baseline prompt (deterministic
   instructions, 3-entry roster with platform playbook_ids, single anomaly per call,
   confidence_score 0.9, required output: JSON array of exactly one tuple, keys position,
   anomaly_type, playbook, playbook_id, match_type, steps_executed, status, position 0).
   Fresh request per instance, stateless, no conversation reuse (FB-7 analog).
4. **Metrics (preregistered, no additions):** per instance — wall-clock ms (request sent to
   full response received), strict validity (byte-parseable conforming tuple), normalized
   validity (fences/whitespace-only normalization, both scores reported). Per leg — valid count
   (strict/normalized), median, p95 wall-clock ms, correctness vs expected_playbook.
   Comparison disclosures: v1.0 B1 mesh median 0.000443 ms (in-memory lookup, same corpus);
   v1.0 Automatic conversation-loop baseline median 4509.1 ms (different substrate — loop vs raw
   API — comparison is directional only, per XPLAT-2/3).
5. **Credit guard:** projected spend ~20 calls x ~$0.005 = ~$0.10 against the $10 balance; the
   leg aborts if a call returns a payment error, and the partial run is recorded, never retried
   silently (FB-1 discipline: no numbers without raw logs).
6. **Raw preservation:** all 20 raw responses preserved verbatim in the evidence folder.
7. **Expected tuples:** per corpus expected_playbook, all thresholds <= 0.9 → all 20 expected
   match_type "exact", steps_executed "isolation,healing,verification", status "resolved".
   Any deviation is a recorded FAIL, not a re-run.

## Falsifiers

- FBD-1: any published number without preserved raw logs = FAIL.
- FBD-2: corpus or selection differing from the frozen rule = FAIL.
- FBD-3: any run omitted or retried to improve the distribution = FAIL.
- FBD-4: any metric added post-execution without a committed prereg amendment = FAIL.
- FBD-5: any PHI, customer identity, or credential in a benchmark artifact = FAIL (synthetic corpus only).

## Claim discipline

This leg characterizes DeepSeek v4-pro via OpenRouter on the frozen 20-instance corpus, October
2026. It is a sampled-baseline measurement, not a certification of the engine, not a universal
performance claim, and not a wall-clock equality claim against conversation-loop legs. Dual Mesh
Benchmark status updates from NOT MEASURED to MEASURED for this column only after raw logs exist
and Leon reviews. Two-key curation before any public artifact.

> This software is a prototype and is provided for educational and research purposes only. It is
> not intended for production use, commercial deployment, or safety-critical environments. All
> systems are experimental and may contain defects on them.
