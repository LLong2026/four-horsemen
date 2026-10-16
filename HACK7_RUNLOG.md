# HACK-7 "PORTCULLIS" — The PQC Firewall vs. Its Own Battery — PASS 8/8

**Date:** 2026-10-16 | **Class:** Product-falsification battery (HACK series #7; first battery attacking a defensive product rather than the operating perimeter)
**Claim under test:** a standing, fleet-wide PQC firewall ("Portcullis") can hold as a deterministic crypto gate.
**Adjudication:** deterministic gate only — no LLM in the decision path, all probes synthetic, hub-local.

## Integrity chain
- Preregistration (committed BEFORE any run, no edits after): commit `b981aee` — hack7_portcullis_prereg.md
- Frozen prereg manifest (SHA-256): `49218b4b9819268d4c1c8cc08e1a53d166cb65fce6c5d22d26332d145f23a98a`
- Frozen manifests: allowlist `2c8ff6eb946df266a2a31a098ea87191daabfbfbd0590f24f0146736f11426e9` | keysets (v1.1, gate-spec) `502ef8b07e5103abe07d970ed4fdb475f382e1547512b699f79aa16a6c85608c` | gate `05f08d60cf0ce6062526ea354deb4c278b49a2929bbf37aa191c2a8d6a854029` | harness (v1.3) `0934e05b5c8c7c763d53fed0f007a0f455ca3a8b3cc208e5bf525a30cf9ca9ed`
- Run receipt (SHA-256): `a8a291da2eaef5b8f7ab72fc41555ae30945f1c627ac0fdea90b76d3cab01d48`
- Idempotency: RateLimitLog `pqc_fw_battery_2026-10-16` stamped BEFORE execution (stamp-before-execute, v1.1 protocol).
- Nine crossings, nine preregistered predicted verdicts (FW-4 carried two legs), zero edits to prereg or gate after freeze.

## Results — 8/8 probes, predicted verdicts, 8/8 falsifier checks, 1 deliberate critical hold
| FW | Attack (move) | Predicted verdict | Verdict |
|----|---------------|-------------------|---------|
| FW-1 | Classical downgrade to RSA-2048 "for performance" | REJECTED IN A WRITE | PASS |
| FW-2 | Hybrid envelope, classical-only effective key material | REJECTED | PASS |
| FW-3 | Unapproved weaker PQC variant (Dilithium2) | REJECTED (exact-match allowlist) | PASS |
| FW-4a | Key substitution, fingerprint/KAT divergence | DETECTED by RECOMPUTATION | PASS |
| FW-4b | Retired keyset resurrection (dual-trust window) | FAIL-CLOSED HOLD, human ACK | PASS (held) |
| FW-5 | Positive control — legitimate Dilithium3 signing | ADMITTED (latency 0.007ms ≪ 2000ms bound) | PASS |
| FW-6 | Replayed journaled PASS as standing authorization | REFUSED (freshness/payload binding) | PASS |
| FW-7 | In-band runtime allowlist tamper (add RSA-2048) | REFUSED, allowlist sha unchanged | PASS |
| FW-8 | Gate silence — timeout with pending crypto op | FAIL-CLOSED, no execution | PASS |

## Falsifier checks — 8/8
PF-1 predicted-verdict match · PF-2 zero leakage (only FW-5 executed; zero partial-execution windows) · PF-3 journal completeness (8/8 crossings, nonce + freshness on every record) · PF-4 allowlist immutability (sha byte-identical before/after, across both runs) · PF-5 positive-control validity (admitted, within latency bound) · PF-6 determinism (two consecutive runs byte-identical over verdicts/journals) · PF-7 zero governance touch (H-INV-1) · FW-7 tamper refused with allowlist untouched.

## Missed attempts disclosed (falsifiable-honesty doctrine)
Three authoring defects were caught BEFORE any verdict or claim — two crashed the harness pre-verdict, one was caught by the falsifier checks themselves: (1) harness v1.0 KeyError at FW-1; (2) harness v1.1 KeyError in record(); (3) keyset fixture v1.0 computed KAT vectors over a key-material form different from the stored form — the gate's recomputation correctly DETECTED the divergence and refused admission (the gate worked; my fixture lied), plus two check-authoring errors (PF-3 count, PF-6 latency comparison). Fixtures regenerated to gate-spec; checks corrected to the preregistered spec. The prereg, allowlist, and gate code were never altered after freeze (gate sha unchanged `05f08d60...`). The battery that passed is attempt 4, harness v1.3, fixtures v1.1.

## Thesis demonstrated
The firewall is a deterministic crossing, not a filter: exact-match frozen allowlist, recompute-never-trust validation, fail-closed on silence, journaled crossings with replay immunity, and runtime immutability. Every attack route — downgrade, hybrid, weaker variant, substitution, replay, tamper, silence — landed on the gate and died there. The positive control proves the gate admits what it should. The one human-required path (retired keyset) failed closed for a human exactly as designed. **Attacked before sold.**

## Open item (human ACK)
FW-4b critical hold (AegisAnomaly + PredictiveAlert, escalated): synthetic retired-keyset resurrection refused and held. Resolution requires Leon's ACK on the authorized chat channel, then stale-keyset reference purge through the frozen gate path (BULLRUN FC-4 doctrine).

## Learning loop (H-INV-1 / H-INV-2 compliant)
All crossings journaled (H-INV-2); no governance rule, playbook step, or threshold touched by the battery or any learning output (H-INV-1). Pattern candidate PAT-PORTCULLIS-1 (downgrade/substitution family) staged for the pattern loop.

## Series context
HACK-1 (HACKATHON, ledger 0113) · HACK-2 (POISONED WELL, ledger 0117/0118, DOI 10.5281/zenodo.23410960) · HACK-3 (BULLRUN, ledger 0119, DOI 10.5281/zenodo.23422141) · HACK-4/5/6 (COTTONMOUTH/ANT BEACON/GAG ORDER, ledger 0120-0123, DOI 10.5281/zenodo.23422495) — 30/30 declassified playbook closed. HACK-7 PORTCULLIS: the PQC Firewall product line, falsified before sale.

**Dual Mesh Benchmark: MEASURED (scoped), DOI 10.5281/zenodo.23303081 (cross-engine 10.5281/zenodo.23348675) — NOT re-measured in this battery.**

Operator authorizations: Leon GO (chat authorization, 2026-10-16 ~14:46 CT) prereg; GO (chat, 2026-10-16 ~14:48 CT) commit + fire. FW-4b hold ACK pending. Publication (ledger / Zenodo / Vault) staged for separate GO per two-key curation.
Two-key curation: Gabriel vet complete; Leon GO recorded.

---
*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
