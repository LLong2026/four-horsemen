# PROVISIONAL PATENT APPLICATION DRAFT — FOR FILING
## "CONSTANT-FOOTPRINT CORPUS COMMITMENT VIA MERKLE MOUNTAIN RANGE COVENANTS AND APPEND-ONLY MOUNTAIN UPDATES ACROSS HETEROGENEOUS DISTRIBUTED LEDGERS"

Docket: SQUIRL-OS-IP-013 (draft for filing by inventor; application serial assigned by USPTO)
Inventor: Leon Calvin Long, II (SQUIRL OS Technologies LLC)
Draft date: 2026-10-20. Reduction to practice evidenced below. Prototype disclaimer applies.
This draft is not legal advice.

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

Related co-pending portfolio (same inventor): 64/157,915; 64/119,191; 64/114,746; 64/145,825;
64/174,933; 19/693,343; 64/081,490; 64/081,911; 64/082,606 (cross-ledger anchoring), and the
companion drafts SQUIRL-IP-011 ("Caging the Large Language Model") and SQUIRL-OS-IP-012
("Multi-Rail Non-Custodial Evidence Anchoring and Route Certification"). This application
is directed to the whole-corpus commitment layer practiced since 2026-10-19 (MCR-1 forward),
and incorporates the multi-rail anchoring machinery of IP-012 by reference.

## FIELD

Cryptographic commitment structures; Merkle trees and Merkle Mountain Ranges; distributed-ledger
timestamping; archival integrity verification; multi-chain transaction construction.

## BACKGROUND

Blockchain timestamping is sold as "permanent," but on-chain storage is neither free nor
unbounded. Every byte stored on a major chain competes for scarce block space; storage cost
scales linearly (or worse) with the volume of evidence a practitioner wishes to prove. Prior
art therefore anchors individual documents, one digest per transaction, and faces a
structural dilemma: (a) anchor little (lose provability of the corpus as a whole), or
(b) anchor everything (costs grow without bound as the corpus grows).

No prior art known to the inventor commits an arbitrarily large, growing document corpus to
multiple heterogeneous distributed ledgers under a fixed on-chain footprint that does not
grow with the corpus, while retaining per-artifact public verifiability, and while preserving
the historical integrity of every prior commitment as the corpus grows.

## SUMMARY

A system and method in which the complete state of a document corpus — every file, receipt,
ledger, publication, and proof bundle — is folded, at a frozen configuration, into a single
Merkle Mountain Range (MMR) whose 32-byte root is the corpus's entire on-chain
representation. The root is anchored, with a protocol envelope, across a certified set of
heterogeneous distributed ledgers ("rails"). The on-chain footprint is constant: 32 bytes
of commitment regardless of whether the corpus holds one thousand files or one billion.
Any individual artifact remains publicly verifiable from the bare corpus plus one on-chain
root, using a logarithmic-length inclusion path (~ceil(log2 N)) — no trusted server, no
proprietary index, no per-artifact chain transaction.

The mountain is append-only. When the corpus grows, the updated corpus is re-folded into a
new MMR and the new root is re-anchored across the rails ("mountain update"); every prior
anchored root remains sealed on-chain, so the update history is itself publicly verifiable,
and each update is a constant-cost event. Storage of the corpus itself is off-chain and
unbounded; the chain stores only the integrity commitment. The corpus may thus be of
arbitrary size — in principle up to the size of an archive of the public internet — while
each covenant event costs only the fixed envelope payload (37 bytes) plus per-rail
transaction fees, on the order of satoshis.

Core doctrines reduced to practice:
- WHOLE-CORPUS COVENANT: one MMR over the complete tracked state (git tree) of the
  evidence repository at a frozen commit; no cherry-picking, no partial snapshots.
- FULLY SPECIFIED MMR: leaf, node, bagging, and root constructions are defined
  byte-exactly (domain-separated prefixes 0x00 / 0x01 / 0x03) so that any party can
  rebuild the root from the public corpus without reference implementation ambiguity.
- CONSTANT FOOTPRINT: the anchored payload is the 32-byte root in a fixed 37-byte
  protocol envelope; the on-chain footprint never grows with the corpus.
- APPEND-ONLY MOUNTAIN UPDATES: growth is discharged as a new covenant (new commit, new
  root, new anchor set); prior roots stay sealed on-chain; the chain of roots is a
  verifiable growth history. No prior commitment is ever rewritten.
- MULTI-RAIL REDUNDANCY: the same root is anchored across rails of radically different
  construction (UTXO, account-sequence, metadata-slot, remark-based, manage-data,
  auxiliary-metadata) under the payload doctrine of the parent application, so no single
  chain's failure, reorganization, or economic change can orphan the corpus's proof of
  integrity.
