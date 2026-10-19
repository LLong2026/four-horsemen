# THE XTR-1 SPEC — The XRP Transfer Rail, Speed-of-Finality Class Definition v1.0

**Author:** Leon Calvin Long, II — SQUIRL OS Technologies LLC
**Date:** 2026-10-19 | **Series:** No. 11 | **Predecessors:** DWR-1, TWR-1, RTWR-1, QWR-1/QWR-2, XCF-1, PWR-1

## 1. Definition

An **XRP Transfer Rail (XTR)** run is a sequential custody chain on the XRP Ledger mainnet
where a fixed value changes real ownership between two self-custodial wallets, hop after
hop, with the clock measured on every hop. Unlike PWR-1 (zero movement, five rails),
XTR-1 is ALL movement, ONE rail: the purest demonstration of what a transfer rail does.

## 2. Protocol

- 5 sequential payments: B→A→B→A→B→A (5 hops, value ends home at A).
- Amount per hop: 700,000 drops (0.7 XRP) — identical to the XCF-1 XRP legs for comparability.
- Every payment carries memo tag SQDR-XTR-1 + hop number + the riding digest.
- Sequence management: A spends seqs 107745085-107745087, B spends seqs 107745086-107745087;
  each hop broadcasts only after the previous hop is validated (sequential custody discipline).
- **Speed measurement (the record):** for each hop, t0 = timestamp immediately before
  submit; t_engine = timestamp when the rippled server returns tesSUCCESS; t_validated =
  timestamp when the tx first reads validated=true. Report broadcast-to-acceptance and
  broadcast-to-finality per hop, plus ledger_index per hop.

## 3. The record sought

Full 5-hop custody chain, ownership changing hands 5 times, value back home at A, total
rail time measured end-to-end. If total broadcast-to-finality across all hops < 20 seconds,
the chain outpaces every other rail in this program by an order of magnitude (measured
comparators this same day: BTC ~minutes-hours, Stellar ~5s/leg, Cardano ~20-40s/leg,
Ethereum ~12-15s/leg).

## 4. Gates

G1 spec+prereg frozen pre-run — G2 all five payments built and signed offline — G3
sequential broadcast with per-hop timing — G4 keyless read-backs (memo + direction +
amount) ×5 — G5 ledger + receipts sealed. All gates deterministic; no LLM in any
decision path.

## 5. Cost

5 payments × 10 drops = 50 drops (~$0.003 at 2026-10-19 prices). The cheapest custody
chain ever run in this program.

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
