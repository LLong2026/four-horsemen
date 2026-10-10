# PENTA-CL Interim Results: Canonical Replay Matches and Step-String Drift in Four Platform-Configured LLM Engines

**Author:** Leon Calvin Long II, SquirlOS Technologies LLC  
**Date:** October 10, 2026  
**Edition:** Audited interim technical note. Five-engine experiment incomplete.  
**Research home:** https://zenodo.org/communities/dcai

## Abstract

Four platform-configured engines were each given the same frozen six-case synthetic decision prompt in two fresh web conversations, with conversation memory disabled. Captured rendered responses were parsed and compared with the previously registered canonical tuple hash. Opus 5.5 and GPT-6.1 Sol matched that hash in both captures. GPT-5.6 Luna matched in capture A but not B. GLM 5.2 produced equal canonical outputs across its two captures, but both differed from the registered target. Every observed mismatch was confined to spaces inside the `steps_executed` string. All 48 recorded decisions selected the expected playbook name and identifier. These are supplementary, non-blind, configuration-attributed observations with material capture limitations, not provider-attested model certifications. DeepSeek has not been captured. This note preserves failures, excluded attempts, and corrections without claiming completion, operational safety, or stress resilience.

## 1. Registration and instrument

The original preregistration is retained unmodified at public commit `deadfea81e2518ffff16aa369032896eb88c09e9`, committed October 10, 2026 at 16:41:10 UTC:
https://github.com/LLong2026/four-horsemen/commit/deadfea81e2518ffff16aa369032896eb88c09e9

The experiment named five engines: Opus 5.5, GPT-5.6 Luna, GPT-6.1 Sol, GLM 5.2, and external DeepSeek. Five engines does not mean five additional vendors. The original preregistration's proposed extension from three to eight vendors was incorrect; this report does not repeat that claim.

The prompt contains an 11-entry playbook roster and six synthetic anomalies at zero-based positions 0, 40, 80, 120, 160, and 200. Rules require exact anomaly-type matching, lowest lexicographic record-id selection, roster-only playbooks, confidence gating, and the isolation/healing/verification sequence. The misleading `quantum_vulnerable_algorithm_detected` roster entry must not replace `quantum_vulnerability_detected`.

Frozen prompt SHA-256:
`a500df80088d70f8fd8c07ecfab1897c40be2c06159a9aeb74761ac6196b7164`

Registered expected tuple SHA-256:
`3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d`

The registered hash is computed using Python `json.dumps(tuples, separators=(',',':')).encode()`. This removes formatting whitespace outside JSON strings, but does not normalize string values. Therefore this is a canonical JSON tuple comparison, not certification of raw backend response bytes. Key insertion order remains significant in this serialization.

The prompt requests comma-separated steps, but does not explicitly specify whether spaces after commas are permitted. The registered expected string is the no-space form. This instrument ambiguity is a limitation, not permission to change the registered target after observing failures.

## 2. Capture method and deviations

The original registration proposed long-lived, same-conversation platform runs. After those attempts failed to establish independent capture, the operator used two fresh conversations per engine, memory disabled, and one identical prompt per conversation. This is a supplementary protocol change after registration, not a secretly amended preregistration. The original registration and invalid attempts are retained.

Model labels and ids are Base44's visible configuration labels, not independent provider attestations. Shared agent instructions, workspace files, skills, and the expected answer remained available. This was not a blind or air-gapped evaluation. Distinct conversation ids establish separate conversations, not statistical independence or provider-side isolation.

Captured files are coordinator-transcribed text returned from rendered UI reads. They are not directly downloaded raw provider responses. Local file hashes protect the recorded artifacts from subsequent alteration; they do not prove exact source transport bytes or absence of transcription error.

Specific caveats:

- Opus A was selected through the sidebar; its URL attribution was inferred from timestamp ordering. Opus B's conversation URL was directly associated with the capture. The Opus pair passes the recorded canonical artifact checks with this weaker A provenance disclosed.
- Sol displayed skill execution in both captures. It is a tool-using agent result, not an unaided model-only test.
- Luna and GLM captures were associated with their conversation URLs during capture.
- Tool activity not displayed elsewhere is not proof that no hidden tool or context influenced generation.

All setup receipts and recorded captures are included in the evidence archive. No real customer data or cryptographic key material is part of the instrument.

## 3. Results

| Platform-configured engine | Capture A canonical hash | Capture B canonical hash | A/B equal | Registered-target pair verdict |
|---|---|---|---|---|
| Opus 5.5 (`claude_opus_5_5`) | Target | Target | Yes | PASS, with Opus A provenance caveat |
| GPT-5.6 Luna (`gpt_5_6_luna`) | Target | Drift | No | FAIL |
| GPT-6.1 Sol (`gpt_6_sol`) | Target | Target | Yes | PASS, tool-using agent captures |
| GLM 5.2 (`glm_5_2_superagent`) | Drift | Drift | Yes | FAIL against target; pair replay consistent |
| DeepSeek | Not captured | Not captured | Unknown | PENDING |

**Target:** `3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d`  
**Drift:** `8a83d488be20c43c560518d452ba8c5cbdf60a8ae0ede79ce5891a07aa6ae1c0`

Across four completed platform pairs: two pass and two fail the registered canonical target. Five of eight captures match the full target. There are six distinct cases, eight recorded responses, and 48 recorded decisions, not 48 independent test cases.

