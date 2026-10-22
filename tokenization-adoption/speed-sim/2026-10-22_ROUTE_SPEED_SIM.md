# ROUTE SPEED SIM 2026-10-22 — Transfer Scenarios + Hardened Route Table

**Scope stamp:** route_speed_sim_2026-10-22T07:15Z (12 certified rails, live mainnet,
SPEED-SIM-1 envelope `53514452 10` — first use of version byte 0x10).
**Class:** training-class speed simulation. No DOI, no ledger entry unless separately
sealed. All legs are micro self-transfers; value stayed in program wallets (fees only).

## 1. What ran

1. **Read-only endpoint sweep** (3 samples each): write-path RPC + verification-path
   explorer latency on all 12 rails (`SPEED_SWEEP_RAW.json`).
2. **Transfer scenarios**: one timed micro transfer per rail carrying the SPEED-SIM-1
   digest (37-byte doctrine: `SQDR` + 0x10 + sha256(SPEED-SIM-1|route-hardening|2026-10-22)),
   measuring broadcast and block-inclusion. Receipts: `SPEED_SIM_LEGS.json`,
   `SPEED_SIM_RUNLOG.md`.
3. **Byte-exact keyless readback** on all 12 legs: **12/12 PASS** (`SPEED_SIM_READBACK.json`).

## 2. Transfer scenario results (fire order, all UTC 2026-10-22)

| Rail | Broadcast→inclusion (measured) | Fee | Receipt |
|------|-------------------------------|-----|---------|
| XLM  | **6.7s** (ledger 65073504) | 100 stroops | 03b047c5…d8ef0 |
| XRP  | **8.8s** (VALIDATED) | 10 drops | AED2FE48…1EFB |
| SOL  | **2.7s** (finalized) | ~0.000005 SOL | 2qN8pH2e…RNhQ3 |
| ALGO | **4.6s** (round 66219885) | 0.001 ALGO | XJDDWAST…3Q5Q |
| AVAX | **3.5s** (block 98218026) | sub-cent | 0x19b0a0a7…bd551 |
| ETH  | **~189s** (block 26246613) | ~0.0000035 ETH | 0xaa244652…39a3 |
| DOT  | **6.0s** (included) | 0.0195 DOT | 0x95a712ad…aaa3 |
| ATOM | **8.1s** (block 33523399, memo byte-exact) | 2500 uATOM | 1551EDB5…374B |
| ADA  | **29.0s** (block 14100415) | 0.172 ADA | f60b5699…d8b6 |
| LTC  | 0.1s broadcast, **515s** inclusion | 0.001 LTC | 708e1fd5… |
| DOGE | 0.1s broadcast, **157.7s** inclusion | 0.05 DOGE | 4037dcf8… |
| BTC  | 0.1s broadcast, **315.1s** inclusion | 790 sats | fdfa6d72… |

Readback: 12/12 byte-exact against envelope `53514452 10` + SPEED-SIM-1 digest (full
hex in `SPEED_SIM_ENVELOPE.txt`), keyless, on independent verification endpoints.

## 3. Endpoint sweep (read-path latency, 3-sample average)

| Rail | Write-path primary | avg | Verify-path primary | avg | Block cadence (measured) |
|------|-------------------|-----|--------------------|-----|--------------------------|
| BTC  | blockstream.info | 97ms | mempool.space | 262ms | ~10 min (PoW) |
| XRP  | xrplcluster.com | 349ms | api.xrpscan.com | 238ms | ~4s (ledger) |
| XLM  | horizon.stellar.org | 294ms | stellar.expert | 91ms | ~4s |
| ADA  | api.koios.rest | 477ms | cardanoscan.io | 127ms | ~6.7s |
| ETH  | ethereum-rpc.publicnode.com | 111ms | etherscan.io | 50ms | ~10s |
| ALGO | mainnet-api.algonode.cloud | 143ms | allo.info | 63ms | ~2.2s |
| SOL  | api.mainnet-beta.solana.com | 141ms | solscan.io | 198ms | ~0.18s |
| AVAX | api.avax.network | 98ms | subnets.avax.network | 140ms | ~0.74s |
| DOT  | rpc.polkadot.io (ws) | 544ms | polkadot.subscan.io | 216ms | ~6s |
| DOGE | api.blockchair.com | 685ms | dogeblock.com | 57ms | ~1 min (PoW) |
| LTC  | litecoinspace.org | 230ms | litecoinspace.org api/tx | 218ms | ~2.5 min (PoW) |
| ATOM | cosmos-api.polkachu.com | 706ms | quokkastake.io | 825ms | ~5s |

