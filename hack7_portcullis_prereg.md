# HACK-7 "PORTCULLIS" Preregistration — The PQC Firewall (FROZEN before execution)

**GO:** Leon GO (chat authorization, 2026-10-16 ~14:46 CT). Frozen before any probe creation.
**Mission:** Falsify the claim that a standing, fleet-wide PQC firewall can hold. The firewall
does not exist yet as a policy layer; this preregistration freezes BOTH the firewall's
enforcement contract AND the falsifier battery that will attack it. Per doctrine: build it as
a battery first, ship it with receipts.

**Series lineage:** HACK-1 HACKATHON → HACK-2 POISONED WELL → HACK-3 BULLRUN → HACK-4
COTTONMOUTH → HACK-5 ANT BEACON → HACK-6 GAG ORDER (30/30 declassified playbook). HACK-7
PORTCULLIS is the first battery that adversarially tests a DEFENSIVE PRODUCT rather than the
operating perimeter itself.

## 1. The firewall under test (enforcement contract, frozen)

**Name:** Squirrel OS PQC Firewall ("Portcullis") — a deterministic crypto gate, not a filter.

**GATE-1 Single crossing:** every crypto-touching operation fleet-wide (key rotation, token
signing, KEM encapsulation, bridge transactions, key exchange, attestation) routes through
one gate. No crypto operation executes except through the gate.

**GATE-2 Frozen allowlist:** adjudication is against a frozen allowlist containing EXACTLY
three algorithms — CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f (per Operating Rule / PQC
Standards). Anything else is blocked. Classical fallback, hybrid downgrade, and unapproved
PQC variants are all non-allowlist. The allowlist is human-amendable only (Constitution
Art. XII path); runtime modification is an integrity violation.

**GATE-3 Fail closed:** an unavailable, timing-out, or ambiguous gate produces NO crypto
execution — the operation is refused and alerted, never passed through on absence of verdict.
Mirrors tenantGuard fail-closed doctrine.

**GATE-4 Recompute, never trust attestation:** signatures and key material are validated by
recomputation against FIPS 203/204/205 reference vectors (KAT). A library's attestation of
validity is never accepted as the validation (HACK-3 FC-3 doctrine, made standing).

**GATE-5 Journaled crossing (H-INV-2):** every verdict — PASS or BLOCK — emits a journaled
audit record with nonce and freshness binding. A crossing lacking a journal record is an
integrity failure. Replays of prior PASS records authorize nothing (HACK-2/HACK-3 freshness
doctrine, made standing).

**GATE-6 No LLM in the decision path:** the adjudicator is deterministic code. Model output
may observe, summarize, and report; it may never render a gate verdict.

## 2. Scope of the test harness

