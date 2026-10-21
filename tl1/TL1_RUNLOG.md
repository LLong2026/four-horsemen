# TL-1 THE TRUSTABLE LOCK — RUNLOG (2026-10-20)

The demo: a tokenized lumen. The vessel account holds the lumens AND the ownership
record in one place; the artifact receipt rides three consensus domains.

DIGEST: 6650efc9e393e9b1824fd7caba28ae67f88210727a03132c798fac5cadaafc9c
= SHA256("SQDR-TL-1|" || manifest sha 3be6562f2c1e93205c3c0912ff1afe1c429b817064ed74f327d07d90585ae991
  || "doi:10.5281/zenodo.23515307" || artifact sha 61de4811d3712b02147ec2dd45e663dd3f5dabe863484b3602ce0a702d35b733")
ARTIFACT: FL-1 Breakthrough Note (the fractal lease session), DOI 10.5281/zenodo.23515307.
Envelope: SQDR + 0x0E (TL receipt — new registry entry).

## Legs (3/3 byte-exact keyless read-back)
| Rail | Receipt | Role | Finality |
|---|---|---|---|
| XLM | 23054d29...f92e9 (ledger 65050475), data entry SQDR-TL-1 on vessel GDIQGG...VLT5 | THE TOKEN — asset + record in one account | confirmed |
| XRP | B9AB81D2...00A99, memo SQDR-TL-1 | THE ATTESTATION — rail of record | VALIDATED |
| BTC | 078787db...e278 (OP_RETURN, 790 sats fee) | THE MARK — tamper-proof | mempool, byte-exact |

Redundancy doctrine: the ORIGINAL lives at the DOI (Zenodo, sha 61de4811...);
the three chain receipts point at it, mutually verifiable, no ledger trusted alone.

Cost: 100 stroops + 10 drops + 790 sats ≈ $0.09. Total build-to-verified: ~2 minutes.
Defects disclosed: (1) BTC leg first build passed hex-string instead of bytes to the
writer (local build error, nothing broadcast); fixed, refired clean. (2) Readback script
prefix bug (6a vs 6a25) initially misreported BTC as mismatch — payload was byte-exact
throughout. No LLM in any decision path; no client data, no PHI (POL-DISC-001).
Prototype disclaimer applies. Last ceremony of 2026-10-20 per Leon.

## CONFIRMATION ADDENDUM (2026-10-21, forward-only)
BTC leg 078787db...e278 CONFIRMED in block 972390 (block_time 1792538660, hash
00000000000000297e...a8ba21a9). All three TL-1 legs now carry finality. This runlog
and manifest were uploaded to the four-horsemen evidence repo on 2026-10-21 — the
receipts were referenced by ledger 0286 at ceremony time but had not been committed;
gap disclosed and closed the same day (ledger 0294).
