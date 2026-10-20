# PREREG FL-1 — THE FRACTAL LEASE: TIME-BOUNDED SATOSHI AUTHORITY (Fractal Tokenization, part 2)

Frozen BEFORE execution (scope stamp 19:36:05Z). Program: SQUIRL OS receipts-first.
Two-key: vetted Gabriel, owner GO (Leon, chat authorization 2026-10-20 ~14:34 CT).

## Claim (scoped)
Authority over a covenant satoshi can be LEASED for an agreed time window without
moving the fraction: the lease is enforced by Bitcoin consensus itself (taproot
script tree + CSV relative timelock), the lease terms are committed inside the
tapscript leaves (thus inside the tweaked output key), and the time contract is
attested on XRP via a native Escrow (FinishAfter) and on Stellar via carrier.
At expiry the owner recovery path activates; the epoch update then chains
prev_state || expiry block hash (stage 2, after T elapses).

## Prior art disclosed (honest)
- Bitcoin covenants/timelock contracts are known (CSV/CLTV, BIP-68/112/113).
- BitVM/Ark-style covenant proposals and CTV (BIP-119) exist but are NOT activated.
- XRP Escrow and Stellar/Soroban smart contracts exist.
NOT claimed: first timelock lease, first covenant, first on-chain contract.
Claimed (scoped): lease-chained fractal ownership — a time-leased covenant sat
whose lease record commits the FT-1 DID + prior block hash, with dual-layer
enforcement (BTC script tree = vault; XRP escrow + Stellar carrier = attested
courtroom), as one deterministic receipts-first ceremony.

## Construction (frozen)
1. FRESH leasee wallet: BIP340 keypair P_l (secret gitignored, never printed).
2. LEASE record (deterministic JSON, sorted keys): {did: FT-1 did:sqdr:ea942df9...,
   leasee_pubkey, owner_pubkey (SAT-A x-only), terms (non-commercial demo),
   window (CSV 7 units x 512s time-based ~= 59.7 min from confirmation),
   anchor_block_hash 000000000000000000017a1f17cc8976688caede4ec1410b3956f2b8a6cbee0e (972367),
   program SQUIRL OS FL-1, version 1} -> LEASE_DIGEST = SHA256(json).
3. TAPSCRIPT TREE (first script-path spend in program history — new library piece):
   - Leaf A (lease window): PUSH32(LEASE_DIGEST) OP_DROP PUSH32(P_l) OP_CHECKSIG
     — leasee sole authority while owner's leaf is locked; commits lease terms.
   - Leaf B (recovery after T): PUSH3(0x400007 CSV-time) OP_CHECKSEQUENCEVERIFY
     OP_DROP PUSH32(P_satA) OP_CHECKSIG — owner reclaim, active only after
     ~59.7 min (7 x 512s) from lease confirmation.
   - Internal key: NUMS point (x = SHA256("SQUIRL-OS-FL1-NUMS-INTERNAL-KEY"),
     even-y lift) — key path deliberately unspendable; both paths are script paths.
   - Root = TapBranch(sorted leaf hashes); Q = NUMS + lift_x(TapTweak(P||root))*G.
4. BTC LEASE TX: spend tank chain only (dd51a797:1, 2670 sats, SAT-A plain key).
   Outputs: (0) lease covenant 330 sats -> spk 5120||Q; (1) change -> SAT-A plain.
   Epoch covenant sat and FT-1 DID sat are NOT inputs (G0).
5. XRP ESCROW (native time contract): EscrowCreate from the rails XRP writer,
   self-destination, FinishAfter = lease expiry unix, memo tag SQDR-FL-1 with
   LEASE_DIGEST — escrow CANNOT release before FinishAfter (consensus-enforced).
   EscrowFinish executes at expiry (stage 2).
6. CARRIER: envelope version byte 0x0B (NEW: LEASE carrier) + composite digest
   SHA256(LEASE_DIGEST||outpoint_internal), XLM + XRP, tag SQDR-FL-1.
7. LOCAL SELF-VERIFY BEFORE BROADCAST: full BIP341 script-path verification
   (tweak from control block, merkle path check, BIP342 sighash, schnorr verify).

## Gates
- G0: epoch + DID covenants untouched (input list = tank only).
- G1: LEASE_DIGEST recomputes from public lease record; anchor block hash real.
- G2: spk byte-matches Q; leaf/branch hashes recompute; local verify PASSes before
  broadcast; mempool accepts (rejection = defect, fix, disclose, rebroadcast).
- G3: escrow validated with correct FinishAfter; carrier legs byte-exact.
- G4: no key material in any artifact.

## Honest limitations (disclosed)
- The leasee window is not hard-closed on-chain at expiry (CLTV gives no upper
  bound; no such opcode pre-CTV). Owner recovery activates at T; post-expiry the
  first-mover wins. During the window the leasee's exclusivity IS consensus-forced
  (owner CSV-locked). Real-world leases would add 2-of-2 co-spend in the window.
- XRP escrow holds attestation value, not the sat; the sat never moves (fractal
  doctrine: the fraction stays, the authority leases).
- Stage 2 (recovery spend + epoch root update chaining expiry block hash) executes
  only after T elapses; a separate seal receipts it.

## Intended artifacts
FL-1 runlog + ledger 0281; route recipe routes/FL1_FRACTAL_LEASE_ROUTE.md; stage-2
recovery queued. Paper part 2 (Fractal Leases) staged for Leon's publish GO.
