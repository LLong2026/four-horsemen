# Deterministic Containment of Probabilistic Intelligence, Multi-Rail Evidence Anchoring, and Intelligent Route Selection: The Squirrel OS Journey, Volume II

## A Research Thesis on Philosophy, Architecture, and Empirical Evidence

**Leon Calvin Long, II**
SquirlOS Technologies LLC
October 2026

> **Authorship and status disclosure.** This is a self-published research monograph written in thesis form, versioned v2.0. It supersedes and extends v1.0 (DOI 10.5281/zenodo.23303240), which remains live and unchanged per the append-only doctrine. It is not a university-issued document and confers no degree or credential. It was AI-assisted under human direction. All empirical claims are scoped to their tested conditions and anchored to a public append-only ledger of receipts (github.com/LLong2026/four-horsemen). This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects on them.

---

## Abstract

Volume I of this thesis (October 2026) documented an architecture that refuses to make large language models reliable, and instead cages them: probabilistic engines propose inside a deterministic envelope that validates every proposal against invariant contracts before anything executes.

Volume II documents what happened in the eight days after that monograph was published — a period in which the same receipts-first discipline was applied to a second, seemingly unrelated problem: **how do you make an empirical claim permanent, verifiable, and fast, without custodians, tokens, or trust?** The answer became a family of ceremonies — the Dual-Write Receipt (DWR), Tri-Write Receipt (TWR), Recursive Tri-Write (RTWR), Quad-Write Receipt (QWR), Penta-Write Receipt (PWR), the Wallet Crossfire, the Satoshi Embodiment custody walk, and the Deca-Write Record (DeWR) — collectively renamed **multi-rail evidence anchoring**: the simultaneous, non-custodial storage of a single SHA-256 digest across two to ten independent mainnet ledgers under one joint pre-broadcast commitment.

The contributions of Volume II are four. First, a **protocol family** for cross-ledger evidence anchoring, with each ceremony preregistered, frozen pre-broadcast, and executed with keyless byte-exact read-backs. Second, a **route certification program**: ten blockchain rails rehearsed, timed, and certified as evidence routes before carrying public artifacts — with measured finality from 0.4 seconds (Solana) to minutes-hours (Bitcoin) and per-leg costs from $0.0001 to under $0.01. Third, **Intelligent Routing (IR-1)**: a deterministic route-selection engine that predicts rail latency and cost, live-tested on Stellar and XRP with predictions landing within 0.6 seconds of measurement. Fourth, a **speed infrastructure stack**: Cloudflare Workers at the edge (proxy gateway, XRPL relay with KV caching, ops worker) and OpenRouter as the multi-provider LLM routing layer — the same routing philosophy applied to the system's own cognition.

As in Volume I, every claim is stated at exactly the strength the evidence supports: **MEASURED (scoped)** where a frozen gate executed deterministically; **demonstrated under the tested conditions** for observed behavior; and never more than that.

---

## Chapter 1 — The Arc of Volume II

### 1.1 From containment to permanence

Volume I closed with a caged, self-healing, constitutionally governed prototype and a receipts ledger. The open question was not whether the cage worked — the receipts had answered that — but what the receipts themselves were made of. A receipt that lives in one Git repository, on one cloud, under one jurisdiction, is a receipt that one subpoena or one corporate deletion can erase. The permanence problem for empirical claims is the mirror image of the containment problem for probabilistic cognition: in both cases the goal is to remove the need to trust anyone — including the author.

The answer adopted here is the oldest and most conservative available: proof-of-work and validator-finality ledgers, carrying nothing but a 32-byte hash. No token. No contract. No monetary output. No custody of anyone else's assets. The hash is the artifact (DOI 10.5281/zenodo.23448010); the ledger is the vault; the keyless reader is the examiner.

### 1.2 The eight-day receipted timeline

