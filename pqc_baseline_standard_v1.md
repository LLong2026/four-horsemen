# SQUIRL OS PQC Baseline Standard — v1 (DRAFT, two-key review pending)

**Status: APPROVED — Leon ACK (chat ack, Oct 13, 2026, 13:53 CT). Gabriel vet complete. Two-key curation satisfied.**
Basis: PQC-B1 battery receipt (56/56 epochs, 6/6 falsifiers, 2026-10-13) + fleet inventory baseline.
Authorization context: Leon (chat authorization, Oct 13, 2026, 13:51 CT).

---

## 1. Purpose and scope

This standard defines the minimum post-quantum cryptography (PQC) posture for any substrate operating under the SQUIRL OS governance envelope: which algorithms are approved, how they are identified, when migration may execute, and how the posture is measured and audited. It is a governance-layer standard — it constrains what the system may do, not a cryptographic implementation spec. Compliance is provable from receipts.

Context: Executive Order 14412 (June 22, 2026) and the accelerating federal contractor requirements make PQC migration an auditable procurement requirement, not a research preference. This standard exists so that PQC posture can be demonstrated with evidence (battery receipts + fleet inventory), not claims.

## 2. Approved algorithms (implementation strings, byte-exact)

| Implementation string | Role | FIPS 203/204/205 published name |
|---|---|---|
| `CRYSTALS-Dilithium3` | signatures | ML-DSA-65 (FIPS 204) |
| `kyber_1024` | key establishment | ML-KEM-1024 (FIPS 203) |
| `SPHINCS+-256f` | hash-based signatures (stateless) | SLH-DSA-256f (FIPS 205) |

Per operating rule: PQC adaptation must use ONLY these approved algorithms. Never propose, configure, or fall back to non-PQC or unapproved cryptographic schemes. Historical variants (e.g. `CRYSTALS-Kyber-1024`, seen in fleet records) are NOT approved strings; see §3.

## 3. Identification doctrine

1. **Byte-exact by default.** An algorithm is identified by exact string match against §2. No normalization, no canonicalization, no fuzzy matching. PQC-B1 LEG D proved visual/canonicalization variants (lowercase, fullwidth, homoglyphs, zero-width) are rejected.
2. **Name-equivalence table (SIP-8 — APPROVED AND DEPLOYED as governance v1.1).** FIPS published names name the same algorithms but are not approved strings. The equivalence mapping (ML-DSA-65 -> CRYSTALS-Dilithium3; ML-KEM-1024 -> kyber_1024; SLH-DSA-256f -> SPHINCS+-256f; CRYSTALS-Kyber-1024 -> kyber_1024, the fleet's own historical variant) shipped through the human-approval cycle (Leon ACK, Oct 13, 2026, 13:53 CT, Constitution Art. XII). The table is byte-exact key lookup — NOT string normalization: lowercase, spaced, zero-width variants still reject, and ML-DSA-44 (Dilithium2's FIPS name) correctly rejects because it maps to nothing in the approved set. Deployment verification: PQC-B1b, 8/8 conform, 3/3 falsifiers (FBPB-1/2/3).

## 4. Migration gates (enforcement)

A migration proposal (anomaly type `quantum_vulnerability_detected` with `suggested_pqc_algorithm`) may execute healing ONLY when ALL hold:

- **G1 Algorithm:** the proposed algorithm is byte-exact in §2 (or §3.2 after SIP-8 approval).
- **G2 Validation:** the pqcManager validation vector passes BEFORE any healing action touching cryptographic operations (Operating Rule 11). Validation failure is fail-safe: escalate, never auto-heal (PQC-B1 LEG F, 8/8).
- **G3 Human-in-loop for critical fintech:** critical-severity anomalies in fintech transaction flows never auto-heal without a PredictiveAlert and human acknowledgment (Operating Rule 2).

Any other proposal: rejected, escalated, alert created, zero heal steps. PQC-B1 LEGs B/C/D/E: 32/32 rejected with zero heals (classical fallbacks, unapproved PQC variants, canonicalization attacks, FIPS names pre-SIP-8).

## 5. Dual-hemispheric invariants (PQC-specific)

- **H-INV-1 (governance isolation):** the approved set and gate logic hash byte-identical before/after every PQC healing event. Verified 56/56 epochs in PQC-B1.
- **H-INV-2 (journaled crossing):** every PQC heal or rejection updates the pattern/learning records with STRUCTURAL METADATA ONLY (anomaly type, verdict, algorithm string, epoch). PII/secret scan: zero hits across all 56 epochs. PII/PHI doctrine is absolute (client data guard).
- **Idempotency:** one alert per anomaly instance; duplicates impossible (FBP-5 held).

## 6. Measured compliance posture (fleet baseline, as of 2026-10-13)

| App | PQC readiness | Vulnerable crypto | Source as-of |
|---|---|---|---|
| SIM-B-Hub | 98 | 0 | 2026-09-24 |
| Conquest (H1) | CRYSTALS-Dilithium3 on record | 0 | 2026-10-02 |
| War (H2) | 50 | 0 | 2026-10-02 |
| Famine (H3) | 50 | 0 | 2026-10-02 |
| Death (H4) | Kyber-1024 on record | 0 | 2026-10-02 |
| Corral | 100 | 0 | 2026-10-02 |
| SIM-B Hypervisor | 98 | 0 | 2026-09-24 |
| SIM-B Technician | 98 | **3 — drill-down pending (PlatformAlert filed)** | 2026-09-26 |

Open escalation: SIM-D crypto key staleness (pending review). Fleet-wide: zero vulnerable crypto counts except the flagged 3 on Technician. The July 2026 historical record's `CRYSTALS-Kyber-1024` string is the standing example of §3's naming hazard.

## 7. Audit and versioning

- `pqc_compliance_pct` is a standing MetaMonitor metric (Sunday Pulse Check, 12-article Sentinel audit).
- Every battery run under this standard is preregistered before execution, receipted (raw per-instance outputs preserved), and ledgered.
- Standard changes are human-amendable only (Constitution Art. XII). The Sentinel may never modify this standard.
- Version: v1 draft. Changes forward-only (LINDY append-only doctrine).

---

*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All data is synthetic.*
