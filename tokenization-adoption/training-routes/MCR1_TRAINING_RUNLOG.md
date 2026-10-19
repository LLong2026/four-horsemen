# MCR-1 TRAINING RUNLOG — THE MERKLE ROOT COVENANT
2026-10-19 (UTC). Leon GO (chat authorization, 2026-10-19 ~17:15 CT). Prereg sha 96ffbb53, frozen before first broadcast. Scope stamp mcr1_covenant_2026-10-19 (22:16:48Z).

## What happened
The entire public evidence record — the complete four-horsemen repository at commit
7c492528c9f9624bb43846b745df9a480f4d1600, 1,891 files — was folded into one Merkle
Mountain Range (leaf = SHA-256(0x00 || sha256(file)), node = SHA-256(0x01 || left || right),
peaks bagged right-to-left, root = SHA-256(0x03 || bag || 1891 as u64 LE)).

**MMR ROOT: 2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a**
Peaks: heights 10, 9, 8, 6, 5, 1, 0 (a true mountain range).

That single 32-byte root was then anchored across ALL TEN certified mainnet rails in one
crossfire, envelope SQDR + 0x05 + root (37 bytes; hex-ASCII on UTF-8 rails, raw bytes on
binary rails, per payload doctrine §2.5).

## Legs (broadcast UTC 2026-10-19, latency-ranked order)
| Rail | Mechanism | Identifier | Inclusion |
|------|-----------|------------|-----------|
| Solana | SPL Memo v2 hex-ASCII | sig 4zgs4tmPvqvRjje8bJCmC7r8iDhF6BQpqvPcYPJjfGCypTTnegSqvN62iAPSXurWGNGhk8HH8Yb4Up16Lx4Qpqnn | confirmed 2.8s |
| Algorand | note field | XLBEIUK6SFKBNUS3FWQNXRDURHFCNEFKTORIE4PTX5M7SY6JFADQ | round 66145569, 3.2s |
| Avalanche | C-chain calldata | 0xf386821b1626b53e4d03dc0dc968f1e9d0625f6a5b7de99624798112cc639bb0 | block 98005575, 2.3s |
| Stellar | ManageData "SQDR-MCR-1" | 5f9ea3c815f9a848d4804166a911f9905c1a57b351f511b6989e82b830bdb536 | ledger 65032495, 7.9s |
| XRP Ledger | AccountSet memo | C42468F0141694969486CBC29005C0E5ACC8623ABF6A4012A14D12C665459480 | VALIDATED, 6.1s |
| Polkadot | System.remark | extrinsic 0x94c6997b...f96a81 | relay block 33505287 |
| Cardano | metadata 1968 {CER: MCR-1, DIGEST: root} | 772b4aa631bf24df010f7461629c909a59a6d63ae9dac21bc86c06bb71bfa51d | block-era, accepted first try |
| Ethereum | calldata | 0xe017e8b2fdc0d645c77fa81f0fdf2c430a8479f6fc9a53c3db08adcbdd0c5289 | block 26229558, 23.5s |
| Dogecoin | OP_RETURN (raw envelope) | 4dc643c424cf8f374fb5f1810f3209dfe561eeab61ff4026cc93b97afb59b0bd | mempool→block |
| Bitcoin | OP_RETURN segwit writer | 8728d0215fd2fc9fb8fb6ff9b011322875e88620a78787d597d529ecc1974195 | fee 790 sats |

## Keyless read-back (independent public endpoints only)
10/10 rails read back BYTE-EXACT against the frozen root. Every inclusion proof for the
demonstration leaves (LEDGER.md, DCAI_DOI_INDEX.md, IR2_FINAL_ROUTING_CHAPTER.md, first/
middle/last leaves) re-folds to the same frozen root. Anyone can rebuild the mountain:
clone the repo at commit 7c49252, hash the 1,891 files per MCR1_LEAF_INDEX.json, and fold.

## Honest disclosure (forward-only)
- SOL: one raw-binary memo simulation rejection before the proven hex-ASCII form (no ledger effect).
- XRP: five local xrpl-py argument-shape errors (all local, no ledger effect, the known library quirks).
- Cardano: two pre-acceptance decoder rejections (output-pair order; aux_data_hash placed at
  body key 16 instead of 7) — both fixed, accepted on the first correct submission, no ledger effect.
- DOGE: Blockchair's outputs endpoint returned a PHANTOM unspent output (bff3312d:0, "146.79 DOGE")
  that does not exist per node-backed BlockCypher and dogechain; the spend built on it was rejected
  by consensus (script-verify) — never landed, no funds moved. The genuine unspent output
  (CFR-9 change a634c34e:1 = 14.85 DOGE) was then spent cleanly. Blockchair also IP-blacklisted
  the broadcast endpoint (430), resolved by broadcasting via BlockCypher (HTTP 201).
- BTC: clean first broadcast; mempool-to-block window disclosed in receipts.
- A verification harness defect (expected-envelope typo "SODR" vs SQDR) was caught mid-sweep
  and corrected — the on-chain legs were byte-exact all along. Disclosed per doctrine.

## Gates
G1 root matches frozen prereg — PASS (recomputed deterministically; every proof re-folds to it)
G2 scope stamp before first broadcast — PASS (22:16:48Z stamp, broadcast after)
G3 keyless byte-exact read-back — PASS 10/10
G4 fees and failed attempts disclosed — PASS (total ceremony postage under $2 across ten mainnets)
G5 independent public-endpoint verification — PASS (ten distinct keyless endpoints)

## The covenant
From this block forward, any of the 1,891 corpus files is provable with: the public repo,
a ~10-sibling inclusion path, and the single on-chain root. Future artifacts join the
mountain as new leaves; future anchors carry only a new peak — the chain stores 32 bytes
forever, the corpus grows without bound. Storage is endless because the anchor never scales.
