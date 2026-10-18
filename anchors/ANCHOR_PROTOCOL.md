# SIP-034 — TRANSPARENCY ANCHOR v1.0 (Protocol)
**Ratified:** Leon GO (chat authorization, 2026-10-17 ~22:23 CT). Deployed: 2026-10-18T03:24Z.

## Design: ANCHOR, NOT A CHAIN
Every sealed transparency artifact (ledger, cage feed, corpus manifests, preregs, receipts)
is committed to the Bitcoin blockchain as a proof-of-existence timestamp via OpenTimestamps.
No tokens, no wallet, no on-chain data beyond SHA-256 digests. Zero PII/PHI/customer identity
ever leaves the repos — only 32-byte hashes cross the boundary (POL-DISC-001 enforced).

## Sealing procedure (bash, deterministic)
1. sha256sum <artifact> — record the digest in the anchor manifest (JSON).
2. ots stamp -c https://alice.btc.calendar.opentimestamps.org -c https://bob.btc.calendar.opentimestamps.org <artifact>
3. Commit the .ots receipt + manifest to this repo. Never modify a stamped artifact afterward
   (append-only doctrine; a changed file needs a NEW stamp, the old stamp remains historical proof).
4. Ledger entry references the artifact hash + .ots receipt filename.

## Verification (anyone, trustless)
pip install opentimestamps-client
ots upgrade <file>.ots && ots verify <file>.ots   (upgraded stamps verify against a Bitcoin node)
Pending stamps confirm on-chain once the calendar's next Bitcoin commitment lands (typically
hours). `ots info` shows attestation status. Verification requires trusting no one: the Bitcoin
PoW chain is the notary.

## Honest disclosure (PQC doctrine)
Bitcoin's own signatures (ECDSA/Schnorr) are not post-quantum. The anchor provides
tamper-evident EXISTENCE PROOF only; the authority layer remains the PQC-signed records
(CRYSTALS-Dilithium3 / kyber_1024 / SPHINCS+-256f doctrine). This split is disclosed by
design: hash-level anchoring now, chain-level PQC migration tracked externally. No non-PQC
cryptographic scheme is used for any SQUIRL OS authority function.

## Anchored 2026-10-18T03:24Z
- LEDGER.md (entries through 0161) — sha256 d6f78786e714f48a1e805dd82e9aef77848e2783e5ed5cf78ac142aeab74d542
- cage_watch_feed.json — sha256 c129f776e239f563be6dad0852460f904fe1634636b7d9d69a233b0aa2a2037c
- ANCHOR-MANIFEST-2026-10-18.json (self-hash: see manifest)
Receipts: OTS-2026-10-18-ledger.ots / -cage_feed.ots / -anchor_manifest.ots (pending → Bitcoin)
