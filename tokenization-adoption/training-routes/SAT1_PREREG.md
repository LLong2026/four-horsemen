# SAT-1 PREREGISTRATION — THE SATOSHI COVENANT (value-carrying root commitment on BTC mainnet)
Frozen BEFORE any broadcast. 2026-10-20 ~01:45 CT. Leon GO (chat authorization, 2026-10-20 ~01:36 CT).

## What the ceremony proves
Prior ceremonies (CFR-9, MCR-1, MCR-2) committed roots in 0-value OP_RETURN envelopes: data
next to coins, never inside one. SAT-1 commits the MCR-2 mountain root INSIDE value: a
330-sat output (the smallest relayable P2TR output — the 1-sat ideal is blocked by the
330-sat P2TR dust floor, disclosed here) whose taproot OUTPUT KEY commits the root via
BIP341 taptweak. The first satoshi of that output is the covenant sat. The output is then
transferred back and forth between two fresh program writer wallets (SAT-A -> SAT-B ->
SAT-A), the root re-committed in the tweaked key at EVERY hop — proving the commitment
travels with the coin, wallet-agnostic, value-carrying. Companion anchors on XRP (memo)
and Stellar (manage_data) bind the same root to the satoshi ceremony — cross-rail
agnosticism: the same 32 bytes ride a value rail (BTC), a transport rail (XLM), and a
memo rail (XRP).

## Frozen commitment
MMR-2 ROOT (parent covenant, already 10-rail anchored 2026-10-20, ledger 0265):
1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60

## Construction (deterministic, BIP86-style key path only, no script tree, no OP_RETURN)
- taptweak: t = SHA256( tagged_hash("TapTweak") || x_only(internal_pubkey) || root )
  output_key Q = internal_pubkey + t*G  (x-only; parity per BIP341 rules)
- covenant output: value 330 sats, scriptPubKey = OP_1 0x20 <Q_x>  (v1 witness program)
- fee tank: separate output (10,000 sats at fund) to the holder's PLAIN P2TR key; each
  hop spends covenant UTXO + tank, re-commits covenant (330 sats) + tank-minus-fee
- SIGHASH_ALL (0x01), 65-byte schnorr sigs, key-path spends only
- Implementation: pure-Python BIP340/BIP341, validated pre-broadcast against the
  OFFICIAL BIP340 test vectors (all must pass — gate G1) and BIP86 taptweak vectors (G1b)

## Wallets (all program-controlled, fresh, WIFs never committed)
- SAT-A, SAT-B: fresh secp256k1 keys generated this ceremony
- Funder: the certified program BTC segwit writer (bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6)

## Transaction plan
1. FUND:  writer P2WPKH -> covenant 330 sats (tweak root, SAT-A) + tank 10,000 sats
          (SAT-A plain) + change (writer)
2. HOP-1: SAT-A -> SAT-B (covenant re-tweaked 330 + tank-minus-fee)   [there]
3. HOP-2: SAT-B -> SAT-A (covenant re-tweaked 330 + tank-minus-fee)   [back]
Companion legs (same session): XRP MemoType "SQDR-SAT-1" (envelope SQDR+0x07+root);
Stellar manage_data "SQDR-SAT-1" (same envelope). Version byte 0x07 = satoshi covenant
(registered forward-only; MCR-2 used 0x06).

## Gate checks (deterministic, no LLM in the decision path)
G1:  pure-python BIP340 impl passes ALL official BIP340 test vectors
G1b: taptweak matches BIP86 reference vectors
G2:  prereg + scope stamp sat1_satoshi_covenant_2026-10-20 before first broadcast
G3:  keyless verification of every hop: recompute Q from published pubkey + root, byte-
     match to on-chain scriptPubKey; covenant value exactly 330 sats at every hop
G4:  all fees recorded; failures disclosed forward-only
G5:  prior-art disclosure: taproot-tweak data commitments are a known technique
     (Opt-In Auditability thesis, Taproot Assets); ordinal inscriptions commit via
     witness, not output key. Claim scoped as: first satoshi covenant under this
     program — value-carrying, hop-portable, cross-rail-bound mountain root. No global
     first-ever claim is made.

## Honest scope statements
- "The satoshi" = the first satoshi (ordinal position 0) of the 330-sat covenant output;
  a literal 1-sat output cannot relay (dust floor disclosed above). The root commits in
  the output key, not the sat itself — the sat is the value carrier.
- Anchor doctrine language applies (ledger 0244): this is value-carrying anchoring,
  not tokenization, in all public artifacts.
- Wallets are program writer wallets (both sides of every transfer) — the back-and-forth
  proves commitment portability under program custody, not third-party transfer.
- Prototype disclaimer applies. Dual Mesh Benchmark: NOT MEASURED (deterministic
  ceremony, no neural-mesh inference).
- Operator privacy: authorization recorded as Leon GO (chat authorization, 2026-10-20
  ~01:36 CT); no operator text quoted.
