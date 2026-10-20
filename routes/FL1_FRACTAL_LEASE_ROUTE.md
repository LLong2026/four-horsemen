# ROUTE: FL-1 — FRACTAL LEASE (TIME-BOUNDED SATOSHI AUTHORITY) — LOCKED RECIPE

Proven 2026-10-20, block 972370, ledger 0281. First script-path (tapscript) spend
architecture in program history. ~$0.90 all-in. Epoch + prior covenant sats untouched.

## Frozen recipe
1. Lease record (deterministic JSON: DID, leasee/owner keys, terms, window,
   anchor block hash) -> LEASE_DIGEST = SHA256(json).
2. Tapscript tree (rails/fl1_tapscript.py — TapLeaf/TapBranch, BIP342 script
   sighash, control block builder, FULL local verifier):
   - Leaf A: PUSH32(LEASE_DIGEST) OP_DROP PUSH32(P_leasee) OP_CHECKSIG
   - Leaf B: PUSH3(0x400007) OP_CHECKSEQUENCEVERIFY OP_DROP PUSH32(P_owner) OP_CHECKSIG
   - NUMS internal key (key path unspendable). Root = TapBranch(sorted leaves).
3. ALWAYS self-verify both leaves locally (verify_script_path_spend) BEFORE
   broadcast — zero mempool rejections when this passes.
4. Lease tx: spend tank chain only; outputs 330 -> 5120||Q + change. CSV window
   opens at confirmation; owner recovery after 7 x 512s.
5. XRP EscrowCreate (self, FinishAfter = expiry + margin) with SQDR-FL-N memo.
6. Carrier envelope version 0x0B (LEASE carrier): SHA256(LEASE_DIGEST||outpoint).
7. Stage 2 after T: recovery spend via leaf B (nSequence = 0x400007, tx version
   >= 2), EscrowFinish, epoch update chaining SHA256(prev_state||block_hash).

## Registry additions
- Envelope version 0x0B = LEASE carrier. Registry: 0x07 root, 0x08 covenant,
  0x09 system direct, 0x0A DID, 0x0B lease.
- Recovery spend REQUIRES: input nSequence = 0x400007 (time-flag + 7), tx nVersion
  = 2, nLockTime = 0. Witness: [sig65, leafB_script, control_block].
