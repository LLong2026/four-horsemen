# TRAINING ROUTES — The Route Certification Roster v1.0

**Status:** 11 rails certified and sealed (Oct 18-21, 2026), Rail #10 HBAR armed and
awaiting its funding hop. Each rail carries: the mechanism (the path we took), the
certification ceremony that sealed it, its receipts, and its standing costs. New rails
are added here ONLY after certification (probe -> training leg -> certification ->
router integration), and certification receipts land in this repo the same day —
standing rule per Leon (2026-10-21).

## Tier 1 — CERTIFIED (11 rails, sealed)

| # | Rail | Mechanism (the path) | Certified by | Measured finality | Cost/leg |
|---|------|----------------------|--------------|-------------------|----------|
| 1 | Bitcoin | OP_RETURN envelope (SQDR + version byte + digest; refire uses 0x0D) | MCR-1/MCR-2, WRAP-1 seal (ledger 0285, ledger 0290 refire) | minutes | ~790 sats |
| 2 | XRP Ledger | Payment/AccountSet memo, rail of record | FL-1 escrow courtroom, WRAP-1, TL-1 attestation | 4-8.5s | 10 drops |
| 3 | Stellar | ManageData data entry on vessel account, public display rail | XLM-COV-1, TL-1 token leg (ledger 65050475), epoch roots | 5-6s | 100 stroops |
| 4 | Cardano | metadata label 1968 | WRAP-1 (tx 4b5d39ea...) | 20-40s | ~171k lovelace |
| 5 | Ethereum | calldata, self-addressed, value 0 | WRAP-1 (tx 0x4f80cf60...) | 12-15s | ~22.5k gas |
| 6 | Algorand | ARC-2 note field | WRAP-1 (JBB5FT2D..., round 66176768) | ~3.5s | ~0.001 ALGO |
| 7 | Solana | SPL Memo instruction data | WRAP-1 (YyNmJnWp..., slot 459392724) | ~2.4s | ~$0.00025 |
| 8 | Avalanche C-Chain | EVM calldata (ETH leg reused) | WRAP-1 (0xd0d14050..., block 98095176) | ~2.4s | sub-cent |
| 9 | Polkadot | system.remark extrinsic | WRAP-1 (0x3ec93e79..., block 33519650) | ~12-30s | fraction of DOT |
| 9b | Dogecoin | OP_RETURN (second PoW anchor) | MCR-2/WRAP-1 (tx 948654fd...) | minutes | dust |
| 11 | Litecoin | OP_RETURN envelope 6a25 53514452 06 <digest> (thesis v2.1 §2.5) | LTC-CERT-1 (ledger 0292, block 3199221) | minutes | 0.001 LTC |

Receipts of record: WRAP-1 phase seal 14b11a77...c72ea, ten-rail table in
`wrap1_receipts_2026-10-20/WRAP1_RUNLOG.md`; LTC in
`tokenization-adoption/ltc-rail/LTC_FIRE_RUNLOG.md` + `LTC_LEGS.json`; TL-1 three-chain
lock in `tl1/` (ledger 0286, uploaded 2026-10-21 per ledger 0294).

## Tier 2 — ARMED / CANDIDATE

**10. Hedera (HBAR) — ARMED, AWAITING FUNDING HOP 1 (~5 HBAR).** Re-opened 2026-10-21
(ledger 0243 waiver reversed by owner GO). ed25519 writer key stands up; gRPC
50211/50212 verified OPEN on all 8 live mainnet nodes. Alias
0.0.vefaw75r... (pub a90a0b7f...83236b). Path: CryptoTransfer memo field, ~3s aBFT
finality, ~$0.0001. Blocker: owner funding via alias-capable wallet (HashPack/Blade).
Recipe: `tokenization-adoption/hbar-rail/HBAR_RECIPE.md`.

**12. Cosmos Hub (ATOM) — ARMED, AWAITING FUNDING HOP 1 (0.5-1 ATOM from Coinbase).**
Armed 2026-10-21 (ledger 0295): writer cosmos1eyplx3a0rskyes6zmqu9pll03uchf8mclrh0gd
generated and bech32-validated, runlog stamped pre-funding. Path: bank send memo field,
envelope SQDR + version byte + digest (37 B doctrine), ~6-7s finality, ~$0.01/leg.
Receipts: tokenization-adoption/atom-rail/ (ATOM_FIRE_RUNLOG.md, ATOM_WALLET_PUBLIC.json).

## Tier 3 — NOT SUBSTRATES (watchlist, not routes)

- **Ethereum L2s (Base, Arbitrum)**: security INHERITS from Ethereum — same
  failure-domain family, not an independent rail. Substrates, not routes.
- **Arweave**: not a blockchain — stores the FULL artifact, not a digest. Archive rail,
  complementary, not notarization.
- **Monero / Zcash (shielded)**: keyless verification impossible — defeats the doctrine.
  Permanently out.
- **Nano**: no data field. Out.
- **Aptos / Sui**: heavy Move tooling; Tier 2.5 if ever needed.

## Route Certification Protocol (unchanged, mirrors ceremony gates)

- **T1 — PROBE (keyless, $0):** live probe of finality, cost, state. Read-only.
- **T2 — TRAINING LEG (micro-fund, < $5):** one test inscription of a training digest.
  Rehearsal only; no DOI, no ledger, disclosed as training.
- **T3 — CERTIFICATION (full ceremony):** spec + prereg frozen, timed leg executed,
  keyless byte-exact read-back, ledger entry sealed. The rail joins Tier 1.
- **T4 — ROUTER INTEGRATION:** the rail enters the IR-1 router's live table and the
  RAIL_PLAYBOOK speed/cost table. It can now be SELECTED, not just used.
- **T5 — RECEIPTS LANDED (standing rule, added 2026-10-21 per Leon):** every
  certification uploads its receipts to this repo the SAME DAY it seals. A ledger
  entry that references receipts not yet in the repo is an open gap, closed within
  the day and disclosed forward-only.

## Activation order (next up)

HBAR (funding hop 1) -> ATOM (probe + training leg). Rationale: HBAR's key is already
armed and its recipe frozen; ATOM is the last pre-vetted candidate before evaluating
new families.

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
