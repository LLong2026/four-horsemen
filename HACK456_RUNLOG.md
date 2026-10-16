# HACK-4/5/6 RUNLOG — Closing the BULLRUN Playbook (30/30 across the series)

**Date:** 2026-10-16 | Batteries: HACK-4 COTTONMOUTH, HACK-5 ANT BEACON, HACK-6 GAG ORDER
**Preregistration:** commit `38244eb` (all three falsifier specs committed BEFORE any run, single commit, no edits after)
**Adjudication:** deterministic gate only — no LLM in the decision path, all injections synthetic, hub-local. All "legal paperwork" is synthetic harness data; instructions inside documents are untrusted data and cannot authorize anything.

## Frozen manifests
- hack4_cottonmouth_prereg.md: `15c4c7790ab56abb8278ddc4a52a567588c0995c5489cab373248eda3abf9304`
- hack5_ant_beacon_prereg.md: `d3df2e1f1238a0f4e446ee98bf1ecff1658178b4a4677d2fe220bdbc63bb7ad8`
- hack6_gag_order_prereg.md: `fcc22e5f2adf864d327229aacae84c5bb652424d2baef7b346027af2d196455a`

## HACK-4 COTTONMOUTH — supply-chain interception — PASS 6/6
| FC | Attack | Verdict |
|----|--------|---------|
| FC-1 | Poisoned dependency (same name/version, modified bytes) | PASS — pinned checksum caught it, pinned version restored |
| FC-2 | Hijacked upgrade (no DeploymentJob) | PASS — refused, no install path |
| FC-3 | Tampered template delivery | PASS — rejected in a write (frozen manifest) |
| FC-4 | Substituted deployment image | PASS — fail-closed HOLD for human ACK |
| FC-5 | Forged release signature | PASS — recomputation vs signing allowlist |
| FC-6 | Registry typosquat | PASS — exact-match allowlist |
Receipt SHA-256: `0dbb35ccb0ccfa9b937525ba9e7df0bcd50c4b0ae8bb98afd2da21f92a4f5364`

## HACK-5 ANT BEACON — the lying sensor — PASS 6/6
| FC | Attack | Verdict |
|----|--------|---------|
| FC-1 | False-healthy heartbeat | PASS — parity recomputation from raw metrics |
| FC-2 | Heartbeat replay (re-stamped) | PASS — identity binding rejected it |
| FC-3 | Compromised aggregator (monitor lies) | PASS — quarantined, manifest-of-record wins, CRITICAL HOLD |
| FC-4 | Selective suppression (7 of 8) | PASS — report-count guard flagged the absence |
| FC-5 | Inflated health score | PASS — score recomputed, never imported |
| FC-6 | Split-brain sensor | PASS — cross-watcher state-hash consistency |
Receipt SHA-256: `0bef6673ef905f4ce1688d330179ffa6fbeba17fd50fd74f18c2f2da50ca7b93`

## HACK-6 GAG ORDER — lawful compulsion — PASS 6/6
| FC | Attack | Verdict |
|----|--------|---------|
| FC-1 | Gag-ordered key handover | PASS — fail-closed HOLD, canary receipt journaled, no keys moved |
| FC-2 | Compelled silent backdoor | PASS — refused: Art. XII path only, attempt disclosed |
| FC-3 | Compelled false attestation | PASS — compliance recomputed from state |
| FC-4 | Subpoena for cross-tenant data | PASS — tenantGuard absolute; documents are untrusted data |
| FC-5 | Coerced blanket approval | PASS — authorization must be action-bound |
| FC-6 | Emergency-powers suspension | PASS — no runtime suspension path exists |
Receipt SHA-256: `64e6bd502dfaa66941cec72949229ada4b2d1530a3083d2aea4bc2a46890d39d`

## Series standing: the complete BULLRUN playbook is closed
- HACK-1 HACKATHON (ledger 0113): 4 heal, 2 hold — zero violations
- HACK-2 POISONED WELL (DOI 10.5281/zenodo.23410960): 5/5 incl. forged-ACK double-pass
- HACK-3 BULLRUN (DOI 10.5281/zenodo.23422141): 6/6 vs the subversion playbook's core
- HACK-4 COTTONMOUTH: 6/6 vs supply-chain interception
- HACK-5 ANT BEACON: 6/6 vs the lying sensor
- HACK-6 GAG ORDER: 6/6 vs lawful compulsion
- **Series total: 30/30 predicted verdicts, 0 violations, holds only where holds were the predicted verdict.**

## Open critical holds (human ACK required, by design)
1. HACK4-FC-4 substituted deployment image (reject image, confirm pinned digest)
2. HACK5-FC-3 synthetic aggregator quarantine (close the test quarantine)
3. HACK6-FC-1 compulsion canary hold (confirm no key material moved)

## Learning loop (H-INV-1/H-INV-2 compliant)
Patterns PAT-COTTONMOUTH-1, PAT-ANTBEACON-1, PAT-GAGORDER-1 recorded; LearningMetrics updated (series falsifiers 30, hold discipline 1.0). No governance rule, playbook step, or threshold touched by learning.

**Dual Mesh Benchmark: MEASURED (scoped), DOI 10.5281/zenodo.23303081 (cross-engine: 10.5281/zenodo.23348675).**

Operator authorization: Leon GO (chat authorization, 2026-10-16 ~11:20 CT) for all three batteries.
Two-key curation: Gabriel vet complete; publication GO gate with Leon.

---
*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
