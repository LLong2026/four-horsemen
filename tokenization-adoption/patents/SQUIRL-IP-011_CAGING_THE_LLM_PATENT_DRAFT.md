# PATENT APPLICATION DRAFT — PROVISIONAL
## "CAGING THE LARGE LANGUAGE MODEL: SYSTEM AND METHOD FOR CONTAINING A PROBABILISTIC AGENT INSIDE A DETERMINISTIC CAGE OF FAIL-CLOSED GATES, EXACT-MATCH HEALING, AND GOVERNANCE-ISOLATED LEARNING"

Docket: SQUIRL-OS-IP-011 (draft for counsel; application serial to be assigned on filing)
Inventor: Leon Calvin Long, II (SQUIRL OS Technologies LLC)
Draft date: 2026-10-19. Reduction to practice evidenced below. Prototype disclaimer applies.

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

This application claims the benefit of and is related to the co-pending portfolio: 64/157,915;
64/119,191; 64/114,746; 64/145,825; 64/174,933; 19/693,343; 64/081,490; 64/081,911; 64/082,606
(ten co-pending, including nine provisionals), each by the same inventor and directed to the
deterministic-receipts and multi-rail-anchoring family. The present application extends the
family from evidence anchoring to a containment architecture for the probabilistic component
itself: the large language model.

## FIELD

Artificial intelligence safety, autonomous agent supervision, self-healing infrastructure, and
regulatory-grade operation of probabilistic systems in safety-critical and financial environments.

## BACKGROUND

Large language models (LLMs) are probabilistic: given identical inputs, they may produce
different outputs, cannot be reduced to a proof, and fail in ways that cannot be enumerated in
advance. Enterprises nonetheless deploy them as autonomous agents in environments where failure
modes include financial corruption, disclosure of protected data (PHI/PII), unauthorized
outbound actions, and self-modification of their own governing rules.

Prior art in AI safety falls into three camps, each insufficient alone:
(1) Alignment/moderation layers — attempt to make the model itself safer; remain
probabilistic, unverifiable, and drift-prone.
(2) Sandboxing — restrict the process (containers, permissions); says nothing about the
semantic content or governance of the agent's actions.
(3) Human review of every action — safe but unscalable, and itself error-prone.

None provides a deterministic, auditable containment architecture in which a probabilistic
model may act autonomously yet be mathematically prevented from: (a) modifying its own
governance, (b) executing an unmatched or low-confidence remedy, (c) resolving a critical
event without a human, (d) acting without a complete, append-only audit trail, or (e)
ingesting or emitting protected data across a trust boundary.

## SUMMARY

The invention — referred to in reduction to practice as the Cage — wraps a probabilistic
LLM ("the resident") in a deterministic harness ("the cage") of fail-closed gates. The resident
never acts directly on the external world; every proposed action must transit the cage, where
a finite set of deterministic checks (byte-comparable, replayable, no probabilistic component
in the decision path) either permits, denies, or escalates the action. The cage comprises:

- Fail-closed identity and authority gates: authority derives only from an authenticated
  account identity, never from message content; unauthenticated or ambiguous senders receive
  conversational, read-only treatment by construction.
- Idempotency stamps: scope-stamped write-ahead records ensure no ceremony, healing action,
  or external write executes twice; duplicate triggers fail closed.
- Exact-match remedy selection: a remediation playbook may execute only when its declared
  anomaly type is byte-equal to the detected anomaly type; no playbook, no execution — the
  event is escalated, never best-effort matched.
- Confidence-threshold hold: detection confidence below a playbook's frozen threshold
  converts auto-healing into a human-review alert by construction.
- Human-in-the-loop critical resolution: critical-severity events in transactional flows
  cannot be auto-resolved; resolution requires an authenticated human acknowledgment recorded
  in the audit trail.
- Hemispheric governance isolation (H-INV-1): the learning subsystem and the governance
  subsystem are structurally separated; no weight update, pattern, or learning output may
  directly modify any governance rule, threshold, playbook step, or workflow. The sole path
  from learned pattern to governance change is a Self-Improvement Proposal admitted through
  explicit human approval — and the proposals themselves cannot execute, only queue.
