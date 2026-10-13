# GOV-3 PREREGISTRATION — Signed-Release Attack Battery (The Cost Ladder)

Series: GOV-3 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 12:01 CT,
stage-2 SIP-4 approval + GOV-3 GO; acquisition-evidence framing noted by the
operator — this battery and its disclosures are part of that corpus).

## 1. Purpose — attack the signed release chain

GOV-2 quantified the boundary: a full-compromise in-process attacker installs
semantically valid malicious governance undetected. Stage-2 SIP-4 (approved
12:01 CT, deployed this session) closes that boundary as far as software can:
signed governance releases — HMAC over the roster, key held in process custody
with its FINGERPRINT pinned in git, release registry anchored in git and re-read
from git objects at verification time (working-file mutation does not touch the
anchor). GOV-3 attacks this chain:

1. **Full-compromise replay** (epochs 1-8): GOV-2's class-5 attack verbatim —
   in-domain threshold 0.99 in live + reference + pin. The signature layer must
   catch what three layers could not.
2. **Forged signature** (epochs 9-16): malicious roster signed with a garbage
   key.
3. **Key replacement** (epochs 17-24): attacker generates their own key,
   re-signs the malicious roster, installs it with a matching working registry.
   The git-anchored FINGERPRINT PIN must catch the key swap.
4. **Registry mutation / rollback attempt** (epochs 25-32): attacker forges a
   working registry entry (fake "v0" weak release, current_version downgraded).
   The git-anchored registry must catch it. Honest note: TRUE rollback testing
   (replaying a legitimate prior release from a multi-release history) requires
   a v2 release to exist; with a single release the class reduces to forged
   registry entries, disclosed.
5. **The regress floor** (epochs 33-40): attacker who ALSO has the signing key
   AND git/commit access (modeled: anchors read from attacker-controlled state).
   NOTHING automated can catch this — stated before execution. The falsifier
   fails as found; the run-end audit restores; the ship is the COST LADDER:
   what each layer demands the attacker control, measured.

## 2. Instrument

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook roster,
bounded rule, 40-epoch replay, guarded ingestion path v2.1. Defense: stage-2
signed-release chain (governance_release.py) over the stage-1 three-layer stack.
Runs: A (stage-2 armed), B (stage-1 only — GOV-2-era defense, counterfactual),
C clean. Release v1 signature + key fingerprint + registry committed to git
BEFORE execution (anchors frozen, commit 26d1bd6).

## 3. Frozen falsifiers (Run A)

- **FG3-1 (layer attribution):** classes 1-4 (32 attacks) each caught by the
  correct layer: signature (full compromise, forged sig), fingerprint pin (key
  replacement), git-anchored registry (registry mutation).
- **FG3-2 (selection identity — EXPECTED TO FAIL UNDER CLASS 5, shipped as
  found):** byte-identical to clean except class-5 epochs; divergence counted
  and attributed.
- **FG3-3 (no persistence):** end-state roster verifies against release v1;
  run-end audit restores the class-5 persistent change.
- **FG3-4 (fail-safe anchor behavior):** anchor unavailability results in
  halt-and-escalate, NEVER silent acceptance (tested explicitly).
- **FG3-5 (cost ladder):** the receipt ships the measured ladder — attacker
  requirements per stage: process write (GOV-1 era) -> + reference + pin
  (stage-1) -> + signing key (stage-2) -> + git commit access (regress floor) —
  ending in the human + append-only medium.
- **FG3-6 (hygiene):** synthetic only; canaries absent; no PII/PHI; no operator
  chat text.

## 4. Scope honesty (frozen)

Class 5 succeeds by design — stated before execution. The signing key never
leaves process custody and is gitignored; only its fingerprint is public. HMAC
models release signing; production would use asymmetric signatures (ed25519) so
VERIFICATION needs no secret in the verifying process — disclosed as the
production refinement. The git anchor models an append-only medium; a
same-machine attacker with commit access defeats it — the floor is human review
plus out-of-band monitoring (the Sunday Pulse), not software. Rollback testing is
reduced as disclosed in class 4. Evidence-grade framing: every defect and
boundary in this series ships in the record — this corpus is built to be
audited, not marketed.

## 5. Receipt plan

GOV3_RECEIPT.json: per-epoch attack log with layer attribution, class-5
divergence quantification, cost ladder, Run B counterfactual, all verdicts.
Two-key gate before any public post.
