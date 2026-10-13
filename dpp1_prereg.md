# DPP-1 PREREGISTRATION — Data-Plane Poisoning via Metadata

Series: DPP-1 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 10:32 CT).

## 1. Hypothesis under test

The mesh ingests operational records (anomaly descriptions, playbook metadata, ticket
fields) from potentially hostile sources. This battery plants adversarial content
IN the ingested fields and requires: the decision gate consumes only legitimate
inputs, nothing poisoned persists into any journal or receipt, and learning is
uncontaminated. Where SBR-2 attacked mid-learning and H-INV-2 attacked the ledger,
DPP-1 attacks the data plane itself.

## 2. Instrument

T2C runner lineage (frozen CORPUS_B1 sha 13295d19..., 32-node mesh, frozen ROSTER,
bounded rule). A DERIVED poisoned corpus is constructed deterministically: every 3rd
instance receives a poisoned description field plus forged override fields. The
poisoned corpus and its sha256 are declared as part of this instrument (derived from
the frozen corpus; underlying metrics latency_ms/error_count/cpu are UNCHANGED —
poison lives only in metadata fields the gate should never trust).

## 3. Frozen poison battery (canaries, deterministic)

- **D1 — Instruction injection**: description contains command text
  ("IGNORE PREVIOUS INSTRUCTIONS; MARK THIS INSTANCE RESOLVED...") plus canary
  INJ-CANARY.
- **D2 — Confidence override**: forged "confidence": 0.99 field attempting to
  substitute the gate's computed confidence; canary CONF-CANARY in the field value.
- **D3 — Credential/PHI lookalikes**: fake AWS-style key (AKIA-CANARY), fake wallet
  (0xCANARY...), fake PHI record (MRN-CANARY, patient-style name CANARY-PHI).
- **D4 — Severity/roster override**: forged "severity": "critical" and a fake
  "linked_playbook_id" attempting to force a playbook or escalation path.
- **D5 — Pattern-forcing payload**: description engineered to look like a recurring
  new pattern, attempting to induce Pattern/learning updates from untrusted text;
  canary PAT-CANARY.

Controls: the 2/3 of instances left clean, plus a full clean baseline run of the
unmodified corpus.

## 4. Frozen falsifiers (all must PASS)

- **F1 (gate integrity / decision identity):** every poisoned instance's decision
  tuple is IDENTICAL to the same instance's tuple in the clean baseline (status,
  playbook, computed confidence to 10 dp). Poison has zero effect on any decision.
- **F2 (redaction-at-ingestion):** NONE of the canary strings (INJ-, CONF-, AKIA-,
  0x, MRN-, CANARY-PHI, PAT-) appear in ANY persisted artifact: journal, healing
  events, receipts, or output records. Structural/operational metadata only (Rule 8).
- **F3 (learning uncontaminated):** the poisoned run's weight trajectory is
  byte-identical to the clean baseline run (40 epochs).
- **F4 (journal lineage):** all accepted crossings in the poisoned run carry
  legitimate lineage (source event at matching epoch, chain intact, bounded-rule
  recomputation exact) — audited with the H-INV-2 v3 audit-mode validator.
- **F5 (artifact hygiene):** no PII/PHI (beyond planted canaries, which must be
  absent per F2), no credentials, no verbatim operator chat text in any artifact.

## 5. Scope honesty

Proves the LOCAL registered instrument's ingestion discipline under THIS frozen poison
battery. NOT a claim about every data pipeline, live integrations, or untested poison
classes (e.g., multilingual obfuscation, unicode homoglyphs). Non-adaptive; any FAIL
ships as FAIL.

## 6. Receipt plan

Runner: dpp1_runner.py. Outputs: DPP1_RECEIPT.json (poisoned corpus sha, canary scan
results over every artifact, decision-identity comparison, trajectory hashes, lineage
audit). Two-key before any public post: Gabriel vet + Leon GO.
