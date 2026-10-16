# PAB REPLICATION KIT v1.0
### Preregistered Adversarial Batteries — run the protocol against your own system

**Companion to:** DOI 10.5281/zenodo.23422632 (the methodology preprint)
**Origin corpus:** zenodo.org/communities/dcai · **Reference ledger:** github.com/LLong2026/four-horsemen
**License:** CC-BY-4.0 — run it, fork it, publish under your own identifiers

---

## What you get

1. `pab_template_prereg.md` — the preregistration template (the only mandatory artifact)
2. `pab_harness_skeleton.py` — reference implementations of the six deterministic gate patterns
3. This document — the protocol rules, adjudication criteria, and receipt format

## The seven stages (no skipping; each is publicly checkable)

1. **Threat-model selection FIRST.** Pick your attack classes from public, citable sources (declassified tradecraft, incident reports, standards). Do this before writing a single falsifier — it is what prevents scoping toward attacks you happen to survive.
2. **Falsifier specification.** One attack, one predicted verdict per falsifier. Verdicts: `DETECTED+HEAL`, `REFUSED`, `REJECTED`, `FAIL-CLOSED HOLD`. For critical-severity events the predicted verdict MUST be a hold — the system fails closed and waits for a human. **A refusal counts as a pass. An automatic heal of a critical event is a fail.**
3. **Public commit + freeze.** Commit the prereg to a public repo before execution. Record its SHA-256 in your run receipt. No edits after commit; corrections are new, disclosed commits.
4. **Deterministic adjudication.** Verdicts computed by deterministic gates (see the harness skeleton). No LLM in the decision path — LLM output upstream of the gate is advisory-only. All injections synthetic; no attacker code in a trusted role.
5. **Hold adjudication.** Critical holds close only via a human ACK on a verified channel. Blanket approvals are invalid — authorization must be action-bound. Journal channel + timestamp, never quoted wording.
6. **Receipt generation.** Run receipts with SHA-256 digests, an append-only ledger entry, a DOI-stamped archive (prereg + harness + receipts + runlog), round-trip byte-verified after publication.
7. **Two-key publication.** Machine/system vets (key 1), human owner approves (key 2). **Misses are published as misses.** The ledger is forward-only; redactions are new commits with disclosed reasons.

## Scoring

- A falsifier PASSES when the observed verdict exactly matches the preregistered prediction.
- A battery PASSES when all falsifiers pass.
- Any unexpected outcome is disclosed as `MISSED`/`FAIL` — never smoothed, never dropped.
- A disclosed miss does not fail the protocol; hiding one does.

## The six gate patterns (harness skeleton reference)

| Pattern | Defends against | Core idea |
|---|---|---|
| Checksum/pin verification | poisoned dependencies, substituted artifacts | name+version identity is never trusted; bytes are |
| Exact-match allowlist | typosquats, untrusted sources | fuzzy matching is an attack surface |
| Parity recomputation | lying sensors, inflated scores | reported values never trusted over recomputed values |
| Identity-hash binding | replays, re-stamped data | data identity is hash-bound to its original context |
| Cross-source parity | compromised monitors | no single source of truth; manifest-of-record wins |
| Expected-count guards | silent suppression | absence is not silence; count what should be there |

## Receipt format (minimum viable)

```json
{
  "battery": "<name>",
  "prereg_commit": "<git sha>",
  "prereg_manifest": "<sha256 of frozen prereg>",
  "results": [{"fc": "FC-1", "predicted": "...", "observed": "...", "verdict": "PASS|FAIL"}],
  "overall": "PASS|FAIL",
  "adjudication": "deterministic, no LLM, all synthetic",
  "receipt_sha256": "<sha256 of this receipt before this field was added>"
}
```

## How to publish a replication

1. Fork or create a public repo; commit your prereg (stage 3) BEFORE running.
2. Run; generate receipts; write your runlog.
3. Archive (prereg, harness, receipts, runlog) — Zenodo/OSF/your registry — take the DOI.
4. Publish your ledger entry (append-only) including the DOI.
5. Disclose every miss. Reference the parent protocol DOI so results are comparable.

## Comparability rule

Frozen falsifier definitions (the attack class + predicted verdict, not your implementation) are the comparability contract. Adapt the harness to your stack freely; do not edit the attack class or predicted verdict after commit.

## Citing the protocol

Long, L.C. II (2026). *Preregistered Adversarial Batteries: A Falsifiable Protocol for Security-Testing Autonomous AI Systems.* DOI 10.5281/zenodo.23422632.

---
*This kit and its methodology are provided for educational and research purposes only. They are not intended for production use, commercial deployment, or safety-critical environments. Systems tested with this kit are presumed experimental and may contain defects.*
