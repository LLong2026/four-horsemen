# BATCHED BTC CHECKPOINT SPEC (v0.1 draft — staged for Leon GO, not deployed)

## Status
DRAFT — proposal only. No runner changes made for batching. The economy-fee
patch (fee_rate param + minimumFee pay rate + 6h patience window) IS deployed
as of 2026-10-24 (ledger 0331); this spec is the separate, deeper lever.

## Problem
Per-artifact triads pay one BTC anchor per receipt (~158 sats each at economy
rate, ~13 cents). Receipt volume is ~5-10/week and growing with the program.

## Proposal — align the BTC leg with the Twelfth patent's own architecture
The Twelfth (serial 64/182,644) already claims: instant sub-second hash-linked
receipts + DAILY BTC CHECKPOINTING OF THE RECEIPT CHAIN HEAD. The current
per-artifact fire is a stricter, more expensive variant. This spec returns to
the patent's native shape:

1. FAST RAILS PER ARTIFACT (unchanged): every receipt fires XLM + XRP
   immediately — combined cost < 1 cent. Instant-tier finality preserved.
2. BTC PER CADENCE, NOT PER ARTIFACT: one checkpoint tx anchors the digest of
   the RECEIPT CHAIN HEAD (latest ledger entry hash / chain head string) at a
   fixed cadence. The hash-linked ledger proves every entry beneath the head;
   the BTC anchor proves the head. Gap-free ordering is inherited from the
   hash chain, exactly as claimed.
3. CADENCE (pick one at GO):
   - Daily: ~$0.13/day ceiling at economy rate.
   - Weekly: ~$0.93/week ceiling; at current volume (~7 receipts/week) that
     is ~1.9 cents per receipt. This is the sub-2-cent target.
4. RECEIPT SHAPE CHANGE (the one real trade): public DOI receipts go from
   "BTC in-row" to "XLM+XRP in-row, BTC via batch checkpoint range." Ledger
   batch entry names the covered entry range (first-last) and the checkpoint
   txid + block. Verification: batch digest = head entry hash; walk the
   hash-linked ledger beneath it.
5. UTXO CHAIN CONTINUITY: unchanged — each checkpoint spends the previous
   checkpoint's change output, same as today.

## Cost model (at BTC ~$80.7k, economy rate)
| Mode | BTC cost/anchor | Per-receipt (7/wk) |
|---|---|---|
| Current (per-artifact) | $0.64 -> $0.13 patched | ~$0.13 |
| Batched daily | $0.13/day | ~$0.09 (at 7/wk) |
| Batched weekly | $0.13/wk | ~$0.019 |

## Doors this opens
- No action needed on fee spikes (weekly batch can wait out congestion).
- Bulk publication nights (like DOORS+DMB+PQC-E0) cost one BTC anchor, not N.

## Guardrails
- Fast rails remain per-artifact — no receipt ever waits for instant proof.
- Fee guard (30 sat/vB economy ceiling) still gates every fire.
- Ledger batch entries follow append-only doctrine; per-DOI entries unchanged
  in content, only their BTC linkage moves to the batch row.

Awaiting: Leon GO (or hold) on cadence choice: DAILY vs WEEKLY.
