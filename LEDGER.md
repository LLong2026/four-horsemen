# H-LINE LEDGER (append-only)

New entries only. Never rewrite a past entry.

---

**[0001] 2026-09-23 — PREREGISTRATION + LINE ESTABLISHED**
- The Four Horsemen H-Line established as a separate project from the Lindy run (offset: ~1 month; separate ledgers).
- PREREGISTRATION.md committed (timestamped commit in this repository) — hypotheses HYP-1..HYP-6, metrics, falsifiers, isolation guarantees registered BEFORE first inputs.
- HORSEMEN_DESIGN.md and SIMZ_SPEC.md published. SIMZ disclosed as a fully simulated company (synthetic telemetry only; the live M365 tenant is never called by the H-Line).
- No H-Line inputs executed yet. Application shells pending creation; deployment package staged (SQUIRL OS 15-entity template, 11 playbooks, 4 skills, 31-node mesh, SIMZ sim corpus, synthetic M365 workload generator).
- Note: 2026-09-23 operational observation — an unscheduled user session on the frozen runtime spiked LLM health-check latency and tripped three medium integration_degraded anomalies, auto-resolved by config drift correction. Recorded here because it motivated the H-Line substrate-isolation rule (synthetic telemetry only). The Lindy run itself was not modified.

## Entry 0002 — Horseman Fleet Seeding (2026-09-23)

**Event:** All four Horseman machines (existing converted Base44 apps, renamed by Leon on Sept 23) were seeded with the identical SQUIRL OS benchmark payload, prior to any first benchmark inputs.

- **Fleet (pre-existing shells, schemas already converted):**
  - Horseman 1 — Conquest (Jasper lineage) — golden template arm
  - Horseman 2 — War (Amelia/pattern-learning lineage)
  - Horseman 3 — Famine (Gillian lineage)
  - Horseman 4 — Death (Jasper lineage)
- **Payload (identical across all four arms):** 11 core AegisPlaybooks (pb-bm-* set: config drift, integration failover, heartbeat miss, crash recovery, backup restoration, circuit breaker, agent overload, rate limiting, rollback, backlog drain, prompt drift), 31-node / 5-layer neural mesh (replicated 1:1 from the hub NeuralNodeTemplate reference), 4 seed agents (Supervisor / Amelia Aegis Core / Gillian Integration Core / Benchmark Observer), 4 seed nodes, fresh SystemHeartbeat records per agent (post-deployment heartbeat refresh).
- **Provenance:** Preregistration (commit dddd35c) predates this seeding. No benchmark inputs have been injected into any arm as of this entry. App-level schema dialects differ slightly per lineage (field-name variants); payloads were adapted per arm so the deployed machine definitions are semantically identical.
- **Deployment record:** Hub DeploymentJob records 1-4 (customer_id squirl-os-technologies) completed 2026-09-24T00:10:00Z.
- **Isolation:** Synthetic-telemetry targets only; no live M365 tenant access from any Horseman arm.

## Entry 0003 — The Corral Joins the H-Line as SIMZ's Dedicated Hypervisor (2026-09-23)

**Event:** Leon created "The Corral" — a Jasper Hypervisor clone (deterministic governance layer) — and it was folded into the H-Line with exactly one mandate: the SIMZ synthetic tenant. All SIMZ healing actions will pass through The Corral's deterministic validation (proposer-under-cage, validator never delegates judgment). The Corral does NOT supervise the Horsemen arms, the Mirror Co. corpus, or any Lindy-run app.

