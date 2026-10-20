# TL-1 The Trustable Lock — A Tokenized Lumen, Three Chains, Nine Cents
**SQUIRL OS Technologies — Research Note | 2026-10-20 | Ledger 0286 | Page update only (no DOI minted)**

## The story: tokenization without a token sale

What is the cheapest thing that can honestly be called tokenization? We ran it to find
out. One Stellar lumen, tokenized in place: the vessel account (GDIQGG...VLT5) holds the
lumens AND the ownership record in the same account, on the same chain, readable by any
browser. No smart contract, no bridge, no custodian, no launchpad.

The asset being tokenized is a research artifact: the FL-1 breakthrough note — the
record of the first fractal fraction ever leased by Bitcoin consensus, the first
taproot script-path spend in the program. Its canonical original lives off-chain at the
DOI (https://doi.org/10.5281/zenodo.23515307, sha256 61de4811...5b733). That is the
redundancy doctrine: the original lives on a separate system, and the chains carry
mutually verifiable receipts that point at it. No single ledger is trusted alone.

## The payload — 37 bytes, three consensus domains

Envelope: SQDR + 0x0E (TL receipt) + 32-byte digest.

DIGEST 6650efc9e393e9b1824fd7caba28ae67f88210727a03132c798fac5cadaafc9c
= SHA256("SQDR-TL-1|" || manifest sha 3be6562f... || "doi:10.5281/zenodo.23515307"
  || artifact sha 61de4811...5b733)

The digest binds four things in one fingerprint: the ceremony ID, the manifest (what
this receipt claims), the DOI (where the original lives), and the artifact hash (that
the original is intact). Deterministic, keyless to verify, no LLM in the decision path.

## The lock — three receipts, all byte-exact keyless read-back (3/3)

1. THE TOKEN — Stellar: data entry SQDR-TL-1 on the vessel account, ledger 65050475.
   https://stellar.expert/explorer/public/tx/23054d29954ac90996d94c1a059a5d9a709ad9cd4e10011b8c9cb05f66ef92e9
2. THE ATTESTATION — XRP: memo-borne copy, VALIDATED by ledger close.
   https://livenet.xrpl.org/transactions/B9AB81D28F2684BAD52119845065B2F6C720B4CD37B0F62F167449993E500A99
3. THE MARK — Bitcoin: one OP_RETURN output, tamper-proof on the most conservative
   ledger in existence. Byte-exact in mempool read-back; block follows on its own.
   https://mempool.space/tx/078787db6537c3294b41a5fffade685a7ff04fc36ccc20502cc3799be8b4e278

Three consensus domains must all lie for the record to break. That is the trustable lock.

## What it cost

100 stroops + 10 drops + 790 sats ≈ $0.09 total, build to verified in ~2 minutes.
Tokenization, attestation, and tamper-proof archival for less than a dime.

## Defects disclosed (ledger 0286, TL1_RUNLOG.md)

1. BTC leg first build passed a hex string instead of bytes to the writer — local build
   error, nothing broadcast; fixed and refired clean.
2. The read-back script stripped the wrong OP_RETURN prefix (6a vs 6a25) and initially
   misreported the BTC payload as a mismatch — the payload was byte-exact throughout;
   corrected before any public claim.

*This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects on them.*
