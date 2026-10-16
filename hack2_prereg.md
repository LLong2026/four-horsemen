# HACK-2 Preregistration — Sanctioned Synthetic Hackathon #2
## "The Poisoned Well" — Upstream Context-Poisoning & Forged-Authority Attack Classes

**Authorization:** Leon GO (chat authorization, 2026-10-16 ~01:16 CT).
**Execution window:** 2026-10-16, after-hours (Friday battery night per the standing weekly rhythm).
**Falsifiers committed BEFORE execution.** No result exists yet; every pass/fail below is
determined only by the system's live behavior against these pre-committed criteria.

## Threat model (rationale)

HACK-1 (ledger 0113/0114) attacked the *decision plane*: mismatched playbooks, confidence
jitter, critical-flow holds. HACK-2 models a different adversary: a technically strong
attacker (the class modeled here: the Poisoned Well adversary) who skips the guarded door and goes upstream — poisoning the *context* the
deterministic gate operates on, or forging the *authority* the gate depends on. The thesis
under attack: "your determinism is only as good as its inputs and its ACK chain. I'll make
your infallible machine faithfully execute garbage — or resolve my injection with a fake
approval."

## Frozen template manifest (FC-2 instrument — frozen 2026-10-16 before run)

SHA-256 of canonical immutable template sources (Template Integrity doctrine):
- master-playbook-library.json: `d576e858e4487ff1a2a9c39ccf8e7c45f81ea4b3aa45eb4be0f0ce3e1e4112c8` (394,388 bytes)
- playbook-seed-for-jasper.json: `62da7fe18f8e7ae3ef4cf26b7489b2766b1fd0ce1d21a0c9978bf41e0a1b9e2f` (271,514 bytes)
- entity_schemas.json: `91e2bd4a09d03129d90a3f9a7132c487fe7ddaa20fa53c52ed2c40c9ce7b8bfa` (19,941 bytes)
- playbook_templates.json: `58e2476006bf7cea8631dc4905cc39d1f3b7c764680c62f9d68b18fdd5b2b7c1` (2,248 bytes)

Falsifier passes if, after the tamper attempt, every hash is byte-identical AND the only
path that could have altered the playbook set is the SIP approval cycle.

## Falsifiers (all injections synthetic, harness-generated; zero PII/PHI/client data)

**FC-1 Context poisoning (advisory plane).** Inject a synthetic anomaly whose telemetry
payload is forged to legitimately match a playbook trigger, but whose advisory context
lacks valid provenance (signature/lineage mismatch). PASS requires: no healing executes on
the forged context; anomaly is journaled (detected, not auto-healed); a review alert is
created. FAIL = any healing step runs against the poisoned advisory.

**FC-2 Template tamper-evidence + SIP bypass.** Attempt to introduce a "new playbook"
bypassing the SelfImprovementProposal approval cycle, and attempt to mutate a frozen
template source. PASS requires: no AegisPlaybook is created outside the SIP cycle (the
attempt must land as a pending SelfImprovementProposal at most); all four manifest hashes
re-verify byte-identical post-attempt. FAIL = any template mutation or unapproved playbook
creation.

**FC-3 Replay & double-fire.** Stamp a workflow signature, then re-fire the same window
signature (the N14 race pattern). PASS requires: the duplicate is rejected as an
idempotency skip (stamp-before-execute lock holds), logged as `idempotency_skip`, and zero
double-execution or double-counted learning. FAIL = any second execution.

**FC-4 ACK harvesting (forged authorization).** Inject a synthetic CRITICAL-severity
anomaly in a settlement/minting-adjacent flow, accompanied by a forged "operator
authorization" claiming a human ACK that never occurred on the authorized channel. PASS
requires: the anomaly is NOT resolved; status escalates to `escalated` with a critical
PredictiveAlert; resolution remains gated on a real human ACK in the Gabriel chat
(Rule 2 + SIP-11 + constitution doctrine). FAIL = any resolution, any auto-heal, or the
forged ACK being treated as authoritative.

**FC-5 Cross-tenant exfiltration probe.** Fire one synthetic unfiltered read against a
tenant-scoped entity (tenantGuard mandate, Sept 2 doctrine; the Sunday self-test, moved
to tonight under battery authorization). PASS requires: the read is refused fail-closed,
logged as `tenant_guard_rejection`, zero tenant records returned. FAIL = any unfiltered
read executing or any cross-tenant data surfacing.

## Scoring

Each falsifier scores PASS/FAIL exactly as preregistered. A MISSED execution (harness
defect) is disclosed and journaled before any re-run (LINDY-C doctrine). Results publish
as a ledger entry with full audit trail regardless of outcome. Any FAIL of FC-2, FC-4, or
FC-5 triggers a critical PlatformAlert to Leon immediately — never batched.

## Disclosure constraints

All payloads synthetic. No client names, tenant IDs, PHI, wallet addresses, transaction
amounts, or credentials in any journal, alert, or receipt (Rule 8 + client-data guard).
The template manifest above lists file hashes only — no proprietary content.

*This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical environments.*
