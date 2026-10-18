# SQUIRL OS Examiner Evidence File
**Generated (UTC):** 2026-10-18T04:34:10Z  |  **Mode:** zero-trust examiner (SIP-039)

## Corpus inventory (anchored receipts)
- ANCHOR-BLOCK-REGISTRY.json.ots: digest 87146a26134441d4... — pending calendar confirmation
- CHAIN_OF_CUSTODY_GRAPH.md.ots: digest a1b3e6315850f344... — pending calendar confirmation
- HASH_NOTARIZATION_SPEC_MHCN1.md.ots: digest e6f7b4a2c104195a... — pending calendar confirmation
- OTS-2026-10-18-anchor_manifest.ots: digest f3e584a7e0197199... — pending calendar confirmation
- OTS-2026-10-18-cage_feed.ots: digest c129f776e239f563... — pending calendar confirmation
- OTS-2026-10-18T0346Z-LEDGER.md.ots: digest 2227fca960c24fcd... — pending calendar confirmation
- OTS-2026-10-18T0418Z-LEDGER.md.ots: digest ba783af8d519093c... — pending calendar confirmation
- OTS-2026-10-18T0418Z-cage_watch_feed.json.ots: digest c129f776e239f563... — pending calendar confirmation
- OTS-2026-10-18T0425Z-LEDGER.md.ots: digest 5442ad503814a303... — pending calendar confirmation
- OTS-2026-10-18T0425Z-cage_watch_feed.json.ots: digest c129f776e239f563... — pending calendar confirmation
- OTS-2026-10-18T0431Z-LEDGER.md.ots: digest 3eb1eff0773fac94... — pending calendar confirmation
- OTS-2026-10-18T0431Z-cage_watch_feed.json.ots: digest c129f776e239f563... — pending calendar confirmation
- SBR7_RECEIPT.json.ots: digest a18cf2d9dfa112f0... — pending calendar confirmation
- sbom-anchor-stack-2026-10-18.spdx.json.ots: digest 4a85d03f1628b360... — pending calendar confirmation

## Reconciliation gate verdict (MHCN-1 R3)
receipts=14 confirmed_onchain=0 pending=14 mismatches=0
RECON VERDICT: PASS

## Block registry
receipts tracked: 12
confirmed: 0 pending: 12

## Independent verification (trusts no third party)
1. pip install opentimestamps-client
2. ots upgrade <receipt>.ots   (fetches the confirmed Bitcoin attestation)
3. ots verify <receipt>.ots    (against a Bitcoin full node)

## Disclosures (load-bearing)
- Pending receipts confirm on Bitcoin within hours of stamping; pending is never reported as settled.
- Anchoring notarizes EXISTENCE. Authority is retained in the separate PQC layer (MHCN-1 R5);
  the reference chain's signatures are not post-quantum.
- Prototype software, educational/research purposes only; no production warranty.
