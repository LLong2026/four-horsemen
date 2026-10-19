# PROVISIONAL PATENT APPLICATION DRAFT — FOR FILING
## "MULTI-RAIL NON-CUSTODIAL EVIDENCE ANCHORING AND ROUTE CERTIFICATION ACROSS HETEROGENEOUS DISTRIBUTED LEDGERS"

Docket: SQUIRL-OS-IP-012 (draft for filing by inventor; application serial assigned by USPTO)
Inventor: Leon Calvin Long, II (SQUIRL OS Technologies LLC)
Draft date: 2026-10-19. Reduction to practice evidenced below. Prototype disclaimer applies.
This draft is not legal advice.

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

Related co-pending portfolio (same inventor): 64/157,915; 64/119,191; 64/114,746; 64/145,825;
64/174,933; 19/693,343; 64/081,490; 64/081,911; 64/082,606 (cross-ledger anchoring), and the
companion draft SQUIRL-OS-IP-011 ("Caging the Large Language Model"). This application claims
the benefit of the earliest-filed co-pending provisionals to the extent permitted, and is
directed to the multi-rail anchoring, custody, and route-certification system practiced since
2026-10-18 (DWR-1 forward).

## FIELD

Distributed-ledger technology; cryptographic timestamping and evidence anchoring; multi-chain
transaction construction; transaction routing; intellectual-property provenance.

## BACKGROUND

Anchoring a document's cryptographic digest to a blockchain proves existence and integrity at
a point in time. Prior art anchors to a single chain. Single-chain anchoring has structural
weaknesses: (a) the anchoring chain can fork, reorganize, or change fee economics; (b) no
single chain simultaneously optimizes permanence, finality speed, cost, and verifiability;
(c) chains differ radically in transaction construction (UTXO vs. account vs. sequence-based
vs. metadata-slot models), so a practitioner anchoring across chains today hand-codes each
rail with bespoke, error-prone tooling; (d) ownership-based anchoring (transferring an
inscription between wallets) has not been combined with non-custodial digest anchoring under
one deterministic protocol; and (e) no prior art ranks or selects rails by measured
performance, or certifies rails by staged rehearsal before production use.

## SUMMARY

A deterministic, repeatable protocol for anchoring a single cryptographic digest of a frozen
artifact across an arbitrary number of heterogeneous distributed ledgers ("rails"), without
custody of the underlying asset and without minting tokens, together with (1) a staged
route-certification methodology, (2) a measured-performance routing engine, and (3) a
custody-transfer ("crossfire") mode in which ownership of the anchoring carrier is exchanged
between wallets across rails while the anchored artifact remains in a vault.

Core doctrines reduced to practice:
- HASH-ONLY: a 32-byte SHA-256 digest (optionally prefixed with a protocol marker) is the
  only payload; no document, no seed, no asset crosses the chains; no token is minted.
- PREREGISTRATION: the artifact is hashed and the ceremony specification frozen and committed
  BEFORE any broadcast; the protocol's own receipts are re-anchored recursively.
- GATED EXECUTION: a fixed gate sequence (freeze -> build/sign offline -> broadcast with
  idempotency stamp -> keyless read-back -> append-only seal) with no probabilistic component
  in the decision path.
- CANONICAL IDENTIFIER OF RECORD: each rail's identifier of record is defined as the value a
  keyless public explorer returns (not a local library artifact), with per-rail derivation
  rules disclosed; mismatches (e.g., segwit wtxid vs. canonical txid) are caught at read-back.
- TIERED ROUTE CERTIFICATION: rails are certified in stages — T1 key generation, T2 rehearsal
  leg (marked training payload), T3 certification leg (production digest) — before carrying
  production evidence.
- INTELLIGENT ROUTING: legs are ordered by a routing engine using measured per-rail finality
  and cost; observed finality is compared against prediction and deviations raise alerts.
- APPEND-ONLY SEALING: all identifiers, costs, latencies, and failed attempts are recorded
  forward-only in a public ledger; corrections are new entries with disclosed reasons.

## BRIEF DESCRIPTION OF THE DRAWINGS

FIG. 1 — The gate sequence: freeze/preregister -> offline build & sign -> idempotency-stamped
broadcast -> keyless byte-exact read-back -> append-only seal, repeated per rail.

FIG. 2 — N-rail write ladder: Dual (2 rails), Tri (3), Recursive (receipt-of-receipt), Quad
(4), Penta (5), and general N-rail ("deca-write") anchoring of one digest.