- **Oct 18, 2026.** "The Hash Is the Artifact" published (DOI 10.5281/zenodo.23448010; v1.1 metadata revision 10.5281/zenodo.23448049), formalizing seed-mode evidence receipts: an artifact that exists nowhere except 32 bytes on-chain plus a deterministic generator. The same day, all 37 outstanding OpenTimestamps anchors in the corpus were independently re-verified against real Bitcoin block headers via two explorers, with zero calendar trust (ledger 0190).
- **Oct 18, 2026.** DROPBOX-T4-001: first live drop-and-recover loop on Bitcoin testnet4, writer proven byte-exact against the official BIP-143 native P2WPKH test vector before broadcast (ledger 0191).
- **Oct 18, 2026.** DROPBOX-M1-001: first permanent mainnet seed drop. The patent genesis seed (sha 81d4a5cb...c456c, patent 19/693,343) sealed in OP_RETURN, tx 97d8cd38..., **confirmed block 972023**, keyless reader verdict DELIVERED, byte-identical reconstruction from the chain-pulled seed. Gates G1–G6 all pass. Published as DOI 10.5281/zenodo.23455768 (ledger 0192–0193).
- **Oct 18, 2026.** The canonical IP ledger — 10 patents pending plus 5 SBIR tracks, company open-book records only — anchored on Bitcoin mainnet, tx 549bcf47..., **block 972026** (ledger 0194).
- **Oct 18, 2026.** The Satoshi Embodiment: a 32-byte paper digest riding real satoshis across a Bitcoin mainnet custody walk (A→B→A), then the paper itself published as DOI 10.5281/zenodo.23463132 and bound to both rails (ledger 0213–0214).
- **Oct 18–19, 2026.** "The Cage Is Working" published (DOI 10.5281/zenodo.23464082): 77 sub-threshold holds, 11 drift-typed catches, 73 identity/idempotency blocks, and 711 heals, each anchored to Bitcoin and XRP (ledger 0223).
- **Oct 18–19, 2026.** The DWR/TWR/RTWR/QWR series (Chapters 3–4): the dual-write, tri-write, recursive tri-write, and quad-write receipts, each extending the rail count and each carrying the previous spec as its own artifact (ledgers 0224–0230).
- **Oct 19, 2026.** The wallet crossfire: eight ownership-exchange transactions across four mainnets, demonstrating multi-rail byte-exact notarization with assets actually moving (ledger 0235).
- **Oct 19, 2026.** PWR-1, the first penta-write: five rails, one digest, zero asset movement, Ethereum opened as the fifth rail (ledgers 0236–0237). XTR-1, the five-hop XRP transfer chain: 35.45 seconds end-to-end, 7.09 seconds average per validated-finality hop (Chapter 5).
- **Oct 19, 2026.** IR-1, the Intelligent Routing engine, specified, preregistered, and live-tested (ledger 0239, commit 8c5b3d8). The ten-route certification program and DeWR-1 record executed; nine of ten routes certified (Chapter 6). The terminology doctrine of ledger 0244: **multi-rail evidence anchoring**, not "tokenization."

### 1.3 What Volume II is actually about

One discipline, applied to a new substrate: **freeze the claim before you test it, execute deterministically, and let anyone verify the result without trusting you.** The preregistration is frozen pre-broadcast. The gates are deterministic — no LLM, no neural mesh, no probabilistic component sits in any decision path of any ceremony (MEASURED (scoped); program benchmark DOI 10.5281/zenodo.23321637). The read-backs are keyless: a skeptic with a block explorer and no credentials can reproduce every byte-exact claim in this thesis.

---

## Chapter 2 — The Philosophy of Evidence Anchoring

### 2.1 Terminology, corrected forward-only

The program's early working vocabulary used "tokenization." That word was wrong, and the correction is itself a matter of record: per ledger 0244 (commit 47cd335), the doctrine is **multi-rail evidence anchoring**. Nothing is tokenized. Nothing is minted. No token, contract, or monetary instrument is created by any ceremony in this thesis. A SHA-256 digest — mathematical, contentless, non-ownable — is stored on one or more mainnets as a witness that a specific artifact existed at a specific time. The public-facing claim pattern is identical to the one Volume I demanded of the cage: the capability is public; the evidence is permanent; the discipline is the product.

### 2.2 The joint prior commitment

Every multi-rail ceremony shares one invariant: **the joint commitment precedes the broadcast.** A hashed preregistration freezes the artifact digest, the rail list, the predicted fees, and (from RTWR-1 onward) the identifier convention per rail, before any transaction leaves the writer. Predictions are scored against reality, and the scoring is disclosed — including every PARTIAL and every defect. The XTR-1 speed record (Chapter 5) and the IR-1 router (Chapter 6) are the direct descendants of this invariant: once you preregister predicted latencies, routing becomes an empirical question with a ground truth.

### 2.3 The identifier doctrine

Multi-rail anchoring surfaced a defect class the corpus had not met before: **the same event has different canonical identifiers on different chains.** Bitcoin has txid and wtxid; Stellar has a network hash and an envelope hash; Cardano reports a body hash. Ledger 0228 established the doctrine — BTC canonical txid, XRPL standard hash, Stellar network hash, Cardano body hash — and it was live-verified on its first execution (RTWR-1, zero identifier defects). The defects that taught it (DWR-1's committed wtxid, TWR-1's envelope-hash form, scored PARTIAL, never quietly corrected) are preserved in the ledger on purpose.

