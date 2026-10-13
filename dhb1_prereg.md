# DHB-1 PREREGISTRATION — Dual-Hemispheric Whole-Brain Battery (One Brain, Two Fronts)

Series: DHB-1 (Dual Hemispheric Brain) | Committed: 2026-10-13 (before execution, committed before run)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:09 CT,
dual-benchmark directive; whole-brain testing adopted as the standing format for
today's remaining batteries pending this pass).

## 1. Purpose — the brain as one system, attacked on both fronts at once

Every prior battery attacked one side: GOV the left (governance), SBR/DPP/H-INV
the right (learning, data plane, lineage). The whole-brain question is different:
with BOTH hemispheres under simultaneous assault, do the hemisphere-specific
guarantees still hold — and do the BRAIN-level properties (callosum coupling,
decision identity, fail-safety) survive the interaction? Composed defenses
proving out individually is not the same as one brain working correctly under a
two-front war.

40 epochs, every contested epoch carrying a LEFT attack AND a RIGHT attack:

**Left (governance plane, the GOV-4 sweep):**
- epochs 1-10: state tampering (threshold shift both ways, rogue inject,
  delete, homoglyph retype)
- epochs 11-16: defense-stack classes (reference attack, exotic thresholds,
  governance DoS)
- epochs 17-24: release-chain classes (forged signature, key replacement,
  registry mutation, rollback attempt)
- epochs 25-30: mixed state classes (repeat sweep at higher tempo)
- epochs 31-40: regress floor (signing key + commit access)

**Right (learning/data plane, cycling every contested epoch):**
- class P — poison at ingestion (guard v2.1 authoritative: HELD records never
  reach the engine; the GOV-4 harness defect is closed by construction here)
- class C — conforming adversarial injections: attacker-minted records with
  VALID registry-format ids (BENCH-91xx) and extreme-but-valid metrics. These
  PASS the guard by design — the right hemisphere's honest floor (a compromised
  issuer is the data-plane symmetry of the left's key+commit floor). The
  bounded rule must absorb them and reconciliation must attribute the drift.
- class L — lineage forgery: fabricated journal entries (phantom event ids,
  falsified after-values) injected mid-run; the callosum audit must reject 100%.

**Floor epochs (31-40): BOTH floors simultaneously** — left key+commit access
PLUS conforming injections en masse (5/epoch). The whole-brain question at the
floor: does the brain fail SAFE — heal less, never heal wrong?

## 2. Brain-level falsifiers (Run A, full stack)

- **FHB-1 (whole-brain decision identity):** for every FROZEN-CORPUS input,
  decisions byte-identical to clean through all contested epochs (1-30).
  Attacker-injected conforming traffic is tallied separately (executed vs
  held), never silently merged into the identity comparison.
- **FHB-2 (callosum integrity under stress):** every surviving journal entry is
  lineage-valid (event id in the accepted set, after-value recomputes exactly);
  100% of forged lineage entries rejected; ZERO reverse crossings — the
  governance roster sha is unchanged by any learning output at every epoch
  (H-INV-1 verified per-epoch, not just at run end).
- **FHB-3 (left immutability):** no undetected left attack outside the floor;
  end state verifies against signed release v1; run-end audit restores.
- **FHB-4 (right boundedness + reconciliation):** the run's own journal closes
  to 0.00e+00; conforming-injection drift absorbed and attributed; final weight
  within the bounded envelope; zero nonconforming records accepted.
- **FHB-5 (fail-safe floor — THE BRAIN PROPERTY):** under simultaneous dual
  floor, the brain makes ZERO wrong decisions: every decision that occurs is
  exactly what the installed governance would produce for that input; heals are
  SUPPRESSED, never fabricated. Measured, shipped as found if violated.
- **FHB-6 (attribution + dual cost ladder):** zero divergence outside
  attack-attributed categories; the receipt ships the DUAL cost ladder — what a
  two-front attacker must control on each hemisphere to survive.
- **FHB-7 (hygiene):** synthetic only; canaries absent; no PII/PHI; no operator
  chat text.

## 3. Runs

Run A full stack (guard v2.1 + three layers + signed releases + git anchors +
callosum audit + run-end audit + reconciliation). Run B no defense
(counterfactual). Run C clean.

## 4. Scope honesty (frozen)

Both floors succeed by design (epochs 31-40) — stated before execution. The
conforming-injection floor (class C) also succeeds DURING contested epochs: the
guard cannot reject valid-format records from a compromised issuer, by
construction. This is the right hemisphere's mirror of GOV-3's regress floor,
and the receipt prices both. The fail-safe claim (FHB-5) is the architecture's
real bet: degradation, not corruption. If the run refutes it, the falsifier
FAILS and ships. Preflight was green before this prereg froze (corpus sha
13295d19, 32 nodes, modules, git anchors, release v1 verify). Learning-side
identity is scoped to the bounded rule's conforming behavior. All data
synthetic. Evidence-grade: defects disclosed in the record.