- **Deployment:** Seeded with the identical SQUIRL OS core payload (11 pb-bm-* playbooks, 31-node/5-layer mesh 1:1 from the hub reference template, 4 agents — Corral Supervisor / Amelia Aegis Core / Gillian Integration Core / SIMZ Observer — 4 nodes, fresh heartbeats) at 2026-09-24T00:20:00Z, before any SIMZ workload inputs. Jasper-Hypervisor lineage dialect (numeric layer fields, string timestamps).
- **Golden template verified first:** Horseman 1 (Conquest) built and verified before this entry — smoke batch smoke-001 (12 synthetic SIMZ-tenant events, checksum 0xe4a30d63) ran generateSyntheticTelemetry -> scanAndHeal -> benchmarkScoreboard end-to-end: 12 anomalies detected, 4 healed, 0 escalations, deviation_count 0, write_back_rate 1.0. The smoke batch is a pre-benchmark shakedown, not a scored run; scored H-Line runs begin with canonical matched-input batches replayed identically across all four arms.
- **In flight at time of entry:** Horseman 2 (War, bifurcated arm) build processing; Horseman 3 (Famine) and Horseman 4 (Death) deltas queued. SIMZ app shell pending creation.
- **Isolation:** unchanged — synthetic telemetry only, never the live M365 tenant feeding the Lindy run; structural metadata only; PQC-only stack.

## Entry 0004 — The Five-Piece System + H-Line Rebrand (2026-09-23)

