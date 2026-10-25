# MCR-4 PREREG — THE THIRD MOUNTAIN UPDATE (2026-10-25)

Frozen before fold and before any broadcast. Series: MCR-1 (ledger 0260, 1,891 leaves,
root 2d1a3214...cc23a), MCR-2 (ledger 0265, 1,906 leaves, root 1929707e...bcb60),
MCR-3 (ledger 0297, 2,082 leaves, root 418fc5a8...eb8d06, commit 4c13ac3, twelve rails).

## Scope
Fold the public corpus at commit 029b32b (Ledger 0350 head, includes the Witness
paper instrument and all entries through 0350) with the frozen MCR-1 covenant spec:
leaf = SHA-256(0x00 || sha256(file)); parent = SHA-256(0x01 || L || R); peaks bagged
right-to-left; root = SHA-256(0x03 || bag || leaf_count u64 LE). No file-level
selection, no exclusions — every blob in the commit tree is a leaf, sorted by UTF-8
byte order of path.

## Hypotheses (falsifiable)
- H1: The fold at 029b32b reproduces the MCR-3 root when run at MCR-3's commit
  (builder determinism gate), and the MCR-1 and MCR-2 gates still PASS byte-identical.
- H2: The new leaf count exceeds 2,082 strictly by append (no leaves removed);
  the MCR-3 leaf set is a prefix-compatible append (MMR append-only property).
- H3: All twelve legs (XLM, XRP, SOL, ALGO, AVAX, ETH, DOT, ATOM, ADA, LTC, DOGE,
  BTC) carry envelope SQDR + 0x06 + root, byte-exact, with independent public
  readback 12/12.

## Gates (deterministic)
- G1 root-frozen: root hex recorded in this run before any broadcast.
- G2 stamp-before-execute: RateLimitLog scope mcr4_mountain_update_2026-10-25
  before the first leg.
- G3 byte-exact readback: every leg verified from a public endpoint not used
  for broadcast.
- G4 disclosure: any leg failure, retry, or defect disclosed in the runlog.
- G5 prereg immutability: this file committed before the first broadcast;
  no post-hoc edits (forward-only corrections only, in new commits).

## Cost envelope
Twelve legs, expected postage under $2 total (XLM 100 stroops, XRP 10 drops,
BTC ~790 sats, remaining rails cent-class). Any wallet shortfall disclosed
rather than skipped silently.

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
