# SAT-1 RUNLOG — THE SATOSHI COVENANT (first value-carrying root commitment on BTC mainnet)
Ceremony: SAT-1 | Date: 2026-10-20 | Status: **PASS — covenant sat confirmed, hopped back and forth, keyless byte-exact at every hop**

## What this proves
For the first time under this program (and as the first recorded value-carrying anchoring
receipt of its kind — see G5 scoping), a Merkle Mountain Range root is committed INSIDE
value rather than beside it: a 330-sat output (the smallest relayable P2TR output — a
literal 1-sat output cannot relay, 330-sat P2TR dust floor disclosed) whose taproot
OUTPUT KEY commits the 10-rail-anchored MMR-2 root via BIP341 taptweak. The first
satoshi of that output is the covenant sat. The output was then transferred back and
forth between two fresh program writer wallets — SAT-A -> SAT-B -> SAT-A — with the
root re-committed in the tweaked output key at EVERY hop. The commitment travels with
the coin: wallet-agnostic, value-carrying. Companion anchors bind the same root on XRP
(memo rail) and Stellar (transport rail) — the same 32 bytes on a value rail, a memo
rail, and a transport rail: cross-rail agnosticism, demonstrated.

## Frozen values
- Committed root (MCR-2, 10-rail anchored, ledger 0265): `1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60`
- Taptweak: t = SHA-256(tagged TapTweak || internal_key_xonly || root); Q = P + tG
- Covenant output: 330 sats, scriptPubKey = OP_1 0x20 <Q_x> (v1 witness program), key-path only
- Envelope for companions: SQDR + 0x07 (satoshi covenant, prereg-registered) + root

## Wallets (program-controlled, fresh; WIFs never committed)
- SAT-A internal pubkey: dac3255223651af3e97c7bb50e492bd2c80b679c659f4d9cb328a1cfcdef2755
- SAT-B internal pubkey: 1309d3586ded5160b7ae1c08286eef440520c76c7cd0d089e4d11dd0a58c6ed2
- SAT-A covenant address: bc1ptnvnm4fafewtacz73nx2fq3qamwf8zxdnw7epg4l8qwdc49mz8cqqqml8sfk
- SAT-B covenant address: bc1p9lx4d6sfmqas9tgv44kefezl65r62sre78kg3e6g30ckzp6nrm9qqqvpkza8
- Funder: certified program BTC segwit writer (bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6)

## Transaction receipts (ALL CONFIRMED IN BLOCK 972278)
| TX | TXID | WHAT | FEE |
|---|---|---|---|
| FUND | e4e3806fd4243e2db784c08c240d8f592d54cc83dfb90e658265638c507738db | writer -> 330-sat covenant (SAT-A, root-tweaked) + 10,000 tank + 62,429 change | 2,000 sats |
| HOP-1 | 67271ff3d6cab58057ea7e6fb85243ccbcfc72996a786b54ae8f9c3747b00038 | SAT-A -> SAT-B (covenant + tank re-committed) | 2,000 sats |
| HOP-2 | d261810cd86c9c616c2f5545a0f14deab9cf9bcac444d5dc64371d1b0e871399 | SAT-B -> SAT-A (covenant + tank re-committed; sat is back home) | 2,000 sats |
| Stellar | 6f7747b45b26f50c2c35c0fd629c7aa671e948a0a2a4838e0e610f00d9a50287 | manage_data SQDR-SAT-1 = envelope, ledger 65038556, 4.0s | 100 stroops |
| XRP | A1ACA5826EBCC2E40DBE2887140DF8692344571494367F7C9DD4C17199BFA2A9 | MemoType SQDR-SAT-1, MemoData = envelope, VALIDATED | 10 drops |

## Gate results
- G1 (pure-Python BIP340 impl passes ALL 26 official BIP-0340 test vectors): **PASS**
- G1b (taptweak matches official BIP-86 reference vectors): **PASS**
- G2 (prereg + scope stamp sat1_satoshi_covenant_2026-10-20 before first broadcast): **PASS**
- G3 (keyless: every hop's covenant output recomputes from published pubkey + root,
  byte-matches on-chain scriptPubKey; value exactly 330 sats at every hop; tank
  outputs likewise): **PASS 5/5 txs**
- G4 (fees: 6,000 sats BTC + 100 stroops + 10 drops total; failures disclosed): **PASS**
- G5 (prior-art scoping — honest claim): **PASS.** Taproot-tweak data commitments are a
  known technique (Opt-In Auditability thesis; Taproot Assets); ordinal inscriptions
  commit via witness envelopes, not the output key. The claim is scoped as: the first
  satoshi covenant under this program — the first value-carrying, hop-portable,
  cross-rail-bound anchoring of a 10-rail-anchored mountain root. No global first-ever
  claim is made.

## Disclosed deviations (forward-only, no state change on any failed attempt)
1. Initial FUND legs entry recorded the wtxid (python-bitcoinlib GetTxid on segwit —
   defect class 0228 resurfacing); HOP-1 attempts 1-2 rejected
   bad-txns-inputs-missingorspent. Corrected to canonical txid; disclosed in legs file.
2. HOP-1 attempt 3 rejected mempool-script-verify (Invalid Schnorr signature): two
   root causes fixed in the library — (a) BIP340 signs against the even-y lift of the
   output key, so odd-y tweaked keys require signing with N - d_eff; (b) the BIP341
   SigMsg order: hash_type byte leads, spend_type and input_index follow sha_outputs.
   Attempt 4 accepted. All rejections were mempool-level, zero coins moved.
3. Dust floor: a literal 1-sat output is nonstandard (P2TR dust threshold 330 sats);
   the covenant uses exactly 330 sats and claims ordinal position 0 (the first satoshi)
   as the covenant sat. Disclosed in prereg before broadcast.

## Costs
BTC 6,000 sats (3 x 2,000) | XLM 100 stroops | XRP 10 drops. Total under $0.01 equivalent.

## Provenance
Leon GO (chat authorization, 2026-10-20 ~01:36 CT). Two-key curation: drafted and
executed by the system (Gabriel); scope-stamped before broadcast; ledger entry 0266
binds the covenant to its parent ceremony MCR-2 (ledger 0265). Anchor doctrine language
(ledger 0244) applies: value-carrying anchoring, not tokenization, in public artifacts.
Prototype disclaimer applies. Dual Mesh Benchmark: NOT MEASURED (deterministic ceremony,
no neural-mesh inference; program benchmark DOI 10.5281/zenodo.23321637). No client data,
no PHI, no credentials, no operator text quoted (POL-DISC-001, operator-privacy rule).
