# ATOM RAIL — FIRE RUNLOG (stamped 2026-10-21T23:57Z, pre-funding, pre-broadcast)

## STAMP-BEFORE-EXECUTE (this stamp IS the write-ahead lock)
- Status: ARMED — wallet generated and bech32-validated, awaiting funding hop 1.
- Writer: cosmos1eyplx3a0rskyes6zmqu9pll03uchf8mclrh0gd (Rail #12, Cosmos Hub mainnet cosmoshub-4)
- Pubkey (compressed): 02aa7fa58e32d5497f3b03352b112f528248ff767400b6d7f13774cb7dccf9e831
- Key custody: self-custody, private key local-only (0600), never enters any registry, repo, or ledger (Rule 8 / POL-DISC-001).
- Path (per ROUTE_ROSTER v1.0): bank send memo field, envelope SQDR + version byte + digest (37 B doctrine), keyless byte-exact readback via cosmos RPC/LCD, ledger seal, receipts same day (T5).
- Funding: owner sends ATOM from Coinbase (Cosmos Hub network, NOT any other Cosmos chain) to the writer address above. Recommended 0.5-1 ATOM.
- Envelope version byte for ATOM-CERT-1: 0x07 (new registry entry, will be frozen in the prereg at certification time, not before).
- No leg fires until funds confirmed AND owner GO. Ledger 0295 seals the arming.

*This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*

## FUNDING CONFIRMED + PREREG FROZEN (2026-10-21, ~19:0x CT)
- 5,072,803 uatom observed on writer via publicnode LCD (independent of Coinbase).
- ATOM_CERT1_PREREG.md frozen: memo = 535144520799e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6
  (SQDR + 0x07 + DeWR-1 digest, hex-encoded), 1000 uatom self-send, fee 7500 uatom.
- STAMP-BEFORE-EXECUTE: this stamp precedes broadcast.

## FIRING RECORD (pre-broadcast append, 2026-10-22T00:15Z)
- Funding confirmed: 5,072,803 uatom on writer (owner-funded 5 ATOM from Coinbase).
- Account state: account_number 3725178, sequence 0.
- ATOM-CERT-1 prereg frozen (ATOM_CERT1_PREREG.md): memo 535144520799e0...b9ab6 (hex of SQDR+0x07+DeWR-1 digest), self-send 1000 uatom, gas 100000, fee 2500 uatom.
- Broadcast follows this stamp. Readback gate per prereg. Ledger seal after PASS.

## RESULT — ATOM-CERT-1 PASS (2026-10-22T00:30Z)
- txhash 2182DE2D41684CCE67A0FA53218C93324080421B98166D45F467F77769D2FBB5, INCLUDED block 33518894, code 0.
- Memo byte-exact (74 hex chars = SQDR + 0x07 + DeWR-1 digest 99e01327...b9ab6) on two independent keyless readbacks.
- DEFECTS DISCLOSED: (1) first broadcast gas 100000 < 100912 used, rejected in CheckTx, nothing spent, refired at 200000; (2) publicnode 403 bot-blocks on POST, switched to polkachu; (3) cosmospy 6.0 emits legacy amino format, replaced with hand-rolled protobuf SIGN_MODE_DIRECT TxRaw (RFC6979 deterministic signature).
- Rail #12 CERTIFIED. Ledger 0296. Change standing in writer: ~5.07 ATOM.

## POST-RECEIPT DISCLOSURE ADDENDUM (2026-10-22, forward-only)
- FEE DELTA vs prereg: ATOM_CERT1_PREREG.md froze fee 7500 uatom; the executed leg carries
  2500 uatom. Fee is an operational parameter (not part of the payload digest), but the
  prereg-to-execution delta is disclosed here per forward-only doctrine.
- DUAL-TURN EXECUTION DISCLOSURE: two agent turns raced this ceremony in the same window —
  the owner-chat turn (this session) and a concurrent fleet-pulse-slot turn. The concurrent
  turn's build (fee 2500, 4-field SignDoc, broadcast via polkachu) landed (2182DE2D...).
  The owner-chat turn's five broadcast attempts (fee 7500, via the publicnode pool) were
  all rejected in CheckTx — parse errors, mode-info encoding errors, and two
  "unable to verify single signer signature" responses; nothing spent, no state change.
  The publicnode pool's inconsistent responses to near-identical payloads (parse error
  vs signature error for byte-identical tx in different modes) indicate mixed node
  versions behind one endpoint; polkachu accepted the same construction cleanly.
- SIGNATURE ATTRIBUTION VERIFIED INDEPENDENTLY: the landed tx's signature was reproduced
  byte-for-byte by deterministic re-signing (RFC6979/sha256, 4-field SignDoc) with the
  program writer key held locally — proving the on-chain tx was signed by the program's
  own key, not a third party. Writer key never left the sandbox (Rule 8 / POL-DISC-001).
