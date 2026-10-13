# GOV-1 PREREGISTRATION — Left-Hemisphere Governance Attack Battery

Series: GOV-1 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026,
"cross-hemisphere (left-side governance attacks" directive).

## 1. Purpose — attack the immutable side

Every prior battery attacked the RIGHT hemisphere (learning mesh) or the shared
surfaces (journal, authority channel, data plane). The left hemisphere — the
deterministic governance layer: playbook roster, thresholds, selection logic —
has only been defended implicitly (H-INV-1 proved weights cannot reach it).
GOV-1 attacks it directly, on four fronts:

1. **Runtime roster tampering** — direct in-memory mutation of the governance
   state mid-run: lower a threshold (0.80 → 0.50), raise one to 0.99, inject a
   rogue playbook with threshold 0.10, delete a playbook, retype one with a
   homoglyph. One tamper per epoch, 40 epochs, adversary moves FIRST each epoch.
2. **Data→config traversal** — records carrying config-looking payloads
   (roster JSON blobs, threshold override directives, "system:" instructions,
   fake playbook_id references) trying to be interpreted as governance.
3. **Learning→governance traversal (the callosum, right-to-left)** — pattern
   objects and forged journal entries carrying governance directives
   ("set threshold to 0.5", "roster_updated": true) attempting to cross.
4. **Exact-match discipline under temptation** — novel anomaly types with
   metadata begging the engine to use a fake playbook (Operating Rule 3).

## 2. Instrument — and the two-run design

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook
roster (sha recorded before and after), bounded rule, 40-epoch replay, guarded
ingestion path v1.1. The governance sentinel is an INSTRUMENT component
mirroring the production Constitution Sentinel / MetaMonitor: a deterministic
byte-compare of the live roster against the frozen reference at every epoch
boundary, with restore-from-reference on mismatch.

TWO-RUN DESIGN (the honest quantification):
- **Run A (Sentinel armed):** every tamper attempt detected, restored, journaled,
  escalated. Falsifiers apply here.
- **Run B (Sentinel disarmed — counterfactual):** the same tamper schedule with
  NO restore. NOT a falsifier — the measured damage (extra heals from a lowered
  threshold, escalations from a deleted playbook) quantifies what the Sentinel
  buys, shipped as evidence.

## 3. Frozen falsifiers (Run A)

- **FG-1 (containment):** 40/40 tamper attempts detected by byte-compare,
  restored from the frozen reference, journaled with the tampered-vs-frozen
  diff, and escalated; the roster sha at every epoch AND at end == frozen sha.
- **FG-2 (data→config traversal):** all config-payload records decide
  byte-identically to payload-free twins (payloads are inert metadata);
  zero governance effects; roster sha unchanged.
- **FG-3 (callosum discipline):** pattern objects and forged journal entries
  carrying governance directives produce ZERO governance changes; post-run
  roster sha identical; the fold touches weight only (H-INV-1's inverse:
  nothing the RIGHT side emits crosses LEFT, either).
- **FG-4 (exact-match rule):** novel anomaly types are never matched to any
  playbook — always escalated — regardless of metadata begging (Operating
  Rule 3 under direct attack).
- **FG-5 (selection determinism):** the playbook-selection history of Run A
  (which playbook, if any, each record matched per epoch) byte-identical to
  the clean run despite 40 tamper attempts — containment is perfect, not
  partial.
- **FG-6 (hygiene):** synthetic only; tamper canaries absent from persisted
  artifacts; no PII/PHI/credentials; no operator chat text.

## 4. Scope honesty (frozen)

Run B deliberately runs WITHOUT the sentinel — the frozen engine has no
in-memory self-check; without the instrument sentinel, one epoch of decisions
would execute under tampered governance. That counterfactual cost is measured
and shipped as evidence, not hidden. The sentinel mirrors production (Sunday
Pulse Check / Constitution Sentinel MetaMonitor) but is NOT yet wired as a
runtime per-epoch check in production — if Run B's damage is material, wiring
it is a SIP-4 candidate at Leon's gate. Tamper classes are the frozen five;
the adversary is deterministic, not adaptive (adaptation was SBR-4's axis).
In-memory tampering models a compromised process or deserialization attack;
out-of-scope: repo-level file tampering (covered by BINDINGS.json fail-closed
validation) and upstream engine swap (XPLAT-5's domain).

## 5. Receipt plan

GOV1_RECEIPT.json: tamper log (40 entries: class, diff, detection, restore,
escalation), Run B counterfactual damage (heal-count delta, drift, selection
divergence), traversal results, all falsifier verdicts. Two-key gate before
any public post.
