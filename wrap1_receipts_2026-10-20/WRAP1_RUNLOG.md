# WRAP-1 — THE PHASE SEAL RUNLOG (2026-10-20)

SEAL: 14b11a77d2b6618569d6f0a3c53f42c96679259c1d62e22f13f8c9ad3e1c72ea
= SHA256("SQDR-WRAP1" || MCR-1 || MCR-2 || SAT-2 || HAND-1 || FL-1 || XLM-COV-1)
PAYLOAD: SQDR + 0x0D + SEAL (37 bytes). Fire order: SOL ALGO AVAX XLM XRP DOT ETH | DOGE | BTC | ADA.

## Legs (10/10 byte-exact keyless read-back)
| Rail | Receipt | Finality |
|---|---|---|
| SOL | YyNmJnWp...kqA3DoyeUSLj (confirmed, 2.4s) | slot 459392724 |
| ALGO | JBB5FT2D...ONNBVA (round 66176768, 3.5s) | deterministic |
| AVAX | 0xd0d14050...9331 (block 98095176, 2.4s) | confirmed |
| XLM | 119e38ef...dacad6b1f (ledger 65049750, 6.0s) | confirmed |
| XRP | AA1339CD...94BE7E (VALIDATED, 8.5s) | 4s ledger |
| DOT | 0x3ec93e79... (block 33519650) | remark sealed |
| ETH | 0x4f80cf60... (block 26236724, status 0x1) | confirmed |
| DOGE | 948654fd...a79e7 (OP_RETURN, spent MCR-2 change 56f0aae3:1) | mempool→block |
| BTC | 65ba8cbc...b54d3d (refire, 790 sats fee) | mempool→block |
| ADA | 4b5d39ea...e0b11e (label 1968, tx 313 B) | mempool→block |

## Defect trail (all disclosed, none in any decision path)
1. SOL first broadcast: BlockhashNotFound (finalized-commitment blockhash expired).
   Refire succeeded in 2.4s. No state change from the failure.
2. DOGE first fire: 400 push rejection — the runner's frozen UTXO (MCR-1 change)
   was already spent by MCR-2's DOGE leg. Patched to the verified-unspent MCR-2
   change (56f0aae3:1 = 14.75 DOGE, BlockCypher-verified). Refire clean.
3. BTC first broadcast (c210382b...1fe5, block 972386): the writer's version byte
   was pinned 0x06 (MCR-2 config) instead of 0x0D — the SEAL is byte-exact on-chain
   but under the wrong envelope label. Refired 65ba8cbc...54d3d with 0x0D; the 0x06
   leg remains on-chain, disclosed here, superseded.
4. ADA metadata tag: field 1968{1} = "MCR-2" (stale tag, sed miss) carrying the
   WRAP-1 seal byte-exact in field {2}. Disclosed; label 1968 + digest are correct.

Gates: G1 seal reproducible from public roots; G2 envelope 0x0D exact (BTC refire);
G3 10/10 keyless byte-exact; G4 no key material public; G0 BTC covenant UTXOs untouched
(OP_RETURN leg spends the writer's own UTXO only). No LLM in any decision path.
Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
