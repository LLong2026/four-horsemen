# TRAINING ROUTES — The Route Certification Roster v0.1 (DRAFT)

**Status:** preset roster, pre-funding. No wallet funded, no leg signed. Each route activates
only on Leon GO + micro-funding (< $5 per rail). This is the training-camp roster for the
certification program: rails get rehearsed, timed, and certified before they ever carry a
public artifact.

## Tier 1 — CERTIFIED (5 routes, fully proven Oct 18-19, 2026)

| # | Rail | Mechanism | Measured finality | Cost/leg |
|---|------|-----------|-------------------|----------|
| 1 | Bitcoin | OP_RETURN | minutes-hours | ~700-1,300 sats |
| 2 | XRP Ledger | AccountSet memo / Payment memo | 5.3-8.0s (accept 0.30s) | 10 drops |
| 3 | Stellar | ManageData / memo_hash | 5-8s | 100 stroops |
| 4 | Cardano | metadata label 1968 | 20-40s | ~171k lovelace |
| 5 | Ethereum | calldata, self-addressed, value 0 | 12-15s | ~22.5k gas @ ~0.4 gwei |

## Tier 2 — CANDIDATE TRAINING ROUTES (the next class, preset)

**6. Algorand (ALGO)** — note field on any txn (ARC-2 convention). ~0.001 ALGO/txn
(~$0.0004), ~2.8s deterministic finality. Purest analog of our XRPL/Stellar doctrine.
PRIME CANDIDATE — first training route.

**7. Solana (SOL)** — SPL Memo program: digest recorded in instruction data, permanently
on-chain. ~$0.00025/txn, ~400ms slots. Keypair wallet, no account reserve surprises.
Tooling lift: solana-py or raw JSON-RPC.

**8. Avalanche C-Chain (AVAX)** — EVM calldata: reuses the Ethereum leg nearly verbatim
(eth-account, EIP-155, self-addressed zero-value). ~1-2s finality, sub-cent. LOWEST
engineering lift of the entire Tier 2 — 90% of the code already exists.

**9. Hedera (HBAR) — RAIL #10 RE-OPENED 2026-10-21 (ledger 0243 waiver reversed by
owner GO, chat ~15:02 CT; armed Oct 19 ed25519 key stands up).** Memo field on a
CryptoTransfer. ~$0.0001, ~3s aBFT finality. gRPC 50211/50212 verified OPEN on all 8
live mainnet nodes probed 2026-10-21 (stale-IP block scare resolved). Alias
0.0.vefaw75r... (ed25519 pub a90a0b7f...83236b). Friction remains the funding hop:
exchanges require 0.0.x, auto-create needs an alias-capable wallet (HashPack/Blade).
AWAITING FUNDING HOP 1 (~5 HBAR). Recipe: hbar-rail/HBAR_RECIPE.md.

**10. Polkadot (DOT)** — system.remark extrinsic: literally purpose-built for data
anchoring, zero movement. Fraction of a DOT; ~12-30s finality. The remark IS the
inscription — cleanest ideological fit.

**11. Litecoin (LTC) — CERTIFIED 2026-10-21 (Rail #11, block 3199221).** OP_RETURN
envelope 6a25 53514452 06 <digest> (thesis v2.1 §2.5 doctrine). Certification leg
LTC-CERT-1: txid 3604955253332f0bd67f59ad1eabc0dda10763265f410d9a0258df0b949abb6e,
payload = SQDR + 0x06 + DeWR-1 frozen digest 99e01327...b9ab6 (37 B), byte-exact on
Blockchair + litecoinspace (keyless, independent). Fee 0.001 LTC; owner-funded
0.15993393 LTC (tx 351c9c98...fd049:0, 2026-10-21 ~20:07Z); change 0.15893393 LTC
standing in writer LYhD9b7ipytek7KcJSU4EtKfqHLg8Kgiuc. Second PoW anchor alongside
DOGE — was 'optional/lowest priority', promoted per owner GO (chat 2026-10-21 ~15:02 CT).
Receipts: ltc-rail/LTC_FIRE_RUNLOG.md, ltc-rail/LTC_LEGS.json.

**12. Cosmos Hub (ATOM)** — memo field on a bank send. ~$0.01, ~6-7s. Simple, but memo
tooling is the least standardized of the set.

## Tier 3 — NOT SUBSTRATES (watchlist, not training routes)

- **Ethereum L2s (Base, Arbitrum)**: same calldata mechanism, security INHERITS from
  Ethereum — same failure-domain family, not an independent rail. Substrates, not routes
  (substrate doctrine: a route must add an independent failure domain).
- **Arweave**: not a blockchain — stores the FULL artifact, not a digest. Different class:
  archive rail, complementary, not notarization. Possible future role: vault's public mirror.
- **Monero / Zcash (shielded)**: privacy chains — keyless verification impossible, which
  defeats the entire doctrine. Permanently out.
- **Nano**: no data field. Out.
- **Aptos / Sui**: possible but heavy Move tooling; Tier 2.5 if ever needed.

## Route Certification Protocol (preset, mirrors ceremony gates)

- **T1 — PROBE (keyless, $0):** live probe of the rail's finality, cost, state. Read-only.
- **T2 — TRAINING LEG (micro-fund, < $5):** one test inscription of a training digest.
  Rehearsal only; no DOI, no ledger, disclosed as training.
- **T3 — CERTIFICATION (full ceremony):** spec + prereg frozen, timed leg executed,
  keyless byte-exact read-back, ledger entry sealed. The rail joins Tier 1.
- **T4 — ROUTER INTEGRATION:** the rail enters the IR-1 router's live table and the
  RAIL_PLAYBOOK speed/cost table. It can now be SELECTED, not just used.

## Activation order (recommendation, pending Leon GO)

ALGO → AVAX (reuse) → SOL → HEDERA → DOT → (LTC optional). Rationale: Algorand first
(doctrinal purity + cheapest rehearsal), Avalanche second (near-zero new code), then the
three new toolchains in order of market relevance.

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
