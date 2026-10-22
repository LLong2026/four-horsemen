# PAT-1 — THE PATENT LOCK RUNLOG

**Operation:** Anchor the SQUIRL OS provisional patent filing evidence bundle
(64/181,667 + 64/181,746) on three consensus domains under envelope byte 0x0F.

**Frozen digest chain (stamp-before-execute honored):**
- Bundle: PAT1_EVIDENCE_BUNDLE.zip, 256,140 bytes, sha256 b4f167cb2916dd3e8513f7c737bcbabbee98e78caf4291bfc3a9521ad64b3dc8
- DOI: 10.5281/zenodo.23554560 (published, keyless re-download byte-exact, metadata verified intact)
- PAT-1 pre-image: SQDR-PAT-1|<bundle_sha>|doi:10.5281/zenodo.23554560|apps=64/181,667+64/181,746
- PAT-1 digest: bd5e3193bde70ea0cd20db1d3214b347d2ff0891a311eae7c085eb14f324ba99
- Envelope: 53 51 44 52 | 0F | <32-byte digest> (37-byte doctrine)

## Legs
| Rail | Receipt | Status | Readback |
|---|---|---|---|
| XLM (Stellar) | tx 32cdd551c115de0aa22c7ba208b7a7a6c9a5cf78cf61394079e153a4725aeabe, ledger 65072525, entry SQDR-PAT-1 | confirmed 5.0s | byte-exact via horizon keyless read |
| XRP | tx D62064138C9BC426664C54FDF15C8A7F2CF03E033667C52CC29F8D048875ED86, ledger 107821197, AccountSet memo | VALIDATED 5.8s | byte-exact via keyless JSON-RPC |
| BTC | tx 602ebfdc922cb5a8b1956f264f856c073e49aebc880340c87491866dc9acbe84, OP_RETURN, fee 790 sats | broadcast | payload byte-exact via mempool.space; confirmation appended below |

## Disclosed (forward-only)
- Filing fees for both applications PENDING at anchor time (USPTO payment system outage ~2 days).
- BTC confirmation status at seal time recorded in this runlog; finality follows the coin.

Prototype disclaimer: This software is a prototype, provided for educational and
research purposes only. Not for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects.

## BTC finality (appended)
- BTC leg CONFIRMED block 972579 — all three rails final. Payload byte-exact on keyless readback at anchor time and at finality.