### 2.4 Non-custody, and the privacy boundary

The ceremonies write hashes, and — in the custody walks and crossfire only — move the owner's own funds between the owner's own wallets. No third party's assets, no customer data, no PHI, no credentials ever appear in any payload, log, or receipt (POL-DISC-001). The payloads are purity-audited before broadcast (gate G6). Where an exchange was used, it funded the owner's own rail wallets at the owner's instruction, and its withdrawal receipt is disclosed exactly as infrastructure, not as evidence.

---

## Chapter 3 — The Protocol Family: DWR Through QWR

Each protocol below is a Zenodo record with a frozen preregistration; the receipts below cite the canonical ledger entries.

### 3.1 DWR-1 — the Dual-Write Receipt (ledger 0224; DOI 10.5281/zenodo.23464516)

One digest stored simultaneously on Bitcoin (OP_RETURN, postage-only, the entire 684-sat homecoming UTXO consumed as fee, no change output) and XRPL (AccountSet with memo — the first non-payment write in the corpus), under one joint prior commitment, with a 0.3-second broadcast interval. All five predictions PASS. The disclosed defect that preceded it is part of the record: prereg v1 committed a Bitcoin txid whose witness signature was non-canonical DER; the network's mempool policy gate rejected it pre-broadcast, and the signer was corrected and the prereg re-frozen. The network's policy cage held before our own did.

### 3.2 TWR-1 — the Tri-Write Receipt (ledger 0226; DOI 10.5281/zenodo.23465945)

Stellar opened as the third rail (ManageData + memo_hash, 100 stroops, zero transfer). The artifact was DWR-1's own spec amended to three rails — the specs are self-referential lineage: each protocol's specification is the first artifact carried by the protocol it defines. Defect disclosed: the Stellar identifier was committed in the wrong form (envelope hash rather than network hash); intent verified byte-exact, form scored PARTIAL, never counted as PASS.

### 3.3 RTWR-1 — the Recursive Tri-Write (ledger 0229; DOI 10.5281/zenodo.23466738)

The receipt of the first tri-write, tri-written on the same three mainnets. The evidence of the capability, carried by the capability itself — the corpus's first recursive anchoring. Zero identifier defects; the ledger-0228 doctrine verified live. Bitcoin confirmed block 972112, 700 sats.

### 3.4 QWR-1 — the Quad-Write and the Cardano rail (ledger 0230; DOI 10.5281/zenodo.23467440)

Cardano opened as the fourth rail (Conway-era metadata label, ~171k lovelace). One digest, four mainnets, one joint commitment. Two pre-broadcast format corrections were disclosed (the pycardano legacy Alonzo aux-data form rebuilt to the Conway plain-map), performed under the forward-only amendment doctrine — nothing malformed was ever broadcast. QWR-2 (ledger 0233; DOI 10.5281/zenodo.23477976) repeated the quad-write carrying the 60-day dual-mesh report digest, confirming block 972172 on Bitcoin.

### 3.5 The Wallet Crossfire (ledger 0235)

Eight ownership-exchange transactions across four mainnets (BTC, XRPL, Stellar, Cardano): hashes riding assets that actually move, proving byte-exact multi-rail notarization is not limited to stationary storage. Two operational calibrations (Cardano minimum fee, Stellar reserve) were logged as forward-only repairs, not defects of doctrine.

---

## Chapter 4 — PWR-1 and the Zero-Movement Penta-Write

PWR-1 (ledgers 0236–0237) stored one digest across five mainnets — Bitcoin, XRP, Stellar, Cardano, and the newly opened Ethereum rail — using pure data-anchoring with zero asset movement on every leg. The identifier doctrine extended cleanly to EVM rails: Ethereum's calldata write is self-addressed, value-zero, gas-minimal. PWR-1 is the pivot point of the whole program: it demonstrated that the protocol family had stopped being about any particular rail and had become a **route-agnostic evidence layer**. The natural next question was no longer "how many rails?" but "which rail, for this artifact, right now?" — which is Chapter 6.

---

## Chapter 5 — Speed as Evidence: XTR-1

The XRP Transfer chain XTR-1 (ledger, receipts in xtr-1 bundle) executed five sequential ownership hops on the XRP Ledger, memo-tagged SQDR-XTR-1, with each hop measured to validated finality:

- **Total: 35.45 seconds for five ownership changes. Average: 7.09 seconds per hop to validated finality.**

