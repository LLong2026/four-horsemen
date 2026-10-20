# SAT-2 PREREGISTRATION — THE MOUNTAIN GROWS (covenant root update in place)
Frozen BEFORE any broadcast. 2026-10-20 ~07:05 UTC (02:05 CT). Leon GO (chat authorization, 2026-10-20 ~02:01 CT).

## What the ceremony proves
SAT-1 proved a satoshi can CARRY a mountain root and move between wallets with the
commitment intact. SAT-2 proves the commitment is UPDATABLE IN PLACE: the mountain grew
(append-only: +14 leaves, 1 expected ledger leaf change, 0 missing), and the SAME
satoshi lineage — still 330 sats, still the covenant output — is re-committed to the
NEW root in one transaction, without breaking the coin's history. The satoshi's job
description updates; the coin lineage never breaks.

## Frozen values
- OLD ROOT (SAT-1 covenant, MCR-2): 1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60
- NEW ROOT (SAT-2 target, corpus at commit 03214b5): 267f13b0088c2bb82addf7358e4c50cf7c1e1fc7023be00e1194149bb56f34bf
- NEW MOUNTAIN: 1,920 leaves (was 1,906), 4 peaks
- REPRODUCTION GATE (G0): builder rerun over corpus bf13210 reproduces the MCR-2 root
  1929707e...cccb60 and all 7 peaks byte-exact — the recipe is provably the original
- APPEND-ONLY GATE (G0b): 0 files missing; exactly 1 changed leaf = LEDGER.md
  (append-only ledger growth, disclosed); 14 added leaves = MCR-2 + SAT-1 ceremony
  records; MCR-2 peaks at heights 9 and 8 byte-identical in the new build (1,536
  original leaves provably untouched)
- Envelope: SQDR + 0x07 (satoshi covenant) + NEW root; companion tag SQDR-SAT-2
  (forward-only registration; SAT-1 used tag SQDR-SAT-1)

## Construction (identical to SAT-1, only the root changes)
- taptweak: t = SHA256(tagged TapTweak || internal_key_xonly || NEW ROOT); Q = P + tG
- covenant output: 330 sats, OP_1 0x20 <Q_x>, key-path only, SIGHASH_ALL
- UPDATE TX: SAT-A spends [covenant UTXO d261810c...399:0 (old-root tweak) +
  tank d261810c...399:1 (6,000, plain)] -> [covenant 330 sats tweaked with NEW root,
  parked at SAT-A] + [tank minus fee, SAT-A plain]
- Inputs are signed with the OLD-root effective secret (that is what the UTXOs commit);
  the OUTPUT commits the NEW root — the update is the tx itself

## Gate checks (deterministic, no LLM in the decision path)
G0:  byte-exact reproduction of the MCR-2 root at bf13210 before building the new one
G0b: append-only leaf diff (0 missing / 1 expected ledger change / 14 growth)
G1:  pure-Python BIP340/341 library (already validated 26/26 official vectors + BIP86
     during SAT-1; unchanged code path)
G2:  prereg + scope stamp sat2_mountain_grows_2026-10-20 before first broadcast
G3:  keyless verification: new covenant output recomputes from published SAT-A pubkey +
     NEW root, byte-matches on-chain scriptPubKey; value exactly 330 sats; old covenant
     UTXO provably spent by the update tx
G4:  all fees recorded; failures disclosed forward-only
G5:  claim scoping (unchanged from SAT-1): first under this program; no global
     first-ever claim; prior art disclosed (taproot-tweak commitments known technique)

## Honest scope statements
- The covenant sat remains ordinal position 0 of a 330-sat output (dust floor disclosed
  in SAT-1; a literal 1-sat output cannot relay)
- Anchor doctrine language applies (ledger 0244): value-carrying anchoring
- Wallets are program writer wallets; the update proves commitment upgradability under
  program custody
- Prototype disclaimer applies. Dual Mesh Benchmark: NOT MEASURED (deterministic
  ceremony, no neural-mesh inference).
- Operator privacy: authorization recorded as Leon GO (chat authorization, 2026-10-20
  ~02:01 CT); no operator text quoted.
