# SIP-042 "DROPBOX" — On-Chain Seed Drop Protocol (PREREG DRAFT — UNFROZEN, not yet authorized)

Status: DRAFT v0.1, authored 2026-10-18 ~02:12 CT, owner design doctrine recorded verbatim in substance:
"it only transfers, never retains. it either hits the destination or not. money is never involved in our process."

## Design Invariants (from owner doctrine, frozen at build GO)
- **D1 TRANSFER-ONLY.** The drop is a pure data delivery. The protocol transfers the 32-byte payload
  to the destination (an OP_RETURN output) and retains nothing. No balances, no custody, no UTXO
  management beyond the single spend, no change-tracking feature, no history of value.
- **D2 BINARY OUTCOME.** The payload either lands on-chain or it does not. Verification reads the
  chain itself (explorer API / node), never a wallet UI and never our own server's word.
  Delivered = bytes present at destination and reconstructable. Not delivered = nothing claimed.
  No partial states, no "probably sent."
- **D3 NO MONETARY FUNCTION.** Money is never involved in the process. The miner fee is postage on
  the writer side — paid once per drop, fixed-size, never displayed as a feature, never tracked,
  never aggregated, never reported. The reader side costs zero. No payments layer, no pricing,
  no balances anywhere in the protocol. (Hard boundary vs. the payments/patent license rails,
  which live in commerce, not in the evidence standard.)
- **D4 READER PURITY (reaffirmed).** The examiner box holds zero key material, never signs, never
  broadcasts, never spends. It only reads the chain and reconstructs. Keys exist only on the writer
  side (the licensed TGC engine), never in the public reader.
- **D5 DESTINATION DETERMINISM.** Payload format: OP_RETURN with marker || 32-byte seed (fits the
  80-byte limit with room for a version byte). Same seed, same marker, same output script — the
  drop address/script content is deterministic and therefore itself verifiable.
- **D6 RECOVER = READ.** Recovery means: anyone reads the transaction off the chain, extracts the
  32 bytes, feeds them to the pinned generator, reconstructs the artifact. Chain + generator =
  artifact. No dependence on Zenodo, GitHub, or company survival for the recovery path (those
  remain as mirrored archives).

## Test Plan (authorized portion TBD by Leon GO)
1. Testnet drop + chain-read recovery (zero monetary exposure).
2. Mainnet drop of the Series No. 1 seed (single OP_RETURN) — requires Leon GO: custody of the
   writer-side key and the postage decision are the owner's gate, never automated.
3. Genesis Viewer v2: "pull from chain" mode — paste a txid (or scan a block), box reads the
   OP_RETURN, extracts the seed, reconstructs, and verifies the canonical hash. The box never
   broadcasts anything.
4. Receipts: prereg freeze sha, runlogs, disclosed results, ledger entry — full receipt-first cycle.

## Out of scope (refused by design)
- Any wallet features in the examiner box (balances, signing, spending, key import).
- Any retention of dropped payloads by our infrastructure (the chain is the storage; we keep nothing).
- Any monetary accounting, fee optimization as a product, or payment acceptance in the protocol.