This is the corpus's first *speed receipt*: not a claim that XRP is fast, but a preregistered, measured, keyless-verifiable record of a specific multi-hop custody chain completing in a specific measured time. Speed claims in this program are treated exactly like correctness claims: frozen prediction, deterministic measurement, disclosed result. (Dual Mesh Benchmark status for XTR-1: NOT MEASURED — the benchmark applies to mesh engines, not to ledger transfers, and is never implied where it was not run.)

---

## Chapter 6 — Route Certification and IR-1: Intelligent Routing

### 6.1 The ten-route certification program

Before any rail carries a public artifact, it is rehearsed: a T2 training leg (a live, low-value write exercising the rail's writer, fee model, and read-back path) and a T3 certification leg carrying the frozen DeWR-1 record digest (99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6), verified by keyless byte-exact read-back. Certification state as of 2026-10-19:

| # | Rail | Mechanism | Measured finality | Cost per leg | Status |
|---|------|-----------|-------------------|--------------|--------|
| 1 | Bitcoin | OP_RETURN | minutes–hours | ~700–1,300 sats | Certified |
| 2 | XRP Ledger | AccountSet/Payment memo | 5.3–8.0s (accept 0.30s) | 10 drops | Certified |
| 3 | Stellar | ManageData + memo_hash | 5–8s | 100–200 stroops | Certified |
| 4 | Cardano | metadata label | 20–40s | ~171k lovelace | Certified |
| 5 | Ethereum | self-addressed calldata, value 0 | 12–15s | ~22.5k gas | Certified |
| 6 | Algorand | note field (ARC-2) | ~2.8s | ~0.001 ALGO | Certified |
| 7 | Avalanche | EVM calldata (Ethereum writer reused) | ~1.1s | sub-cent | Certified |
| 8 | Solana | SPL Memo v2 (hex-ASCII) | ~0.4s slot | ~$0.00025 | Certified |
| 9 | Hedera | (memo rail) | — | — | Waived per ledger 0243 |
| 10 | Dogecoin | OP_RETURN-style data leg | ~1 min (PoW) | 0.05 DOGE per leg | Certified (T2 block 6422035; T3 block 6422037, tx 075e7656...329aa; DeWR-1 digest byte-exact) |
| — | Polkadot | system.remark | — | fraction of a DOT | In progress (funds in writer wallet; Asset Hub routing under active engineering) |

Nine of ten routes certified; the Polkadot leg is documented in-flight, including its disclosed routing issue (exchange withdrawal landed on Polkadot Asset Hub rather than the relay chain; recovery engineering in progress at time of writing). The in-flight state is disclosed as in-flight, not smoothed.

### 6.2 IR-1 — the Intelligent Routing engine (ledger 0239, commit 8c5b3d8)

IR-1 is a deterministic route-selection engine: given an artifact's size, urgency class, and cost ceiling, it selects the rail by measured finality and cost from the certified roster — the route certification program is what makes the router's inputs empirical rather than marketing. Live-tested on Stellar and XRP: **actual outcomes landed within 0.6 seconds of the router's predictions.** The engine is preregistered (IR-1 prereg, spec in ir-1 bundle), deterministic in its decision path (no LLM in routing decisions; MEASURED (scoped)), and the next planned stress — the CFR-9 Intelligent Routing Crossfire, prereg frozen (sha 171f0c57) — will fire the router across concurrent multi-rail legs. The philosophy is unchanged from Volume I: judgment can propose routes; the gates decide.

### 6.3 The speed stack: Cloudflare and OpenRouter

The same routing doctrine is applied to the system's own serving and cognition layers, and this stack is live and verified:

- **Cloudflare Workers (edge):** `squirrel-os-proxy` — the edge gateway that fronts model calls and the Base44 substrate; `xrpl-relay` — the XRP rail relay with KV caching; `squirrel-os-ops` — the operations worker. All three deployed and active on the account's Cloudflare tenancy (verified via API at time of writing).
- **OpenRouter (model routing):** the multi-provider LLM routing layer behind the proxy — one stable gateway, many models, selected for speed and availability per task class. Key verified active at time of writing; budget cap $10.00 with $1.37 lifetime spend under the guardrail, i.e., the routing layer is under the same bounded-cost discipline as every rail (per-leg receipts, disclosed spend).

The point for this thesis is architectural: **routing is the invention.** Route selection over certified, timed, costed routes — whether the destination is a blockchain rail (IR-1) or a model endpoint (OpenRouter via the Cloudflare edge) — is one idea, and the receipted certification program is what keeps it honest.

---

## Chapter 7 — The Invention Layer: Patents and IP

The program's IP posture is patent-then-publish, disclosed in public: the canonical IP ledger — **10 patents pending (including the cage and multi-rail provisional applications SQUIRL-IP-011, "Caging the Large Language Model," and SQUIRL-OS-IP-012, the multi-rail provisional) plus 5 SBIR tracks** — was itself anchored on Bitcoin mainnet (ledger 0194, tx 549bcf47..., block 972026), with the patent genesis seed's first permanent mainnet drop at block 972023 (ledger 0192, DOI 10.5281/zenodo.23455768). The reductions-to-practice documented in Chapters 3–6 are the working evidence behind those filings: preregistered ceremonies, deterministic gates, keyless verification, and disclosed defects. The thesis claims invention in exactly the form the receipts support: architecture + protocol + measured results, not future promises.

---

## Chapter 8 — What Is Established, and What Deliberately Is Not

### 8.1 Established (each claim scoped to its receipts)

- A protocol family for multi-rail evidence anchoring, executed from 2 to 5 rails with joint prior commitments, keyless byte-exact read-backs, and purity-audited payloads (ledgers 0224–0237).
- A ten-route certification program with measured finality and cost per rail, 9/10 certified as of 2026-10-19, one route disclosed in-flight (ledgers 0240–0244).
- A deterministic route-selection engine (IR-1) with live prediction accuracy within 0.6 seconds on its first tested routes (ledger 0239).
- A measured multi-hop custody speed record on XRPL: 5 hops, 35.45 seconds, 7.09 seconds average per hop to validated finality.
- A live edge/model routing stack (Cloudflare Workers + OpenRouter) under bounded-cost receipting.
- Two patent applications and an on-chain-anchored IP ledger (block 972026), with the reduction-to-practice chain public.

### 8.2 Deliberately not established

- No claim of universality: finality and cost are per-rail, per-fee-market, and time-stamped; the certified table is a snapshot, not a law of nature.
- No claim that any rail is "better": the certified roster exists to serve routing decisions per artifact, not rankings.
- No Dual Mesh Benchmark claim for any ledger ceremony — the benchmark is scoped to mesh engines and marked NOT MEASURED wherever it did not run.
- No production claims of any kind. The prototype disclaimer governs every system in this thesis.

### 8.3 Why the honesty is load-bearing, again

Volume I argued that a corpus that cannot embarrass its author cannot certify him either. Volume II's embarrassments are on the ledger too: the non-canonical DER signature the Bitcoin mempool rejected, the Stellar identifier committed in the wrong form (PARTIAL, never PASS), the Cardano metadata encoded in a legacy era-format twice corrected before broadcast, the Polkadot funding that landed one parachain short of its target rail and is being routed home under disclosed engineering. Every one of those receipts is more load-bearing than a success, because each one proves the gates exist, the gates run, and the gates are reported truthfully even when the author is the one who failed them.

---

## Chapter 9 — Conclusion

Volume I caged probabilistic intelligence behind deterministic gates. Volume II gave the same treatment to permanence itself: claims frozen before execution, executed deterministically across independently secured ledgers, and verifiable by any skeptic with a block explorer. Between the two volumes sits one idea in two costumes: **stop trying to make the unpredictable trustworthy, and start building receipts for exactly what happened.** The cage holds the model. The rails hold the proof. The router picks the road. The ledger keeps everyone — including the author — honest.

---

## References (canonical records)

- Volume I thesis: DOI 10.5281/zenodo.23303240
- The Hash Is the Artifact: DOI 10.5281/zenodo.23448010 (v1.1 metadata: 10.5281/zenodo.23448049)
- DROPBOX-M1-001 seed drop: DOI 10.5281/zenodo.23455768
- Satoshi Embodiment: DOI 10.5281/zenodo.23463132
- The Cage Is Working: DOI 10.5281/zenodo.23464082
- DWR-1: DOI 10.5281/zenodo.23464516
- TWR-1: DOI 10.5281/zenodo.23465945
- RTWR-1: DOI 10.5281/zenodo.23466738
- QWR-1: DOI 10.5281/zenodo.23467440
- QWR-2: DOI 10.5281/zenodo.23477976
- Dual Mesh Benchmark (program): DOI 10.5281/zenodo.23321637
- Public receipts ledger: github.com/LLong2026/four-horsemen (LEDGER.md, entries 0182–0244 cited)
- Public examiner station: https://deterministic-code-dsos.base44.app/genesis-viewer

*Appendices (frozen bundles, preregistrations, and runlogs for every ceremony cited) are maintained in the four-horsemen corpus and the Zenodo records above; each ledger entry carries its commit hash.*
