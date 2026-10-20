# MCR-2 RUNLOG — THE MOUNTAIN UPDATE (append-only MMR root re-anchor, 10-rail crossfire)
Ceremony: MCR-2 | Date: 2026-10-20 | Status: **PASS — 10/10 rails byte-exact, G1-G5 all green**

## What this proves
The public evidence corpus grew from 1,891 to 1,906 files (now containing SQUIRL-OS-IP-013,
the constant-footprint MMR storage-covenant patent, and its Zenodo DOI
10.5281/zenodo.23491295). The full corpus at commit `bf13210` was re-folded into a
Merkle Mountain Range and the new 32-byte root anchored across all ten certified mainnet
rails in a fixed 37-byte envelope (`SQDR + 0x06 + root`). The prior MCR-1 root
(`2d1a3214…`) remains sealed and unmodified on-chain — spot-verified post-update on BTC
(block 972219), XRP, and XLM. This is the first MOUNTAIN UPDATE: corpus growth discharged
at constant on-chain footprint, append-only, per the IP-013 doctrine.

## Frozen values
- MMR-2 ROOT: `1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60`
- Leaf count: 1,906 (peak heights 10, 9, 8, 6, 5, 4, 1)
- Corpus commit: `bf13210` (four-horsemen, origin/main)
- Parent covenant: MCR-1 root `2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a` (ledger 0260)
- Envelope: `SQDR` + `0x06` (mountain-update covenant, registered in prereg) + root = 37 bytes
- Append-only continuity: the height-9 peak `e173493c…b2d6` is byte-identical to MCR-1's
  height-9 peak — the first 1,536 leaves are provably unchanged.

## Gate results
- G1 (builder validated against MCR-1 frozen root, byte-exact, 1,891 leaves): **PASS**
- G2 (prereg + scope stamp `mcr2_mountain_update_2026-10-20` before first broadcast): **PASS**
- G3 (keyless byte-exact read-back on every rail): **PASS 10/10**
- G4 (all fees recorded; zero failed attempts in broadcast; DOGE spends MCR-1 change
  4dc643c4…b0bd:1 verified unspent pre-broadcast): **PASS**
- G5 (MCR-1 anchors verified unmodified post-update — BTC, XRP, XLM): **PASS**

## Preflight (all writers funded; MCR2_PREFLIGHT.json)
SOL 0.284 | ALGO 49.9 | AVAX 2.50 | XLM 53.5 | XRP 30.18 | DOT 9.42 | ADA 74.55 |
ETH 0.0123 | DOGE 14.80 (MCR-1 change UTXO) | BTC 75,549 sats (MCR-1 change UTXO)

## Crossfire receipts (latency-ranked fire order; keyless-verified)
| RAIL | TXID | BYTE-EXACT | TIME | LINK |
|---|---|---|---|---|
| SOL | `ioWqRNt1imp1w7qfvnpnBLaH…` | True | 2.2s | https://solscan.io/tx/ioWqRNt1imp1w7qfvnpnBLaHQuQrgVGbvSUkFLrmkc1bYLfiWSqwGBDqmmaGk1pkg8vzpRgEguvdnseK2juK8Ve |
| ALGO | `4AXOU73K4GAMIYN6QDYJ5AHB…` | True | 3.9s | https://allo.info/tx/4AXOU73K4GAMIYN6QDYJ5AHBOB5KG7LC5IUMKQJHCASGSEEUNV2Q |
| AVAX | `0xe452d69de742f688bebf42…` | True | 1.2s | https://snowtrace.io/tx/0xe452d69de742f688bebf4276fe0f0d1dae0e07e9d33b0e3d3c518d301d9640cc |
| STELLAR | `835b6292a4e5703c5ce1fa2f…` | True | 5.5s | https://stellar.expert/explorer/public/tx/835b6292a4e5703c5ce1fa2f94d171bb49f41052831f98747399a5db01544527 |
| XRP | `5E606006FAB120C7781C297C…` | True | 8.3s | https://livenet.xrpl.org/transactions/5E606006FAB120C7781C297C7E27A4C69A9C67E06AA9482247ED2B6A72842DCD |
| DOT | `0x457581f03366b8122fb7cf…` | True | 8.4s | https://polkadot.subscan.io/extrinsic/0xfebd73b4 |
| ETH | `0xa59987bd38c5f87a8f19e5…` | True | 11.8s | https://etherscan.io/tx/0xa59987bd38c5f87a8f19e532243c6b6114a621b4c771a8498a2d0988c311adc5 |
| DOGE | `56f0aae3a3a8f8cd34eeab92…` | True | 0.1s | https://dogechain.info/tx/56f0aae3a3a8f8cd34eeab92111fcda05e166f5dbc6af501098804eb547ead85 |
| BTC | `909f8ec8ff93d240afa39b33…` | True | 0.2s | https://mempool.space/tx/909f8ec8ff93d240afa39b332ec6db0ad767be6fce7f2afe01b7904d8b7eb524 |
| CARDANO | `159b9d115743744e4d448c9f…` | True | 0.1s | https://cardanoscan.io/transaction/159b9d115743744e4d448c9f429c77c374dabb218071db95a31e8c00602c0f5e |

## Inclusion proofs (all six re-verified to the frozen root; MCR2_INCLUSION_PROOFS.json)
- leaf 0 (.gitignore), leaf 1, mid leaves 952/953, last leaf 1905 (zenodo_deposit_settings.json),
  and LEDGER.md (leaf 62) — each with O(log N) ≈ 10-hop paths, ROOT-VERIFIED.

## Read-back notes (G3 details)
- SOL: hex-ASCII memo, base58-decoded from getTransaction — byte-exact
- ALGO: raw 37-byte envelope in note field via indexer — byte-exact
- AVAX/ETH: calldata `0x`+envelope — byte-exact (ETH status 0x1, gas 22,480; AVAX gas 21,592)
- XLM: manage_data `SQDR-MCR-2`, base64 value — byte-exact
- XRP: MemoType `SQDR-MCR-2`, MemoData = raw envelope — byte-exact, validated
- DOT: hex-ASCII remark found in confirmed block extrinsics (keyless chain_getBlock)
- ADA: metadata label 1968, `CER: MCR-2`, digest = root — byte-exact (Koios tx_metadata)
- DOGE: raw envelope in OP_RETURN — byte-exact
- BTC: `6a25` + envelope OP_RETURN, segwit writer, canonical txid — byte-exact, block 972275

## Costs (measured)
- ETH: 22,480 gas @ ~0.05 gwei | DOT fee: ~0.0195 DOT | BTC: 790 sats | ADA: 172,000 lovelace
- XLM: 300 stroops | XRP: 10 drops | SOL/ALGO/AVAX/DOGE: sub-cent equivalents (legs file)
- Total ceremony cost: under $1 equivalent at broadcast-time prices.

## Provenance
Leon GO (chat authorization, 2026-10-20 ~00:50 CT). Two-key curation: drafted and
executed by the system (Gabriel); scope-stamped before broadcast; ledger entry 0265
seals the update and binds it to parent covenant MCR-1 (ledger 0260). Prototype
disclaimer applies. Dual Mesh Benchmark: NOT MEASURED (no neural-mesh inference
involved; deterministic ceremony). No operator text quoted; no customer-identifiable
data; all payloads synthetic/structural.
