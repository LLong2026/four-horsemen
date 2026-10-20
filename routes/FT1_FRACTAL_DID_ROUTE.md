# ROUTE: FT-1 — SATOSHI-NATIVE DID (FRACTAL CLAIM) — LOCKED RECIPE

Proven 2026-10-20, block 972367, ledger 0279. Deterministic, keyless, ~$0.84 all-in.
NOTE: this route does NOT touch the epoch covenant sat — it spends the tank only.

## Frozen recipe (byte-level)
1. **Wallets** (verification methods, all fresh, secrets gitignored):
   - BTC sat_c: 32-byte secret -> BIP340 pubkey P_c (sat1_bip340.pubkey_gen)
   - XRP: xrpl.core.keypairs.generate_seed() -> derive_keypair -> classic address
   - XLM: stellar_sdk Keypair.random()
2. **DID core** (outpoint-free, deterministic): JSON sorted keys, separators (",",":")
   {doctrine, fractal_claim, keys{btc,xrp,xlm}, method:"did:sqdr", program, version:1}
   -> DID_CORE_DIGEST = SHA256(core_json)
3. **BTC covenant tx** (mirror sat2_update.py construction EXACTLY):
   - Input: tank UTXO only (plain SAT-A key; taptweak_secret(sk, b""))
   - Output 0: 330 sats -> Q_c = taptweak(P_c, DID_CORE_DIGEST), spk = 5120||Q_c
   - Output 1: tank change -> SAT-A plain key. Fee 1000 sats.
   - Sign: bip341_sighash_all(nVersion=2, nLockTime=0, ins, outs, 0) + bip340_sign
   - **PITFALL (bit us once, disclosed): first arg of bip341_sighash_all is
     nVersion (2), NOT input count. Signing with 1 = invalid Schnorr, mempool
     rejects. Fix and rebroadcast.**
   - Broadcast: POST raw hex to mempool.space/api/tx. Claimed sat = ordinal
     position 0 of output 0.
4. **DID identifier** (keyless): did:sqdr:SHA256(outpoint_internal(36B) || P_c)[:40]
5. **Carrier legs** (envelope version byte 0x0A = DID carrier, NEW in registry):
   SQDR + 0x0A + DID_CORE_DIGEST (37 bytes total), tag SQDR-FT-N
   rails/squirrel_rails.py carrier SQDR-FT-N <hex> (XRP AccountSet memo + XLM
   manage_data, ~6s, ~$0.00003)
6. **Gates**: G0 epoch covenant untouched (input list = tank only) | G1 digest
   recomputes from public doc | G2 on-chain spk byte-matches tweaked key |
   G3 both rails byte-exact | G4 no key material in any artifact.

## Registry additions (this route)
- Envelope version 0x0A = DID carrier (SQDR envelope registry).
- did:sqdr method: identifier = SHA256(outpoint_internal || P_c)[:40]; DID
  document = core doc + post-confirmation outpoint/block.

## Cost & timing (measured, scoped)
- BTC: 1000 sats fee @ 6.48 sat/vB, confirmed next block (watch mempool feerate;
  fire when fastestFee < fee rate). Carrier: 6.1s. Total under $0.84.
- The DID is durable as long as the output is unspent; moving the sat requires
  re-tweak (same doctrine as the SAT-2 in-place update).
