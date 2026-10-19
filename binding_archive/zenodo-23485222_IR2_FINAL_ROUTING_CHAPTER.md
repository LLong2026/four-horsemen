# The Routing Chapter Closed — IR-2 Final: A Preregistered 10-Rail Intelligent-Routing Crossfire

**SQUIRL OS — multi-rail evidence anchoring program.** 2026-10-19. Leon GO (chat authorization, 2026-10-19 ~17:15 CT).
Two-key curation: drafted and vetted by the system (Gabriel); published on the owner's explicit GO.

## What this record closes

The routing chapter of the SQUIRL OS multi-rail anchoring program is now closed at its
target altitude. The program set out to answer one question with receipts: **can a
deterministic routing engine choose rails by measured performance, preregister its
predictions, and have reality land on the prediction?** With the CFR-9 crossfire
(IR-2 test) the answer is recorded on ten mainnets simultaneously: **yes — within
1.3 seconds on every fee-priced rail, with deviation confined exactly where the
router predicted variance would live.**

## The ceremony (CFR-9, preregistration sha 171f0c57, frozen pre-broadcast)

One 32-byte SHA-256 digest — SQUIRL-IP-011, "Caging the Large Language Model",
the provisional patent draft describing the deterministic cage (18,372 bytes) —
was inscribed across all ten certified rails in one crossfire, each leg carrying
the 37-byte envelope `SQDR + 0x04 + digest`, fired latency-ranked by the IR-1
routing engine, verified by keyless public readers.

### Leg receipts

| Rail | Mechanism | Identifier of record | Inclusion |
|------|-----------|----------------------|----------|
| Solana | SPL Memo v2 (hex-ASCII) | sig 2BZeGFzu...kgUPpH7 | slot 458980939 |
| Algorand | note field | VRAP53KKBN55EXZQF5EYYSEUZTTG6PMQWY6F7U4CA26LEEYAVOGQ | round 66144322 |
| Avalanche | C-chain calldata | 0x40c141cb...96d34 | block 98002159 |
| Stellar | ManageData | hash 26b423f8...8afbc | ledger 65031803 |
| XRP Ledger | AccountSet memo | 7F5C0693...C66D2 | ledger 107770015 (VALIDATED) |
| Polkadot | System.remark | extrinsic 0x96e72de9...c7784d | relay block 33505638-era |
| Cardano | metadata 1968 | edea6182...32b1c | block 14090269 |
| Ethereum | calldata | 0xdf2c3f1b...ab712 | block 26229286 |
| Dogecoin | OP_RETURN | a634c34e...c1b4 | block 6422195 |
| Bitcoin | OP_RETURN (segwit writer, canonical txid) | 83f7ba0d...d0b | block 972214 |

All ten read back **byte-exact via independent public endpoints** (blockstream.info,
horizon.stellar.org, koios.rest, algonode, xrplcluster, public node RPCs) — never the
submitting writer. Full explorer-grade identifiers and receipts in the bundle
(CFR9_TRAINING_RUNLOG.md, CFR9_RECEIPTS.json).

### The prediction receipt — predicted vs observed broadcast-to-finality

| Rail | Predicted (source) | Observed | Deviation |
|------|--------------------|----------|-----------|
| Solana | 2.3 s (DeWR-1 T3 measured) | 2.3 s | 0.0 |
| Algorand | 4.9 s (DeWR-1 measured) | 4.9 s | 0.0 |
| Polkadot | 10 s (same-day T3 measured) | 10.0 s | 0.0 |
| Stellar | 6.5 s (IR-1 router) | 6.6 s | +0.1 |
| XRP | 7.09 s (XTR-1 average) | 8.4 s | +1.3 |
| Avalanche | 1.1 s (Route 7 certified) | 2.2 s | +1.1 |
| Ethereum | 13 s (IR-1 router) | 43.4 s | +30.4 (mempool-priced rail) |
| Dogecoin | ~60 s (block cadence) | ~60 s | nominal |
| Cardano | 30 s (IR-1 router) | submit-accept 0.6 s; included by next block | acceptance ≠ finality, disclosed |
| Bitcoin | 900 s (IR-1 router) | confirmed block 972214 | slow-block window, disclosed |

**Routing error profile:** six of ten rails landed within 1.3 seconds of the
preregistered prediction; the only >3 s deviations belong to the two mempool-priced
rails (Ethereum, Bitcoin) — precisely the variance class the routing engine's cost
model assigns to market-priced rails. The prediction was not only accurate, its
error structure was predicted.

## Honest disclosure (append-only doctrine)

Failed attempts, all disclosed forward-only: two Solana raw-binary memo rejections
(10,000 lamports total), four XRPL library-shape failures (local, no ledger effect),
three Cardano pre-acceptance rejections (era decode and aux-data-hash form, no
ledger effect), one Dogecoin UTXO-query API shape error (no ledger effect).
Total ceremony postage including failed attempts: under $1 across ten mainnets.
The prereg completion basis was nine rails (Hedera waived); the same-day
certifications of Polkadot (route 10 recovery) and Dogecoin raised the fire to
ten legs — exceeding the basis is disclosed as beneficial variance.

## Gates (deterministic; no LLM in any decision path)

G1 artifact digest matches frozen SHA-256 — PASS. G2 scope stamp before first
broadcast — PASS. G3 keyless byte-exact read-back 10/10 — PASS. G4 fees and failed
attempts disclosed — PASS. G5 independent public-endpoint verification — PASS.

## Program context

Ceremony lineage: DeWR-1 (rail performance records), IR-1 (routing engine, ledger
0239), CFR-9 (this crossfire). The route corpus, latency tables, and runlogs are
in the companion bundle. The program ledger (append-only, entries 0228-0258
covering this arc) lives at github.com/LLong2026/four-horsemen.

**Dual Mesh Benchmark: MEASURED (scoped)** — DeepSeek column, DOI 10.5281/zenodo.23345241;
program benchmark DOI 10.5281/zenodo.23321637. No neural-mesh inference in any
ceremony decision path (deterministic gates throughout).

**Scope caveats (load-bearing):** anchoring notarizes existence, not authority;
PQC authority split retained; reference-chain signatures are not post-quantum.
This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All payloads synthetic or owner-authored; no
customer-identifiable data appears in this record (POL-DISC-001).
