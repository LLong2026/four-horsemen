# MCR-4 RUNLOG — THIRD MOUNTAIN UPDATE (2026-10-25)

Fold: commit 029b32b (Ledger 0350 head), 3,377 leaves (2,082 -> 3,377 append-only).
ROOT: 38089f07ca7e3b76baa83a897eefe04f53a7893df3c84b5a4e4a436ddee8daaa
Envelope: SQDR + 0x06 + root (hex-ASCII 535144520638089f07... on UTF-8 rails, raw on binary rails).

## Gates (prereg MCR4_PREREG.md, committed ed86820 before fold/fire)
- G1 root-frozen: root recorded in MCR4_FOLD.json before broadcast. PASS
- G2 stamp-before-execute: RateLimitLog mcr4_mountain_update_2026-10-25 (20:35Z), before first leg. PASS
- G3 byte-exact readback: 12/12 keyless via public endpoints (algonode, horizon,
  xrplcluster, api.mainnet-beta.solana, publicnode, api.avax, rpc.polkadot.io,
  polkachu/mintscan, koios, blockcypher, blockchair, mempool.space). PASS
- G4 disclosure: see below. PASS
- G5 prereg immutability: prereg committed pre-broadcast, untouched after. PASS

## Crossfire legs (all first-pass clean, zero retries, zero failures)
xlm d38970dc... ledger 65134868 (3.7s) | xrp C0DBF58D... VALIDATED (5.8s) |
sol 3ig2R488... finalized (2.3s) | algo DTIOS4QW... round 66331095 (4.6s) |
avax 0xc48a2d36... block 98544328 (2.3s) | eth 0x5b993ae2... block 26272088 (36.2s) |
dot 0x4f6b02c9... included | atom D65D5A7F... block 33577129 code 0 (7.6s) |
ada 513103d0... accepted | ltc f1a1f535... push 201 (0.1s) |
doge e6448b73... push 201 (0.1s) | btc 3c52d450... 790 sats (0.2s broadcast; OP_RETURN
readable at readback time; confirmation pending at press time, block per mempool.space).

## Disclosures (G4)
1. TOOLING DEFECT FOUND AND DISCLOSED — mcr3_builder.py (committed e2fa836) omits the
   covenant leaf wrapper: it folds sha256(file) as the leaf directly instead of
   SHA-256(0x00 || sha256(file)) stated in its own docstring and in MCR1_LEAF_INDEX.json.
   First run reproduced neither the MCR-1 nor the MCR-3 recorded roots (581ca18e / 5740b1ae).
   The covenant SPEC is sound: with the wrapper applied, all three frozen roots
   (MCR-1 2d1a3214..., MCR-2 1929707e..., MCR-3 418fc5a8...) reproduce BYTE-IDENTICAL
   from the committed trees. The defect is in the committed replication TOOL only, not in
   any published root, envelope, or on-chain anchor. MCR-4 was folded with the corrected
   spec; the mcr3_builder.py defect is corrected forward-only in mcr4/mcr4_fold.py.
2. Readback preparation fix: MCR4_ENVELOPE.txt initially contained the bare root; the
   readback harness expects the full hex-ASCII payload (5351445206+root). Corrected
   before the first readback run; no on-chain effect (the fired payloads were correct
   throughout — verified 12/12 after the file fix).
3. Costs: BTC 790 sats; LTC 100000 lits; DOGE 5,000,000 koinu; ATOM 2500 uatom fee +
   1000 uatom self-send; ETH 22480 gas; AVAX 21592 gas; XLM 100 stroops; XRP 10 drops;
   SOL/ALGO/DOT/ADA minimum. Total postage on twelve mainnets under $2 (MCR cost doctrine
   holds).

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
