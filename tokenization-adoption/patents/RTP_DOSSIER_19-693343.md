# REDUCTION-TO-PRACTICE DOSSIER — Patent 19/693,343 ("The Hash Is the Artifact" / seed mode)
Assembled 2026-10-18 for owner and patent counsel. Receipts-first; every claim links to a
committed record. Prototype disclaimer applies. Not legal advice.

## Subject
US application 19/693,343 (full application; one of ten co-pending: nine provisionals
incl. 64/157,915, 64/119,191, 64/114,746, 64/145,825, 64/174,933 + this full app).
Subject matter: dual-mode evidence receipts with seed-reconstructed originals — a 32-byte
seed deterministically regenerates the full artifact; the hash IS the artifact.

## Refile status — THREAD ZERO (PENDING OWNER INPUT)
Owner states 19/693,343 was refiled under a new application he calls "Thread Zero."
No Thread Zero record exists in the public ledger, notes, or four-horsemen corpus as of
2026-10-18; the private portfolio repo (squirlos-technologies, private) was not reachable
from the hub session. NEEDED FROM OWNER: application number, filing date, exact title,
and confirmation whether it claims priority to 19/693,343. Add to the IP ledger on receipt.

## Reduction-to-practice evidence chain (chronological)
1. 2026-10-14 — Genesis artwork minted from 32-byte seed (4f539b5f...d939859), double
   reconstruction byte-identical (90a30490...136c52d7). Ledger 0182, gate verification 24/24.
2. 2026-10-16 — Patent Genesis Series No. 1 memorializing 19/693,343 minted from seed
   81d4a5cb...c456c; canonical v1.1 artifact 3c130d66...de69. DOI 10.5281/zenodo.23447609.
   Disclosed v1.1 rendering correction (original seed and anchor unchanged).
3. 2026-10-16 — Zero-Trust Examiner Box (Genesis Viewer) live: public in-browser
   reconstruction from the hash, no Python, no keys. https://deterministic-code-dsos.base44.app/genesis-viewer
4. 2026-10-17 — Technical paper "The Hash Is the Artifact: Dual-Mode Evidence Receipts
   with Seed-Reconstructed Originals, Notarized on the Bitcoin Blockchain."
   DOI 10.5281/zenodo.23448049. SIP-042 DROPBOX protocol spec (sha 25a45075).
5. 2026-10-18 — DROPBOX-T4-001: first live drop-and-recover loop, Bitcoin TESTNET4
   (ledger 0191). Seed sealed in OP_RETURN, keyless reader DELIVERED, byte-identical
   reconstruction from the chain-pulled seed.
6. 2026-10-18 — DROPBOX-M1-001: FIRST MAINNET PERMANENT DROP. Patent genesis seed
   81d4a5cb...c456c sealed in OP_RETURN, tx 97d8cd38...a5b89, BLOCK 972023, postage 790 sats.
   Keyless reader pulled the seed from chain; reconstruction from the chain-pulled seed
   BYTE-IDENTICAL (3c130d66...de69). All preregistered gates G1-G6 PASS (prereg M-DROP-1
   frozen pre-broadcast, sha 95c322ea...785de). DOI 10.5281/zenodo.23455768. Ledger 0192.

The invention works for its intended purpose: an artifact is permanently, trustlessly
recoverable from 32 bytes on Bitcoin by a keyless reader. Working reduction to practice,
timestamped independently by: Bitcoin proof-of-work (block 972023), Zenodo DOI record,
and git commit history (four-horsemen, commits 0e03d11, 85bc3ff, cf8753d).

## Disclosure chronology (grace-period accounting; inventor = discloser in all cases)
- Earliest public disclosure of the subject matter: the Patent Genesis DOI (2026-10-16)
  and the technical paper DOI (2026-10-17) precede the mainnet drop (2026-10-18).
- US 12-month inventor grace period runs from the FIRST such disclosure.
- Non-US: strict novelty jurisdictions may treat these disclosures as prior art against
  any LATER filing on the same claims — material to the Thread Zero refile strategy.
- For each disclosure: who (inventor), what (subject matter disclosed), when (DOI dates,
  block timestamps), where (Zenodo, Bitcoin mainnet, public viewer site).

## Counsel verification kit
- Evidence bundle: zenodo.org/records/23455768 (runlog, prereg, writer+reader, chain-pulled
  seed, reconstructed artifact — re-runnable).
- Ledger of record: github.com/LLong2026/four-horsemen (LEDGER.md, entries 0182, 0189-0193).
- Three-tier verification: browser (Genesis Viewer) / examiner (bundle tools) /
  skeptic (fetch block 972023, parse the OP_RETURN, hash what you find).
