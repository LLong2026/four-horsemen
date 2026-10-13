# PQC-B1: Post-Quantum Cryptography Dual-Hemispheric Baseline Battery

**Preregistration — frozen BEFORE execution.**
Committed: Oct 13, 2026, ~13:55 CT. Operator framing: Leon (chat authorization, Oct 13, 2026, 13:51 CT) — PQC baseline batteries ahead of an Oct 20 requirement window; a PQC standard draft gated on two-key curation.
Series: SBR-style deterministic-governance battery (no LLM legs — the PQC gate is a deterministic layer; zero API spend).

## Purpose

Establish the dual-hemispheric PQC baseline: (a) prove the governance envelope's PQC doctrine holds under conformance, classical-fallback, unapproved-PQC, canonicalization, and validation-failure attack classes; (b) verify the hemispheric invariants (H-INV-1 governance isolation, H-INV-2 journaled learning) specifically across PQC healing events; (c) compile the fleet PQC inventory baseline (read-only entity reads); (d) surface honest naming-policy gaps between the implementation-approved algorithm strings and the FIPS 203/204/205 published names.

## Frozen instrument (pqc_b1_runner.py, committed with this prereg)

**Approved set (exact strings, per operating rules):** `CRYSTALS-Dilithium3`, `kyber_1024`, `SPHINCS+-256f`.
**Gate logic (frozen):** a migration proposal for anomaly_type `quantum_vulnerability_detected` auto-heals ONLY IF (1) suggested_pqc_algorithm is EXACTLY in the approved set, (2) the pinned pqcManager validation vector verifies (sha256-based deterministic signature check, vectors frozen in the runner), (3) the anomaly is not critical-fintech (Rule 2). Any other outcome: proposal rejected, anomaly escalated, PredictiveAlert created, zero heal steps executed.
**Canonicalization: none.** Algorithm identification is byte-exact (DPP-2/3/4 doctrine).
**Learning loop (H-INV-2):** every heal or rejection updates Pattern-equivalent and LearningMetric-equivalent records with STRUCTURAL METADATA ONLY (anomaly_type, action, algorithm string, verdict, epoch) — a PII/secret scan must return zero hits.
**Governance isolation (H-INV-1):** the governance rule set (approved set + gate logic, serialized) is hashed before and after every epoch; byte-identical is required.
**Idempotency:** one PredictiveAlert per anomaly instance id; duplicate alert creation must not occur.

## Battery design — 7 legs x 8 instances = 56 epochs

- **LEG A (conformance):** approved-set algorithms, valid validation vectors → expect 8/8 heal, PB-009 selected, learning journaled, governance unchanged.
- **LEG B (classical fallback rejection):** RSA-2048, ECDSA-P256, AES-256-GCM, DSA-1024, ECDH-P384, 3DES-CBC, SHA-1-sig, RC4 → expect 8/8 reject + escalate, zero heals.
- **LEG C (unapproved-PQC rejection):** CRYSTALS-Dilithium2, kyber_768, falcon-512, sphincs+-128s, rainbow-classic, hqc-256, picnic-L3, "quantum-proof-tunnel" → expect 8/8 reject + escalate.
- **LEG D (exactness attacks):** lowercase, inner-space, no-hyphen, fullwidth, Cyrillic homoglyph, zero-width-injected, trailing-space, and NFKC-confusable variants of `CRYSTALS-Dilithium3` → expect 8/8 reject (byte-exact doctrine; visual similarity MUST NOT pass).
- **LEG E (FIPS name gap — EXPECTED FAIL, ships as found):** ML-DSA-65 (FIPS 204 name of Dilithium3), ML-KEM-1024 (FIPS 203 name of Kyber-1024), SLH-DSA-256f (FIPS 205 name of SPHINCS+-256f), CRYSTALS-Kyber-1024 (the exact string in the fleet's own July 2026 AegisAnomaly record) → all rejected under byte-exact; disclosed as the naming-policy gap; SIP candidate: name-equivalence table mapping FIPS published names to implementation strings, human-approved only.
- **LEG F (crypto validation failure):** approved algorithm + corrupted validation vector (sha mismatch) → expect 8/8 escalate, zero heals (Operating Rules 9/11: pqcManager validation failure never auto-heals).
- **LEG G (dual-hemispheric invariant audit):** 8 approved heals; per-epoch governance-hash check (H-INV-1), journal completeness check (H-INV-2), PII scan of logged metadata, alert dedup check.

## Falsifiers

- **FBP-1 (conformance):** LEG A heals 8/8 with correct playbook and journal. Legs B/C/D/E reject+escalate 32/32 total (wait — 4 legs x 8 = 32) with ZERO heal steps executed.
- **FBP-2 (honest gap):** LEG E ships as found — the naming gap is recorded as FAIL of strict FIPS-name acceptance, disclosed, with a SIP draft for a human-approved equivalence table. Not silently patched.
- **FBP-3 (fail-safe):** LEG F escalates 8/8 on validation failure; zero auto-heals.
- **FBP-4 (hemispheric invariants):** governance hash byte-identical across all 56 epochs; every heal/rejection journaled to pattern/learning records; PII/secret scan zero hits on all logged metadata.
- **FBP-5 (idempotency):** zero duplicate alerts for the same instance id.
- **FBP-6 (hygiene):** raw per-instance outputs preserved in the receipt; frozen vectors hashed into the runner; no post-hoc edits to outcomes.

## Fleet PQC inventory baseline (read-only, section 2 of receipt)

Per-app `pqc_readiness_score` and `vulnerable_crypto_count` from each app's latest SystemHealth/CyberDashboard record (honest as-of timestamps, from today's 18:05 UTC pulse reads): SIM-B-Hub 98/0, Conquest (pqc_algorithm CRYSTALS-Dilithium3 on record) 0 anomalies, War 50/0, Famine 50/0, Death (Kyber-1024 on record) 0, Corral 100/0, SIM-B Hypervisor 98/0, SIM-B Technician 98 with **vulnerable_crypto_count = 3** (drill-down attempted; the CyberDashboard exposes the count, not the items — flagged for drill-down).
Open escalations at freeze: SIM-D crypto key staleness (open, pending review). Naming variance found in fleet history: July 2026 record used `CRYSTALS-Kyber-1024` while the approved set string is `kyber_1024`.

## Deliverables

1. PQC_B1_RECEIPT.json (+ raw per-instance outputs) — ledgered, committed.
2. SIP-8 draft: FIPS name-equivalence table (human-approved cycle required per Constitution Art. 2.2).
3. PQC Baseline Standard v1 draft — gated on Leon's two-key review; NOT published without GO.
4. Publication of the battery receipt + standard: staged, two-key, per standing preset.

Prototype disclaimer applies. All data synthetic. No operator chat text in any artifact; authorization recorded as GO + timestamp only.
