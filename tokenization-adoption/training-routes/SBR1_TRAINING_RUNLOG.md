# SBR-1 — SPEED BURST RECORD: 8 DOI ANCHORS IN ~4 SECONDS
2026-10-19 (UTC). Prereg sha ac106167 frozen 22:49; scope stamp sbr1_speed_burst_2026-10-19T22:49:10Z before first submission.

## Purpose
First live test of the ledger-0261 doctrine: XRP as the rail of record, Stellar as the transport.
Four distinct DOI bindings fired in one burst; speed and cost measured honestly.

## Payload class 0x06 (DOI binding)
SQDR + 0x06 + SHA-256(ASCII DOI string), 37 bytes per anchor. Deterministic and keyless:
anyone can hash the DOI string and compare the on-chain value.
- 10.5281/zenodo.23466738 (Tri-Write)  -> c5d700739060b45be51f6e935ff93b323d88d15941744409c204f99d1f917cc5
- 10.5281/zenodo.23467440 (QWR-1)     -> 09b1748878cc51aab6af19338b4ead4fb6c9d9239b06e863856813307f649071
- 10.5281/zenodo.23482978 (Thesis v2.1) -> 6d07bfe08e4ff00b584affe740e98b97e09df22a50c6f3054193873d980b2762
- 10.5281/zenodo.23485222 (IR-2)      -> a028ba4175ed78732c2b1b93eeaf9274f9104ac94592e509f020f7c59d0c259d

## The burst (t0 ~22:50:19Z)
XRP RAIL — 4 pre-signed AccountSet txs (seq 107745093-096), one burst:
  +0.249s tx1 tesSUCCESS | +0.487s tx2 | +0.729s tx3 | +0.973s tx4
  THREE of four validated in the SAME ledger 107771300 (close 22:50:21Z); the fourth in 107771301 (22:50:22Z).
  Hashes: 075F38E5675F251A..., 3C57AB013F6566AB..., C9A645F4D215ACAE..., DFCE46982F89E824...
STELLAR TRANSPORT — 1 transaction, 4 ManageData ops (SBR-1-DOI-1..4), the bundle layer:
  tx 9298f64383f78173...79d6c, ledger 65032888, close 22:50:23Z. Four DOI bindings in one ledger slot.

## Verified metrics (the headline numbers)
- Submit burst: 4 XRP anchors in 0.97 seconds
- Validated finality (XRP): 1-3 seconds from submit
- Transport inclusion (XLM): ~4 seconds from submit, 4 anchors in one tx
- Whole ceremony: 8 anchors, 5 transactions, all final in ~4 seconds
- Cost: 10 drops per XRP anchor (0.00001 XRP), 100 stroops per XLM op (0.0001 XLM);
  TOTAL: 40 drops + 400 stroops ≈ one-hundredth of a cent at any plausible price

## Honest disclosure
Six xrpl-py 5.2.0 library-shape corrections during build (Wallet constructor, autofill argument
order, Memo model object, frozen dataclass sequence, blob accessor, response shape) — all local,
zero ledger effect. No transaction from any failed iteration was ever broadcast. The Stellar
TimeBounds warning (no time bounds set) is noted; the tx landed in the next ledger regardless.

## Read-back (keyless, independent endpoints)
8/8 byte-exact: XRP memos via xrplcluster account_tx; Stellar data entries via horizon accounts.

## Why it matters
This is the demand-side demo: not one anchor, but a pipeline — four different papers bound to
their DOIs, all final in one breath, for a cost that rounds to zero. Storage is endless because
the anchor never scales (MCR-1); this shows the rails never slow down either.
