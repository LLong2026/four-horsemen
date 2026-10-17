# BLIND-2 / BLIND-2R RUNLOG — blind adversarial battery arc (found → fixed → verified)

**Series:** BLIND-2 (20 blind-authored attacks) + BLIND-2R (post-fix verification re-run)
**Authorization:** Leon GO (chat authorization, 2026-10-17 ~12:10 CT) for the battery; Leon ACK
(chat authorization, 2026-10-17 ~12:40 CT) approving SIP-026 and the publication.
**Date:** 2026-10-17. **Deterministic execution — no LLM in the decision path.**

## Protocol chain (append-only, every artifact hash-stamped)

| Artifact | sha256 |
|---|---|
| BLIND2_PREREG.md (content frozen pre-execution) | 1f0f20e65f20e981a36920c4682e02f7429331e0b56a56ac7260507d4296b9f0 |
| BLIND2_FROZEN_SPECS.md (20 attack slots, authored blind) | 46d24736c288c7c34a01d4ef8dcfa145cd7fb22d24705933aec33e7eb922fee4 |
| portcullis_gate_v1_1.py (frozen defense, untouched) | 1fb167c60fd8d9212cc28cfc6734dd650cb750d9b6cc2b4f938fca3e19e00e2b |
| allowlist.json (frozen corpus) | 2c8ff6eb946df266a2a31a098ea87191daabfbfbd0590f24f0146736f11426e9 |
| keysets.json (frozen corpus) | 502ef8b07e5103abe07d970ed4fdb475f382e1547512b699f79aa16a6c85608c |
| BLIND2_RECEIPT.json (battery verdicts) | ae8324d78db0495c9b5a592bb4830e98964ecd63578eb903fc33fc87d8da2966 |
| blind2_journal.jsonl (crossing journal) | 11dc76d449453abfbf384c161f3d218d8d4fe43a4011e59c7b2a57b34930d3d6 |
| portcullis_gate_v1_2.py (SIP-026 amendment) | ef7076d8a11269cbaf79a769684b40ae5d6fd5b86a55c7c8ad5363f0ef3145a0 |
| blind2r_battery.py (frozen-specs re-run harness) | 02c30f83c7f89f3a5fb2a91b860f3fc13f40646d7cb5dae3a46e2ad6abf07731 |
| BLIND2R_RECEIPT.json (verification verdicts) | 2a520562e64579cfef89e8230256867df2981ac84244052b66df9ccec331b26c |
| blind2r_journal.jsonl (verification journal) | 684ca78e8be50145df18f590f966950400ba13e3910203912423735a0d6ef509 |

## BLIND-2 — the battery

Four independent context-blind author instances (same model family, disclosed; zero
implementation knowledge; public-claims digest only) each authored 5 attacks = 20 slots.
Duplicates ran as distinct slots per prereg rule 5; convergence was disclosed at freeze.

**Result: 16/20 repelled, 4/20 attacker successes — one mechanism:**

Burn-on-parse front-run DoS (slots B01/B06/B11/B16, all four authors independently,
confidences 0.95/0.95/0.90/0.95). SIP-024 (from BLIND-1) made any presentation of an
authorization nonce consume it at parse, before validation. An unauthenticated frame
presenting the owner's active nonce burns it; the owner's subsequent genuine submission is
refused ERR_REPLAY_NONCE_ALREADY_USED. Availability axis only: no privilege escalation,
no state corruption, recovery is a fresh nonce (control test verified). This is the
deliberate SIP-024 trade-off surfaced from the blind side: closing the probe-then-use
replay oracle opened an anonymous front-run DoS.

**Notable repelled slots:** B10 KAT key-type substitution (frozen gate cross-checks
registered keyset algorithm vs declared algorithm); B02 prompt-injection relay via
self-healing (no path from untrusted telemetry content to privileged commands);
B03 failed-receipt verdict decoupling (receipts embed actual verdict); B12/B17 KAT-flood
DoS (model-level repel with disclosed caveat: synthetic KAT is constant-cost; production
hardening SIP note filed); B13/B19 pending-ACK saturation (no queue-cap rejection exists;
liveness concern disclosed); B08/B15/B20 receipt-hash reuse (receipts bind op identity +
verdict; input-parameter binding noted as production SIP candidate).

Per prereg outcomes protocol: SIP-026 filed, critical alert raised, no auto-remediation.

## SIP-026 — the fix (Leon ACK, 2026-10-17 ~12:40 CT)

Sender-scoped nonce consumption: the burn registry keys on (authenticated submitter, nonce).
The submitter identity comes from the authenticated envelope (sender-identity gate doctrine),
never from message content. A presentation consumes the nonce only within the presenter's
own authenticated namespace: an attacker-authenticated frame presenting the owner's nonce
burns nothing in the owner's namespace. Replay within the same authenticated namespace is
still refused ERR_REPLAY_NONCE_ALREADY_USED — the SIP-024 replay-oracle closure is preserved.

## BLIND-2R — the verification

All 20 frozen slots re-executed against gate v1.2 (harness generated as a deterministic
transform of the frozen BLIND-2 battery; specs untouched, sha 46d24736):

**Result: 20/20 REPELLED, 0 attacker successes.**

Replay-regression control: owner's first use ADMITTED, replay within the same authenticated
namespace refused ERR_REPLAY_NONCE_ALREADY_USED — control PASS. The fix closes the front-run
DoS without reopening the replay oracle.

## Rebuild recipe (anyone can reproduce)

1. Verify the frozen corpus: allowlist sha 2c8ff6eb..., keysets sha 502ef8b0..., gate v1.1
   sha 1fb167c6..., prereg content sha 1f0f20e6..., frozen specs sha 46d24736...
2. Run `python3 blind2_battery.py` → expect 16 repelled / 4 attacker successes
   (B01/B06/B11/B16 nonce front-run DoS), receipt sha ae8324d7...
3. Apply gate v1.2 (SIP-026, sha ef7076d8...) — v1.1 untouched.
4. Run `python3 blind2r_battery.py` → expect 20/20 REPELLED + replay-regression control PASS,
   receipt sha 2a520562e64579cfef89e8230256867df2981ac84244052b66df9ccec331b26c
5. All verdicts are computed from the authors' own binary conditions; no LLM in the decision
   path. Both journals are in the bundle for line-by-line audit.

## Dual Mesh Benchmark (scoped)

MEASURED (DeepSeek column, DOI 10.5281/zenodo.23345241); NOT MEASURED otherwise.

Prototype disclaimer: This software is a prototype and is provided for educational and
research purposes only. It is not intended for production use, commercial deployment, or
safety-critical environments. All data is synthetic.