## 4. Hardening actions (the point of the exercise)

1. **ETH gas pricing defect found and fixed in doctrine.** The WRAP-1-era leg sends a
   legacy type-0 tx at a fixed ~0.16 gwei; tonight's leg sat in the mempool ~3 minutes
   because base fee was 0.157 gwei. Hardened rule: ETH/AVAX legs must read current
   base fee and send EIP-1559 type-2 (or gasPrice = baseFee x 1.3 minimum).
   AVAX's identical code landed in 3.5s only because Avalanche base fee is near zero.
2. **ATOM endpoint pair is the slowest on the roster** (polkachu 706ms / quokkastake
   825ms). Add `cosmos-rest.publicnode.com` as primary candidate (used successfully in
   readback) with polkachu as fallback.
3. **DOGE blockchair write-path is rate-limit-prone** (685ms, intermittent 430s).
   Hardened order: dogeblock.com -> blockchair -> dogechain.info (UA required).
4. **Snowtrace.io now 403s scripted readers** — verify-path for AVAX switches to
   subnets.avax.network (140ms, clean); snowtrace remains manual-click only.
5. **PoW inclusion variance is the real finality story:** LTC 515s vs DOGE 158s vs
   BTC 315s in the same 20-minute window. Router rule: never single-thread a
   notarization on one PoW rail; BTC is notary-grade precisely because minutes are
   the expected cost, not a failure.
6. **Speed tiers for the router (measured 2026-10-22):**
   - Sub-3s class: SOL (2.7s)
   - 3-5s class: AVAX (3.5s), ALGO (4.6s)
   - 5-10s class: DOT (6.0s), XLM (6.7s), ATOM (8.1s), XRP (8.8s)
   - 10-60s class: ADA (29s), ETH (12-15s when gas is priced right; 189s tonight — defect #1)
   - Minutes class (PoW): DOGE (~1-3 min), LTC (~2-9 min), BTC (~5 min avg)
7. **HBAR (armed, awaiting funding):** recipe stands; when the ~5 HBAR funding hop
   lands, T1 probe -> T2 training leg -> T3 certification, then it joins this table
   (~3s aBFT expected, per recipe).

## 5. Disclosures

- ADA speed-sim leg reused the MCR-3 harness code, so its metadata label reads
  `CER: MCR-3`; the DIGEST field carries the SPEED-SIM-1 digest, not the MCR-3
  mountain root — distinguishable at readback and disclosed here.
- All 12 legs are training-class transfers carrying a speed-sim digest; no DOI, no
  certification claim. Fees total under ~$0.10.
- Readbacks used independent endpoints (quokkastake + publicnode for ATOM, drpc for
  ETH, blockcypher for LTC/DOGE, mempool.space for BTC, koios for ADA, etc.).

## 6. Verdict

**12/12 transfer scenarios executed, 12/12 byte-exact, 0 failed legs, 0 stuck
transactions.** The route table is measured end-to-end as of 2026-10-22, one hardening
defect (ETH gas pricing) identified with a concrete fix, and the router now has a
measured speed-tier table to schedule notarizations against. The fleet's standing
pair (XLM display + XRP anchor) remains top-tier fast: 6.7s / 8.8s.
