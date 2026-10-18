# DCAI / SQUIRL OS — COMPLETE PUBLIC RECEIPTS CORPUS (as of 2026-10-18)

This is the receipts documentation layer of the SQUIRL OS open-book research program:
every prereg, runlog, receipt, spec, and index committed to the public four-horsemen
repository through ledger entry 0194, plus the Bitcoin anchor registry that notarizes them.

CONTENTS
- LEDGER.md — the append-only public transparency ledger, entries 0001-0194
- DCAI_DOI_INDEX.md — every Zenodo DOI cited in the ledger (93 records)
- *.md (root) — all preregistrations, runlogs, receipts, specs, and indexes
- anchors/ — the Bitcoin anchor registry: manifests, OTS stamps, reconciliation
  and examiner evidence (SIP-034 through SIP-041 chain-of-custody stack)
- tokenization-adoption/seed-mode/ — the DROPBOX seed/digest drop tooling, preregs,
  receipts, and today's two permanent mainnet anchors (patent seed block 972023,
  IP ledger digest block 972026)

HOW ANYONE CAN VERIFY (three tiers)
1. Zenodo: every DOI in the index resolves to a public, citable record with files.
2. Bitcoin: ledger and corpus states are notarized in the Bitcoin blockchain
   (anchor blocks include 971956, 971961, 972023, 972026). Verify any anchored
   artifact by re-hashing it and checking the OTS stamp / OP_RETURN anchor.
3. Git: the full commit history is public at github.com/LLong2026/four-horsemen —
   every entry here has a commit hash, forward-only from Sept 7, 2026.

Dual Mesh Benchmark status: MEASURED (scoped) — DOI 10.5281/zenodo.23345241
(DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.

<em>This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects. All battery payloads
are synthetic.</em>

Publication: two-key curation — drafted and vetted by the system (Gabriel), published
on the owner's explicit GO (chat authorization, 2026-10-18 ~11:51 CT).
