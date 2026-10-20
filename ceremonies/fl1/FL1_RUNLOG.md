# FL-1 RUNLOG — THE FRACTAL LEASE (Fractal Tokenization, part 2)

Ceremony FL-1 | 2026-10-20 | Leon GO (chat authorization ~14:34 CT). Prereg sha
9082897f27a86b2a3f8fcb0d2f8360f1952e4ee887b2770ec3a4f132f8653da0 frozen before
broadcast. Scope stamp 19:36:05Z. ALL GATES PASS.

## What is leased
Authority over covenant sat bc1ptgcxdnrqtwees95k7tu6sm7lpceh4qxpsf68zdn87pp4ed95k3hqgrc6m2
(330 sats, ordinal position 0), for a ~59.7-minute window, enforced by Bitcoin
consensus. The fraction never moves. Lease record commits the FT-1 DID
(did:sqdr:ea942df94668c93955fb8792c029a4aa82f6d179) and anchor block 972367.

## Construction executed
1. Fresh leasee wallet P_l = 08d204fe...93dbb (secret gitignored).
2. LEASE record (deterministic JSON) -> LEASE_DIGEST 6248b8e3...2ebf6.
3. FIRST SCRIPT-PATH SPEND ARCHITECTURE in program history (fl1_tapscript.py:
   TapLeaf/TapBranch, BIP342 script sighash, control blocks, local verifier):
   - Leaf A (lease window): PUSH32(LEASE_DIGEST) DROP PUSH32(P_l) CHECKSIG
   - Leaf B (recovery): PUSH3(0x400007) CSV DROP PUSH32(P_satA) CHECKSIG
   - Internal key: NUMS (nonce 0) — key path unspendable; both paths are scripts.
   - Tree root fc87dbef...1410; Q = 5a3066cc...b46e (parity 1).
   - LOCAL SELF-VERIFY BEFORE BROADCAST: leaf A PASS, leaf B PASS (full BIP341/342
     verification: tweak recompute from control block, merkle path, script sighash,
     schnorr). Zero mempool rejections this ceremony.
4. BTC lease tx daf1137c...2147: spends ONLY tank (dd51a797:1, 2670 sats).
   Outputs: lease covenant 330 -> 5120||Q (spk byte-match G2); change 1340 -> SAT-A.
   Fee 1000 sats. CONFIRMED BLOCK 972370. Epoch covenant (1f6d4b53:0) and FT-1 DID
   (dd51a797:0) untouched (G0).
5. XRP ESCROW (native time contract): txid 32D82BE06724A475BF33BEDC2DE43C0EDA5727F918EE654DFEA7A159CA948512,
   validated ledger 107790104, tesSUCCESS, self-escrow 1 XRP, FinishAfter
   1792529539 (20:52:19Z) — consensus-enforced: cannot release before expiry.
   Memo SQDR-FL-1 byte-exact.
6. CARRIER (NEW envelope version byte 0x0B = LEASE carrier): composite digest
   SHA256(LEASE_DIGEST||outpoint) = d854e592...d0a4, XLM ledger 65047855 +
   XRP tesSUCCESS, both byte-exact read-backs (G3), 7s, ~$0.00003.

## Timeline (consensus-enforced)
- ~19:45Z: lease tx confirmed block 972370 — leasee window OPEN.
- ~20:45Z: CSV(7x512s) elapses — owner recovery path ACTIVATES.
- 20:52:19Z: XRP escrow becomes finishable (FinishAfter).
- STAGE 2 (queued, after T): owner recovery spend via leaf B (first real
  script-path spend), EscrowFinish, epoch root update chaining
  SHA256(prev_state||expiry_block_hash), carrier legs, seal 0282.

## Costs
1000 sats (~$0.86) + 1 XRP escrow value (returns via finish) + 20 drops + 200
stroops. Under $0.90 total.

## Honest limitations (from prereg, unchanged)
Leasee window not hard-closed (no upper-bound opcode pre-CTV); post-expiry
first-mover wins; escrow attests, does not hold the sat.

## STAGE 2 — Owner Recovery (executed 2026-10-20, Leon GO chat ~20:10Z re-affirmed 20:45Z)

### Recovery spend (leaf B — first script-path spend in program history)
- Built by fl1_recover.py: spends lease output daf1137c:0 via leaf B, nSequence
  0x400007 (BIP68 time-based CSV), tx nVersion 2, nLockTime = current unix time
  (>= 500000000 REQUIRED by BIP68 for time-based CSV to be enforced — the route
  recipe line "nLockTime = 0" is a recipe defect; 0 would DISABLE the CSV check.
  Recipe amended forward-only on the next fold; recipe never changed mid-ceremony).
- Local full BIP341/342 verification of the BROADCAST witness: control block
  derives covenant Q (5a3066cc...b46e) PASS; schnorr over BIP342 script sighash
  with true nLockTime PASS. Defects caught and fixed PRE-broadcast (never left
  the shop): (a) nLockTime placed before witness in final serialization;
  (b) input-count byte sliced out (stripped[5:-4] instead of stripped[4:-4]).