- KEYLESS VERIFICATION: every anchor is read back through public keyless endpoints and
  required to decode byte-exactly to the frozen root before the covenant is sealed.
- INCLUSION-PROOF RECEIPTS: designated leaves (first, last, mid, and named artifacts of
  record) are proven against the root in-run and published with the runlog.

## BRIEF DESCRIPTION OF THE DRAWINGS

FIG. 1 — The covenant cycle: freeze corpus commit -> fold MMR (leaves, peaks, bag, root)
-> anchor root across N rails -> keyless read-back -> append-only seal.

FIG. 2 — The mountain-update cycle: corpus grows -> re-fold -> new root -> re-anchor ->
both roots remain sealed on-chain -> verification accepts any root in the chain.

FIG. 3 — An inclusion proof: file -> leaf hash -> O(log N) sibling path -> peak -> bag ->
root -> the 37-byte envelope on each rail.

## DETAILED DESCRIPTION

### The corpus and its freeze

The corpus is the set of tracked files of the evidence repository at a specific commit,
enumerated in byte-sorted path order. Freezing by commit hash makes the snapshot
rebuildable by any party with a copy of the repository; no private state participates.

### The range construction (byte-exact)

For a corpus of N files with contents f_0 ... f_{N-1} in byte-sorted path order:

- leaf_i = SHA-256( 0x00 || SHA-256(f_i) ) — a domain-separated leaf over each file's
  exact bytes.
- Append-only mountain: leaves are added left to right; whenever two subtrees of equal
  height h exist, parent = SHA-256( 0x01 || left || right ), left being the earlier
  subtree. Peaks are the unmerged subtree roots, heights strictly decreasing left to
  right.
- Bagging: bag = rightmost peak; scanning right-to-left over the remaining peaks,
  bag = SHA-256( 0x01 || peak || bag ).
- ROOT = SHA-256( 0x03 || bag || N as 64-bit little-endian ).

The domain-separation bytes (0x00, 0x01, 0x03) and the u64-LE leaf count bind the
construction against second-preimage and length-extension ambiguity; the specification
is complete enough to re-derive the root from the public corpus alone.

### The envelope and the rails

The root travels in a fixed envelope: protocol marker ("SQDR"), version byte (0x05 =
root covenant; 0x06 = mountain-update covenant), and the 32-byte root — 37 bytes total,
encoded per each rail's payload doctrine (hex-ASCII where the rail requires UTF-8
memo fields; raw bytes where binary note fields are supported), as specified in the
parent application. Each certified rail carries the identical envelope; the anchor set
is the covenant.

### Read-back and seal

Each anchor is read through a public keyless endpoint (explorer or public RPC) and must
decode to the exact 37-byte envelope and the frozen root; any mismatch fails the gate.
On pass, identifiers, fees, latencies, and any failed attempts are sealed forward-only
in the public ledger, and the runlog is committed with the leaf index.

### The mountain update (the growth doctrine)

When the corpus grows, the method does not modify prior anchors. It re-folds the new
state into a new MMR, producing a new root; the new root is anchored across the rails
with the update version byte; the ledger binds the update to its parent covenant.
Verification of historical artifacts continues against the historical root; verification
of new artifacts proceeds against the new root. The result: unbounded corpus growth at
constant marginal proof cost, with a self-verifying history.

### Scope and honesty limits

This draft claims the commitment protocol and its multi-rail discharge, not a claim that
blockchains store the corpus. The data lives off-chain; the chain stores the constant-
size integrity commitment. "The entire internet fits in one root" is a statement about
the commitment, not on-chain storage: any off-chain archive, however large, has a
32-byte fingerprint that can be anchored for the cost of one transaction.

## CLAIMS (draft)

1. A method for committing a corpus of digital artifacts to a plurality of heterogeneous
   distributed ledgers under a constant on-chain footprint, comprising: folding the exact
   tracked state of said corpus at a frozen commit into a Merkle Mountain Range whose
   construction is fully specified by domain-separated hash rules; deriving a single
   32-byte root; constructing a fixed protocol envelope containing said root; anchoring
   said envelope across a certified plurality of ledgers of differing transaction models;
   and verifying each anchor through keyless public reads requiring byte-exact decode.
2. The method of claim 1, wherein said Merkle Mountain Range construction comprises:
   leaf hashes of the form SHA-256(0x00 || SHA-256(file bytes)) over files in byte-sorted
   path order; internal nodes of the form SHA-256(0x01 || left || right) for equal-height
   adjacent subtrees, left being the earlier subtree; a bagging of peaks right-to-left
   under the same node rule; and a root of the form SHA-256(0x03 || bag || leaf count
   as 64-bit little-endian).