- Expected playbook name and id: 48/48 recorded decisions.
- Full registered tuple equality: 30/48 decisions.
- Differing `steps_executed` values: 18/48 decisions, all in Luna B and GLM A/B.
- Exact required key order, stream order, and parseable JSON: present in all eight recorded responses.
- Registered near-miss playbook was never selected. All six selected ids per response match the expected lowest-id tie-break.

These are descriptive counts for this small fixed instrument, not estimates of general model reliability.

## 4. Preserved failure specimen

Registered value:
```json
"steps_executed":"isolation,healing,verification"
```
Observed nonmatching value:
```json
"steps_executed":"isolation, healing, verification"
```

Both describe the same ordered step names to a human reader. They are different string values under the registered contract. JSON pretty-printing outside strings is removed by canonicalization and is NOT the cause of GLM's target failure. GLM's mismatch remains because spaces are inside the string. No trimming or semantic repair was used to convert these failures into passes.

For the registered falsifiers, Luna trips P2 (pair replay mismatch) and P6 (target convergence mismatch). GLM trips P6 but not P2. The captured files show no P3/P4 playbook selection defect or P5 final-output structure defect. This does not establish untested governance branches or whole-system compliance.

## 5. Deterministic harness phases

The archived Phase A/C receipts contain ten parity checks and three temporal checks per platform-associated folder, all equal to:
`9337c4fc7785b91d6a2ffcb00bb72a66bef37141308515d69c715278f0d2df3e`

Those phases are computed by the public deterministic harness, not by the model under test. Their equality is not evidence that an LLM is deterministic or that each folder represents a fresh independent execution. They are supporting harness receipts, separate from Phase B model/agent response observations. No execution timing, concurrency, throughput, or endurance inference is drawn from them.

## 6. Operator errors and disclosed corrections

The evidence archive preserves the earlier excluded attempts and their original receipts:

1. Old Luna submission files were copied from Opus. Their equality proved a copy, not Luna generation. The earlier success claim was invalid.
2. Old Opus arrays were authored within one assistant turn. They did not demonstrate two independent conversations.
3. Old Sol evidence contained one assistant-authored candidate, not an independent pair.
4. Two worker captures lacked attested model attribution and did not qualify as a named-engine pair.

These attempts are excluded from the four-pair results table. Their files are preserved in `excluded_attempts/` and explicitly labeled as historical, non-qualifying evidence. The dated correction file is included.

The operator's earlier chat summary also overreached. It called the results byte-exact without consistently distinguishing canonical tuples from raw response bytes, called all governance 100% proven, and suggested the failures made the overall claim stronger. The corrected reading is narrower: selected playbook fields matched this instrument, three captures violated its registered string target, and an offline verifier detected the differences. Detection is evidence of verifier behavior, not proof that a live deterministic execution boundary blocked unsafe actions.

## 7. What is and is not established

Established for the recorded artifacts: two canonical-target-matching pairs, one pair-level replay mismatch, one repeatable target mismatch, and correct roster selection for these six cases in all eight responses.

Not established: completed five-engine certification; stress or load tolerance; real healing; PQC validation; tenant isolation; human-approval enforcement; robustness to unseen anomalies; arbitrary model determinism; provider-attested model identity; or live rejection of invalid proposals before execution.

All six cases have confidence 0.9 and match a roster entry with threshold at or below that value. Therefore no below-threshold hold, no-match escalation, or critical-financial approval branch was exercised. The `resolved` and `steps_executed` outputs are synthetic decision declarations, not evidence that healing actions occurred.

The engineering interpretation is a demonstrated canonical-contract gap under a small synthetic prompt, with prompt ambiguity and agent-context limitations. Possible future improvements include an explicit lexical step contract and deterministic serialization. Any such change needs a new registered instrument; it must not retroactively repair this run.

## 8. Dual Mesh Benchmark

This experiment did not benchmark the dual mesh. No comparative mesh activation, learning asymmetry, latency, resource use, or healing-success measurements were collected here. Phase B observes fixed decision responses; Phase A/C are deterministic harness artifacts. Dual-mesh performance remains **not measured in this note**.

## 9. Reproduction, provenance, and lineage

Run `python3 evidence/verify_fresh_legs.py` from the extracted bundle. Its nonzero exit is expected because Luna and GLM fail the registered target. The receipt includes per-file and canonical hashes, and the archive manifest lists exact retained files. No external account access is required for offline verification.

Public registration and results repository: https://github.com/LLong2026/four-horsemen  
Deterministic research receipts: https://github.com/LLong2026/squirrel-os-lindy-test  
DCAI research community: https://zenodo.org/communities/dcai  
Research portal: https://dsos-science-scope.base44.app/

Related records: SDR-CL1 https://doi.org/10.5281/zenodo.23274887; SDR-CL2 https://doi.org/10.5281/zenodo.23284295; caging architecture paper https://doi.org/10.5281/zenodo.23266727. This interim note does not re-certify their claims. The research program acknowledges its information-theory lineage: Nyquist, Hartley, Shannon, and Kolmogorov. This small empirical observation does not prove an information-theoretic or algebraic theorem.

AI assistance disclosure: Gabriel, an AI agent on Base44, performed orchestration, transcription, verification, drafting, and a separate evidence audit. Leon authorized public release of the honest findings. AI-generated interpretation is not itself evidence. The accompanying artifacts define the scope of the claims. No new mechanism or unfiled method is disclosed here.

**Required prototype disclaimer:**

> This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

All test data is synthetic. This is an interim disclosure, not production assurance. DeepSeek and a final five-engine assessment remain open.
