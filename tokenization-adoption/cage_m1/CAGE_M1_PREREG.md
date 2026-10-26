# CAGE-M1 PREREG — LLM-CAGING MOUNTAIN GENESIS (2026-10-25)

Frozen before any broadcast. New dedicated series, distinct from the MCR corpus
series (MCR-1..4 fold the whole public repo; CAGE-M1 folds a dedicated caging
corpus). Series rationale: owner-directed second mountain (chat authorization,
2026-10-25), triad-anchored; MCR-4 root 38089f07... remains frozen on twelve rails.

## Scope
Genesis fold of the dedicated LLM-caging corpus at
tokenization-adoption/cage_m1_corpus/ — every file in the folder is a leaf,
sorted by UTF-8 byte order of path, no selection, no exclusions. Starting point
per owner: the Caging-of-LLM paper plus today's caging update.

## Corpus (4 leaves)
- Deterministic_Caging_of_Probabilistic_LLMs_v1.1.pdf
  sha256 b03bd77a5752a481a2ef523231ea874adc65262ec7521316ab0de9604009cd31
  (published DOI 10.5281/zenodo.23284729, round-trip verified)
- TROPHY_ROSTER.csv
  sha256 02886ea4e7dd58ea98e1cb043ef1f0c56bc99dd52c27ab80e88bbdfcf14c9b88
- cage_watch_feed.json (today's feed regen, 58 recorded cycles)
  sha256 70a1310b4fe43fac41d05960ac29277c41b44cad89242abae102148e1aebcbbe
- hemi_n_receipt_20261025.json (today's falsifier epoch, all_pass)
  sha256 a57a4a873a553f231978f938b0e76707f25e13d450cd0268ec4ad0dee37db14b

## Covenant (frozen MCR-1 spec, byte-identical to corrected mcr4_fold.py)
leaf = SHA-256(0x00 || sha256(file)); parent = SHA-256(0x01 || L || R);
peaks bagged right-to-left (bag starts at rightmost peak, then
bag = SHA-256(0x01 || peak || bag) leftward);
root = SHA-256(0x03 || bag || leaf_count u64 LE).

## Predictions (falsifiable)
- Root: 3bde5c53278573962e93c87bed912612d263def15748398e5b73d4aa91db461e
  (4 leaves, single peak height 2, digest
  8db84b7caa02d773a5d60d5c48491309847fe438de998a7a0f2840277e04d56f).
- Envelope: SQDR + 0x07 + root (CAGE series version byte, new;
  hex-ASCII payload 5351445207 + root on UTF-8 rails, raw on binary rails).
- Fold determinism: cage_m1_fold.py fold() verified byte-identical to
  mcr4_fold.py fold() on random leaf sets (n=1,2,3,4,7,12,33) before freeze.

## Hypotheses
- H1: The committed corpus folds to the predicted root byte-identical from the
  committed tool (determinism gate PASS pre-freeze).
- H2: All three triad legs (XLM, XRP, BTC) carry the envelope byte-exact with
  independent public keyless readback 3/3.
- H3: The MCR-4 root and its twelve anchors are unaffected (no MCR series
  artifact touched by this genesis).

## Gates (deterministic)
- G1 root-frozen: root recorded here before any broadcast.
- G2 stamp-before-execute: RateLimitLog scope cage_m1_mountain_genesis_2026-10-25
  before the first leg.
- G3 byte-exact readback: every leg verified from a public endpoint not used
  for broadcast.
- G4 disclosure: any leg failure, retry, or defect disclosed in the runlog.
- G5 prereg immutability: this file committed before the first broadcast; no
  post-hoc edits (forward-only corrections in new commits only).

## Cost envelope
Triad: XLM 100 stroops, XRP 10 drops, BTC ~800 sats (1 sat/vB class).
Expected total under $0.20. Any wallet shortfall disclosed, never skipped
silently.

Prototype disclaimer applies. No client data, no PHI (POL-DISC-001).
