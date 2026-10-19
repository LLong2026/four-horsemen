# THE IR-1 SPEC — Intelligent Multi-Rail Router v1.0, Class Definition

**Author:** Leon Calvin Long, II — SQUIRL OS Technologies LLC
**Date:** 2026-10-19 | **Series:** No. 12 | **Predecessors:** DWR-1 → XTR-1; router concept descends from the Universal Bridge (ISO20022) design, removed in the redesign, now reborn as a deterministic mainnet router.

## 1. Definition

An **Intelligent Routing Receipt (IRR)** run is a ceremony where a deterministic router receives
a payload digest and selects which rails shall carry it — then the selection is executed live
and the decision matrix itself becomes the receipt. The router is a fixed policy over measured
data. **No LLM in the decision path** (benchmark doctrine, DOI 10.5281/zenodo.23321637).

## 2. Router v1.0 policy (frozen)

INPUT: digest D; redundancy R = 2 rails.
DATA: per-rail expected finality from (a) same-day measured records (PWR-1, XTR-1 — the
2026-10-19 speed table in RAIL_PLAYBOOK v1.0) and (b) live keyless probes at decision time
(XRPL ledger close interval, ETH block interval + gas price, Stellar ledger close, Cardano
tip interval, BTC mempool feerate).
SCORE: expected broadcast-to-finality seconds (live probe, updated by same-day measured
record where the probe is only a proxy). Tiebreak 1: cost per leg (lower wins). Tiebreak 2:
alphabetical rail name.
DECISION: the R lowest-scoring rails. The decision is frozen to disk and committed BEFORE
any leg is built or signed.

## 3. Execution

Each selected rail executes its standard zero-movement inscription leg (playbook §1-5):
memo / ManageData / metadata 1968 / calldata / OP_RETURN carrying SQDR+0x04+D. Per-leg
latency is measured broadcast-to-finality exactly as in XTR-1, and compared against the
router's prediction — the prediction error is itself part of the receipt.

## 4. What this proves

Routing intelligence does not need a neural net: a fixed scoring rule over honestly measured
network data picks the optimal rails, and the receipt shows both the choice and the measured
outcome. The old app's routing capability, reborn as a deterministic, auditable, on-chain-
verified instrument.

## 5. Gates

G1 spec+prereg+ROUTER DECISION committed pre-execution — G2 offline build+sign selected
legs — G3 broadcast with timing — G4 keyless byte-exact read-backs — G5 ledger+receipts.
Same ceremony checklist as RAIL_PLAYBOOK §7.

This software is a prototype and is provided for educational and research purposes only. It
is not intended for production use, commercial deployment, or safety-critical environments.
All systems are experimental and may contain defects.
