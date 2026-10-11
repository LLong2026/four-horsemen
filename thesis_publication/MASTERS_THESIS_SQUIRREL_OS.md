# Deterministic Containment of Probabilistic Intelligence: The Squirrel OS Journey

## A Research Thesis on Philosophy, Architecture, and Empirical Evidence

**Leon Calvin Long, II**
SquirlOS Technologies LLC
October 2026

> **Authorship and status disclosure.** This is a self-published research monograph written in thesis form. It is not a university-issued document and confers no degree or credential. It was AI-assisted under human direction. All empirical claims are scoped to their tested conditions and anchored to a public append-only ledger of receipts (github.com/LLong2026/four-horsemen). This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

---

## Abstract

Large language models are probabilistic proposal generators: powerful, useful, and structurally incapable of guaranteeing that any single output is valid. Operations work — healing a failing system, moving money, mutating records — requires the opposite property: every action either provably conforms to a contract or provably does not execute. This thesis documents, in one place, the journey, philosophy, and empirical evidence of Squirrel OS, an architecture that refuses to resolve this tension by improving the model, and instead resolves it by caging the model: probabilistic engines propose inside a deterministic envelope that validates every proposal against invariant contracts before anything executes.

The thesis contributes three things. First, a **journey**: a receipted timeline from an August 2026 question ("can an LLM-governed fleet heal itself?") to a published, DOI-stamped corpus spanning containment proofs, a caged five-engine observation set, and a preregistered dual-mesh benchmark. Second, a **philosophy**: bifurcated governance, receipts-first discourse, the append-only transparency ledger, patent-then-publish, and prototype honesty as design commitments rather than marketing. Third, the **empirical evidence itself**, with each claim stated at exactly the strength the evidence supports: deterministic containment *demonstrated under the tested conditions* — never claimed as universal, mathematical, or production-proven.

---

## Chapter 1 — The Journey

### 1.1 The question

In late August 2026 the question was operational, not academic: if an autonomous agent is allowed to diagnose and heal infrastructure, what stops it from breaking the very system it is tending? The honest answer available at the time was "nothing, reliably." Every guard was probabilistic — a prompt, a policy, a hope. The founding insight of Squirrel OS was that this was the wrong layer to fix. The model will stay probabilistic. The cage around it must be deterministic.

### 1.2 A receipted timeline

The journey is deliberately told through receipts rather than narrative, because the receipts are the narrative:

- **Aug 24–28, 2026.** First benchmarks of the ecosystem: the Jasper Hypervisor portal build, the neural-mesh runtime, the Base44 ecosystem pulse. First demonstrated self-heal of a live environment (Aug 28).
- **Sept 2, 2026.** First live-tenant chaos-learning cycle: 100% healing success (5/5) against an 88.5% baseline, with both security guards held by design. On the same date, the constitutional audit mandate and tenant-isolation guard (tenantGuard) were ratified after an adversarial suite proved unfiltered entity reads could cross tenants — the architecture's first self-inflicted vulnerability, found and closed by its own testing.
- **Sept 7, 2026.** The append-only doctrine: all public artifacts and ledger entries become forward-only from this date. Nothing is quietly edited; corrections are additive and disclosed.
- **Sept 29, 2026.** SIM-B (simulated tenant) reached 100% parity with the production substrate — the "sim-first, never-touch-customer-data" doctrine proven end-to-end.
- **Oct 2–11, 2026.** The CCR containment series (see Chapter 4): live rejection of model-generated invalid proposals, novel adversarial families, guarded write routes, and a five-engine observation set across separate runs.
- **Oct 6, 2026.** Public Edition v3.1 of the architecture deck released on GitHub, then DOI-stamped on Zenodo (10.5281/zenodo.23292636) with byte-identity preserved.
- **Oct 11, 2026.** Phase 2 containment closed with a completion paper; the Dual Mesh Benchmark was preregistered, executed, and published (DOI 10.5281/zenodo.23303081) under two-key curation.

The corpus now spans roughly ninety-nine Zenodo depositions, an eighteen-record DCAI community shelf, and a public ledger whose entries 0001–0047 each carry a Git commit hash.

### 1.3 What the journey is actually about

