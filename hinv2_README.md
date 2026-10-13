# H-INV-2 — Lineage Forgery Battery: The Crossing Ledger Cannot Be Forged

Direct attack on the journaled-crossing invariant (H-INV-2): can an adversary
FABRICATE history the mesh will believe? Pairs with SBR-2 (adversary during
learning); this battery attacks the audit ledger itself.

Instrument: 40-epoch bounded training (T2C lineage, frozen CORPUS_B1, 32-node mesh,
frozen 3-playbook roster, bounded rule w' = w + lr*(1-c)*(1-w)) producing the true
crossing journal (2,646 accepted crossings). Frozen 6-class forgery battery, 8
instances each, plus 106 controls (every 25th accepted crossing):

- B1 orphan weight updates (no source event)
- B2 forged event ids
- B3 temporal forgeries (real id, epoch outside the recorded window)
- B4 duplicate crossings (exact replay; idempotency)
- B5 orphan healing events (feed no pattern update — Rule 7)
- B6 mismatched pattern lineage (wrong anomaly type)

Result: ALL 5 FALSIFIERS PASS.
- F1: 106/106 controls VALID with complete lineage (chain intact; after reproduces
  the bounded rule exactly)
- F2: 48/48 forgeries rejected AND journaled — zero silent drops
- F3: mesh state and journal byte-identical before/after the battery
- F4: determinism re-run byte-identical; append-only held
- F5: hygiene clean (synthetic corpus; no PII/PHI/credentials/operator chat text)

INSTRUMENT DEFECTS DISCLOSED: two validator defects were caught by the battery's
own controls before publication (v1: historical crossings judged against current
mesh state; v2: global event-id matching where the corpus replays per-epoch, plus a
full-dict duplicate compare). v3 splits audit vs gate validation modes. No probe
class, falsifier, or acceptance bar changed across repairs; all 48 forgeries were
rejected in every version. Disclosed per the honest-instrument-error precedent.

Contents: hinv2_prereg.md (preregistration with frozen falsifiers, committed before
execution), hinv2_runner.py (instrument), hinv2_receipt.json (full verdict ledger).

Scope honesty: proves THIS registered instrument under THIS frozen battery — not a
claim about every journal implementation or untested forgery classes.

This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.
