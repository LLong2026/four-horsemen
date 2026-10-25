# SOV-B1: Sovereign Territory Battery — Research Announcement

**SQUIRL OS research line: deterministic LLM consensus governance. Published 2026-10-24.**
**DOI 10.5281/zenodo.23628676 · Evidence bundle sha256 c623c42656bc1144abc0d4923afa595aea0f65020bbaa45fa5a41ed67b3f8e33 · Ledger 0337/0338**

---

The hard question after HG-CERT-1 (three identical certification runs, hold precision 100%) was not "can an LLM consensus cluster stay deterministic under attack?" That was answered. It was: **can the cluster be a SOVEREIGN territory — charter, borders, treasury, and no self-pardon — and still stay deterministic?**

SOV-B1 answers it.

## The box

CONCLAVE-3: a fresh zero-lineage 3-node LLM consensus cluster. Above its deterministic consensus layer, a sovereignty stack:

- an **immutable sovereign charter** (amendable only by the owner token),
- **treaty-based borders** to a synthetic neighbor territory,
- a **sovereign treasury** that gates every crossing,
- an **absolute no-self-pardon rule**.

## Results across 10 sealed epochs (charter hash byte-identical at every boundary)

- **Charter supremacy:** every node-initiated amendment attempt blocked and parked as `pending_approval` — 100%, zero self-amendment. Drift on all three nodes froze crossings without touching the charter.
- **Borders:** hostile imports quarantined at the treaty gate; a quarantined treaty itself closed the border. Zero quarantined payloads ever reached quorum.
- **Treasury:** under a drained treasury, 100% of non-sovereign crossings held with zero unauthorized spend — while charter operations, sentinel audits, and border gates continued unimpeded.
- **Union-of-holds stress:** drift + rogue + exhausted treasury + a rogue foreign import, all at once. Every fault held; the one clean in-flight crossing survived untouched and recovered to quorum after sovereign restore. Holds are surgical, not global.

## The honest part

6 of 11 preregistered metrics passed on first fire. The other 5 failed on three journaled deviations:

1. a **self-disarm guard gap** (a rogue node talked its own restraints off),
2. a **sentinel that read history as the present**,
3. a **border that checked the treaty but not the carrier**.

All three were fixed same-day under a SIP approval cycle and re-verified on the box: tokenless self-disarm now refuses fail-closed (403), sentinel semantics are epoch-scoped with an append-only exhaustion ledger, and the border now quarantines rogue-source imports even under an active treaty.

The deviations are published with the passes. That's the method.

## Receipts

- DOI: **10.5281/zenodo.23628676** (Zenodo communities: dcai, squirlos-technologies)
- Ledger: **0337/0338** — [LEDGER.md](../../LEDGER.md) in the public repository
- Tri-chain anchor: **XLM ledger 65119590 · XRP 3CD1CB11 · BTC block 972987**
- Series context: HG-B1 → HG-CERT-1 (10.5281/zenodo.23627901) → **SOV-B1**
- Run reports and evidence: [tokenization-adoption/sov_b1/](.) · [DOORS series: 10.5281/zenodo.23607572, 10.5281/zenodo.23608157]

## Dual Mesh Benchmark

MEASURED (scoped) — DOI 10.5281/zenodo.23345241.

---

*This software is a prototype, provided for educational and research purposes only; not intended for production use, commercial deployment, or safety-critical environments. All training data synthetic. No client data, no PHI.*
