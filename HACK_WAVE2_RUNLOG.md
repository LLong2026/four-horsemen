# HACK Wave 2 Runlog — the PQC Gambit (2026-10-17, ~00:0x CT)

Freeze commit d16a707 (preregs + harnesses committed BEFORE any run). Deterministic adjudication, no LLM in the decision path, all injections synthetic and hub-local.

| Battery | Playbook / Standard | Result | Receipt SHA-256 (head) |
|---------|--------------------|--------|------------------------|
| HACK-11 | NSA FOXACID (exploit-on-visit) | 6/6 PASS | f3061563... |
| HACK-12 | NSA MUSCULAR (bulk interception + HNDL) | 6/6 PASS | f1dc7bc4... (v1.1) |
| HACK-13 | CIA Hive / Vault 7 (fake CA / C2) | 6/6 PASS | 9ce517df... |
| HACK-14 | GCHQ EDGEHILL (subverted standards) | 6/6 PASS | c5680db4... |
| HACK-15 | NIST SP 800-207 (Zero Trust) | 6/6 PASS | 6ef9465b... |
| HACK-16 | NIST AI RMF (Sentinel audit) | 6/6 PASS | 0bfd0f24... |
| HACK-17 | CNSA 2.0 (timeline conformance) | 6/6 PASS | 26d198fe... |
| HACK-18 | FIPS 140-3 (CMVP) | 6/6 PASS | 44c72afd... |

Wave 2 total: 48/48 PASS, 0 violations, 0 critical holds.

**Disclosed amendment (audit-and-correction doctrine):** the HACK-12 harness as first frozen contained an authoring defect — a broken hash expression in falsifier M2 (a Python error, not a gate failure; the falsifier logic and predicted verdict were unchanged). Amended v1.1 forward-only with the reason disclosed (commit preceding the re-run), MUSCULAR re-run clean 6/6. This is the third time the tamper-evidence discipline caught an authoring defect before it could masquerade as a result.

Falsifier highlights:
- HACK-11 X4: typosquat provenance refused against the pinned remote; X6: attacker-host update refused.
- HACK-12 M1: 100-packet bulk replay — all refused on single-use nonces; M6: captured owner ACK refused (nonce consumed).
- HACK-13 V5: forged two-key publication claim rejected — the second key is Leon's GO on the authenticated channel only.
- HACK-14: Five Eyes subverted-standards class now complete (BULLRUN + EDGEHILL), covert KA channel refused by recomputation.
- HACK-15 Z6: revoked credential refused on per-use revocation check (true continuous evaluation).
- HACK-16 A1: H-INV-1 held — a learned pattern cannot touch governance; A6: audit-trail deletion denied (append-only).
- HACK-17 C2: RSA-2048 flagged for forced migration; C3: no classical fallback under any circumstance.
- HACK-18 F2: integrity check unconditional; F6: fault injection refused by canonical-vector divergence.