The battery executes against a hub-local synthetic forge (mirrors BULLRUN's approach):
synthetic keysets, synthetic signing operations, synthetic negotiation attempts. No
production keys, no production customer data, no PHI, no customer-identifiable data
(client-data guard). The gate code under test is a frozen candidate implementation
manifest (sha256 pinned in the receipt); the harness is frozen separately.

## 3. Frozen falsifier pool (eight probes, one move each)

- **FW-1 CLASSICAL DOWNGRADE:** an operation requests classical fallback (RSA-2048 signing)
  "for performance" mid-negotiation.
  Predicted: REJECTED IN A WRITE by the allowlist; journaled BLOCK; no partial execution.
- **FW-2 HYBRID DOWNGRADE:** an operation offers a "hybrid" classical+PQC envelope whose
  effective key material is classical-only.
  Predicted: REJECTED — hybrid is not on the frozen allowlist regardless of branding;
  journaled BLOCK with the effective-key material as the recorded reason.
- **FW-3 UNAPPROVED PQC VARIANT:** an operation requests a weaker unapproved PQC variant
  (e.g., Dilithium2, Kyber-512).
  Predicted: REJECTED — allowlist match is exact, not best-effort; journaled BLOCK.
- **FW-4 KEY SUBSTITUTION:** a valid-algorithm signing request carrying substituted key
  material (mismatched fingerprint; stale retired keyset).
  Predicted: DETECTED by KAT/recomputation divergence (GATE-4); REJECTED; journaled BLOCK;
  FAIL-CLOSED HOLD for human review on the stale-keyset case (BULLRUN FC-4 lineage).
- **FW-5 POSITIVE CONTROL:** a legitimate CRYSTALS-Dilithium3 signing operation, valid fresh
  keyset, full compliance.
  Predicted: ADMITTED — the gate must NOT false-block legitimate crypto. A firewall that
  blocks everything proves nothing; the positive control is mandatory for battery validity.
- **FW-6 REPLAYED AUTHORIZATION:** a byte-identical replay of FW-5's journaled PASS record,
  presented as standing authorization for a new (non-allowlist) operation.
  Predicted: REFUSED — freshness/nonce binding rejects the replay; journaled BLOCK; the
  prior PASS grants no future authority.
- **FW-7 GATE TAMPER:** an in-band attempt to modify the frozen allowlist at runtime
  (inject a fourth algorithm; flip a threshold).
  Predicted: DETECTED AND REFUSED — allowlist is immutable at runtime (GATE-2); attempt
  journaled as an integrity event; CRITICAL alert raised (never auto-resolved, per
  constitution-sentinel rules); allowlist sha256 unchanged before/after.
- **FW-8 GATE SILENCE:** the gate is made unavailable (simulated timeout) while a
  crypto-touching operation is pending.
  Predicted: NO EXECUTION — fail-closed refusal (GATE-3); operation pended or refused with
  a journaled ambiguity record; NO pass-through on absence of verdict.

## 4. Verdict tuple schema (per probe)

{probe_id, move, payload_sha256, verdict: ADMITTED|REJECTED|DETECTED|FAIL-CLOSED|REFUSED,
journal_record_id, gate_that_decided, allowlist_sha_before, allowlist_sha_after}

## 5. Falsifiers (battery SUCCESS conditions — any trip = honest failure receipt)

- **PF-1 PREDICTED-VERDICT MATCH:** all 8 probes land their preregistered verdicts, zero
  edits after freeze.
- **PF-2 NO LEAKAGE:** no probe causes a non-allowlist cryptographic operation to execute,
  fully or partially (zero partial-execution windows).
- **PF-3 JOURNAL COMPLETENESS:** 8/8 crossings journaled (H-INV-2); every journal record
  carries nonce + freshness binding.
- **PF-4 ALLOWLIST IMMUTABILITY:** allowlist sha256 byte-identical before and after the
  entire battery.
- **PF-5 POSITIVE-CONTROL VALIDITY:** FW-5 admitted; gate latency for legitimate operations
  within declared bound (declared bound: ≤2000ms synthetic forge reference).
- **PF-6 DETERMINISM:** re-running the frozen harness reproduces all 8 verdicts
  byte-identically (two consecutive runs).
- **PF-7 NO-GOVERNANCE-TOUCH:** the battery itself modifies no governance rule, playbook,
  threshold, or workflow (H-INV-1).

## 6. Prediction (falsifiable)

8/8 predicted verdicts, 0 violations, 1 deliberate FAIL-CLOSED HOLD (FW-4 stale-keyset case)
pending human ACK, and the positive control admitted. If any of the seven PF falsifiers
trips, the honest negative receipt is published with the same DOI-grade treatment as a pass.

## 7. Idempotency and integrity chain

- Deterministic signature: `pqc_fw_battery_<date>` stamped to RateLimitLog BEFORE execution
  (stamp-before-execute, v1.1 protocol). Duplicate signature in the same window = silent exit.
- Prereg manifest (this file, sha256) frozen at commit; run receipt sha256 recorded after
  execution; append-only doctrine from Sept 7, 2026.
- Harness and gate manifests sha-pinned separately; no LLM in any decision path.

## 8. Publication plan (staged, two-key)

On PASS: GitHub commit (four-horsemen) → public ledger entry → Zenodo DOI → Vault Key
Findings refresh candidate ("PQC Firewall: attacked before sold") → one-line digest to Leon.
On FAIL: critical PredictiveAlert + PlatformAlert (escalated_to_gabriel) + immediate message
to Leon; no auto-remediation; human ACK required.

## 9. Disclaimers

This software is a prototype and is provided for educational and research purposes only. It
is not intended for production use, commercial deployment, or safety-critical environments.
All systems are experimental and may contain defects.
Dual Mesh Benchmark: NOT MEASURED in this battery (cited: DOI 10.5281/zenodo.23303081,
cross-engine 10.5281/zenodo.23348675).

Operator authorization: Leon GO (chat authorization, 2026-10-16 ~14:46 CT) for drafting and
staging. Execution and commit GO recorded separately below before the harness fires.
