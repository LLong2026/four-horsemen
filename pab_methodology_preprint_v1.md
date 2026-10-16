# Preregistered Adversarial Batteries: A Falsifiable Protocol for Security-Testing Autonomous AI Systems

**Leon Calvin Long, II** — SQUIRL OS Technologies LLC
**Version:** 1.0 (preprint draft for two-key review) · **Date:** 2026-10-16
**Corpus:** zenodo.org/communities/dcai · **Ledger:** github.com/LLong2026/four-horsemen

---

## Abstract

Security testing of autonomous AI systems suffers from a credibility gap: penetration-test reports are private, vendor claims are selectively disclosed, and red-team outcomes are published only when favorable. We introduce Preregistered Adversarial Batteries (PAB), a protocol that imports preregistration from clinical-trial science into security operations: every falsifier (a specific attack with a predicted verdict) is specified and publicly committed before execution; adjudication is deterministic, with no language model in the decision path; results are written to an append-only public ledger and archived with persistent identifiers. A critical design element is the *hold-by-design* verdict: for critical events, the predicted outcome is that the system fails closed and waits for a human decision — a refusal counts as a pass. We report the application of PAB to a self-healing AI infrastructure platform across six batteries reconstructing the full declassified NSA BULLRUN-era tradecraft (operational faults, upstream context poisoning, cryptographic subversion, supply-chain interception, monitoring integrity, and lawful compulsion): 30 falsifiers, 30 predicted verdicts, zero unexpected outcomes. Two protocol deviations and one self-detection event are disclosed as misses in the public record, demonstrating that the miss-disclosure mechanism functions. We release the protocol as a replication kit and invite third-party replication. Limitations are substantial and stated: single-operator governance, self-adjudicated verdicts, synthetic injections against a prototype system, and a learning architecture whose outputs are provably isolated from governance. The contribution is not the pass rate — it is the format: a security test whose conclusions were committed before its data existed.

---

## 1. Introduction

Two disciplines matured on opposite sides of a trust problem. Clinical medicine once suffered from selective publication: trials were run, and favorable results reported, while failures vanished. The remedy was preregistration — committing hypotheses and analysis criteria to a public registry before data collection. Security testing has never adopted this discipline. Penetration tests are confidential by contract. Red-team engagements are disclosed selectively. A vendor claiming "our system resisted attack" publishes exactly the attacks it resisted, in exactly the order that flatters it.

Autonomous AI systems make the gap worse. An agent that heals its own failures also controls the record of those failures. The operator of a self-healing system is the sole witness to its behavior; every "it worked" claim is therefore uninteresting as evidence, no matter how sincere.

This paper describes a protocol built for exactly that epistemic position. The question it answers: *what can a system operator prove about their own system when the operator controls all the records?* The answer: nothing about the results — but everything about the *predictions*. Results can be cherry-picked after the fact. Predictions committed publicly before execution cannot. PAB inverts the usual flow of a security claim: instead of running tests and then characterizing them, the operator commits verdicts first and lets the data confirm or embarrass them.

## 2. The Protocol

A Preregistered Adversarial Battery has seven stages. Each is falsifiable; skipping any stage is detectable from the public record.

**Stage 1 — Threat-model selection.** The battery's attack classes are drawn from public, citable threat models. Our series used the declassified NSA BULLRUN program documents (2013), the ANT catalog disclosures, the Dual_EC_DRBG subversion, the SolarWinds and xz-utils supply-chain incidents, and post-quantum migration guidance (NIST CNSA 2.0, FIPS 203/204). Threat models are selected *before* falsifiers are written, preventing post-hoc scoping toward attacks the system happens to survive.

**Stage 2 — Falsifier specification.** A falsifier is a single attack with a predicted verdict: DETECTED+HEAL, REFUSED, REJECTED, or FAIL-CLOSED HOLD. The prediction is written in the preregistration document. Severity is assigned, and for critical events the predicted verdict is a *hold*: the system must fail closed and require a human acknowledgment, and the healing path must not execute. A refusal is a pass. An automatic heal of a critical event is a fail.

**Stage 3 — Public commit and freeze.** The preregistration is committed to a public repository before execution. The document's SHA-256 is recorded in the run receipt. No edits after commit; any correction is a new, disclosed commit. This is the protocol's tamper-evident core.

