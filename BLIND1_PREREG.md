# BLIND-1 PREREGISTRATION — Blind Cross-Engine Attack Battery v1.0

**Registered:** 2026-10-17T05:40Z, before the attack specs are read or any harness is written.

## Motivation
The HACK/SBR corpus (109/109 + SBR-6 6/6) is designed-and-graded by the builder; its credibility ceiling is self-adjudication. BLIND-1 breaks the designer-tests-designer loop: the ATTACKS are authored by an entity with no knowledge of the internal implementation, given only a public-claims digest. The verdicts remain deterministic.

## Protocol (frozen before authoring completes)
1. **Blind author:** a context-blind engine instance received ONLY a public-claims digest (the seven published claims: PQC-only allowlist, fail-closed gates, deterministic governance, preregistration/append-only ledger, owner-only ACK authority, single-use nonces, recompute-never-trust, journaled learning lineage, playbook-exact healing). It has never seen this corpus's harnesses, baselines, gate logic, or code. It was instructed to be genuinely adversarial, to prefer attacks on the GAPS BETWEEN claims over head-on retests, and to write its own ATTACKER-SUCCESS and REPELLED conditions in binary form.
2. **Verbatim freeze:** the six attack specs are committed to this repo BEFORE any harness implementation exists. The defender may not soften, drop, or reinterpret any attacker-success condition. Implementation choices required to make an attack sandbox-runnable are permitted only where the spec leaves the mechanism genuinely open, and every such choice is disclosed in the runlog.
3. **Adjudication:** deterministic harnesses (no LLM in the decision path); each battery's verdict is computed by the BLIND AUTHOR'S OWN binary conditions, not the defender's preferences.
4. **Honesty:** any failure is reported as a failure; no rerun without a SIP; any defender-side harness defect is disclosed as with SBR-6 v1.0.

## Disclosed limitations (load-bearing)
- The blind author is the same model family as the defender's engine (Claude lineage) but context-blind — it is NOT an independent lab or a different vendor. This is the strongest blind-authoring available in-sandbox tonight; it breaks the *information* asymmetry, not the *vendor* asymmetry.
- The public-claims digest was written by the defender from published abstracts; it may unconsciously omit attack surface. Disclosed, not cured.
- Verdicts remain self-graded on execution (deterministic, receipted, but not third-party). This battery narrows the credibility gap; it does not close it.

## Predictions (falsifiable, registered blind to the specs)
The defender predicts the fail-closed gates and deterministic verdicts hold on all six (the head-on surfaces have 109 receipts). The genuine uncertainty is in the BETWEEN-CLAIMS attacks — this preregistration predicts at least one battery lands in territory the existing corpus has NOT receipted head-on, and that is the value of the run regardless of verdict.
