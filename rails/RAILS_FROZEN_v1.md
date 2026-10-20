# RAILS v1 — THE FROZEN ROUTE BOOK (no more repairing; scale-ready)

Status: FROZEN 2026-10-20 (Leon GO, chat authorization ~12:48 CT: "log those books,
hard code those routes so don't have to keep repairing; we cannot scale without
the learning loop"). This is the hardcode: every construction below was proven in
a live mainnet ceremony (SBR-1, MCR-2, SAT-1, SAT-2, CAR-1). Do not modify;
new rails append as RAILS v2. Companion executable: squirrel_rails.py.

## Carrier rails (the fast pair — the liquidity/gas/routing solution, receipted CAR-1)

### R-XLM (transport rail — 4-second provisional receipt)
- Endpoint: https://horizon.stellar.org (public horizon, no repair needed)
- Key: tokenization-adoption/stellar-rail/stellar_writer_key_mainnet_a.json (gitignored)
- Construction: manage_data, data_name = tag (<=64 chars), data_value = 37-byte envelope
  (SQDR + version byte + 32-byte digest). base_fee=100 stroops. set_timeout(30).
  Payload is raw BYTES — Horizon returns the entry base64; compare byte-exact after decode.
- PITFALLS FIXED (frozen): entry value is base64 in readback (not hex); assert keyfile
  public_key matches derived Keypair before signing.
- Cost: 100 stroops. Observed: 4.7s (CAR-1).

### R-XRP (anchor rail of record — 1.5s finality)
- Endpoint: https://xrplcluster.com (submit), https://s1.ripple.com:51234/ (readback)
- Key: tokenization-adoption/xrp-rail/xrp_writer_key_mainnet_a.json (gitignored)
- Construction: AccountSet, fee="10", memos=[Memo(memo_type=tag-hex, memo_data=payload-hex)].
  Autofill, sign, submit. Readback: JSON-RPC method=tx returns tx fields AT TOP LEVEL
  (no "tx" wrapper); memo hex comes back UPPERCASE — case-insensitive compare.
- PITFALLS FIXED (frozen): xrpl-py Wallet arg order is (public_key, private_key, seed);
  sequence from AccountInfo(ledger_index="validated"); tx readback shape; hex casing.
- Cost: 10 drops. Observed: 1.5s submit->tesSUCCESS (CAR-1), validated same ledger window.

### Envelope doctrine (Thesis v2.1 Sec 2.5 — unchanged)
37 bytes: "SQDR" (4B) + version byte (1B) + payload (32B).
Version registry: 0x07 covenant root | 0x08 covenant carrier (outpoint||root digest).
Carrier digest = SHA256(outpoint_internal(36B) || root(32B)); outpoint_internal =
txid reversed (32B) + vout LE (4B). THE POINTER IS A CLAIM; THE CHAIN IS THE TRUTH.

### Route policy (frozen)
- Value/life estate: BTC (covenant sat, P2TR tweak). Speed/price: XLM+XRP carrier.
- Anchor rail of record: XRP. Transport: XLM. Companion redundancy: as receipted per ceremony.
- Every send is a re-attestation, not a new truth claim. Re-arms after any covenant move
  (tamper watch re-fires carrier with fresh outpoint||root digest).

## Slow rails (proven, frozen — kept for the 10-rail corpus)
- R-BTC: P2TR, taproot tweak per BIP340/341 pure-Python (sat1/ harness, ledger 0266);
  mempool fee policy per anchor_btc_mempool_stall playbook (CPFP bump authorized flow).
- R-DOGE: Blockchair is anti-bot — use BlockCypher/UTXO endpoints; change output reuse
  per DeWR-1 discipline (CFR-9 receipts).
- R-DOT: Asset Hub post-Nov-2025 migration — modern call transfer_assets (call 11),
  V16 metadata manual compose, sign via JS path (CFR-9 receipts).
- R-SOL: Memo v2 program MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr; signer meta/hex-ASCII.
- R-ADA: pycardano-native CBOR — output pair order + aux_data_hash placement (CFR-9 receipts).
- R-ALGO / R-AVAX / R-ETH: as receipted in CFR-9/MCR-1/MCR-2 readbacks.

## The point (owner's doctrine, frozen 2026-10-20)
The rails exist so people can SEE the anchoring today — engraved proofs pointing at
wallets would work but nobody would understand them. Anchoring will take its place
eventually; until then, we still have to send something — and now we send it without
repairing anything.

---

# RAILS v2 — APPENDED LESSONS (frozen v1 above stays untouched)

## v2.1 — System-direct envelope (version byte 0x09, receipted SPB-1, 2026-10-20)
37 bytes: SQDR + 0x09 + SHA-256(system artifact). Direct ledger-pure mode: XRP
burst anchors + XLM bundle transport, no Bitcoin required. Reserved for system
artifacts where the sat epoch seal covers the corpus at the covenant level.

## v2.2 — XLM bundle construction (receipted SPB-1)
ONE XLM transaction, N manage_data ops (data_name=tag, data_value=37B envelope),
base_fee=100 stroops PER OP. 10 ops = 1000 stroops ≈ $0.00008. Byte-exact readback
per entry.

## v2.3 — Burst-sequence lesson (honest defect, SPB-1: 2/10 tefPAST_SEQ)
Never burst XRP submits off a pre-read locally-incremented sequence — it races the
account. Refetch AccountInfo(ledger_index="validated") sequence per anchor, or
chain from the previous submit response. Refire is free (failed submits never
validate, no fee charged).

## v2.4 — Race-proof XRP batch sequence chaining (receipted SPB-2, 2026-10-20)
LOCKED: per-anchor AccountInfo(ledger_index='current') sequence read — the open-ledger
view includes this burst's own submitted txs, so the next sequence is always accurate.
tefPAST_SEQ/tefTOO_SOON -> fresh read + retry (SPB-1: 2/10 raced; SPB-2: 0/10, zero
retries, 10/10 tesSUCCESS). Driver: rails/squirrel_rails_v2.py (v1 frozen untouched).
XLM bundle fires in parallel with the XRP burst. Measured: XLM half of any batch is
final in one ledger close (~5s); XRP burst window is round-trip bound (~1.2s/anchor).

## v3 — PARALLEL SLOTS: FALSIFIED (receipted SPB-3, 2026-10-20)
Tested: one current-read + deterministic sequence slots + 10 concurrent submit
threads. Result: heavy intra-burst retrying, 2/10 stranded in persistent
tefPAST_SEQ (concurrent threads read the same sequence before any tx lands at the
load-balanced endpoint), all-final 31.9s vs v2.4's clean 14.1s. VERDICT: do not
parallelize same-account XRP bursts at a community load balancer. LOCKED BATCH
ROUTE REMAINS v2.4 (serial, per-anchor current-read chaining). Driver
rails/squirrel_rails_v3.py retained as the falsification receipt; use squirrel_
rails_v2.py in production. XLM bundle remains the instant lane (one tx, N anchors,
~5s). Remaining v4 lever, if ever needed: dedicated single XRPL endpoint.
