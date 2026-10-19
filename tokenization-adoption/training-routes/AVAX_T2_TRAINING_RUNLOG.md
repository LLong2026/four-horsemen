# AVAX T2 TRAINING RUNLOG — 2026-10-19 ~12:29 CT — PASS (fired manually, funding confirmed inbond)

- Wallet: 0xbd7370bF3d627a339401052bE8DfA711f4986570 | 2.5 AVAX arrived from Coinbase (Leon).
- T2 leg (training rehearsal, honestly labeled): txid 0x7ebb433cfb51544289745b95ffbf2609afc0875fc7693aed476d2e6549770443,
  block 97987709, 3.3s to receipt, 21336 gas, 0.00008232 AVAX. Calldata marker SQDR-AVAX-T2-TRAINING.
  Byte-exact keyless read-back via eth_getTransactionByHash: PASS.
- DISCLOSED deviation from watcher spec: rehearsal calldata used the plain marker string instead of the
  32-byte SHA-256 training digest (training leg only, no effect on certification; T3 below carries the
  canonical frozen digest).
- T3 CERTIFICATION LEG (DeWR-1, digest 99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6):
  txid 0x671d7002098803f53b8bcc7785ba1a0e2048168bb196f55dab3f810973c29988, block 97987712,
  1.1s to receipt, 21512 gas, 0.00008300 AVAX. Byte-exact: PASS. AVALANCHE IS TIER 1 CERTIFIED (route 7).
- No DOI, no separate ledger line for the T2 rehearsal (training doctrine); certification sealed in
  the DeWR-1 leg set (ledger 0241).

Prototype disclaimer: this software is a prototype, educational/research purposes only, not production use.
