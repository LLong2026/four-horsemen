# HAND-1 RUNLOG — THE HANDOVER RING

Ceremony HAND-1 | 2026-10-20 | Leon GO (chat authorization ~14:50 CT). Prereg sha
64c22a6ddc8d9f9340e8c43d778c467f8b5da91df7418b18f449119dd755baa8 frozen before
broadcast (stamp 19:51:18Z, tip 00000000...4a719cc).

## What was demonstrated
Global fraction ownership transfer AND return: covenant authority passed
hand-to-hand across the owner's wallet ring on Bitcoin (real on-chain ownership
changes), visibly relayed through his XRP and Stellar wallets, returned home,
with the epoch merkle root updated and committed at the moment of return.
This is the standing demo answer to "how does a fraction change hands and come
back?" — deterministic, replayable, receipts-first.

## Construction executed
1. MMR RE-FOLD: 1,992 leaves -> NEW_ROOT 88903202273adeba0f411529abbd522fd2c1f1
   83f7d0b688e9f1b32ce2c9bd4 (G1: reproduces from public corpus).
2. HANDOVER_RECORD (deterministic JSON; ring, purpose, NEW_ROOT, anchor block
   hash) -> HANDOVER_DIGEST 0b16140928d34d357967485b2bbd2080745d4b344a435bcbd6
   ef04b34bef2c14.
3. BTC AUTHORITY RING (taproot key-path, SAT-1 machinery; funding leg BIP143
   P2WPKH via proven custody_transfer machinery):
   - H0 fund 2be120b34c0d0595d5931c6f778737c444436d109438ba0fcdf8caf63ecc9e57
     (segwit writer -> 2670 sats covenant at tweak(P_satA, D); change 31425 home)
   - H1 SAT-A->SAT-B dbb5b3b38112a894dd78da655beccdc39824db51419a0fd5a85b7f6457773fe4
   - H2 SAT-B->SAT-C a650601c8c8ed8d249c5c972607d135dba107f427d9802f2554a55bc5aff8713
   - H3 SAT-C->SAT-A RETURN a4a4041b7d17637a748148390cc63793c16c72045aec30dc046ade915db2bd00
     (final spk = tweak(P_satA, D): the returned covenant commits the NEW_ROOT)
   Same digest re-committed under each successive owner key: the transfer IS the
   key change; the payload rides unchanged.
4. XRP HANDOVER RELAY: writer rBbxYuBk... -> DID wallet r9p4qq... (1 XRP, created
   the account, ledger 107790346, memo SQDR-HAND-1 byte-exact), return 0.9999 XRP
   ledger 107790359 (memo SQDR-HAND-1R byte-exact). DID wallet retains 1.00007
   XRP (account reserve).
5. XLM HANDOVER RELAY: writer GDIQGGTU... -> DID wallet GDDMXP... (create 1 XLM,
   ledger 65048107, memo SQDR-HAND-1), return 0.9 XLM ledger 65048176 (memo
   SQDR-HAND-1R). DID wallet retains ~1.1 XLM (reserve).
6. EPOCH ROOT ANCHOR (fast lane): envelope 0x07 + NEW_ROOT on XRP (txid
   613AFCD21247E092A0E9E6F7E85551ABBEF05059970B42F54D634A8766CE956F, tesSUCCESS)
   and XLM (data entry SQDR-HAND-1-ROOT, ledger 65048182), both byte-exact (G3).
7. CARRIER: composite SHA256(HANDOVER_DIGEST || H3 outpoint) 494b1c91fb04c8fbf4
   0546ea60993802b4c4b2e17522fa0ec5f96a00596348a7 on the XRP relay memos
   (envelope 0x08 covenant carrier), byte-exact.

## Gates
- G0: epoch covenant (1f6d4b53:0), FT-1 DID sat (dd51a797:0), FL-1 lease sat
  (daf1137c:0) untouched. PASS.
- G1: NEW_ROOT reproduces from corpus fold (sat2_mmr machinery). PASS.
- G2: every hop spk byte-matches its announced tweak (H0 verified on-chain;
  H1-H3 chained inputs accepted by mempool = key-path verification by consensus).
- G3: all relay/anchor read-backs byte-exact. PASS.
- G4: no key material in any artifact. PASS.

## Defects encountered and disclosed (the honest engineering log)
1. H0 local txid computation diverged from the broadcast txid (manual stripped
   serialization vs library serialization). First H1-H3 builds referenced a
   nonexistent outpoint and were rejected by the mempool (no funds moved, no
   harm). Fixed by adopting the broadcast txid as authoritative and rebuilding.
2. XRP return leg initially failed tecUNFUNDED_PAYMENT: the DID wallet was a
   fresh account whose entire 1 XRP first hop became the account RESERVE.
   Fixed with a top-up; return executed at 0.9999.
3. XLM return initially failed op_underfunded repeatedly: Stellar's basic-
   account reserve is (2 + subentries) x base = 1.0 XLM (not 0.5). A dust probe
   isolated the true cause; failed attempts each charged 100 stroops (fees on
   failed txs). Fixed via top-up + 0.9 XLM return.
4. An unsolicited 0.0001 XLM credit arrived at the DID XLM wallet from
   GDIQ4JOS7T4VDBYDYSPOAER323KF2BHFWD4OUAMO2NROVGBJKHTWVLT5 carrying a matching
   SQDR-HAND-1 memo at ledger 65048109 (before any public mention). Attributed
   to the bash retry mechanism re-executing an earlier script variant (writer
   key B hypothesis) — not fully resolved, harmless, left on record. The ring's
   integrity does not depend on it.

## Costs
BTC ~600 sats total fees; XRP 30 drops; XLM ~1.0 XLM retained reserves (2 x
account minimums, recoverable on account merge). Under $1 all-in excluding
retained reserves.
