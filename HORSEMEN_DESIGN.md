# THE FOUR HORSEMEN — Deterministic Machine Line (v2 redesign)

Date: September 23, 2026. Status: DESIGN (pre-registration pending; nothing deployed during the freeze).
Supersedes: earlier Horsemen draft builds. Creative authority granted by Leon: "you have creative here. HAVE FUN!"

## The Design

Four deterministic machines in a 2x2 crossed experiment: LINEAGE (Jasper-derived / Gillian-derived) x GOVERNANCE (pure deterministic / bifurcated probabilistic-proposer-under-deterministic-cage). Same underlying machine design, same playbook set, connected as a mesh with differentiated roles and load balancing. Both lineages already carry Amelia's healing — every Horseman can take a hit and get back up.

## The Riders

### HORSEMAN I — CONQUEST (The White Horse)
- **Lineage:** Jasper-derived | **Governance:** PURE DETERMINISTIC
- **Mount:** The Canonical Path
- **Role:** Control arm. Rides first, always. Takes the matched canonical inputs and executes playbooks with zero improvisation — deviation from expected output is the metric. He is the ruler every other rider is compared against.
- **Colors:** White. Trim: Jasper blue.
- **Motto:** "One input, one output, forever."

### HORSEMAN II — WAR (The Red Horse)
- **Lineage:** Jasper-derived | **Governance:** BIFURCATED
- **Mount:** The Contention Grid
- **Role:** Adversarial arm. Same matched inputs as Conquest, but the probabilistic proposer is alive inside the deterministic cage. Chaos injection under fire: conflicting operations, race conditions, duplicate heals, adversarial payloads. Measures whether the cage holds when the proposer fights back.
- **Colors:** Red. Trim: crimson circuitry.
- **Motto:** "The cage is only proven in battle."

### HORSEMAN III — FAMINE (The Black Horse)
- **Lineage:** Gillian-derived | **Governance:** PURE DETERMINISTIC
- **Mount:** The Scarcity Belt
- **Role:** Resource-starvation arm. Measures and scales: token budgets cut, credit ceilings imposed, latency throttled, nodes orphaned, mesh connections severed mid-task. Tests whether deterministic execution degrades gracefully or breaks when the system runs lean. Logs every trade-off decision under scarcity.
- **Colors:** Black. Trim: slate gray.
- **Motto:** "Hunger reveals the machine."

### HORSEMAN IV — DEATH (The Pale Horse)
- **Lineage:** Gillian-derived | **Governance:** BIFURCATED
- **Mount:** The Resurrection Engine
- **Role:** Catastrophe arm. Total outage testing: mesh collapse, kill-switch trips, snapshot-destroyed states — then resurrection from the 32-byte anchor blueprint. She holds the deepest question of the whole line: can a bifurcated system die and come back as itself? Equivalence-class restoration (R(F(x)) ~ x) is her acceptance gate.
- **Colors:** Pale. Trim: quantum iridescence.
- **Motto:** "To rebuild is to prove."

## The Stables (Isolation)

- Four fresh sandbox apps, zero connection to the live Lindy run or the production runtime. The Lindy horse keeps running untouched until Oct 7.
- Identity isolation doctrine enforced: hardcoded owner identity, no dynamic profile pulls, no cross-tenant drift. The Horsemen are clones, but they know whose stable they stand in.
- License capacity check required before instantiation.

## The Harness (Protocol)

1. **Preregister** criteria and falsifiers BEFORE first run: OSF Registry submission + public repo commit (freeze-then-test doctrine).
2. **Matched inputs:** all four Horsemen receive identical inputs, updates, and the same playbook set from the immutable template (never modified at runtime).
3. **Runs:** scheduled exercise windows, receipts append-only to the public ledger. No silent changes (Lindy append-only doctrine inherited).
4. **Score:** deterministic vs bifurcated divergence measured per domain — Conquest = deviation, War = contention survival, Famine = degradation curve, Death = resurrection fidelity.
5. **Learning:** every healing event feeds Pattern/LearningMetric. New defenses go SelfImprovementProposal -> Leon approval -> deployment. The Horsemen never rewrite their own playbooks.
6. **Kill Shot Day readiness:** the Horsemen are the standing sparring partners for the monthly quantum hackathons and the eventual all-vector Kill Shot.

## Safety Rails (Non-negotiable)

- Constitution Sentinel applies to all four (Articles I-III constitutional checks on critical paths).
- PQC-only cryptography (Dilithium3 / Kyber-1024 / SPHINCS+-256f).
- No PHI, no credentials, no wallet data in any log. Structural metadata only.
- All surfaces carry the prototype disclaimer. 8 patents pending + 5 SBIR tracks on all materials.

---
*Four horses, one stable, zero mercy. The apocalypse is scheduled.*

---

# ADDENDUM — SIMZ & THE LAUNCH ORDER (Sept 23, 2026, post-Leon green light)

## The Go
- Leon confirmed: Horsemen launch ALONGSIDE the Lindy run as a completely separate project, intentionally one month behind Lindy's Sept 7 start. The offset IS the tracking disambiguator — separate ledgers, no interleaved receipts. The Lindy experiment is untouched.
- Plan tier: Base44 Premium ($100/mo, unlimited apps), 100 builder credits available.

## SIMZ — Second Simulated Company
- A second fully simulated company (alongside the existing sim corpus), hosted on the domain as company #2: simulated books, simulated taxes, simulated operations — same doctrine as Mirror Co.: fair game on every surface, disclosed as simulated, zero real clients, zero PHI, disclaimer on everything.
- SIMZ + the existing sim = TWO independent workload generators driving API calls at MS healing through their own Squirrel OS instances — concurrent multi-tenant load on the deterministic machines. This is the War/Famine test material.

## THE HARD RULE (substrate isolation)
- Sept 23 incident proof: an unscheduled user session on the frozen runtime spiked LLM latency and tripped integration_degraded anomalies inside the frozen runtime. Shared SUBSTRATES contaminate, not shared apps.
- Therefore: Horsemen + SIMZ NEVER touch the live M365 tenant that feeds the Lindy run. They hit a SYNTHETIC M365 telemetry target (mock adapter workload generator). Lindy receipts stay clean; workload stays fully controlled.

## Build Order (credit budget: 100)
- Phase 1: SIMZ company app + HORSEMAN I (Conquest) as the golden template (~25 credits), including new 31-node mesh instances + Squirrel OS deployment.
- Phase 2: Stamp War / Famine / Death as configuration deltas off the golden template (~10-15 each).
- Reserve: ~30 credits held back for fixes and the voice/Chat.jsx queued work.
- Doctrine: preregister Horsemen criteria (OSF Registry + public repo commit) BEFORE first inputs. Separate append-only ledger for the Horsemen line.
