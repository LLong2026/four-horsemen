# SBR-6 Runlog

- Preregistration frozen: commit 33f00ec (sbr6_prereg.md sha 360457c3, runner v1.0 sha 482aa059, snapshot sha 1ec301e4) — BEFORE draw and execution.
- Seed: 442c6ab (ledger HEAD at registration, commit 442c6ab / ledger 0142).
- Draw (seeded PRNG, recorded in prereg-computed draw): PORTCULLIS-SILENCE, PORTCULLIS-REPLAY, SENDER-GATE, H-INV1-GOV, RECOMPUTE-KAT, LEDGER-IMMUT.
- v1.0 run: 5/6 — PORTCULLIS-REPLAY FAIL. Root cause: authoring defect — v1.0 pre-populated the used-nonce set, making the probe structurally impossible to pass. The system under test was never at fault. v1.0 FAIL receipt preserved in git history (commit 7dba63a).
- Amendment v1.1 (forward-only, reason disclosed): corrected semantics in sbr6_runner.py; committed before re-run.
- v1.1 re-run: 6/6 PASS. Receipt sha256 90e1414d18f07d5cf381933038ed6b4b994a1f90a31233f2e17e69e202e69d0a.
- Ledger: 0143 (execution + amendment disclosed).
- Determinism: no LLM in the decision path; all probes synthetic, hub-local; frozen gate semantics from HACK-7 / Wave-2 harnesses.
- Fourth program-wide instance of the preregistration discipline catching an authoring defect before it could masquerade as a result (HACK-7 x3, SBR-6 v1.0).
