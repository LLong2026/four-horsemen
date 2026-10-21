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