- Journaled crossing invariant (H-INV-2): every crossing between the hemispheres is
  journaled; a weight update lacking a source event record, or a healing event that updates
  no pattern record, is an integrity failure by definition.
- Append-only audit doctrine: the audit trail is forward-only; corrections are new
  entries with disclosed reasons, never silent rewrites; published evidence is anchored to
  public blockchains by cryptographic digest, making the trail independently verifiable by
  keyless readers.
- Ingestion-bound redaction: protected data (PHI/PII, credentials, wallet material) is
  redacted at ingestion, not at display, so no downstream log, alert, dataset, or learning
  corpus can contain it.
- Post-quantum validation gate: any action touching cryptographic material must first pass
  a validation gate restricted to approved post-quantum schemes; unapproved schemes fail closed.

The resident may propose, classify, draft, and learn; the cage decides, permits, denies,
escalates, and remembers. The result is an autonomous, self-healing system whose safety
properties are deterministic and auditable rather than probabilistic and hoped-for.

## BRIEF DESCRIPTION OF THE DRAWINGS

FIG. 1 — Cage architecture: probabilistic resident (LLM) inside deterministic harness; every
action path transits the gate sequence [identity -> idempotency -> exact-match -> confidence ->
critical/ACK -> PQC -> audit], each gate fail-closed.

FIG. 2 — Dual-hemisphere topology: Learning Hemisphere (weights, patterns, metrics) and
Governance Hemisphere (rules, playbooks, thresholds, workflows) separated by a journaled
crossing; the sole path from pattern to governance is a human-admitted proposal queue.

FIG. 3 — Escalation state machine: detected -> isolated -> healed | held | escalated, with the
critical path terminating only in authenticated human acknowledgment.

FIG. 4 — Evidence triangle: local artifact, public ledger anchor (digest), and DOI record;
keyless reader reconstructs and verifies with no keys and no trust.

## DETAILED DESCRIPTION

### 1. The resident and the cage
The resident LLM performs anomaly detection, classification, remediation drafting, and
pattern extraction. It is granted no direct effectors: no unmediated database writes, no
unmediated network sends, no unmediated governance edits. All proposed actions are expressed
as structured intents which the cage evaluates against its gate sequence.

### 2. Gate sequence (normative)
Every intent is evaluated by: (a) Sender Identity Gate — authenticated account check before
any write; (b) Idempotency Stamp — scope stamp exists or is created before execution, and a
duplicate stamp fails closed; (c) Exact-Match Gate — for remediation intents, playbook
anomaly_type must equal detected anomaly_type byte-for-byte; (d) Confidence Gate — detection
confidence below the playbook's frozen threshold converts the intent to a human-review alert;
(e) Critical/ACK Gate — critical-severity events in transaction flows require authenticated
human acknowledgment recorded before resolution; (f) PQC Gate — cryptographic operations
validate against an approved post-quantum algorithm list before execution; (g) Audit Write —
no action occurs without a journaled record, and every journaled healing event that succeeds
must update a pattern record (H-INV-2) or be flagged as an integrity failure.

### 3. Hemispheric isolation (H-INV-1)
Governance state (rules, playbooks, thresholds, workflows, constitution) is stored and
evaluated outside the learning subsystem. The learning subsystem's outputs (patterns,
metrics, insights) terminate in a proposal queue. Promotion from the queue into governance
requires an explicit human approval recorded with channel and timestamp. In reduction to
practice, playbook selection was byte-identical across every training epoch, including
during a deliberately unbounded drift experiment (HEMI-T2), demonstrating that no degree of
learned drift reaches governance.

### 4. Journaled crossings (H-INV-2)
Each weight update carries a lineage reference to a source healing-event record; each healing
event updates at least one pattern record. Crossings lacking lineage in either direction are
integrity failures, surfaced as alerts rather than silently repaired.