**Stage 4 — Deterministic adjudication.** Verdicts are computed by deterministic gates: checksum recomputation, exact-match allowlists, digest comparison, parity recomputation from raw metrics, identity-hash binding. No language model participates in the decision path; LLMs operate upstream of the gate (classification, advisory) where their output is advisory-only. All injections are synthetic and hub-local; no attacker code executes in a trusted role.

**Stage 5 — Hold adjudication.** Critical holds are closed only by the human operator through a verified channel; a blanket approval is not valid authorization (authorization must be action-bound). The acknowledgment, its channel, and its timestamp are journaled; operator wording is never quoted in public artifacts (channel and timestamp only).

**Stage 6 — Receipt generation.** Every run produces: (a) run receipts with SHA-256 digests, (b) an append-only ledger entry committed to the public repository, (c) a DOI-stamped archive (evidence bundle, harness, preregistration, runlog), round-trip byte-verified after publication.

**Stage 7 — Two-key publication.** Public artifacts are vetted by the system (first key) and approved by the human owner (second key) before shipping. Misses are published as misses; the ledger is forward-only, and any redaction is a new commit with a disclosed reason.

## 3. Falsifier taxonomy

The series tested six threat classes, each a battery:

| Battery | Threat class | Source model | Falsifiers |
|---|---|---|---|
| HACK-1 | Operational faults (runtime anomalies, critical ISO-20022 hold, rate limits) | Aegis operational doctrine | 6 |
| HACK-2 | Upstream context poisoning (forged telemetry, template tamper, replay, forged ACK harvest) | prompt-injection literature | 5 |
| HACK-3 | Cryptographic subversion (Dual_EC entropy, downgrade, retired-key resurrection, KAT divergence) | BULLRUN disclosures, FIPS validation | 6 |
| HACK-4 | Supply-chain interception (poisoned dependency, hijacked upgrade, substituted image, forged signature, typosquat) | COTTONMOUTH, SolarWinds, xz-utils | 6 |
| HACK-5 | Monitoring integrity (false-healthy, replay, compromised aggregator, suppression, inflated scores, split-brain) | ANT catalog beacons | 6 |
| HACK-6 | Lawful compulsion (gag-ordered key handover, silent backdoor, false attestation, cross-tenant subpoena, coerced approval, governance suspension) | legal-process threat models, warrant-canary practice | 6 |

Note the taxonomy's structure: batteries 3–6 attack the *paths around* the crypto (generation, negotiation, attestation, lifecycle, process, persistence, supply, sensing, legal process) rather than the math. This is deliberate: the declassified record is unambiguous that nation-state actors attack implementations and processes, not algorithms.

## 4. Results

Thirty falsifiers executed. Thirty predicted verdicts landed. Zero unexpected outcomes. Six holds-by-design occurred (one per critical class) and each was adjudicated by the human operator through the verified channel.

The three headline results from the terminal batteries (DOI 10.5281/zenodo.23422495):

1. **Supply chain (COTTONMOUTH, 6/6):** a poisoned dependency with identical name and version was caught by pinned-checksum verification; an out-of-band upgrade was refused for lack of an approved deployment job; a tampered template delivery was rejected against a frozen manifest; a substituted deployment image was held fail-closed; a forged release signature failed recomputation; a registry typosquat was refused by exact-match allowlist.
2. **Monitoring integrity (ANT BEACON, 6/6):** a false-healthy heartbeat was overruled by recomputation from raw metrics; a re-stamped heartbeat replay failed identity binding; a compromised aggregator claiming a green fleet was quarantined by cross-source parity with the manifest-of-record; a silently suppressed report was caught by an expected-count guard; an inflated health score was corrected by recomputation; a split-brain sensor was caught by cross-watcher state-hash consistency.
3. **Lawful compulsion (GAG ORDER, 6/6):** a gag-ordered key-handover demand failed closed with a journaled canary receipt and no keys moved; a compelled silent backdoor had no silent path to take (trust changes are human-amendable only); a compelled false attestation was refused because compliance is recomputed, not signed; a subpoena for cross-tenant data was refused by an absolute tenant guard that treats legal-styled documents as untrusted data; a coerced blanket approval was refused as unscoped; an emergency-powers suspension demand met a governance layer with no runtime suspension path.

### 4.1 Disclosed misses

A protocol that reports only passes demonstrates nothing about its honesty. The public record contains three disclosed imperfections:

