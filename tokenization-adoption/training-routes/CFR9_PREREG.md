# CFR-9 PREREGISTRATION — The Intelligent Routing Crossfire (IR-2 test)
Frozen BEFORE any broadcast. 2026-10-19 ~13:05 CT. Leon GO (chat authorization, 2026-10-19 ~12:58 CT).

## Artifact (the payload)
SQUIRL-IP-011_CAGING_THE_LLM_PATENT_DRAFT.md — "Caging the Large Language Model" provisional
patent application draft (docket SQUIRL-OS-IP-011). Canonical form: the Markdown file, byte-for-byte.
SHA-256 (frozen): bf9b8b4c608cdf68655efd9a1d8bce80f55969c0196fac9b9f1abea377c28909
Size: 18372 bytes.

## What the ceremony proves
The patent that describes the deterministic cage is inscribed across every certified rail by
the intelligent routing engine (IR-1, ledger 0239) — the invention documenting its own
containment evidence chain, routed by measured performance, verified by keyless readers.

## Protocol
1. Route table: the IR engine reads live rail telemetry (measured finality from XTR-1, IR-1,
   DeWR-1 leg receipts) and produces an ordered route table: legs fire fastest-predicted-first.
   A second ordering (cost-ranked) is computed and recorded for comparison; the fire order is
   latency-ranked (primary metric: time-to-finality).
2. One inscription leg per certified rail, each carrying the 32-byte digest
   bf9b8b4c...7c28909 byte-exact via the rail's native inscription mechanism:
   BTC OP_RETURN | XRPL AccountSet memo | Stellar ManageData | Cardano metadata 1968 |
   ETH calldata | ALGO note field | AVAX calldata | SOL SPL Memo (hex-ASCII) | DOT System.remark.
3. Each leg measured: broadcast-to-finality seconds, fee, keyless read-back (byte-exact required).
4. Prediction check (IR doctrine): predicted vs observed finality per rail; deviation > 3s raises
   an operational note in the runlog; the run records the routing engine's error profile.
5. Completion basis: 9 rails (HBAR waived, ledger 0243). Fires when DOT certifies (route 9 T3).
   If DOT funding has not landed by 2026-10-19 20:00 CT, fires on 8 rails with the waiver
   disclosed, and the DOT leg appends as an addendum when it certifies.
6. Idempotency: scope stamp cfr9_crossfire_<date> written before the first broadcast.
7. Sealed: runlog commit + ledger entry 0244 (or next open) + receipts to Leon. Total postage
   disclosed per rail and summed. No DOI mint in this ceremony unless Leon GOs a Zenodo record
   for the patent draft (separate two-key decision).

## Gate checks (deterministic, no LLM in the decision path)
G1: artifact digest matches frozen sha bf9b8b4c608cdf68655efd9a1d8bce80f55969c0196fac9b9f1abea377c28909
G2: scope stamp present and unique before first broadcast
G3: every leg keyless-readable and byte-exact
G4: all fees recorded; no undisclosed retries (failed attempts disclosed forward-only)
G5: read-back of at least one leg by an independent public endpoint (not the submitting node)