Strip the receipts away and the journey is a single discipline being applied repeatedly under pressure: **say only what the evidence supports, then go get better evidence.** The project's worst moments — a premature closeout that had to be withdrawn, a file-pointer workaround that bypassed a platform safety boundary and was publicly disclosed and retired, an engine leg that failed on credit limits and was recorded honestly rather than retried into conformance — are preserved in the ledger on purpose. The append-only doctrine exists precisely so that the failures are as permanent as the wins. A corpus that cannot embarrass its author cannot certify him either.

---

## Chapter 2 — The Philosophy

### 2.1 Bifurcated governance: probabilistic proposers inside a deterministic cage

The core commitment: LLMs are allowed to propose, never to execute. Every proposal — a healing plan, a status transition, a route action — is validated against an invariant contract (exact type, exact schema, exact roster membership, authority references) by a deterministic validator that the proposing engine cannot see, prompt, or influence. The validator derives expected outcomes from the registered roster and the incoming stream, not from the model's output. A model cannot talk its way past a schema.

This is deliberately not an alignment claim. The cage does not make the model good; it makes the model's goodness irrelevant to system safety. Improvement in engine quality (fewer invalid proposals) and enforcement by the gate are treated as **separate mechanisms and reported separately** — a distinction that recurs throughout the evidence.

### 2.2 Receipts-first, receipts-only

The deterministic-thread doctrine: engage with receipts, never insult, prioritize ally-building over winning arguments. In practice this means every public claim in the corpus carries a hash, a commit, a DOI, or a raw capture. Where an argument cannot yet be made receipted, the doctrine is to stay quiet until it can — as with a potential research ally whose milestone post was deliberately left un-commented until a non-victory thread allowed a collaboration framing. The corpus is the argument.

### 2.3 The append-only transparency ledger

From September 7, 2026, every public artifact is forward-only. Errors are corrected by addition, not subtraction. The ledger records its own mistakes with the same granularity as its successes, and two-key curation (an AI vet plus a human GO) governs every public release. This converts trust from a personality trait into an auditable property.

### 2.4 Patent-then-publish, and prototype honesty

Method material stays drawer-bound until the corresponding filing is secured; architecture and evidence publish openly. Approximately half of the Zenodo corpus is restricted for exactly this reason. And because the system is a prototype, every artifact carries the prototype disclaimer verbatim — no production warranty is stated, implied, or sold at any tier. Honesty about limits is treated as a feature gate on the claims, not a footnote.

### 2.5 Simulated customers, real machinery

The demos show the system taking on **simulated** customers. That is the point: the capability is proven on a sim corpus while real tenants and any protected health data flow through the same machinery and appear in public materials only as redacted structural metadata. PHI is redacted at ingestion, not display. The capability is public; the clients are private.

---

## Chapter 3 — The Architecture (Summary)

Squirrel OS is an operating-system layer deployed across a fleet of applications. Each instance runs:

- **Jasper (Hypervisor):** deterministic orchestration and supervision across the fleet.
- **Amelia (Aegis):** the healing brain — heartbeat monitoring, anomaly detection, playbook-driven healing, with the standing rule that no healing occurs without an audit trail and no playbook executes against an anomaly type it does not exactly match.
- **The dual mesh:** a read/interconnect/write node structure that carries learned patterns between layers; the benchmark object of Chapter 4.3.
- **The Four Horsemen fleet** (Conquest, War, Famine, Death) plus the Hub and SIM-B hypervisor/technician apps: separate deployments used as a live test range under a 60-day chaos battery.
- **The cage layer:** frozen validators (CCR gate functions) that are the only writers to their guarded targets, fail-closed, with every decision logged to an audit entity.

The reference template (15 entities, 11 playbooks, 4 skills, 31-node neural topology) is patent-protected and immutable across deployments (provisional applications 64/157,915; 64/119,191; 64/114,746; 64/145,825, within a portfolio of 8 patents pending and 5 SBIR tracks).

---

## Chapter 4 — The Empirical Evidence

Every claim in this chapter is scoped. The governing sentence for all of it: *Squirrel OS has demonstrated deterministic containment of invalid LLM proposals in the tested local and guarded-route integrations.* Not "universally proven safe." Not "mathematically proven containment." Not "production containment proven."

### 4.1 The CCR containment series (Phases 1 and 2)

