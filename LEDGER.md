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
