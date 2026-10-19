# THE MULTI-RAIL INSCRIPTION PLAYBOOK v1.0
### SQUIRL OS Technologies — compiled from all successful ceremonies DWR-1 → XTR-1 (Oct 18-19, 2026)

This is the operator playbook for every rail we have proven on mainnet. Doctrine first, then per-rail playbooks with the exact traps we hit and the exact fixes. Forward-only; update on each new lesson.

## 0. Standing Doctrine (applies to every rail)

1. **Hash-only, zero-token:** only a SHA-256 digest (32 bytes) ever touches a chain. No tokens minted, no custody taken, documents live in the vault. Prefix standard: `SQDR` + version byte (`0x01` DWR … `0x03` PWR/IR) + digest.
2. **Gates G1–G5:** G1 spec+prereg frozen and committed pre-broadcast → G2 offline build+sign → G3 broadcast (back-to-back or sequential per protocol) → G4 keyless read-backs byte-exact → G5 ledger+receipts sealed. No gate may be skipped.
3. **Canonical identifiers of record (ledger 0228/0237 lesson):** the id of record is what a keyless explorer returns. BTC: canonical txid = dsha(serialization WITHOUT witness); the witness-serialized hash is the wtxid, never the id of record. XRPL: sha512-half of `54584E00`+blob. Cardano: blake2b256 of tx body. Verify every id against a public explorer before writing the ledger entry.
4. **Retries are disclosed, forward-only:** rejected fees, stale sequences, underfunded ops — repair, disclose in the ledger, never rewrite history.
5. **Key hygiene:** writer keys live locally in the rail folder, gitignored BY PATTERN (`*_writer_key*.json`), and audited with `git ls-files | grep -i key` before every push. Zero keys tracked, ever.
6. **Authorization is recorded as `Leon GO (chat authorization, <date/time>)`** — no operator quotes in any public artifact (operator-privacy rule).
7. **Every public artifact carries:** MEASURED (scoped) footer with program benchmark DOI 10.5281/zenodo.23321637, POL-DISC-001 reference, and the prototype disclaimer.

## 1. Bitcoin (anchor rail, canonical ID of record)

- **Writer:** segwit P2WPKH, BIP143 signing, hand-rolled low-S normalization. Fee targeting 1-2 sat/vB (~700-1,300 sats/leg).
- **Inscription:** OP_RETURN output (value 0). **Custody:** P2WPKH-to-P2WPKH change/transfer, dust guard active (guard fired in DGPNM: enforce ≥ 546 sats + fee).
- **TRAP (twice):** local hash of the witness-serialized tx = wtxid, not the canonical txid. Always `tx.wit = CTxWitness()` (empty) before hashing, or take the explorer-returned id.
- **TRAP:** spending an unconfirmed parent is legal (chained broadcast) — disclose it; the pair confirms together.
- **Speed (measured 2026-10-19):** minutes to hours to confirm; block ~10 min. Use as permanence anchor, never for speed.

## 2. XRP Ledger (speed rail — the transfer rail)

- **Writer:** seed → Wallet; Sequence from `account_info` (precompute consecutive seqs for chains: sender N, N+1, …).
- **Inscription (zero-movement):** `AccountSet` + Memo (memo_type=tag, memo_data=digest.hex). **Transfer/custody:** `Payment` 700,000 drops standard hop; flat fee 10 drops regardless of size.
- **Txid:** sha512("54584E00"+blob)[:32].upper().
- **Speed record (XTR-1, 2026-10-19):** acceptance 0.30s avg, validated finality 5.3-8.0s/hop, 5-hop custody chain 35.45s total, 50 drops (~$0.003). Ledger closes ~3-4s. Fastest rail in the family and cheapest per custody hop.
- **TRAP:** a chain of hops from the same account must strictly increment its own sequence; fetch both accounts' next seq before building.
- **TRAP:** mempool/ledger truncation bugs in downstream UIs — always write FULL 64-char hashes into receipts, cards, and ledgers (ledger 0237 lesson: verify char-for-char before sealing).

## 3. Stellar (cheap data rail, named ledger entries)