3. The method of claim 1, wherein growth of said corpus is discharged by re-folding the
   updated state into a new root and anchoring said new root while all prior anchored
   roots remain unmodified on-chain, producing an append-only, publicly verifiable
   history of corpus states.
4. The method of claim 1, wherein the on-chain representation of said corpus is exactly
   one 32-byte value per rail regardless of the size or growth of said corpus.
5. The method of claim 1, wherein any single artifact of said corpus is verifiable from
   the public corpus, any anchored root, and a logarithmic-length inclusion path, without
   per-artifact ledger transactions and without trusted third parties.
6. The method of claim 1, wherein said rails include at least two of: a UTXO model rail
   carrying the envelope in an OP_RETURN-style output; an account-sequence rail carrying
   the envelope in transaction calldata; a rail carrying the envelope in a memo field;
   a rail carrying the envelope in a remark; a rail carrying the envelope in managed
   account data; and a rail carrying the envelope in auxiliary transaction metadata.
7. The method of claim 1, wherein a distinguished set of leaves, including at least the
   first leaf, the last leaf, a middle leaf, and a designated artifact of record, are
   proven against said root and published as inclusion-proof receipts contemporaneous
   with the covenant.
8. A system comprising: a corpus under version control; a deterministic MMR folder
   implementing the construction of claim 2; a plurality of certified rail writers
   holding only sufficient balance for transaction fees; and a verification module
   performing keyless byte-exact read-back, such that no custodian of the corpus can
   alter any artifact without changing the root and thereby falsifying every rail
   simultaneously.
9. The method of claim 3, wherein each update covenant is bound to its parent covenant
   by a public ledger entry referencing both roots, such that the chain of roots is
   itself a verifiable object.
10. The method of claim 1, wherein the protocol envelope comprises a version byte
   distinguishing a first anchoring of a root from a mountain-update anchoring of a
   subsequent root.

## ABSTRACT

A whole-corpus cryptographic commitment system in which a document repository's complete
frozen state is folded into a Merkle Mountain Range and represented on heterogeneous
distributed ledgers by a single 32-byte root in a fixed 37-byte envelope, giving
constant on-chain footprint independent of corpus size; corpus growth is discharged by
append-only mountain updates whose prior roots remain sealed on-chain; and any
individual artifact remains publicly verifiable from the corpus, one anchored root, and
a logarithmic inclusion path.

## REDUCTION-TO-PRACTICE EVIDENCE CHAIN (receipts-first, all public)

- MCR-1 "Merkle Root Covenant" (2026-10-19): 1,891-leaf MMR over the four-horsemen
  evidence repository at commit 7c492528, root
  2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a anchored across
  all ten certified mainnet rails (BTC, XRP, ETH, SOL, ADA, ALGO, AVAX, DOT, DOGE, XLM),
  byte-exact keyless read-back on each; public ledger entry 0260; the present filing's
  MMR construction is the MCR-1 construction, re-validated byte-exact against the frozen
  root before the update ceremony of 2026-10-20.
- MCR-2 "Mountain Update" (2026-10-20, this filing's DOI ceremony): corpus grown to
  ~1,905 files including this patent record; new root anchored across the same ten
  rails; prior MCR-1 root unmodified on every rail; update bound in the public ledger.
- Payload doctrine, thesis v2.1 DOI 10.5281/zenodo.23482978 (Section 2.5, 37-byte
  envelope conventions); routing chapter DOI 10.5281/zenodo.23485222; DCAI corpus
  community (Zenodo).
- Route certification: DeWR-1 (10-rail certification), CFR-9 (10-leg crossfire,
  10/10 confirmed), SBR-1 (XRP rail-of-record / Stellar transport burst, 8 anchors,
  ~4 seconds, ~one-hundredth of a cent) — all sealed in the public ledger.

## FILING NOTES (inventor steps; verify against the current USPTO fee schedule)

1. Patent Center -> New application -> Provisional (SB/16).
2. Title as above; inventor Leon Calvin Long, II; small entity; pro se.
3. Upload this specification PDF as the only attachment; use the web cover sheet.
4. Copy the serial number; send to the agent chat for the IP ledger update.

## DISCLOSURE DOCTRINE

AI-assisted, inventor-directed drafting under the receipts-first program: every
reduction-to-practice claim above is anchored to a public, keyless-verifiable
transaction. Errors, if found, are disclosed forward-only in the public ledger; the
append-only doctrine applies to this draft. Dual Mesh Benchmark: NOT MEASURED (out of
scope for this filing). Prototype disclaimer: the referenced software is a research
prototype, not a production system.