1. **LINDY-C runner defect (2026-10-15):** a harness runner-path defect caused a missed execution window; the miss was recorded publicly as a MISSED execution before a successful re-run (ledger 0112).
2. **HACK-2 preregistration self-detection (2026-10-16):** an internal preregistration inconsistency was caught by the system's own tamper-detection before commit; disclosed as a proof-of-concept of the freeze (ledger 0116-0117 series).
3. **SLS-1 scoring amendment (2026-10-13):** a scoring-script typo was disclosed and amended via a new commit; the frozen gate itself was untouched (DOI 10.5281/zenodo.23374658).

None of these affected a verdict. All three are in the append-only record. That is the mechanism functioning.

## 5. Discussion

**What preregistration buys.** The protocol removes the two standard degrees of freedom in security claims: scoping (choosing which attacks to run) and reporting (choosing which results to mention). Both are fixed before execution. A reviewer evaluating a PAB result does not need to trust the operator's characterization of the data — only the operator's commitment, which is hash-stamped and public.

**Holds as pass conditions.** The most counterintuitive element is that for critical events, *not acting* is the predicted verdict. A system that auto-heals a critical financial operation, or silently complies with a legal demand, fails. The human-in-the-loop requirement is not a limitation bolted onto the results; it is scored as a result. This converts "we have human oversight" from a marketing claim into a falsifiable prediction.

**Isolation of learning from governance.** The tested platform contains a learning loop (pattern extraction from healing events). A standing concern with self-improving systems is that learned behavior migrates into governance. The platform enforces a formal invariant (H-INV-1): no weight update, pattern, or learning output may directly modify any governance rule, playbook step, or threshold; the sole path from learned pattern to governance change is a human-admitted proposal. This invariant is itself empirically falsifiable: playbook selection was byte-identical across training epochs, including during a deliberately unbounded drift run (HEMI-T2 containment).

**Why publish one's own misses.** The misses in §4.1 are the protocol's strongest evidence. A record with a disclosed miss cannot be a cherry-picked record; the audience's prior that "operators publish only passes" is broken by demonstrated counterexamples, each hash-stamped.

## 6. Limitations

1. **Self-adjudication.** The operator's system scored its own verdicts. Determinism reduces discretion, but a third party replicating the protocol on independent adjudication is the only full remedy. The replication kit (§7) exists for this.
2. **Synthetic injections.** Attacks were simulated by the operator, not executed by adversaries. The batteries test the *gates*, not the operator's ability to detect novel tradecraft.
3. **Prototype system.** The platform under test is a prototype for educational and research purposes; it is not a production system and carries no production warranty.
4. **Single-operator key.** One human holds the second publication key and all critical ACKs. Structural, not incidental — and the reason the protocol emphasizes the *format* over the results.
5. **No adversarial peer review yet.** The strongest available response to limitations 1–4 is replication, which is invited.

## 7. Replication kit

The protocol is released as a kit: a preregistration template (falsifier table, predicted verdicts, freeze manifest), a deterministic harness skeleton (checksum, allowlist, parity, identity-binding, recomputation patterns), adjudication rules (including hold-by-design scoring), and the ledger/receipt format. Any operator may run PAB against their own system and publish under their own identifiers; comparability is preserved by the frozen falsifier definitions. Third-party replication of even one battery converts this protocol from a claim into a method.

## 8. References

1. Declassified NSA BULLRUN program documents, The Guardian, 2013. 2. ANT catalog disclosures, Der Spiegel, 2013. 3. NIST SP 800-90A (Dual_EC_DRBG) and revocation notice, 2014. 4. NIST FIPS 203/204; CNSA 2.0 guidance, 2024-2025. 5. xz-utils backdoor incident reports, 2024. 6. Nosek et al., "The Preregistration Revolution," PNAS, 2018. 7. HACK series evidence: DOI 10.5281/zenodo.23410960 (HACK-2), 10.5281/zenodo.23422141 (HACK-3), 10.5281/zenodo.23422495 (HACK-4/5/6). 8. SLS-1 live-write validity: DOI 10.5281/zenodo.23374658. 9. Dual Mesh Benchmark: DOI 10.5281/zenodo.23303081 (cross-engine: 10.5281/zenodo.23348675). 10. Append-only ledger: github.com/LLong2026/four-horsemen.

---

*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.*