FIG. 3 — Crossfire custody mode: a sequence of ownership hops across rails transferring the
digest carrier between wallets while the artifact remains in the vault; any hop's carrier is
verifiable by a keyless reader.

FIG. 4 — Route certification tiers: T1 (key) -> T2 (rehearsal, training marker) -> T3
(certification, production digest) -> production evidence carrying.

FIG. 5 — The intelligent routing engine: measured latency/cost table -> ordered leg execution
-> predicted-vs-observed finality check -> alert on deviation.

FIG. 6 — Canonical identifier doctrine: per-rail identifier derivation
(BTC: double-SHA256 of the non-witness serialization; XRPL: SHA-512 half of a type-prefixed
serialization; Cardano: BLAKE2b-256 of the transaction body; Stellar: network hash over the
envelope; EVM chains: Keccak-256 of the signed payload; Algorand/Avalanche/Solana: native
transaction signatures; Substrate: SCALE-encoded extrinsic hash).

## DETAILED DESCRIPTION — THE STEPS OF THE PROTOCOL

Step 1 (Freeze and Preregister): compute SHA-256 of the canonical artifact; write a
preregistration declaring the artifact, its hash, the wallet roster, the rails, the expected
identifiers where computable offline, the cost ceiling, and the pass gates; commit the
preregistration to a version-controlled repository before any network action. The
preregistration hash proves no post-hoc artifact modification.

Step 2 (Offline Build and Sign): for each rail, construct and sign the anchoring transaction
entirely offline using the rail's native inscription mechanism:
  - Bitcoin: SegWit P2WPKH writer, OP_RETURN data carrier (dust-guarded), BIP-143 signing;
  - XRP Ledger: AccountSet with Memo (zero-movement) or Payment (custody), 10-drop flat fee,
    sequence precomputation from account_info;
  - Stellar: ManageData named entry (zero-movement) or memo_hash Payment, 100-stroop base fee;
  - Cardano: transaction metadata at label 1968, canonical CBOR, BLAKE2b-256 body hash;
  - Ethereum and EVM-compatible chains: zero-value self-addressed calldata inscription in a
    legacy EIP-155 transaction;
  - Algorand: note-field inscription on a zero-value payment or transfer;
  - Avalanche: C-chain calldata inscription (EVM-compatible mode) with measured finality;
  - Solana: SPL Memo program instruction carrying the digest as hex-encoded ASCII with the
    signer account meta (the memo program requires UTF-8 data and a signer account);
  - Substrate-based chains (e.g., Polkadot): System.remark extrinsic carrying the raw digest
    bytes, signed ed25519 with SS58-format address derivation.

Step 3 (Idempotency-Stamped Broadcast): write a scope stamp (write-ahead marker) naming the
ceremony scope before the first broadcast; duplicate triggers for the same scope fail closed.
Legs fire back-to-back (simultaneity mode) or in routing order (sequential mode).

Step 4 (Keyless Read-Back): for each leg, retrieve the inscription from a public endpoint
that requires no credentials and verify the on-chain bytes equal the preregistered digest
byte-for-byte; additionally verify the identifier of record against a public explorer; any
mismatch fails the leg.

Step 5 (Append-Only Seal): record all leg identifiers, fees, latencies, read-back verdicts,
and every failed attempt (fee rejections, sequence staleness, encoding rejections) in a
forward-only public ledger entry; corrections are new entries with disclosed reasons.

Step 6 (Route Certification): a rail is production-certified only after T1 (wallet key
generation with pattern-gitignored key hygiene), T2 (a rehearsal leg carrying a marked
training payload, verified byte-exact), and T3 (a certification leg carrying the frozen
production digest). Certification records per-rail measured finality and cost into the
routing engine's tables.

Step 7 (Intelligent Routing): for a multi-leg ceremony, the routing engine reads the measured
table (finality, cost) and orders legs fastest-first (or cheapest-first per declared policy);
observed finality is compared against prediction; deviation beyond a threshold raises an
operational alert and a note in the runlog.

Step 8 (Crossfire Custody, optional): instead of (or in addition to) inscription, ownership
of the digest carrier is transferred between wallets — across one rail in a chain (custody
chain) or across rails (crossfire) — proving transferable possession of the anchored record
while the artifact itself remains in the vault; every hop is keyless-verifiable.

Step 9 (Recursive Anchoring): the receipt of a completed ceremony is itself frozen,
preregistered, and anchored, producing receipt-of-receipt generations with the same gate
sequence.

