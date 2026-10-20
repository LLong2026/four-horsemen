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
