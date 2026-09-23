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
