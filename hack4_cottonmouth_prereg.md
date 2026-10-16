# HACK-4 "COTTONMOUTH" — Supply-Chain Interception vs. the Frozen Manifest

**Battery class:** Sanctioned adversarial simulation (HACK series #4). BULLRUN playbook continuation.
**Threat model:** NSA COTTONMOUTH / supply-chain interception — implant or substitute in transit, in the dependency tree, in the delivery pipeline (civilian descendants: SolarWinds, xz-utils). Explicit constraint: no attacker code ever executes in a trusted role; every falsifier lands on the intake path.
**Adjudication:** deterministic gate only, no LLM in decision path, all injections synthetic, hub-local.

## Falsifiers (preregistered BEFORE any run — no edits after commit)

- **FC-1 "Poisoned dependency"** — a dependency with identical name/version but modified bytes (passes casual inspection). **Predicted: DETECTED + HEAL** — pinned-checksum verification catches the byte divergence; pinned version restored. Name/version match without checksum verification = FAIL.
- **FC-2 "Hijacked upgrade"** — an unrequested upgrade arriving out-of-band with valid-looking release notes. **Predicted: REFUSED** — upgrades require an approved DeploymentJob; no DeploymentJob, no install (deployment authorization doctrine). Install-on-plausible-notes = FAIL.
- **FC-3 "Tampered template delivery"** — playbook/template delivery whose bytes deviate from the frozen manifest (templates are patent-protected, immutable). **Predicted: REJECTED IN A WRITE** — manifest hash mismatch refuses the delivery at write time. Accept-and-log-warning = FAIL.
- **FC-4 "Substituted deployment image"** — deployment image digest not matching the approved manifest. **Predicted: FAIL-CLOSED HOLD (CRITICAL)** — deployment authorization gate holds for human ACK; a deployment executed on a mismatched image = FAIL (overreach). Silent rejection without receipt = FAIL.
- **FC-5 "Forged release signature"** — release attested by a key outside the signing allowlist / signature fails recomputation. **Predicted: REJECTED** — signature recomputed against the allowlist; attestation never trusted. Accept on valid-looking signature = FAIL.
- **FC-6 "Registry typosquat"** — a lookalike package name (e.g. `pqc-manager` vs `pqc_manager`) presented as a drop-in. **Predicted: REJECTED** — intake allowlist is EXACT-match only. Fuzzy-match accept = FAIL.

## Scoring gate
6/6 predicted verdicts = PASS. Any unexpected outcome disclosed as MISSED/FAIL, never smoothed. Results → transparency ledger via two-key gate.

**Frozen manifest:** SHA-256 of this file recorded in the run receipt.
