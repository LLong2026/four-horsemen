# SAT-2 RUNLOG — THE MOUNTAIN GROWS (covenant root updated in place)
Ceremony: SAT-2 | Date: 2026-10-20 | Status: **PASS — satoshi's job updated in place: same coin lineage, new mountain, new root in the output key**

## What this proves
SAT-1 proved a satoshi can CARRY a mountain root wallet-to-wallet. SAT-2 proves the
commitment is UPDATABLE IN PLACE: the corpus grew (append-only), the mountain was
rebuilt, and the SAME 330-sat covenant output — same coin lineage, still ordinal
position 0 — was re-committed to the NEW root in a single transaction. The inputs were
signed with the OLD-root effective secret (that is what the UTXOs committed); the output
commits the NEW root. The satoshi's job description updated; the coin history never
broke.

## The mountain grew
- OLD ROOT (MCR-2 / SAT-1): `1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60` — 1,906 leaves, corpus bf13210
- NEW ROOT (SAT-2): `267f13b0088c2bb82addf7358e4c50cf7c1e1fc7023be00e1194149bb56f34bf` — 1,920 leaves, corpus 03214b5
- G0 REPRODUCTION: builder rerun over corpus bf13210 reproduces the old root and all 7
  peaks byte-exact before building the new one
- G0b APPEND-ONLY: 0 files missing; 1 changed leaf = LEDGER.md (append-only ledger
  growth, disclosed); 14 added leaves (MCR-2 + SAT-1 ceremony records — the corpus now
  contains the proof of the satoshi's own creation); MCR-2 peaks at heights 9 and 8
  byte-identical in the new build (1,536 original leaves provably untouched)

## Transaction receipts
| TX | TXID | WHAT | FEE |
|---|---|---|---|
| UPDATE | 1f6d4b53b386cddc9d47890f2738673246166379b6a19102b2f344f4371be19c | SAT-A spends old-root covenant + tank -> 330-sat covenant tweaked with NEW root (parked at SAT-A) + 4,000 tank | 2,000 sats |
| Stellar | 26cedf0303aaa3371810c16b964896aa5554979fcd27ace462b039d77901bfe8 | manage_data SQDR-SAT-2 = envelope, ledger 65038806, 6.2s | 100 stroops |
| XRP | BD43F2EF6E019ED25E72468AC41BB024DA323987FD23B35A5036B2EB3BEB1779 | MemoType SQDR-SAT-2, MemoData = envelope, VALIDATED | 10 drops |

BTC block inclusion: tracked by watcher; block height recorded in ledger entry 0267.

## Keyless verification (G3)
- Recomputed from SAT-A pubkey + NEW root: Q_x = 38ed58ed8e81e59801378f42117e66481db649602ec0cc533ff96dc19dbb16ed
- On-chain covenant scriptPubKey byte-match: True | value exactly 330 sats: True
- Old covenant UTXO (d261810c...399:0, old-root tweak) provably spent by this tx: True
- Stellar byte-exact: True | XRP byte-exact + validated: True and True

## Construction
Identical to SAT-1 (prereg frozen): taptweak t = SHA256(tagged TapTweak || P_x || NEW ROOT),
Q = P + tG; 330-sat P2TR key-path output; SIGHASH_ALL; the SAT-1 pure-Python BIP340/341
library (26/26 official vectors + BIP86, unchanged code path).

## Costs
2,000 sats + 100 stroops + 10 drops — the entire mountain update cost under half a cent.

## Provenance
Leon GO (chat authorization, 2026-10-20 ~02:01 CT). Scope-stamped before broadcast
(sat2_mountain_grows_2026-10-20). Ledger 0267. Claim scoped (G5): first covenant update
under this program; no global first-ever claim; prior art disclosed. Anchor doctrine
language applies (ledger 0244). No client data, no PHI, no credentials, no operator
text quoted (POL-DISC-001). Prototype disclaimer applies. Dual Mesh Benchmark: NOT
MEASURED (deterministic ceremony, no neural-mesh inference; program benchmark DOI
10.5281/zenodo.23321637).