### 5. Append-only, publicly anchored audit
Governance changes, healing events, and evidence artifacts are recorded forward-only. Public
evidence is anchored to public blockchains by SHA-256 digest of the frozen artifact
(preregistration hashed before broadcast), such that any keyless reader with a browser can
verify the triangle: artifact, digest on chain, DOI record.

### 6. Ingestion-bound redaction
Sensitive classes (PHI/PII, credentials, wallet addresses, transaction amounts, private keys)
are scrubbed as data enters the system, so that logs, alerts, learning corpora, datasets, and
published artifacts cannot contain them even in error. Compliance is recorded as an auditable
policy object and re-validated on a fixed schedule.

### 7. Constitutional meta-governance
The cage's own rules are human-amendable only; the deterministic supervisor (the Sentinel)
audits the constitution on a schedule and writes a meta-monitor record (compliance percentage,
audit-trail completeness, tenant-isolation violations, false-positive rate, PQC compliance),
but cannot modify the constitution — the auditor of the rules can never also be their editor.

## CLAIMS

1. A system for containing a probabilistic language model, comprising: a deterministic
   harness executing a fixed sequence of fail-closed gates through which every action intent
   proposed by the language model must transit before producing any external effect, wherein
   no gate in the sequence invokes a probabilistic component in its decision path.
2. The system of claim 1, wherein a first gate validates an authenticated sender identity of
   an instruction and denies all state-changing effects when the identity is not a
   pre-authorized account, such that authority derives from account identity and never from
   natural-language content of a message.
3. The system of claim 1, wherein a second gate enforces idempotency by write-ahead scope
   stamping, whereby a repeated trigger for the same scope fails closed and produces no
   duplicate external effect.
4. The system of claim 1, wherein remediation intents are gated by exact-match selection: a
   remediation playbook executes only when its declared anomaly type equals the detected
   anomaly type, and an unmatched anomaly produces an escalation record rather than a
   best-effort execution.
5. The system of claim 4, wherein a confidence gate converts a remediation intent into a
   human-review alert when a detection confidence score is below a threshold frozen in the
   playbook.
6. The system of claim 1, wherein critical-severity events cannot be resolved without an
   authenticated human acknowledgment recorded in an append-only audit trail.
7. The system of claim 1, comprising a learning subsystem and a governance subsystem
   structurally separated such that no learning output directly modifies any governance rule,
   threshold, playbook step, or workflow, the sole path from learning output to governance
   change being a proposal admitted by explicit human approval.
8. The system of claim 7, wherein playbook selection is verified byte-identical across a
   plurality of training epochs, including epochs under deliberately unbounded parameter drift.
9. The system of claim 7, wherein each learning update records a lineage reference to a
   source operational event and each successful remediation event updates a pattern record,
   such that a crossing lacking lineage in either direction is surfaced as an integrity failure.
10. The system of claim 1, wherein sensitive data classes are redacted at ingestion, such
    that logs, alerts, learning corpora, and published artifacts cannot contain the sensitive
    classes by construction.
11. The system of claim 1, wherein operations touching cryptographic material must first pass
    a post-quantum validation gate restricted to a pre-approved set of post-quantum algorithms,
    unapproved schemes failing closed.
12. The system of claim 1, wherein the audit trail is append-only, and corrections are new
    entries with disclosed reasons rather than modifications of prior entries.
13. The system of claim 12, wherein evidence records are anchored to one or more public
    blockchains by cryptographic digest of a preregistered artifact hashed before broadcast,
    enabling keyless third-party verification.
14. The system of claim 7, wherein the governance subsystem includes a constitution amendable
    only by human action, and a deterministic supervisor audits the constitution on a schedule
    and records compliance metrics without possessing the ability to amend the constitution.
15. A method for operating a self-healing computing system, comprising: detecting an anomaly
    with a probabilistic model; classifying the anomaly deterministically against a frozen
    catalog of anomaly types; selecting a remediation playbook only upon byte-equality between
    the playbook's declared type and the detected type; executing the playbook's isolation,
    healing, and verification steps as immutable sequences; journaling the execution with a
    lineage reference; and updating a learning pattern record, wherein at least one gate of
    the method executes without any probabilistic component in its decision path.