- Recovery txid 343a9172d50b32ce583a87732dc176ad46ed03d70cc90e74dc3899b6a15bd1d1
  (spk 5120 Q2 = b36b1e74...6f13, 200 sats to owner park key).
- Epoch root update: D2 = SHA256(LEASE_DIGEST || block 972376 hash
  00000000000000000000b184...f738) = b2a198c8...35cb, committed in Q2.
- Broadcast: network rejects pre-MTP ("non-final" as designed — the consensus
  lock itself enforcing the lease). Auto-retry loop from 20:46Z; acceptance
  and block confirmation recorded below when landed.

### XRP EscrowFinish — DEFECT DISCLOSED (epoch-unit error at CREATE)
- EscrowFinish attempts at 20:52Z+ returned tecNO_PERMISSION. Root cause: the
  stage-1 EscrowCreate set FinishAfter = 1792529539 (unix seconds). rippled
  compares against ledger close time in RIPPLE EPOCH (unix - 946684800);
  current close times are ~8458448xx. Effective protocol release time is
  therefore ripple-epoch 1792529539 = 2056-10-20 20:52:19Z (~30 years out).
  No CancelAfter was set, so the 1 XRP self-escrow (index
  8EB4B6E82C264BF526146703EF90006A7EA0316A0E7A3AC3353E2967C171B58D) is
  consensus-locked until then; it cannot be finished or cancelled earlier.
- Impact honestly scoped: the escrow was the ATTTESTATION layer only ("escrow
  attests, does not hold the sat" — prereg limitation unchanged). The
  consensus-enforced lease claim rests on the Bitcoin script path, which is
  unaffected and now proven by this recovery spend. The 1 XRP (~$3) is the
  price of the defect; disclosed, not smoothed. Stage-1 ledger 0281 described
  FinishAfter as "20:52:19Z consensus-enforced release time" — that protocol
  claim is corrected here, forward-only.
- Carrier legs for stage 2 (after BTC confirmation): envelope 0x0B (lease
  lifecycle), composite SHA256(D2||recovery_outpoint) =
  d3ac390ab05822c2bb6c838f6fc7a655ea5ca9f5754e8897e3f7bf06e8637780 on XRP
  + XLM, per the proven stage-1 byte convention.

## STAGE 2 — Build History and Defect Trail (final, supersedes the builds above)

Five build/broadcast attempts, all network-rejected pre-confirmation (no funds ever
at risk; nothing malformed ever entered a block). Every defect disclosed, every
root cause identified and fixed:

1. Build #1 (txid 343a9172...): nLockTime = broadcast-time unix seconds. Node
   rejected "non-final" ~30 times over 22+ min. ROOT CAUSE: BIP113 finality uses
   MTP(tip), which lags wall clock by ~11 blocks (~50 min), so a wall-clock
   nLockTime is always ahead of MTP. BIP68 note: nLockTime must be >= 500000000
   (LOCKTIME_THRESHOLD) for time-based CSV to be enforced — the route recipe's
   "nLockTime = 0" would DISABLE the CSV check entirely. Correct value: exactly
   500000000 (enables BIP68, always final). Recipe defect, forward-only amend.
2. Build #2 (nlt=500000000): node rejected "dust, tx with dust output must be
   0-fee". P2TR dust threshold at 1 sat/vB = 330 sats; a 330-sat input cannot
   fund a non-dust output plus relayable fee. FIX: two-input recovery — added
   the funded BTC writer P2WPKH utxo (e4e3806f:2, 62429 sats) as fee-funding
   input; park output = full 330 sats to Q2, change to writer.
3. Builds #3-4 (txid ef1509b4..., two witness variants): node rejected
   "Invalid Schnorr signature". Local verify passed — because signer and
   verifier shared the same buggy helper. ROOT CAUSE (found by reading the
   FINAL BIP342 spec text): my tapscript SigMsg extension was the OLD 2020
   DRAFT layout "script || leaf_version || key_version || codesep_pos";
   the FINAL ratified extension is "tapleaf_hash (32) || key_version (1) ||
   codesep_pos (4)". First parity-variant attempts (leaf_ver 0xC0 vs 0xC1)
   were both invalid because the layout itself was wrong.
4. Build #5 (txid 4fbdf071d8aa632751bebfdff1fdfb9ba8bb0e1ec9db323072d5fe457f259d3a):
   final-spec sighash, all three local checks PASS (control block derives Q;
   schnorr over BIP342 SigMsg; ECDSA over BIP143 for the fee input).
   BROADCAST ACCEPTED 21:36:59Z into the mempool. First script-path
   (tapscript leaf B) spend in program history, consensus-validated.

Final spend parameters: 2 inputs (lease daf1137c:0 via leaf B, nSequence
0x400007; writer e4e3806f:2), 2 outputs (330 sats -> Q2 park, change to writer),
nVersion 2, nLockTime 500000000, fee 300 sats. Q2 = fb8a6b7bd2ef...02cc,
D2 = SHA256(LEASE_DIGEST || tip hash at build) = a031e61b...ed43.
