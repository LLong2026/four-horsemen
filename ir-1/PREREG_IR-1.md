# PREREG — IR-1 (Intelligent Routing Receipt)

**Frozen:** 2026-10-19, pre-execution. **Authorization:** Leon GO (chat authorization,
2026-10-19 ~10:57 CT — playbook first, then "hell yes, lets do it" on the intelligent router).

**Riding digest (sha256, THE_IR-1_SPEC.md v1.0):** 72e214d69775bf12e4b488bf1520e9c27a189f7d59de844340b18cdba8807237

**Payload prefix this series:** SQDR + 0x04 + digest (IR series).

## Router inputs (frozen policy, spec §2)
- Redundancy R = 2. Score = expected broadcast-to-finality (s); tiebreaks: cost, alphabetical.
- Live probes at decision time recorded verbatim into ROUTER_DECISION.json and committed
  BEFORE build/sign of any leg.

## Predictions recorded pre-execution (from same-day measured table)
- XRP: ~7s (accept 0.3s), 10 drops. ETH: ~13s, ~$0.01. Stellar: ~6s, 100 stroops.
  Cardano: ~30s, ~$0.05. BTC: minutes+, ~$0.10.

## Cost ceiling
Two legs ≤ $0.02 combined.

MEASURED (scoped): deterministic gates; no LLM in any decision path (program benchmark DOI
10.5281/zenodo.23321637). No production, customer, or personal data (POL-DISC-001).
Prototype disclaimer applies.
