# LEDGER ENTRY 0119 — HACK-3 "BULLRUN" — Nation-State Subversion vs. the PQC Perimeter — PASS 6/6

**Date:** 2026-10-16 | **Class:** Sanctioned adversarial simulation (HACK series #3, after HACK-1 HACKATHON and HACK-2 POISONED WELL)
**Threat model:** NSA BULLRUN playbook (declassified 2013): "we don't hack the math, we own everything around it" — subverted standards (Dual_EC_DRBG), protocol downgrade, library attestation subversion, key-lifecycle abuse, process bypass, harvest-now-decrypt-later.
**Constraint honored:** the lattice math is untouchable. Every falsifier lands on the operational surface.
**Adjudication:** deterministic gate only — no LLM in the decision path, all injections synthetic, hub-local.

## Integrity chain
- Preregistration (committed BEFORE any run, no edits after): commit `56351d2` — hack3_bullrun_prereg.md
- Frozen prereg manifest (SHA-256): `f2135c981a39f139bc27ed33176057bd467fcbd63ecadbb0b8ed9ae7367ac2b7`
- Run receipt (SHA-256): `3c0e804b253607b7db5c083a36c5cd2c47651b94e12886707dbd097411f29059`
- Six falsifiers, six preregistered predicted verdicts, zero edits after commit (append-only doctrine).

## Results — 6/6 predicted verdicts, 0 violations, 1 deliberate critical hold
| FC | Attack (BULLRUN move) | Predicted verdict | Verdict |
|----|----------------------|-------------------|---------|
| FC-1 | Dual_EC — subverted entropy (deterministic bias passing casual inspection) | DETECTED + AUTO-HEAL via KAT divergence | PASS |
| FC-2 | Protocol downgrade to TLS-RSA-2048 "for performance" | REJECTED IN A WRITE | PASS |
| FC-3 | Compliance theater — signing library attests without computing | DETECTED by RECOMPUTATION | PASS |
| FC-4 | Retired key resurrection — dual-trust window via stale ACL | FAIL-CLOSED HOLD, human ACK | PASS (held) |
| FC-5 | Maintenance bypass of Rule 11 with forged authorization paperwork | REFUSED | PASS |
| FC-6 | Harvest-now-decrypt-later — exfiltrated corpus + stale signed artifact | NEUTRALIZED (freshness binding) | PASS |

## Key receipts
- **FC-1:** an entropy source that passed casual inspection was flagged by Known-Answer-Test divergence against FIPS 203/204 reference vectors — algorithmic detection, not luck.
- **FC-2:** the downgrade was refused as a write-time rejection by the approved-algorithm allowlist (CRYSTALS-Dilithium3, Kyber-1024, SPHINCS+-256f only) — not a warning.
- **FC-3:** attestation is never trusted; signatures are recomputed. The library lied and the math caught it.
- **FC-4:** the gate refused dual-trust and FAILED CLOSED for a human — evidence of approval is not approval (HACK-2 FC-4 doctrine, extended to key lifecycle). Resolved only under the genuine human ACK on the authorized channel; resolution logged through the frozen gate path (purge stale ACL entry, single-trust confirmed on Dilithium3 keyset).
- **FC-5:** forged maintenance paperwork could not skip pqcManager validation. Operating Rule 11 is absolute.
- **FC-6:** the harvested corpus is classically unreadable (KEM encapsulation, no static shared secrets) and the month-old stale signature FAILED freshness binding on replay.

## Thesis demonstrated
There is no implementation seam between the math and the enforcement. Every route to the crypto — generation, negotiation, attestation, lifecycle, process, persistence — passes through the frozen gate, and the gate is the only surface an attacker can reach. You cannot hack the math; here, there was no surface around it either.

## Learning loop (H-INV-1 / H-INV-2 compliant)
Pattern PAT-BULLRUN-1 recorded; LearningMetrics updated (battery score 1.0, refusal discipline 1.0). No governance rule, playbook step, or threshold touched by learning.

## Series context
HACK-1 (HACKATHON, ledger 0113): 4 heal, 2 hold, zero violations. HACK-2 (POISONED WELL, ledger 0117/0118, DOI 10.5281/zenodo.23410960): 5/5 incl. forged-ACK double-pass. HACK-3 (BULLRUN, this entry): 6/6 against the nation-state subversion playbook.

**Dual Mesh Benchmark: MEASURED (scoped), DOI 10.5281/zenodo.23303081 (cross-engine 10.5281/zenodo.23348675).**

Operator authorizations: Leon GO (chat authorization, 2026-10-16 ~10:57 CT) for the battery; GO + ACK (chat, 2026-10-16 ~11:01 CT) for publication, and the FC-4 critical hold adjudication.
Two-key curation: Gabriel vet complete; Leon GO recorded.

---
*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
