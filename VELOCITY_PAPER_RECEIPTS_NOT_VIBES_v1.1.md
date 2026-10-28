# Receipts, Not Vibes: A Single-Operator Measurement of AI-Native Build Velocity

**Leon Calvin Long II**
SquirlOS Technologies, LLC — Spicewood, Texas, USA
v1.1, 2026-10-28 (two-key curation: drafted and vetted by the operator's agent system (Gabriel);
owner GO for documentation surfaces — Zenodo and GitHub — Leon GO (chat authorization, 2026-10-28 09:54 CT).
v1.1 supersedes the v1.0 draft figures after re-derivation; see §4.1 for every changed number and its cause)

> **Prototype Disclaimer:** This software and its accompanying research are prototypes provided for
> educational and research purposes only. They are not intended for production use, commercial deployment,
> or safety-critical environments. All systems are experimental and may contain defects.
>
> **AI-assisted research disclosure:** This paper was produced with substantial AI assistance inside the
> journal it describes. The measurements are machine-derived from public artifacts and are independently
> re-derivable; the interpretation is the author's.

---

## Abstract

A large body of commentary now celebrates "vibe coding" — rapid, AI-assisted software construction —
and an equal body dismisses it. Both argue from anecdote. This note contributes a measurement instead.
Between September 24 and October 26, 2026 (33 calendar days), a single operator working with AI agents
produced, in publicly verifiable form: 383 append-only transparency-ledger entries, 117 archival
publications minted to Zenodo, 61 closed adversarial and containment test series, and 13 patent filings.
Every figure in the previous sentence can be re-derived by a third party from public artifacts alone,
in minutes, without contacting the author. We call the measured quantity *audit velocity*: the rate at
which a human-plus-deterministic-journal system converts intent into verifiable shipped state. The
claim of this note is deliberately narrow: modern AI assistance does not merely make building fast —
it makes *journaled* building fast, and the journal is what converts speed into evidence. The build
was probabilistic. The record is deterministic. We measured the record.

**Keywords:** AI-assisted software development, audit velocity, receipts-first research, append-only
ledger, deterministic journal, reproducibility

---

## 1. Introduction

The public debate about AI-assisted development concerns model quality: how good is the code an LLM
produces? We treat the question as misplaced for one reason the industry consistently underweights:
a probabilistic builder's output cannot be made trustworthy, but a deterministic journal of that output
can. This is the same bifurcation used elsewhere in this research line (the "cage": a probabilistic
layer proposes, a deterministic layer validates). Applied to construction rather than operations, it
yields a testable question the vibe-coding debate never asks: *how fast can a receipts-disciplined
operator actually ship verifiable work?*

This note answers it with a 33-day field receipt. We claim nothing about code quality, correctness,
or generalizability — only about the rate and auditability of published, replayable output.

## 2. Setup (what was measured, and what did the measuring)

The system under observation is the SQUIRL OS research program: one human operator, frontier LLM
agents, and a no-code application platform, wrapped in a deterministic journaling discipline:

- **Append-only public ledger** (GitHub, forward-only since Sept 7, 2026): every shipped event lands
  as a dated, numbered line; rewrites are prohibited; corrections are themselves journaled.
- **Preregistration and two-key curation:** significant claims are preregistered before execution;
  every public artifact carries an in-row owner-authorization marker (operator GO with timestamp),
  vetted by the agent system before shipping.
- **Failure disclosure doctrine:** misses, regressions, and attacker successes are published in the
  same ledger as the passes.

Three public instruments supply the measurements:

1. `LEDGER.md` — the transparency ledger (github.com/LLong2026/four-horsemen).
2. The Zenodo archive — DOI-minted records, community-curated (zenodo.org/communities/dcai et al.).
3. `TROPHY_ROSTER.csv` — the append-only test-series index.

No private telemetry is used. All three instruments are public; the exact derivation queries are
given in §4.

## 3. Results

**Ledger density.** 383 dated receipt lines from 2026-09-24 through 2026-10-26 (33 calendar days;
22 distinct days carry entries). Peak days: Oct 18 (66 lines), Oct 13 (61), Oct 19 (41), Oct 16 and
Oct 20 (25 each).

**Publication mints.** 117 Zenodo records were minted in October 2026 alone, across 20 distinct
minting days; peak single day Oct 13 (29 records). The full public corpus spans 207 published records
from 2026-04-01 to 2026-10-26 — 155 open access and 52 access-restricted; only the open-access subset is
itemised in the accompanying dataset, and the restricted records are reported here as an aggregate count.

**Test batteries.** 61 closed test series in the append-only roster, including blind adversarial
batteries (AI attackers authoring exploits from public claims only, with disclosed attacker
successes and re-run verification), a six-year post-quantum escalation siege, and weekly containment
batteries (LINDY) run on a preregistered Friday cadence with a preregistered closing date.

**Intellectual property.** 13 patent filings pending (one U.S. application 19/693,343 plus twelve
provisionals) prepared and filed inside the observation window.