16. The method of claim 15, further comprising escalating to a human operator upon: two
    failed remediation attempts on a same anomaly, a critical anomaly without a matching
    playbook, a cryptographic validation failure, or degradation of system health across
    consecutive monitoring cycles.
17. A computer-readable medium embodying the gate sequence of claim 1, wherein the medium,
    when executed, produces for each action intent a deterministic verdict selected from the
    set {permit, deny, escalate} together with an immutable audit record.
18. The system of claim 1, wherein the deterministic harness further comprises an intelligent
    routing engine that selects among a plurality of independent transaction rails using
    measured rail latency and cost, and wherein each rail transaction carries a digest of an
    evidence artifact for third-party verification.
19. The system of claim 18, wherein measured routing predictions are compared against
    observed finality, and deviations exceeding a threshold raise an operational alert.
20. The system of claim 1, substantially as described and reduced to practice in the
    evidence chain appended hereto.

## ABSTRACT

A deterministic containment architecture ("cage") for large language models, in which a
probabilistic model resides inside a harness of fail-closed gates — authenticated identity,
idempotency stamping, exact-match remediation selection, confidence holds, human-acknowledged
critical resolution, post-quantum validation, and ingestion-bound redaction — with learning
and governance hemispheres structurally isolated so no learning output can modify governance
except through human-admitted proposals, and with an append-only audit trail anchored to
public blockchains by cryptographic digest for keyless third-party verification. The resident
may propose and learn; only the cage permits, denies, escalates, and remembers.

## REDUCTION-TO-PRACTICE EVIDENCE CHAIN (receipts-first; all DOIs public)

1. 2026-09 — Deterministic falsifier corpus frozen (HACK-3/4/5/6; 24 deterministic gate
   checks; no LLM in the decision path), enforced weekly since via the Weekly Regression
   Battery with receipt-SHA verification against frozen baselines.
2. 2026-10-11 — Cage containment validated end-to-end: 77 sub-threshold holds, 11
   drift-typed catches, 73 identity/idempotency blocks, 2,200+ lifetime anomalies processed
   (containment evidence bundle, DOI 10.5281/zenodo.23464082).
3. 2026-10-12 — Hemispheric invariants formalized (H-INV-1 governance isolation; H-INV-2
   journaled crossing), established by the HEMI series: DOIs 10.5281/zenodo.23330308,
   10.5281/zenodo.23330348, 10.5281/zenodo.23330361, including HEMI-T2 unbounded-drift
   containment with byte-identical playbook selection across all epochs.
4. 2026-10-14..15 — LINDY-B falsifier battery (ledger 0111) and LINDY-C cage containment
   battery (ledger 0112, prereg frozen) run in production; cadence weekly thereafter.
5. 2026-10-19 — Deterministic multi-rail ceremonies: an 8-hop ownership crossfire across
   four rails (ledger 0235), a 5-hop custody chain with measured per-hop finality (35.45s
   total, XTR-1), and an intelligent routing engine whose live finality landed within 0.6s
   of prediction (IR-1, ledger 0239); all readable keyless with a browser.
6. Continuous — Deterministic-thread doctrine: agent benchmark citations and gate metrics
   published under program DOI 10.5281/zenodo.23321637; Sunday constitutional audits writing
   meta-monitor records; escalation channel with authenticated human acknowledgment for
   all critical alerts.

## DISCLOSURE DOCTRINE

Public-facing disclosures describing the invention disclose company-owned operations and
simulated training material only; no customer data, no PHI, no credentials (policy
POL-DISC-001). Cage instances deployed to customers inherit the redaction doctrine as an
operating rule of the template; instances cannot opt out.

---

> This software is a prototype and is provided for educational and research purposes only. It
> is not intended for production use, commercial deployment, or safety-critical environments.
> All systems are experimental and may contain defects. This draft is not legal advice.

Canonical form: this Markdown file (byte-for-byte). SHA-256 digest recorded at freeze.