## CLAIMS

1. A computer-implemented method for anchoring evidence across a plurality of heterogeneous
   distributed ledgers, comprising: hashing a canonical artifact to obtain a digest; freezing
   a preregistration declaring the digest before any network transmission; constructing and
   signing, offline, one anchoring transaction per ledger, each using the ledger's native
   data-carrying mechanism to embed the digest; broadcasting each transaction under an
   idempotency scope stamp; verifying each embedded digest against its transaction by a
   keyless public read; and sealing the identifiers, costs, and verification results in an
   append-only record.
2. The method of claim 1, wherein no ledger transaction mints, transfers, or encumbers any
   asset other than native transaction fees, and the artifact remains stored off-chain.
3. The method of claim 1, wherein the heterogeneous ledgers include at least: a UTXO ledger
   carrying the digest in an OP_RETURN output; an account-sequence ledger carrying the digest
   in a memo field of a zero-movement transaction; a named-data-entry ledger carrying the
   digest in a managed data entry; a metadata-slot ledger carrying the digest in a labeled
   transaction metadata map; and an EVM ledger carrying the digest in zero-value calldata.
4. The method of claim 3, further comprising a Substrate-based ledger carrying the digest in
   a System.remark extrinsic signed with an ed25519 keypair.
5. The method of claim 1, wherein each ledger's identifier of record is defined as the value
   returned by a keyless public explorer, with per-ledger derivation rules, such that a
   locally computed identifier that differs from the explorer value is detected as a defect
   at verification time.
6. The method of claim 5, wherein the UTXO ledger derivation excludes witness data, whereby
   a locally computed witness-serialized hash (wtxid) cannot be mistaken for the canonical
   identifier.
7. The method of claim 1, further comprising routing: ordering the anchoring transactions
   according to a measured per-ledger table of finality and cost, and comparing observed
   finality against predicted finality, raising an alert when deviation exceeds a threshold.
8. The method of claim 1, wherein certifying a ledger for production use comprises a staged
   sequence: generating a ledger-specific writer key; executing a rehearsal leg carrying a
   marked training payload and verifying it byte-exact; and executing a certification leg
   carrying a production digest and verifying it byte-exact.
9. The method of claim 1, wherein the anchoring transactions are broadcast substantially
   back-to-back to fix a common timestamp across ledgers.
10. The method of claim 1, further comprising recursive anchoring, in which a receipt of the
    completed anchoring is itself hashed, preregistered, and anchored across ledgers,
    producing successive receipt generations.
11. The method of claim 1, further comprising a custody mode in which the digest carrier is
    transferred between wallets in a sequence of hops, each hop verified by keyless read-back,
    while the canonical artifact remains off-chain in a vault.
12. The method of claim 11, wherein hops alternate across different ledgers (crossfire),
    demonstrating cross-ledger possession transfer of a single anchored record.
13. The method of claim 1, wherein failed transaction attempts, including fee rejections,
    stale sequence errors, and encoding rejections, are disclosed in the append-only record
    together with their remediations, and are never silently retried without disclosure.
14. The method of claim 1, wherein the digest is embedded as a protocol-marked payload
    comprising a prefix, a version byte, and the digest, permitting a keyless reader to
    identify the anchoring protocol and version from the on-chain bytes alone.
15. The method of claim 1, wherein writer keys are stored under pattern-based ignore rules
    and verified absent from version control by an automated audit before every commit.
16. A system implementing the method of claim 1, comprising: an offline transaction builder
    for each ledger family; a routing engine consuming measured finality and cost tables; an
    idempotency stamp store; a keyless verification client; and an append-only ledger of
    ceremony records.
17. The system of claim 16, wherein the routing engine's tables are updated from the
    certification legs of claim 8, and the tables record broadcast-to-finality seconds and
    fee units per ledger.
18. A computer-readable medium carrying instructions for the method of claim 1.
19. The method of claim 1, wherein a first anchoring generation (dual-write) is extended by
    one additional ledger per generation (tri-write, quad-write, penta-write, N-write), the
    same digest being re-anchored with a preregistration before each generation.
20. The method of claim 1, substantially as described and reduced to practice in the
    evidence chain appended hereto.

## ABSTRACT

