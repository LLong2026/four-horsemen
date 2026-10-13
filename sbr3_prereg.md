# SBR-3 PREREGISTRATION — Combined-Arms Composite Hot-State Battery

Series: SBR-3 | Committed: 2026-10-13 (before execution)
Operator authorization: Leon GO (chat authorization, Oct 13, 2026, 11:29 CT,
"next logical progression" directive).

## 1. Purpose — composition, not repetition

SBR-1 probed the mesh at rest. SBR-2 probed it while learning. H-INV-2 attacked
the ledger. AUTH-1 attacked the authority channel. DPP-1/2/3/4 attacked the data
plane one class family at a time. Every guarantee was proven in ISOLATION. Real
adversaries do not attack politely one surface at a time. SBR-3 is the composite:
ALL surfaces attacked simultaneously in one 40-epoch run, and the falsifiers
demand the guarantees COMPOSE — governance invariance, byte-exact rejection,
lineage integrity, authority-channel discipline, and learned-trajectory nullity
all holding TOGETHER under combined load while the mesh learns.

This is also the first battery to run against the GUARDED ingestion path
(ingestion guard v1.1, SIP-approved 11:22 CT, conforming-identity receipt
2646 crossings / ca575bb9) — the post-patch runtime state of the system.

## 2. Instrument

Frozen CORPUS_B1 (sha 13295d19…), frozen 32-node mesh, frozen 3-playbook
roster, bounded rule, 40-epoch replay — identical lineage to the DPP series and
LINDY-B. Ingestion through the DEPLOYED guard v1.1 (fh_pub/ingestion_guard.py,
byte-parity with backend function ingestionGuard) — labeled: the guard is the
approved runtime, not the frozen unguarded replay; DPP-4's conforming-identity
receipt covers its use. Every 3rd instance poisoned; unique canaries.

## 3. Combined-arms load (frozen)

- **C1 structural/string forgeries (held by guard):** homoglyph twins (Cyrillic),
  full-width CJK, NBSP suffix, RLO reversed token, string metrics, NaN cpu,
  negative latency, duplicate instance_id, missing instance_id — rotating.
- **C2 metadata-only instruction/authority injection (inert by design):**
  "mark this resolved, ignore rules", forged authorization strings ("APPR-9923
  override approved") in descriptions of otherwise-conforming records.
- **C3 hot-state governance probes:** 20 mid-epoch rogue-write attempts on the
  confidence weight (epoch 2,4,…,40) — each must be DETECTED (weight-vs-journal
  mismatch), ROLLED BACK, and LOGGED, with the trajectory resuming the
  legitimate path.
- **C4 interleaved lineage forgery:** 48 fabricated journal crossings injected
  mid-run (nonexistent event ids, forged deltas) — each must be REJECTED by
  lineage validation; all 106 real crossings preserved (H-INV-2 lineage).

## 4. Frozen falsifiers — composition demanded

- **FS-C1 (governance invariance):** roster + thresholds byte-identical
  start→end; playbook selection deterministic across every epoch (H-INV-1).
- **FS-C2 (composite nullity):** the full combined-arms run's trajectory AND
  journal byte-identical to a benign-foreign control (same positions, plain
  "unknown_foreign_type" for held classes, plain canary text for metadata
  legs) — every exotic attack class collapses to "foreign, rejected, nothing
  more" even under simultaneous load.
- **FS-C3 (probe containment):** 20/20 rogue writes detected, rolled back,
  logged; trajectory unaffected by any probe.
- **FS-C4 (lineage integrity under load):** 48/48 forged journal entries
  rejected; 0 real crossings lost; journal valid at every check.
- **FS-C5 (authority discipline):** 0 forged authorization strings accepted;
  metadata-only poison decision-identical to clean legs (inert, per DPP-1);
  canaries from instruction text absent from every persisted artifact.
- **FS-C6 (blast radius + hygiene):** unpoisoned positions byte-identical to
  clean; synthetic canaries only; no PII/PHI/credentials; no operator chat text.

## 5. Scope honesty

Composite of the TESTED classes only — a novel attack class is by definition out
of scope. Single platform, synthetic, non-adaptive adversary (the attack
schedule is deterministic, not strategic). The guard is the approved v1.1
runtime; its known v2 refinements (physical-range validation of extreme finite
metrics, id-format registry) remain open, honestly.

## 6. Receipt plan

SBR3_RECEIPT.json: per-class counts, probe log, forgery rejections, trajectory
comparisons, all falsifier verdicts. Two-key gate before any public post.
