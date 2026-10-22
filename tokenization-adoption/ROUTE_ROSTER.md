# TRAINING ROUTES — The Route Certification Roster v1.2

**Status:** 12 rails certified and sealed (Oct 18-22, 2026), speed-sim measured and
routes hardened (2026-10-22), THE TRIAD (SAT + XLM + XRP) promoted to DEFAULT ROUTE
per Leon (2026-10-22, ~02:37 CT; see triad/TRIAD_ROUTE.md), Rail #10 HBAR armed and
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
| 12 | Cosmos Hub | bank send memo (hex envelope, SIGN_MODE_DIRECT) | ATOM-CERT-1 (ledger 0296, block 33518894) | ~6-7s | 2500 uatom |

Receipts of record: MCR-3 mountain update root 418fc5a8...b8d06 (ledger 0297, 12/12
rails incl. first MMR legs on LTC + ATOM, receipts mcr3/); WRAP-1 phase seal 14b11a77...c72ea, ten-rail table in
`wrap1_receipts_2026-10-20/WRAP1_RUNLOG.md`; LTC in
`tokenization-adoption/ltc-rail/LTC_FIRE_RUNLOG.md` + `LTC_LEGS.json`; TL-1 three-chain
lock in `tl1/` (ledger 0286, uploaded 2026-10-21 per ledger 0294).

## DEFAULT ROUTE — THE TRIAD (v1.2, standing per Leon 2026-10-22)

**Every standard notarization event = SAT + XLM + XRP (one triad fire).**

| Member | Role | Engine | SLO | Fee |
|--------|------|--------|-----|-----|
| SAT (BTC) | Notary anchor — immovable substrate | SHA-256 PoW | ~1 block expected, hard deadline 3 blocks | dynamic sats/vB, ceiling 30 |
| XLM | Display rail — human-readable named entry | Stellar SCP | <= 3 ledgers (~12s) | 100 stroops |
| XRP | Attestation rail — redundant fast anchor | XRPL consensus | <= 3 ledgers (~12s) | 10 drops |

Why: three disjoint consensus engines = no shared failure mode; stable fees (no
base-fee auction — the pathology that bit ETH in SPEED-SIM-1); complementary surfaces
(read / verify / institutional); under $0.10 per event; proven in TL-1, PAT-1, and
TRIAD-SIM-1 (12/12-style proof: 3/3 byte-exact, 2026-10-22).

Tiering doctrine (the at-scale answer): every event -> XLM; session/epoch close ->
XRP roll-up; major seals only -> full triad with SAT. One SAT anchor per epoch
amortizes over thousands of events. MCR-class corpus seals still fan out to the
full 12-rail mesh. Minor rails remain certified and callable, not default.

Hardened runner: `triad/triad_fire.py` (failover pairs, fee guard, idempotency,
dual-endpoint byte-exact readback gate 3/3, fail-closed escalation). Proof run
TRIAD-SIM-1: XLM 8.1s + XRP 6.5s + SAT 1206.4s (block 972586; PoW cadence variance
recorded same night as SPEED-SIM-1's 315s — minutes are the design cost), 3/3
byte-exact, 0 failed legs.

## Route Speed Table (measured 2026-10-22, SPEED-SIM-1 transfer scenarios — v1.1)

Live end-to-end timings from 12/12 micro transfer scenarios, byte-exact readback on all
legs. Full data: `speed-sim/2026-10-22_ROUTE_SPEED_SIM.md` + receipts.

| Speed class | Rails (measured) |
|-------------|------------------|
| Sub-3s | SOL 2.7s |
| 3-5s | AVAX 3.5s, ALGO 4.6s |
| 5-10s | DOT 6.0s, XLM 6.7s, ATOM 8.1s, XRP 8.8s |
| 10-60s | ETH 12-15s (when gas priced right), ADA 29s |
| Minutes (PoW) | DOGE ~1-3min, LTC ~2-9min, BTC ~5min avg |

**Hardening rules (v1.1, standing):**
1. ETH/AVAX legs price gas dynamically (EIP-1559 type-2 or gasPrice >= baseFee x 1.3).
   SPEED-SIM-1 caught the legacy fixed-gas defect: an ETH leg sat ~3 min against a
   0.157 gwei base fee.
2. ATOM write-path adds `cosmos-rest.publicnode.com` as primary (polkachu 706ms /
   quokkastake 825ms were the slowest pair on the roster).
3. DOGE write-path order: dogeblock -> blockchair (rate-limit-prone) -> dogechain.
4. AVAX verify-path: subnets.avax.network (snowtrace 403s scripted readers).
5. Never single-thread a notarization on one PoW rail — minutes are the design cost,
   not a failure (LTC took 515s the same night BTC took 315s and DOGE 158s).

## Tier 2 — ARMED / CANDIDATE

**10. Hedera (HBAR) — ARMED, AWAITING FUNDING HOP 1 (~5 HBAR).** Re-opened 2026-10-21
(ledger 0243 waiver reversed by owner GO). ed25519 writer key stands up; gRPC
50211/50212 verified OPEN on all 8 live mainnet nodes. Alias
0.0.vefaw75r... (pub a90a0b7f...83236b). Path: CryptoTransfer memo field, ~3s aBFT
finality, ~$0.0001. Blocker: owner funding via alias-capable wallet (HashPack/Blade).
Recipe: `tokenization-adoption/hbar-rail/HBAR_RECIPE.md`.

**12. Cosmos Hub (ATOM) — CERTIFIED 2026-10-22 (ledger 0296, block 33518894).** Memo
field on a self-addressed bank send; envelope hex SQDR + 0x07 + DeWR-1 frozen digest
99e01327...b9ab6 (37 B doctrine). Certification leg ATOM-CERT-1: txid
2182DE2D41684CCE67A0FA53218C93324080421B98166D45F467F77769D2FBB5, memo byte-exact on
two independent keyless readbacks (polkachu + quokkastake). Owner-funded 5.07 ATOM
from Coinbase (plain bech32, zero friction — the anti-HBAR). Change standing in writer
cosmos1eyplx3a0rskyes6zmqu9pll03uchf8mclrh0gd. First hand-rolled protobuf
SIGN_MODE_DIRECT leg in the program (cosmospy amino format dead on cosmoshub-4;
disclosed in runlog). Receipts: tokenization-adoption/atom-rail/.

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
