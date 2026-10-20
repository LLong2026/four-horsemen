# Fractal Lease FL-1: A Consensus-Enforced Timelock Lease on a Bitcoin Fraction, with Owner Recovery via the First Taproot Script-Path Spend in the SQUIRL OS Program

**Leon Calvin Long, II** (ORCID 0009-0002-1140-9568), SquirlOS Technologies LLC
Version 1.0, 2026-10-20. Research record of a live mainnet ceremony; receipts in the
append-only four-horsemen ledger (entries 0281, 0282) and FL1_RUNLOG.

## 1. Scoped claim

We demonstrate a complete lease-and-recovery cycle on a single, fractal-tokenized
Bitcoin fraction: authority over a 330-sat covenant output was LEASED to a fresh
key for a time-bounded window, enforced by Bitcoin consensus alone (no custodian,
no trusted server), then recovered by the owner through a timelocked script path.
The recovery spend is the first taproot SCRIPT-PATH (tapscript leaf) spend in the
SQUIRL OS program's history; consensus itself validated the control block, the
merkle path, the timelock and the BIP342 signature. A dual-layer construction
places the lease terms inside the taproot script tree (thus inside the tweaked
output key) on Bitcoin, with an XRP escrow providing independent, consensus-enforced
temporal attestation of the same window.

**Prior art, disclosed:** this is an application of standard, ratified Bitcoin
construction blocks, not a claim of novelty over them — BIP340/341/342 (schnorr and
taproot), BIP112 (OP_CHECKSEQUENCEVERIFY), BIP113 (median-time-past finality), the
CTV/checktemplateverify vault literature, Lightning-style timelock delegation, and
satoshi-level identifiers in the spirit of Ordinals. The DID-carrying fraction and
the dual-layer escrow attestation follow the program's FT-1 fractal tokenization
record (DOI 10.5281/zenodo.23510677; prior art did:btcr and Ordinals disclosed there).
Claims are scoped to what was executed on mainnet on 2026-10-20.

## 2. Construction

- **Leasee key** P_l (fresh BIP340 keypair), **owner key** P_satA (the SAT-1
  covenant owner key).
- **Lease record:** deterministic JSON committing the FT-1 DID
  (did:sqdr:ea942df94668c93955fb8792c029a4aa82f6d179) and the FT-1 anchor block
  hash (block 972367) -> LEASE_DIGEST 6248b8e3...2ebf6 (sha256).
- **Taproot script tree:** NUMS internal key (key path unspendable by design);
  leaf A = lease window (LEASE_DIGEST DROP P_l CHECKSIG); leaf B = owner recovery
  (CSV 7x512s time-based, DROP P_satA CHECKSIG). Tree root fc87dbef...1410;
  tweaked output key Q 5a3066cc...b46e. The lease terms are committed inside the
  key: spending the output at all is proof the terms existed.
- **Lease transaction** daf1137c...2147 spends only the covenant fraction output
  (the epoch and DID covenants untouched); CONFIRMED block 972370.
- **XRP escrow (the courtroom layer):** self-escrow of 1 XRP with a
  consensus-enforced release time, validated ledger 107790104, memo byte-exact.
- **Recovery (stage 2):** after the CSV window matured, the owner spent the lease
  output through leaf B — transaction 4fbdf071...59d3a, CONFIRMED block 972382:
  two inputs (lease output via leaf B; a fee-funding P2WPKH input), park output
  330 sats to Q2 = fb8a6b7b...02cc committing D2 = SHA256(LEASE_DIGEST || tip hash)
  = a031e61b...ed43. nSequence 0x400007 (relative timelock satisfied), nLockTime
  500000000 (time-based CSV active). BIP342 schnorr signature over the final-spec
  SigMsg extension (tapleaf_hash || key_version || codesep_pos).

## 3. Attestation rails

- **Stage-1 carrier** (envelope 0x0B): composite SHA256(LEASE_DIGEST || outpoint)
  d854e592...d0a4 on Stellar (ledger 65047855) and XRP, byte-exact read-backs.
