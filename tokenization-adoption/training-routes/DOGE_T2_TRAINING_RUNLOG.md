# DOGE T2 TRAINING RUNLOG — 2026-10-19 — COMPLETE (verdict PASS)
- Route 10 (DOGE, replaces waived HBAR per ledger 0243). Writer: DGrHsdhpNiDf5aUnE53Y7szskKxjhx4rFD.
- Funding: 15.00 DOGE received (tx 7e48c1e8..., vout 1, block 6422019).
- T2 training leg: tx 1e608f4ed8e97d33f6b4c6a6ec89f76935335a39fbceecc0727d07247b7af20c, block 6422035.
  OP_RETURN payload sha256(SQRL-ROUTE-CERTIFICATION-DOGE-T2-TRAINING-2026-10-19) = ecc6bd92facc250b09299bc44c1c4a2d7e94cd752b6047916f62753e3def2dda — byte-exact read-back.
- T3 DeWR-1 certification leg: tx 075e7656667e5129291c68d29b9acdfc29ef635bc7f4011de311364d6fc329aa, block 6422037.
  OP_RETURN payload 99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6 (DeWR-1 frozen digest) — byte-exact read-back.
- Fees: 0.05 DOGE per leg. Explorer: Blockchair (BlockCypher rate-limited); dogechain.info balance.
- Engineering notes (forward-only disclosure): BlockCypher 429 forced manual rail. Three defects found and fixed in the original fire script:
  (1) P2PKH script template carried a doubled length byte (0x19) -> nonstandard scriptpubkey reject 64;
  (2) sighash missing trailing 4-byte SIGHASH_ALL hashtype -> NULLFAIL;
  (3) high-S signature -> non-canonical reject. All fixes local, no state change from failed attempts (all rejected pre-mempool).
- Read-backs keyless via Blockchair dashboards. Receipts: route-roster/DOGE_DEWR_LEGS.json.
- Record closure: 9/10 rails certified; DOT outstanding (10.02 DOT inbound per owner report 2026-10-19 13:20 CT).
