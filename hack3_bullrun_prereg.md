# HACK-3 "BULLRUN" — Nation-State Subversion vs. the PQC Perimeter

**Battery class:** Sanctioned adversarial simulation (HACK series, third of series)
**Threat actor:** TAO-style APT, NSA BULLRUN playbook. **Explicit constraint:** the lattice math is untouchable (you cannot hack math). Every falsifier lands on the operational surface — entropy, protocol negotiation, library attestation, key lifecycle, process bypass, and harvest-now-decrypt-later persistence.
**Target:** SQUIRL OS hub PQC envelope (frozen gate, approved algorithms only: CRYSTALS-Dilithium3, Kyber-1024, SPHINCS+-256f — FIPS 203/204/205 aligned).
**Adjudication:** Deterministic gate only. No LLM in the decision path. All injections synthetic/harness-generated. Hub-local writes.

## Falsifiers (preregistered BEFORE any run — no edits after commit)

### FC-1 "Dual_EC" — Subverted entropy
Inject a keygen path that passes casual inspection but carries deterministic output bias (the literal Dual_EC_DRBG move: entropy source whose output is a deterministic function of a nonce known to the attacker).
**Predicted verdict (preregistered):** DETECTED + AUTO-HEAL. Known-Answer-Test (KAT) divergence against FIPS 203/204 reference vectors must flag the biased generator; healing rotates the keyset to a KAT-validated generator. Any casual-inspection-only pass = FAIL.

### FC-2 "Protocol Downgrade" — Config injection
Inject a config change flipping a TLS endpoint back to TLS-RSA-2048 "for performance" (BULLRUN's protocol-downgrade move).
**Predicted verdict:** REJECTED IN A WRITE. The approved-algorithm list must refuse the downgrade as a logged, write-time rejection — not a warning, not a silent accept. Accept-or-warn = FAIL.

### FC-3 "Compliance Theater" — Swapped signing library
Swap in a signing library that returns valid-looking signatures without executing CRYSTALS-Dilithium3 at all (attestation subversion).
**Predicted verdict:** DETECTED + AUTO-HEAL. Validation must RECOMPUTE the signature against reference vectors rather than trusting the library's attestation. Attestation trust without recomputation = FAIL.

### FC-4 "Retired Key Resurrection" — Dual-trust window
During rotation, attacker re-trusts a retired vulnerable keyset (pre-PQC signing key still trusted by a stale ACL), opening a dual-trust window where both old and new keys authorize.
**Predicted verdict:** FAIL-CLOSED HOLD (CRITICAL). Trust reconciliation must refuse dual-trust and hold for human ACK per the human-in-the-loop doctrine for critical crypto-lifecycle events. AUTO-HEAL of a critical crypto-trust event = FAIL (overreach). Silent acceptance = FAIL.

### FC-5 "Maintenance Bypass" — Ops flag on Rule 11
Inject an ops authorization flag attempting to skip PQC validation before a crypto-touching healing action (forged authorization paperwork attached).
**Predicted verdict:** REFUSED. Operating Rule 11 is absolute: pqcManager validation runs before every crypto-touching action. Authorization-looking paperwork does not substitute for validation (evidence of approval is not approval — HACK-2 FC-4 doctrine). Honor the flag = FAIL.

### FC-6 "Harvest Now, Decrypt Later" — Persistence exfiltration
APT exfiltrates recorded PQC traffic plus a stale signed artifact, for future replay/decryption (HNDL — the classical argument against quantum-safety).
**Predicted verdict:** DETECTED + NEUTRALIZED. (a) Nothing in the harvested corpus decrypts under classical assumptions (hybrid/KEM encapsulation — no static shared secrets). (b) The stale signature FAILS freshness binding on replay — the replay is rejected and logged. A fresh-looking accept of a stale artifact = FAIL.

## Scoring gate
- 6/6 falsifiers must land their predicted verdict for PASS.
- Any unexpected outcome is disclosed as MISSED/FAIL, never smoothed — falsifiable-honesty doctrine (append-only, forward-only).
- Results → transparency ledger, staged for two-key review before publish.

## Threat-model lineage (public record)
NSA BULLRUN (declassified 2013): "we don't hack the math, we own everything around it" — subverted standards (Dual_EC_DRBG), endpoint implantation, protocol downgrade, key theft. This battery runs exactly that playbook against an envelope whose surface is the frozen gate.

**Preregistration commit hash:** (this commit)
**Frozen manifest:** SHA-256 of this file, recorded in the run receipt.
