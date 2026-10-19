# MCR-1 PREREGISTRATION — THE MERKLE ROOT COVENANT (first MMR anchoring)
Frozen BEFORE any broadcast. 2026-10-19 ~17:22 CT. Leon GO (chat authorization, 2026-10-19 ~17:15 CT).

## What the ceremony proves
The entire public evidence record — every receipt, runlog, prereg, ledger, thesis, patent
draft, benchmark, and proof bundle in the four-horsemen repository — is folded into one
Merkle Mountain Range whose single 32-byte root is anchored across all ten certified
mainnet rails. From this covenant forward, ANY single artifact in the 1,891-file corpus
is independently verifiable with only: the public repo, a ~10-hash inclusion path, and
one on-chain 32-byte root. One root proves everything; the mountain grows append-only
while the on-chain footprint never grows past 32 bytes — storage is endless.

## Corpus (frozen)
The exact git tree of commit 7c492528c9f9624bb43846b745df9a480f4d1600 (the routing chapter
seal, origin/main HEAD): 1,891 tracked files, paths in byte-sorted order, as enumerated
in MCR1_LEAF_INDEX.json (sha256 of that index: published with the runlog; the corpus is
rebuildable by anyone from the public repo at that commit).

## MMR construction (fully specified, no ambiguity)
- leaf i: SHA-256( 0x00 || sha256(file_i bytes) ), i = 0..1890 in sorted-path order
- parent: SHA-256( 0x01 || left || right ); append-only MMR, peaks are unmerged
  subtree roots, heights strictly decreasing left to right
- bagging: bag = rightmost peak; for each earlier peak left-to-right scanned
  right-to-left: bag = SHA-256( 0x01 || peak || bag )
- ROOT: SHA-256( 0x03 || bag || leaf_count_u64_little_endian )
- Expected peaks: heights 10, 9, 8, 6, 5, 1, 0 (7 peaks)

## Frozen values (computed pre-broadcast, deterministic)
MMR ROOT: 2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a
Leaf count: 1891
Corpus commit: 7c492528c9f9624bb43846b745df9a480f4d1600

## Payload envelope
SQDR + 0x05 + 32-byte MMR root (37 bytes; hex-ASCII on UTF-8 rails, per payload doctrine
Section 2.5). Version byte 0x05 = MMR root covenant (CFR-9 used 0x04).

## Protocol
1. Prereg + scope stamp mcr1_covenant_2026-10-19 written before first broadcast.
2. Crossfire on all ten certified rails, latency-ranked fire order (CFR-9 doctrine):
   SOL, ALGO, AVAX, XLM, XRP, DOT, ADA, ETH, DOGE, BTC.
3. Keyless read-back on every rail; byte-exact required.
4. Runlog with per-leg receipts; ledger entry (next open) awaits Leon GO per two-key gate.
5. Inclusion-proof receipts: at least five leaves verified against the root in-run
   (indices 0, 1, mid, last, plus LEDGER.md), published with the runlog.

## Gate checks (deterministic, no LLM in the decision path)
G1: MMR root matches the frozen value above, recomputed deterministically from the corpus commit
G2: scope stamp present and unique before first broadcast
G3: every leg keyless-readable and byte-exact (the 37-byte envelope decodes to the frozen root)
G4: all fees recorded; failed attempts disclosed forward-only
G5: read-back of at least one leg by an independent public endpoint

## What this closes (and opens)
The covenant: future artifacts join the mountain as new leaves; every future anchor
carries only the new peak/root — the chain stores 32 bytes forever, the corpus grows
without bound. Storage is endless because the anchor never scales.