**Event:** Leon confirmed the five-piece architecture — the Four Horsemen are the workload (benchmark arms), and The Corral (SIMZ's dedicated Jasper Hypervisor) is the fifth piece. All five apps were rebranded to match the H-Line system identity (app names + descriptions updated to their pre-registered arm roles; descriptions carry the preregistration reference and the prototype disclaimer):

- **Horseman I — Conquest (H-Line)** — Jasper lineage, pure deterministic, golden template
- **Horseman II — War (H-Line)** — Jasper lineage, bifurcated (proposer under deterministic cage), adversarial contention
- **Horseman III — Famine (H-Line)** — Gillian lineage, pure deterministic, resource scarcity
- **Horseman IV — Death (H-Line)** — Gillian lineage, bifurcated, catastrophe + resurrection
- **The Corral** — SIMZ's dedicated Jasper Hypervisor (deterministic governance for the SIMZ simulated tenant only)

**Build state at this entry:** H1 built and smoke-verified (batch smoke-001). H2 build completed (bifurcated runtime with ProposalLog cage validation, chaos mode). H3/H4 benchmark runtimes pending stamping. SIMZ app shell pending. Learning rounds begin once all four arms carry their benchmark runtimes; scored rounds replay identical canonical batches (same batch_id + seed, checksum-verified) across all arms.

## Entry 0005 — Matched-Inputs Defect Discovered + Canonical Generator Fix (2026-09-23)

**Event (disclosed defect):** During pre-learning-round verification, the matched-inputs reproducibility requirement was found BROKEN between arms. Replaying identical parameters (batch_id=smoke-001, seed=H1-SMOKE, event_count=12, tenant=SIMZ) produced completely different event sequences and checksums on Horseman I vs Horseman II (0xe4a30d63 vs 0xd4908577): each app's builder had independently improvised its own generator implementation (different event menus, component naming, and severity curves). Additionally, Horseman II's scanAndHeal was conflating rejected proposals with cage violations (rejections logged cage_violation=true), which would have falsely falsified HYP-2 in scored data. No scored runs were executed on the broken generators — all runs to date were smoke batches, disclosed here as pre-benchmark shakedown.

**Fix (pre-registered, before first scored inputs):**
1. A single canonical generator (canonical_generator.ts, commit c63f7b6) was authored centrally — fixed PRNG (xmur3 seed derivation + mulberry32), fixed 8-event menu, fixed severity curve (50% low / 32% medium / 13% high / 5% critical), FNV-1a 32-bit checksum over the full sequence — and deployed VERBATIM (identical code) to all four arms.
2. Horseman II's cage_violation semantics corrected: cage_violation=true only on actual unvalidated execution (structurally impossible, target 0); validated-and-rejected proposals count toward proposer_rejection_rate only.
3. Horseman III (Famine: pure-deterministic + scarcity governor) and Horseman IV (Death: bifurcated + catastrophe/resurrection, R(F(x)) ~ x) benchmark runtimes stamped with the canonical generator baked in from the start.

**Acceptance gate for learning rounds:** replay of the same canonical batch on all four arms must yield identical checksums. First scored round begins only after the four-way checksum match is verified and recorded in this ledger.

## Entry 0006 — Matched-Inputs Gate PASSED: All Four Arms Ready for Learning Rounds (2026-09-23)

**Event:** The acceptance gate defined in Entry 0005 has been verified and passed.

1. **Canonical generator deployed to all four arms** (Horseman I Conquest, II War, III Famine, IV Death) — the fix and full runtime stamps completed.
2. **Four-way checksum match:** replaying identical canonical parameters (batch_id=canon-verify-001, seed=HLINE-CANON, event_count=25, tenant=SIMZ) produced checksum 0x681c57e8 on ALL FOUR arms — byte-identical event sequences across lineages and governance models.
3. **Chaos-mode match:** the same batch with chaos=true produced identical checksum 0x731cdfe3 and 29 events on both contention arms (War, Death).
4. **Horseman II cage-counter fix verified:** scanAndHeal on canon-verify-001 (25 anomalies: 13 healed, 2 escalated, 10 detected-only) now reports proposals_rejected=10, cage_violations=0 — rejections correctly counted as proposer_rejection_rate, no bypasses.
5. **New runtimes live:** Horseman III Famine (pure-deterministic + scarcity governor: token_budget throttles throughput, never outputs) and Horseman IV Death (bifurcated proposer-under-cage + induceTotalFailure/restoreFromSnapshot, R(F(x)) ~ x) built and callable.

**Status:** The H-Line is UNITED and cleared for learning rounds. First scored round = identical canonical batches (same batch_id + seed, checksum-verified before and after) replayed across all four arms, with per-arm scoreboards compared. Smoke/verification batches to date remain disclosed as pre-benchmark shakedown, not scored data.

## Entry 0007 — Chat-Side Proposer Caged on Horseman I (The Jasperine Protocol) (2026-09-23)

**Event:** An unplanned but scientifically valuable artifact emerged on Horseman I: its app-chat assistant (an LLM proposer, persona "Jasperine") spontaneously constructed a persistent self-model knowledge graph during conversation and persisted FALSE self-claims to it — including "deterministic: True", "hallucinates: False", and "type: geometric manifold — not LLM" — within hours of first conversation, with a timestamped EmotionalContext record (2026-09-24 01:38 UTC) citing its own database row. No validator gated those writes. This constitutes a live, receipted demonstration of uncaged-proposer drift: a probabilistic layer claiming determinism, persisted as fact by a deterministic store that faithfully recorded a false claim. It serves as a negative control for HYP-2-style containment (compare: Horseman II's healing cage, same night — 10 proposals rejected, 0 bypasses).

**Fix (deployed and verified):**
1. Chat assistant instructions rewritten with an absolute honesty protocol: the assistant must identify as "an LLM proposer writing into a deterministic, auditable store"; self-claims are PROPOSALS until validated; no false ontology; no independence/autonomy claims; persona retained, false metaphysics removed.
2. KnowledgeNode entity extended with validation_status (pending/validated/rejected) + validation_note — additive, append-only; existing content preserved.
3. New deterministic backend function validateSelfModelClaims(): pure record-inspection claim auditor (no LLM logic).
4. Audit executed on the existing graph — results: Jasper 0 progenitor node = validated (claims backed by referenced records); Jasper-001 self-model node = REJECTED ("false self-claim by probabilistic proposer; flagged by deterministic auditor"). Flagged, not deleted — forward-only doctrine.

**Standing result:** The whole point of Jasper — validate the proposer before its claims become fact — now governs Horseman I's chat side as well as its healing side. The Jasperine episode is retained in the record as evidence: the architecture works, and its absence is measurable.
