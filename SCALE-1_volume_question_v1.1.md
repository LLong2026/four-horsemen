# SCALE-1: The Volume Question — Can a Register Hold Trillions?

**v1.1 — 2026-10-28 — two-key curation: drafted and vetted by the operator's agent system (Gabriel);
owner GO for documentation surfaces — Zenodo and GitHub — Leon GO (chat authorization, 2026-10-28 09:54 CT).**
All measured figures re-derived on 2026-10-28; see the derivation note at the end.

*Author: Leon Calvin Long II, SQUIRL OS Technologies LLC*

> Prototype disclaimer: This software and its measurements are provided for
> educational and research purposes only. It is not intended for production
> use, commercial deployment, or safety-critical environments.

---

## 1. The question the industry has not asked

Institutional tokenization marketing projects trillions of dollars in
tokenized real-world assets within the decade. Every projection of that
market — issuer decks, consultancy reports, conference keynotes — is a
*notional* figure: the value the assets would represent.

Not one of them is a *volume* figure. The question that matters for
infrastructure is not "how much value is represented" but **"how many
transactions per second must your own hardware process, hold, and keep
consistent to represent it?"**

This note compares two architectures on exactly that question:

1. **The register model** (custodial tokenization): the ownership record is a
   row in a chain state or proprietary ledger; every transfer is processed,
   validated, and enforced by infrastructure the operator owns.
2. **The witness model** (anchoring): the asset and its legal record stay
   off-chain and sovereign; a cryptographic digest of each ownership event is
   committed to public chains, which serve as permissionless, replicated
   witnesses.

## 2. What each model's hardware must actually do per transaction

### Register model (per transfer)

| Operation | Where it runs | Cost profile |
|---|---|---|
| Ownership row update | Operator's chain or SQL-backed "truth ledger" | Linear in transaction count, on owned hardware |
| Compliance/enforcement check | Pre-execution gate on operator's stack | Linear, per transaction, per rule |
| Identity / permission resolution | Operator's identity layer (ERC-3643-style) | Lookup + storage, per holder |
| Post-trade reconciliation | Operator + institutional back offices | The cost the model was supposed to remove |
| Reconciliation of chain vs. register | Both | Inherent to the mirror architecture |

Every transfer in this model is **a stateful write on someone's machine.**
Throughput, storage, consistency, and audit all scale with transaction count
on hardware one organization must size, staff, and secure. "Trillions in
assets" here means "trillions of notional settled through our servers."

### Witness model (per ownership event)

| Operation | Where it runs | Cost profile |
|---|---|---|
| SHA-256 digest of the event record | Any commodity hardware | Constant, nanoseconds; independent of asset value |
| Merkle tree leaf insert | Local ledger | O(log n), nanoseconds |
| Merkle root anchor to public chains | Bitcoin / Stellar / XRP | ~$0.25 per triad anchor, *amortizable*: one root can commit thousands of events |

The load-bearing property: **per-event cost is independent of the notional
value and nearly independent of event volume.** A receipt witnessing a
$1,000,000,000 ownership event costs the same quarter as one witnessing $1,
because what is anchored is a 32-byte digest, not the asset. Batch
amortization is explicit in the design: one Merkle root anchors an arbitrary
number of leaves, so per-event chain cost falls toward ~$0.0001 as volume
rises — cost per event *decreases* with scale in the witness model and
*increases* with scale in the register model.

And critically, the expensive part of the witness model — permanent,
tamper-evident storage — is outsourced to the three most load-tested
transaction ledgers in existence, run by thousands of independent operators
who do not know or care what the digests reference. The witness operator's
own nodes can be stateless between anchors; the evidence does not live on
them. **There is nothing to "hold trillions" because the trillions never
enter the system — only their fingerprints do.**

## 3. Measured receipts (what we have actually run)

Receipts-first: the following are measured facts on record, not projections.

- **FRACTAL-2** (2026-10-25): three-way fractional ownership transfer of a
  research artifact, 30/30/40 split, anchored across Bitcoin, Stellar, and
  XRP. Total three-rail cost: **$0.2509**. Public explorer-verifiable;
  no relationship with the operator required to verify. (DOI 10.5281/zenodo.23655614)
- **Receipt pipeline volume:** 383 append-only ledger entries and 207 published
  Zenodo records (155 open access) produced to date by the same anchoring pipeline — a working,
  journaled evidence stream, not a whitepaper diagram.
- **Containment record:** 7,083 anomalies detected / 6,789 resolved across
  60 recorded watch cycles with zero containment breaches (DOI 10.5281/zenodo.23703012)
  — the governance layer that generates and journals the receipts is itself
  volume-tested at thousands of events.
- **Public chain capacity (public, independent data):** the anchor rails
  have operated continuously for 10–17 years through bull-market load,
  exchange failures, and adversarial mempool congestion without loss of
  committed history. The witness model inherits this; it does not have to
  build it.

What is *not* claimed: neither SQUIRL OS nor any tokenization platform has
published a measured trillion-dollar, sustained-TPS load test of a full
ownership stack. The difference is that the witness model does not need one
to make its scaling argument — its per-event work is a hash and a batched
anchor — whereas the register model's scaling case *is* its hardware, and
the hardware is precisely what has not been volume-exercised at the scale
the marketing projects.

## 4. The asymmetry, stated plainly

- Register model: **cost per event rises with volume** (state, enforcement,
  reconciliation, hardware), and **failure concentrates** on one operator's
  stack. Trillions of notional means trillions routed through machines one
  company can be sued over, hacked, or capacity-capped.
- Witness model: **cost per event falls with volume** (batch amortization)
  and is **value-independent**; the trust load is distributed to public
  consensus networks that fail only if arithmetic stops working on three
  continents simultaneously.

When the industry "figures out it never tested for volume," the discovery
will not be that databases are slow. It will be that it put the register in
front of the asset — making its own hardware the bottleneck and the liability
— when the only thing that needed to scale was the proof, and proof was
never supposed to be a server.

## 5. Bottom line

Trillions do not need warehouses. They need witnesses.

---

*Sources: FRACTAL-2 receipts (DOI 10.5281/zenodo.23655614); containment
record (DOI 10.5281/zenodo.23703012); public explorers for BTC/XLM/XRP anchor
transactions. Companion artifacts: measured containment receipt card
(2026-10-27); this document is a draft and has not been minted, posted, or
ledgered.*

---

## Derivation note (v1.1, 2026-10-28)

Every measured figure in §3 was re-derived on 2026-10-28 from the artifacts themselves: ledger rows counted
by parsing dated table rows in the public `LEDGER.md`; Zenodo counts read from the owner account's deposit
API (207 published, of which 155 open access and 52 restricted); anomaly and healing counts read from the
system's own entity store rather than from any summary document. The v1.0 draft carried 373 ledger entries,
159 Zenodo records, and 7,076 / 6,776 anomaly figures, all of which had drifted with ordinary daily activity
or had been undercounted by a keyword search that excluded access-restricted records. Those draft figures
are superseded here and the change is disclosed rather than absorbed.

The projection arithmetic in §2 is analytical, not measured: it is a per-transaction cost argument about
where state is written, and the paper claims nothing about its own hardware benchmarks beyond the measured
anchoring costs in §3. Where a figure is a projection it is labelled as one.