- **Writer:** Keypair.from_secret; sequence is a huge int fetched from Horizon account read (never hand-write it).
- **Inscription (zero-movement):** `ManageData` op — data_name="CEREMONY-ID", data_value=digest bytes; readable permanently on the account itself. 100 stroops fee + 0.5 XLM data-entry reserve (retained, refundable).
- **Inscription (payment-carried):** memo_hash on a Payment — established pre-ManageData pattern.
- **TRAPS (XCF-1):** (a) `op_underfunded` — account reserve is 1 XLM base; size payments to leave reserve intact (18.5 XLM worked where 19.5 failed); (b) stale sequence after a failed tx — re-fetch sequence before every retry; failed tx consumes a sequence + 100 stroops.

## 4. Cardano (metadata rail, structured on-chain records)

- **Writer:** payment key only (Ed25519 via nacl; secret stored CBOR-encoded), raw CBOR tx construction (canonical=True throughout).
- **Inscription:** tx metadata label **1968**, map {"PWR": id, "RAIL": n, "DIGEST": hex}. Carry on a self-transfer (value returns to sender, only fee leaves).
- **Txid:** blake2b256(tx body). Submit via Koios `/submittx` (application/cbor).
- **TRAPS:** (a) fee minimums are 1-lovelace strict and output-count-dependent (170,957 for 2-out, 171,001 for 1-out, same day) — quote min from the rejection or precompute; margin of +1,000 lovelace is cheap insurance; (b) pycardano's default era encoding (Alonzo/tag-259) is rejected by current Conway nodes — build the raw 4-element CBOR array `[body, witness_set, aux_valid, aux]`.
- **Speed (measured 2026-10-19):** ~20-40s/leg to metadata visibility; block ~30s era.

## 5. Ethereum (newest rail — pure calldata, dirt cheap)

- **Writer:** secp256k1 + keccak256; EIP-55 checksummed address (verify before funding). Sign with eth-account (`Account.sign_transaction`); no eth-keys libraries needed beyond pip install.
- **Inscription (zero-movement):** legacy EIP-155 tx, `to` = own address, `value` = 0, `data` = SQDR+0x03+digest. Nonce from `eth_getTransactionCount`.
- **Cost (measured PWR-1, 2026-10-19):** gasUsed 22,480 at 0.4 gwei ≈ $0.01. Gas price is near-floor in this era — check `eth_gasPrice` and set with margin; legacy txs (fixed gasPrice) simplest.
- **RPC notes:** publicnode, flashbots, drpc all worked keyless; llamarpc/ankr 403'd our UA; blockscout's account API returned garbage balance once — always cross-check via ≥2 RPCs before declaring a funding failure.
- **Speed:** block ~12-15s; inscription visible with receipt in one block.

## 6. Cross-rail comparison table (all measured same day, 2026-10-19)

| Rail | Finality (measured) | Cost/leg | Best at |
|------|--------------------|----------|---------|
| XRP Ledger | 5.3-8.0s (accept 0.3s) | 10 drops (~$0.002) | transfer rail, speed |
| Stellar | ~5-8s | 100 stroops (~$0.00003) | cheap named data entries |
| Ethereum | 12-15s | ~22.5k gas (~$0.01) | cheap calldata, smart-contract composability |
| Cardano | 20-40s | ~171k lovelace (~$0.05) | structured metadata |
| Bitcoin | minutes-hours | 700-1,300 sats (~$0.10) | permanence anchor, canonical ID |

## 7. Ceremony checklist (copy per run)

1. Write spec (self-referential artifact rides its own digest) → freeze sha256 → prereg with wallet roster, ids-to-be, cost ceiling, gates → commit (G1).
2. Build + sign ALL legs offline; precompute ids; verify addresses/keys locally (G2).
3. Broadcast per protocol (back-to-back or sequential); capture engine results and rejections verbatim (G3).
4. Read back KEYLESS from public explorers: byte-exact digest, direction, amount, and canonical id; verify ledger-typed ids char-for-char (G4).
5. Ledger entry (full ids, all retries disclosed, speeds, costs) + receipts → commit → optional DOI via two-key gate (G5).

This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.