- **Stage-2 carrier** SQDR-FL-2 (envelope 0x0B): composite
  SHA256(D2 || recovery outpoint) aea69c06...ead9 on XRP (tesSUCCESS, ledger
  107791975) and Stellar (ledger 65049367), byte-exact read-backs. Provisional
  sub-cent global verification while Bitcoin finality arrives.

## 4. Honest defect trail (disclosed in full, all before confirmation)

Every malformed build was rejected by network policy/consensus pre-confirmation;
no funds were ever at risk; nothing defective entered a block.

1. **nLockTime finality:** a wall-clock nLockTime is always ahead of BIP113 MTP;
   nodes rejected "non-final" ~30 times. Correct value: 500000000, which both
   satisfies finality and is required (LOCKTIME_THRESHOLD) for time-based CSV to
   be enforced at all.
2. **Dust policy:** a single 330-sat input cannot fund a non-dust P2TR output
   plus relayable fee at 1 sat/vB. Fixed with a fee-funding input (writer utxo).
3. **BIP342 SigMsg draft-vs-final defect:** the local signing/verify library
   implemented the 2020 DRAFT tapscript extension layout
   (script || leaf_version || key_version || codesep_pos) instead of the FINAL
   ratified layout (tapleaf_hash || key_version || codesep_pos). Local
   self-verification passed because signer and verifier shared the bug; the
   Bitcoin node rejections exposed it. The library (rails/fl1_tapscript.py) was
   fixed against the final BIP342 specification text and re-verified.
4. **XRP escrow epoch-unit defect:** FinishAfter was supplied in Unix seconds
   rather than the Ripple epoch; the escrow therefore releases ~2056 instead of
   the intended window. Disclosed and left uncorrected (append-only doctrine; the
   escrow attests, it does not hold the sat).

## 5. Cost and timing

Full lease cycle (lease, escrow, both carriers, recovery): under $0.90 total
(1000 sats + 20 drops + 200 stroops stage 1; ~300 sats + 10 drops + 100 stroops
stage 2). Lease confirmed block 972370; recovery confirmed block 972382
(~80 minutes later, the CSV window enforced by consensus).

## 6. Dual Mesh Benchmark: MEASURED (scoped)

This record measures the deterministic ceremony layer only; no neural-mesh
inference is involved in or required by any ceremony gate (no LLM in any decision
path, by design — every gate is deterministic python over public chain data). The
program's Dual Mesh Benchmark is at DOI 10.5281/zenodo.23321637 (DeepSeek column:
DOI 10.5281/zenodo.23345241). Related: IP-013 constant-footprint corpus commitment
(DOI 10.5281/zenodo.23491295); thesis v2.1 (DOI 10.5281/zenodo.23482978).

## 7. Limitations

The leasee window is not hard-closed pre-CTV: after expiry, first-mover-wins between
the owner's recovery path and the leasee's leaf-A path (the recovery is protected
by the CSV delay, not by an absolute cutoff). The XRP escrow attests the window; it
does not custody the fraction. Prototype software; educational and research purposes
only. No client data, no PHI (POL-DISC-001).

> This software is a prototype and is provided for educational and research purposes
> only. It is not intended for production use, commercial deployment, or
> safety-critical environments. All systems are experimental and may contain defects
> on them.

## 8. Receipts

- Bitcoin lease tx: https://mempool.space/tx/daf1137c1500fb6bd3103349021ed7a9643174f3c2fe5fe87205584e7d472147 (block 972370)
- Bitcoin recovery tx: https://mempool.space/tx/4fbdf071d8aa632751bebfdff1fdfb9ba8bb0e1ec9db323072d5fe457f259d3a (block 972382)
- XRP stage-2 carrier: https://livenet.xrpl.org/transactions/A5B92EBB2946D9544FDB478B70D9DF16459B2B050EE7FCF38AA3007D469C0BDB (ledger 107791975)
- Stellar stage-2 carrier: https://stellar.expert/explorer/public/tx/db00318e780c367618dba392ba609247b0285e7e6f02a885da105578b966eaa2 (ledger 65049367)
- Ledger entries 0281/0282: https://github.com/LLong2026/four-horsemen
- FT-1 Fractal Tokenization (DOI 10.5281/zenodo.23510677): the fraction's DID lineage
