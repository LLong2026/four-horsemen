# MCR-2 PREREGISTRATION — THE MOUNTAIN UPDATE (append-only MMR root re-anchor)
Frozen BEFORE any broadcast. 2026-10-20 ~01:12 CT. Leon GO (chat authorization, 2026-10-20 ~00:50 CT).

## What the ceremony proves
The corpus has grown (1,891 -> 1,906 files) and the mountain must be re-anchored. The
entire public evidence record — now including the SQUIRL-OS-IP-013 patent record and its
Zenodo DOI 10.5281/zenodo.23491295 — is re-folded into one Merkle Mountain Range whose
new 32-byte root is anchored across all ten certified mainnet rails. This is the first
MOUNTAIN UPDATE under the IP-013 doctrine: the prior MCR-1 root stays sealed on-chain,
unmodified, on every rail; the update chain is itself a verifiable object. Storage
remains endless: the on-chain footprint is still exactly 37 bytes no matter how large
the corpus grows.

## Corpus (frozen)
The exact git tree of commit bf13210 (the IP-013 corpus-fold commit, origin/main HEAD):
1,906 tracked files, paths in byte-sorted order, as enumerated in MCR2_LEAF_INDEX.json
(published with the runlog; the corpus is rebuildable by anyone from the public repo at
that commit). Includes the new leaves: SQUIRL-OS-IP-013_MMR_STORAGE_COVENANT_DRAFT.md,
SQUIRL-OS-IP-013_MMR_STORAGE_COVENANT_SPEC.pdf (sha256 22441aa77f0501c3a855b6f3124cf48935549db70e8e4a100ae04ef890a1be3c),
IP013_ZENODO_RECEIPT.json — the patent DOI is literally inside the mountain.

## MMR construction (unchanged from MCR-1, byte-exact)
- leaf i: SHA-256( 0x00 || sha256(file_i bytes) ), i = 0..1905 in sorted-path order
- parent: SHA-256( 0x01 || left || right ); append-only MMR, peaks are unmerged
  subtree roots, heights strictly decreasing left to right
- bagging: bag = rightmost peak; scanning right-to-left over earlier peaks:
  bag = SHA-256( 0x01 || peak || bag )
- ROOT: SHA-256( 0x03 || bag || leaf_count_u64_little_endian )
- Expected peaks: heights 10, 9, 8, 6, 5, 4, 1 (7 peaks)
- Builder validated first: rebuilding MCR-1's corpus (7c492528, 1,891 files) reproduced
  root 2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a and all 7
  peaks byte-exact (G1-VALIDATE PASS, 2026-10-20 ~00:57 CT).
- Append-only continuity evidence: the height-9 peak e173493cc6714cd17a9b1d9dfa25127f7e572a3ce25ddddb4672f052b0a0b2d6
  is IDENTICAL to MCR-1's height-9 peak — the first 1,536 leaves are unchanged.

## Frozen values (computed pre-broadcast, deterministic)
MMR-2 ROOT: 1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60
Leaf count: 1906
Corpus commit: bf13210
Parent covenant: MCR-1 root 2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a (ledger 0260)

## Payload envelope
SQDR + 0x06 + 32-byte MMR-2 root (37 bytes; hex-ASCII on UTF-8 rails, per payload
doctrine Section 2.5). Version byte 0x06 = MOUNTAIN-UPDATE covenant (MCR-1 used 0x05;
registered forward-only in this prereg). Rail-specific tags: XRP memo_type and Stellar
data_name = "SQDR-MCR-2"; Cardano aux metadata CER = "MCR-2".

## Protocol
1. Prereg + scope stamp mcr2_mountain_update_2026-10-20 written before first broadcast.
2. Crossfire on all ten certified rails, latency-ranked fire order (CFR-9 doctrine):
   SOL, ALGO, AVAX, XLM, XRP, DOT, ADA, ETH, DOGE, BTC.
   DOGE spends the MCR-1 change output (4dc643c4...b0bd:1, 14.80 DOGE), verified unspent
   pre-broadcast. BTC spends the largest writer UTXO via the proven dropbox software path.
3. Keyless read-back on every rail; byte-exact required (37-byte envelope decodes to the
   frozen MCR-2 root).
4. Runlog with per-leg receipts; ledger entry (next open) binds this update to its parent
   per Leon GO under the two-key gate.
5. Inclusion-proof receipts: at least five leaves verified against the new root in-run
   (indices 0, 1, mid, last, plus LEDGER.md), published with the runlog.

## Gate checks (deterministic, no LLM in the decision path)
G1: MMR-2 root matches the frozen value above, recomputed deterministically from the
    corpus commit; builder pre-validated against the MCR-1 frozen root
G2: scope stamp present and unique before first broadcast
G3: every leg keyless-readable and byte-exact (the 37-byte envelope decodes to the
    frozen MCR-2 root)
G4: all fees recorded; failed attempts disclosed forward-only
G5: MCR-1 anchors verified UNMODIFIED on every rail post-update (append-only doctrine;
    spot-check at least BTC, XRP, XLM)

## Honest scope statements
- The chain stores the 32-byte commitment, not the corpus; "the entire internet fits in
  one root" is a statement about the commitment, not on-chain storage.
- Prototype disclaimer applies. Dual Mesh Benchmark: NOT MEASURED (no neural-mesh
  inference involved; deterministic ceremony).
- Operator privacy: authorization recorded as Leon GO (chat authorization, 2026-10-20
  ~00:50 CT); no operator text quoted anywhere.