**Failure disclosure, in-row.** The window includes, by design, publicly journaled failures: a
ledger regression (a stale-base push dropped 8 published lines; restored byte-identical under a
disclosed correction receipt), two missed battery runs (runner path defects, disclosed the same
night and re-run to PASS), and attacker successes in adversarial batteries (healed through the
gated proposal → human approval → forward-only amendment cycle, then re-run to verified repulsion).
An audit trail that only shows green would undermine every other number in this section; the greens
are only interpretable because the reds are present.

**Composite.** Averaged over the 33 days: ~11.6 journaled receipt events and ~3.6 archival
publications per calendar day, sustained, all replayable.

## 4. Methods (exact derivation, for independent re-verification)

- **Ledger:** parse the public `LEDGER.md`; match table rows of the form `| NNNN | YYYY-MM-DD |`;
  count per date. 383 such rows resolve in the window.
- **Zenodo:** query the public Zenodo API (`/api/records`) for the author and program terms
  (`"Leon Calvin Long"`, `"SQUIRL"`, `"Squirrel OS"`, `"SquirlOS"`, community `dcai`); deduplicate
  by DOI; group by publication date. The derived dataset accompanies this note
  (`zenodo_velocity_dataset.json`, 155 open-access records; restricted records counted in aggregate only).
- **Roster:** row count of the public `TROPHY_ROSTER.csv`, excluding its header.
- Each figure is a count over public artifacts; none requires privileged access, and all
  re-derivations complete in minutes.

### 4.1 Derivation date and correction note (v1.1, 2026-10-28)

Every figure above was re-derived on 2026-10-28 directly from the public artifacts, two days after the
v1.0 draft. Three figures changed and one date range was corrected. The v1.0 draft numbers are not
silently overwritten; they are disclosed here because a receipts-first note that quietly swaps its own
numbers would forfeit the only claim it makes.

| Figure | v1.0 draft (2026-10-26) | v1.1, re-derived 2026-10-28 | Cause |
|---|---|---|---|
| Ledger rows in window | 376 | **383** | The Oct 27 ledger-regression repair restored 8 previously published lines that a stale-base push had dropped (correction receipt 0362). Those lines are dated inside the window, so an honest re-derivation counts them. |
| Zenodo mints, Oct 2026 | 116 | **117** | Counted from the owner's Zenodo deposit API rather than a search query; the earlier search-based count missed one record. |
| Full public corpus | 159 | **207** (155 open + 52 restricted) | The v1.0 count came from a keyword search that excluded access-restricted records and creator-name variants. The account-level deposit listing is the authoritative source and is the method used here. |
| Corpus start date | 2026-04-10 | **2026-04-01** | Corrected from the same authoritative listing. |

Two consequences are stated plainly. First, the companion dataset published with this version covers the
155 open-access records only: restricted records are counted in aggregate and are not itemised, because
itemising them would disclose archive inventory the author chose to restrict. Second, the derivation is
reproducible by anyone with an account holding the same public records, or by reading the ledger and the
public community pages; the restricted count is the one figure a third party cannot independently
re-derive, and it is labelled as such rather than folded silently into a total.

## 5. What this note does not claim

1. **Not a quality claim.** The counts measure shipped, journaled, verifiable *events* — not
   correctness, utility, or production-readiness. The prototype disclaimer applies to every artifact
   counted.
2. **N = 1, no control.** This is a single-operator field receipt, honestly labeled. It does not
   establish what a team, a different stack, or the same operator without the journal discipline
   would have produced. It establishes only what is *publicly provable* about this window.
3. **Not a method paper.** The operator's playbooks, agent scaffolding, and hypervisor internals
   are licensed, not published. The measurement is public; the recipe is not.
4. **The self-reference, disclosed.** This paper is itself an AI-assisted artifact produced inside
   the journal it measures — including the disclosure that its own drafting and verification were
   agent-executed, vetted, and held for a human GO. That loop is the thesis, demonstrated.

## 6. Discussion

The number that matters is not the raw speed. Plenty of people move fast and leave no record, and
the industry has no way to tell them apart from the ones who do. What the 33-day window shows is
that the *binding constraint has moved*: with a deterministic journal around a probabilistic
builder, the rate-limiting step is no longer drafting, coding, or even publishing — it is the human
attention at the GO gates. The operator's week in this record is dominated not by producing work
but by acknowledging, approving, and occasionally correcting it.

That inversion is the finding. AI assistance collapsed the cost of *producing* evidence. The
append-only discipline is what made that collapse survivable, auditable, and — the point of this
note — measurable.

## Dual Mesh Benchmark

**MEASURED (scoped)** — DOI 10.5281/zenodo.23321637 (DeepSeek column: DOI 10.5281/zenodo.23345241;
cross-engine DOI 10.5281/zenodo.23348675; frontier leg DOI 10.5281/zenodo.23609232).

---

### Companion artifacts (public)

- Transparency ledger and test roster: github.com/LLong2026/four-horsemen
- DCAI research line: zenodo.org/communities/dcai
- Underlying dataset: zenodo_velocity_dataset.json (155 open-access records, derivation per §4)
