# HBAR RAIL — RE-OPENED (ledger 0243 waiver reversed by owner GO, chat 2026-10-21 ~15:02 CT)

## Basis
- Ledger 0243 (2026-10-19) waived route 10 (Hedera) from DeWR-1: alias auto-create friction +
  exchange incompatibility. Waiver explicitly stated the armed ed25519 writer key was
  "retained, rail re-openable in a future ceremony."
- Owner GO 2026-10-21 ~15:02 CT: "HBAR + LTC - yes set those up as one .. like we did with
  stellar and xlm." This re-opens the rail. Forward-only per the append-only doctrine.

## Writer key (REUSED — the armed Oct 19 key stands up again)
- File: /app/tmp_push/fh_push/tokenization-adoption/hbar-rail/hbar_writer_key_mainnet.json
  (copied to hbar-rail/keys/hbar_writer_key_mainnet.json)
- ed25519 public key: a90a0b7fb134563694457b6ccb476d983ea0ff2e551ef8c2cf4d8fcb2283236b
- DER: 302a300506032b6570032100a90a0b7fb134563694457b6ccb476d983ea0ff2e551ef8c2cf4d8fcb2283236b
- Alias (0.0.<base32>): 0.0.vefaw75rgrldnfcfpnwmwr3nta7kb7zokupprqwpjwh4wiudenvq

## Connectivity — VERIFIED 2026-10-21 ~15:05 CT
- Mirror node HTTPS: mainnet.mirrornode.hedera.com/api/v1 — OPEN (readback path)
- Consensus gRPC 50211/50212 on mainnet nodes (34.64.136.190, 43.202.249.148,
  3.130.52.236, 35.186.191.247, 3.114.54.4, 35.203.82.240, 16.170.54.28, 35.228.232.18) —
  ALL OPEN from the sandbox. (An earlier probe hit a stale IP; live node list re-pulled.)

## Recipe (native memo transfer — the original ledger-0243 plan)
1. FUNDING (two-hop, the friction that caused the waiver):
   - Hop 1: owner sends HBAR from exchange/wallet to the alias. Auto-create via alias
     transfer: any wallet that supports alias destinations (HashPack, Blade) accepts
     `0.0.vefaw75r...`. Plain exchange withdrawals typically require a 0.0.x account ID,
     which does not exist until auto-create — hence two-hop (exchange -> wallet -> alias),
     or a direct alias send if the owner's wallet supports it.
   - Recommended amount: 5 HBAR (auto-create ~0.05 HBAR + tx fees + balance headroom).
2. CERTIFICATION LEG (fired from sandbox once the account exists):
   - CryptoTransfer with memo = envelope bytes "SQDR" + 0x07 + digest (37 bytes, hex-ASCII
     per the WRAP-1 convention; memo field max 100 bytes — fits).
   - SDK: hedera Python SDK over gRPC 50212 (confirmed open). Fallback: raw protobuf build.
3. READBACK (keyless, byte-exact):
   - Mirror node /api/v1/transactions?account.id=0.0.x -> transaction.memo_base64 decode,
     byte-exact vs envelope. HashScan public explorer shows the memo on the tx page.
4. STAMP-BEFORE-EXECUTE: hbar-rail/HBAR_FIRE_RUNLOG.md stamped before any broadcast.

## Status: AWAITING FUNDING (hop 1) — no HBAR moved, no leg fired, no ledger seal.
## Ledger: a rail-setup entry + certification receipt will be drafted at fire time,
## sealed only under the two-key gate (owner GO).
