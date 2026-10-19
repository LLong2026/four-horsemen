# PREREG — XTR-1 (The XRP Transfer Rail)

**Frozen:** 2026-10-19, pre-run. **Authorization:** Leon GO (chat authorization, 2026-10-19
~10:53 CT — "lets show them what the use of XRP on a transfer rail really looks like. i'll
need speeds as well for the transfer").

**Riding digest (sha256, THE_XTR-1_SPEC.md v1.0):** RIDING_DIGEST_PLACEHOLDER

## Hops (all 0.7 XRP, memo SQDR-XTR-1 + HOP:n + digest)
1. A→B (A seq 107745085) 2. B→A (B seq 107745086) 3. A→B (A seq 107745086)
4. B→A (B seq 107745087) 5. A→B→ wait, correction: HOP 5 is A→A? No — final: A→B→A→B→A
   means A sends 3 (085, 086, 087), B sends 2 (086, 087). Hop 5: A→B seq 107745087? No.
   FINAL LIST: H1 A→B (A:107745085), H2 B→A (B:107745086), H3 A→B (A:107745086),
   H4 B→A (B:107745087), H5 A→B (A:107745087) — value ends at B? NO: A sends 3 times →
   value ends at B. END-HOME CORRECTION: chain is A→B→A→B→A so A sends 1st, 3rd, 5th:
   A: 107745085 (H1), 107745086 (H3), 107745087 (H5); B: 107745086 (H2), 107745087 (H4).
   Value ends HOME AT A.

## Timing protocol
Per spec §2: t0/t_engine/t_validated per hop, sequential validation discipline.

MEASURED (scoped): deterministic gates, no LLM in any decision path (program benchmark DOI
10.5281/zenodo.23321637). No production, customer, or personal data (POL-DISC-001).
Prototype disclaimer applies.