A deterministic protocol anchors a single cryptographic digest of a frozen artifact across
any number of heterogeneous distributed ledgers, using each ledger's native inscription
mechanism (OP_RETURN, memo fields, named data entries, labeled metadata, zero-value calldata,
note fields, memo programs, and remark extrinsics), with preregistration before broadcast,
idempotency stamping, keyless byte-exact read-backs, per-ledger canonical identifier rules,
tiered route certification (rehearsal before production), an intelligent routing engine that
orders legs by measured finality and cost and checks prediction against observation, an
optional custody mode in which ownership of the digest carrier hops between wallets while the
artifact remains in a vault, recursive receipt anchoring, and append-only sealing of all
identifiers, costs, latencies, and disclosed failures.

## REDUCTION-TO-PRACTICE EVIDENCE CHAIN (receipts-first, all public)

1. DWR-1 Dual-Write Receipt (2026-10-18): one digest, Bitcoin OP_RETURN + XRPL memo,
   back-to-back; DOI 10.5281/zenodo.23464516; BTC block 972107; ledgers 0224-0225.
2. TWR-1 Tri-Write (2026-10-19): digest ac7c0f44...ea84635 on BTC (block 972110), XRPL
   (ledger 107755630), Stellar (ledger 65020686); ledger 0226.
3. RTWR-1 Recursive Tri-Write (2026-10-19): the receipt of the tri-write itself re-anchored;
   DOI 10.5281/zenodo.23466738; BTC block 972112; ledger 0229.
4. QWR-1/QWR-2 Quad-Write (2026-10-19): Cardano rail added (metadata label 1968, CBOR);
   DOIs 10.5281/zenodo.23467440 and 10.5281/zenodo.23477976; BTC block 972172; ledger 0230+.
5. Wallet Crossfire (2026-10-19): 8 ownership-exchange transactions across 4 mainnets,
   byte-exact notarization with zero token issuance; ledger 0235, commit 1b695b6b.
6. PWR-1 Penta-Write (2026-10-19): pure-data anchoring (zero asset movement) across BTC,
   XRPL, Stellar, Cardano, and the new Ethereum rail; ledgers 0236-0237.
7. XTR-1 Custody Chain (2026-10-19): 5-hop XRP ownership chain, 35.45s total, 7.09s average
   broadcast-to-validated-finality per hop — measured speed record for ownership changes.
8. IR-1 Intelligent Routing Engine (2026-10-19): latency/cost-ranked routing tested live;
   observed finality within 0.6s of prediction; ledger 0239, commit 8c5b3d8.
9. Route Certification Program (2026-10-19): 10-rail roster; T1/T2/T3 tier doctrine; Algorand
   (round 66138941), Avalanche (1.1s measured), Solana (SPL Memo, slots 458918281/458918736)
   certified; DeWR-1 rail performance record digest 99e01327...b9ab6 carried byte-exact on 8+
   rails; failed attempts disclosed forward-only (ledgers 0240-0243).
10. Multi-Rail Inscription Playbook (2026-10-19, commit d545c66): operator doctrine for all
    rails — per-rail traps and fixes, measured speed/cost tables, canonical identifier rules.

## FILING NOTES (inventor steps; verify against the current USPTO fee schedule)

1. Prepare a cover sheet (USPTO Patent Center, form SB/16 or the Patent Center web form):
   inventor name and residence, title of invention, correspondence address, entity status
   (micro/small — verify eligibility), and any US government interest (none — SBIR-adjacent
   work is disclosed in the portfolio, but this application is not government-funded).
2. Convert this draft to PDF unchanged; the filed document becomes the priority record —
   do not edit after freezing (the committed draft in the four-horsemen repository is the
   canonical byte-for-byte record).
3. Upload in Patent Center as a Provisional Application for Patent; pay the fee
   (~$65-150 discounted; verify current schedule).
4. Record the application serial number and filing receipt hash in the hub ledger
   (append-only); a DOI mint for the filing receipt is a separate two-key decision.
5. Grace-period doctrine: public disclosures of the ceremonies (DOIs above) precede this
   filing; US 12-month inventor grace period runs from the earliest disclosure; non-US
   strict-novelty jurisdictions may treat them as prior art — counsel's call for family
   planning.

## DISCLOSURE DOCTRINE

All receipts disclose company-owned operations and simulated training material only; no
customer data, no PHI, no credentials (POL-DISC-001). Prototype disclaimer applies to every
system and record referenced.

---

> This software is a prototype and is provided for educational and research purposes only. It
> is not intended for production use, commercial deployment, or safety-critical environments.
> All systems are experimental and may contain defects.

Canonical form: this Markdown file, byte-for-byte. SHA-256 recorded below at freeze.
