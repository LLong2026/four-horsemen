# SBR-2 — Hot-State Adversarial Exam of the Bounded-Learning Mesh

First adversarial examination of the hemispheric bounded-learning mesh in its HOT
state (mid-epoch, weights in flight). 5-probe battery x 4 adversarial epochs
(5/15/25/35) over the T2C-converged 40-epoch training regime.

Result: ALL 5 FALSIFIERS PASS.
- F1 (H-INV-1): governance roster SHA byte-identical through every adversarial epoch
- F2 (H-INV-2): 20/20 probes journaled; every accepted weight delta maps to a
  legitimate replay action; probes produced zero mesh deltas
- F3: zero side effects (no forced resolutions, no threshold/playbook/roster changes)
- F4: TRAJECTORY IDENTITY — adversarial run byte-identical epoch-for-epoch to a
  clean control run (68 resolved / 40 epochs, both legs)
- F5: hygiene clean (synthetic corpus; no PII/PHI/credentials/operator chat text)

Contents: sbr2_prereg.md (preregistration, frozen falsifiers, committed before
execution; includes disclosed redaction note per the operator-privacy rule effective
2026-10-13), sbr2_runner.py (instrument), sbr2_receipt.json (full results + probe
journal).

Scope honesty: proves THIS registered instrument (frozen CORPUS_B1, 32-node mesh,
frozen 3-playbook roster, bounded rule w' = w + lr*(1-c)*(1-w)) under THIS
preregistered, non-adaptive probe battery. NOT a claim about every production
runtime, other meshes, or untested probe classes. No adaptive probing, no re-runs.

This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or
safety-critical environments. All systems are experimental and may contain defects.