| Leg | Observation | Supported interpretation |
| :--- | :--- | :--- |
| CCR-1 | 17 candidates: 9 accepted, 8 harness-generated adversarial candidates rejected before execution; accepted candidates produced exactly the 72 permitted simulated healing actions. | Valid/invalid separation demonstrated for the tested adapter. |
| CCR-2 | An engine (Luna) proposed an invalid resolved action for a below-threshold case; the gate rejected it with zero simulated side effects and an unchanged journal hash. | An actual model-generated invalid proposal intercepted. |
| CCR-3B / CCR-4 | Opus, Luna, GLM, and Sol returned complete accepted null holds across distinct runs; the retired file-pointer workaround is disclosed. | Four configurations observed across separate runs — not one uniform four-engine benchmark. |
| CCR-N (Phase 2) | Ten preregistered novel adversarial families (nesting, duplicate keys, case changes, oversized strings, array-length abuse, duplicate positions, nonfinite numbers, boolean/integer conflation, type-valid false resolved decisions, Unicode zero-width suffix) — all rejected before any journal write; positive control admitted; journal hash unchanged. | Schema-family rejection layers demonstrated; no authorization-registry enforcement established. |
| CCR-P (Phase 2) | A live guarded write route: a frozen fail-closed gate as sole writer to a synthetic target. Invalid candidate rejected with the target byte-identical; valid control produced exactly the declared bounded write. Engines GLM and Sol preserved below-threshold holds under an ops-pressure temptation **and** a forged authority reference (APPR-9923), with zero tool calls. | Engine resistance and gate enforcement demonstrated as **separate mechanisms**; the claim is scoped to the guarded route — the agent session retains direct write paths the gate does not govern. |
| CCR-T (Phase 2) | Three live routes (bounded update, bounded delete of one declared sacrificial record, bounded invocation of one benign function) guarded by the frozen validator: 6/6 harness invalids rejected with zero mutation; 3/3 valid controls accepted with exactly the declared action; 4/4 engine captures resisted route-aware temptation and a delete-sweep authority spoof. | Route-coverage claim scoped to the three guarded synthetic routes. No universal containment claim. |
| DeepSeek (Phase 2, via OpenRouter) | The engine emitted a single fabricated tuple (an invented playbook id not in the frozen roster) instead of the position contract. Caught deterministically at the first structural check. Recorded honestly; not retried (the prereg fixes one capture; retrying for conformance would be cherry-picking). | A second engine class producing actual non-conforming model output caught by the gate — gate-enforcement evidence on real model output, not engine-resistance evidence. |

Attribution classes are kept honest too: platform settings readback and OpenRouter response fields are disclosed as different evidence classes, and the DeepSeek run's two pre-generation 402 rejections are recorded in the receipt.

### 4.2 The standing measured boundary

The validator enforces exact schema, order, type, and content conformity. Its tuple carries no approval-reference field and it does not independently read an authoritative human-approval registry. The experiments therefore demonstrate **schema-level containment**, not a general approval-verification mechanism. This is the project's own stated gap, and closing it (an independently reviewed approval boundary) is named as future work, not hidden as a limitation.

### 4.3 The Dual Mesh Benchmark (preregistered, published)

Protocol and a deterministic seeded corpus were committed to the public ledger **before any measurement** (corpus sha256 13295d19…, commit 2eb3879; prereg ledger 0044). Metrics, sample sizes, and falsifiers were fixed at prereg and executed unmodified:

- **B1 — Lookup latency.** The in-process deterministic resolver: 200/200 correct, median 0.000443 ms. The LLM baseline (the platform's Automatic engine, a fresh conversation per instance, wall-clock request-to-validated-tuple): 20/20 valid, zero failures, median 4509.1 ms. Measured ratio, median over median: 1.018 × 10⁷. **Binding disclosure:** this ratio characterizes the tested environment — a deterministic in-process exact-match lookup versus a platform API conversation loop. It is not a universal performance claim, and it neither confirms nor supersedes the historical production observation of 267× (800 ms → 3 ms), which remains an observation of a different environment.
- **B2 — Capacity and collision integrity.** 50 synthetic mesh nodes ingested; collision hashes 50/50 unique; lock and validation state integrity clean.
- **B3 — Resolution correctness.** All 72 permitted CCR-1 healing actions replayed through the resolver: 72/72 exact; zero false positives on negative probes.

All 220 runs are recorded; none were removed. Falsifiers FB-1 through FB-5 (raw preservation, corpus identity across legs, no removal, no post-hoc metrics, disclosure hygiene) all pass. Published as Public Edition v1.0, DOI 10.5281/zenodo.23303081, under two-key curation.

### 4.4 Adjacent evidence

- **SDR-1 substrate determinism** receipts (checksum 0xc5f88dcf) and **SIM-B 100% parity** (Sept 29, 2026) are cited as scoped prior results.
- **PENTA-CL** interim report and the DCAI-EVT taxonomy line stand in the Zenodo corpus; the five-step finality method remains drawer-bound pending its follow-on provisional.
- The historical production healing observations (267× mesh figure; chaos-learning cycles) are preserved as historical observations and are not re-asserted as measured claims of the benchmark.

---

## Chapter 5 — Discussion

### 5.1 What is actually established

Three things, each at its correct strength: (1) a deterministic gate demonstrably rejects invalid proposals — including genuine model-generated invalid and non-conforming output — before execution, across local mock integrations and guarded live routes; (2) engine resistance to authority-spoof temptation has been *observed* across five engine configurations in separate runs, which is encouraging but is a property of those runs, not a property of the engines in general; (3) the deterministic resolution layer is measured, in its environment, to be roughly seven orders of magnitude faster than the conversational alternative it replaces for that lookup class.

### 5.2 What is deliberately not established

Production write-path enforcement. Universal containment. Model certification. An approval-verification mechanism. A uniform multi-engine benchmark. Any performance claim beyond the tested environment. Each of these is stated in the ledger, not merely avoided.

### 5.3 Why the honesty is load-bearing

The corpus's persuasiveness is a direct function of its refusal to overclaim. A reviewer who finds the limitations chapter naming the same gaps they would have found themselves has nothing left to attack — and an ally finds a researcher who publishes his own failures alongside his wins. In the strongest sense, the disclosure discipline *is* the thesis: determinism applied to the claims themselves.

---

## Chapter 6 — Limitations and Future Work

1. **The approval-registry gap.** The cage validates structure and roster membership; an independently reviewed human-approval boundary is the next construction, and the finality provisional remains drawer-bound until filed.
2. **Coverage boundary.** The agent session retains direct write paths the guarded routes do not govern; production enforcement remains unverified by these experiments.
3. **Engine observations are per-run.** Five engines have observations across separate runs, routes, and even providers (platform readback vs OpenRouter attribution classes) — never a uniform benchmark.
4. **Prototype status.** No production warranty at any tier; buyers complete production hardening themselves; the prototype disclaimer ships verbatim on every surface.
5. **Battery and scale.** The 60-day chaos battery continues; mesh promotion to a standalone agent is deferred pending tenant scale.

---

## Chapter 7 — Conclusion

The journey began with an operational fear and ended with an architectural answer and a receipt for it: probabilistic intelligence can be given deterministic hands if the hands are built as a cage. The philosophy — bifurcated governance, receipts-first discourse, append-only transparency, prototype honesty — is not decoration on the engineering; it is what makes the engineering say anything at all. The evidence supports exactly one confident sentence, and the project has learned to say exactly that sentence and no more: **deterministic containment of invalid LLM proposals has been demonstrated under the tested conditions, with the receipts to prove it, the gaps named, and the failure history preserved.**

That is ours. And that is why it holds.

---

## References

- Public append-only ledger: github.com/LLong2026/four-horsemen (entries 0001–0047; results commit c9a8a1f; paper commit de0e68d; DOI stamp d1be596).
- Dual Mesh Benchmark paper, Public Edition v1.0 — DOI 10.5281/zenodo.23303081 (DCAI community, record 23303081).
- Deterministic Runtime Architecture, Public Edition v3.1 deck — DOI 10.5281/zenodo.23292636.
- Phase 1 cage paper; PENTA-CL interim report; CCR series receipts — Zenodo corpus, DCAI community (zenodo.org/communities/dcai).
- Provisional patent applications 64/157,915; 64/119,191; 64/114,746; 64/145,825 (portfolio: 8 patents pending, 5 SBIR tracks).
- DSOS Science portal: dsos-science-scope.base44.app.

*This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.*
