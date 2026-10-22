# THE TRIAD — Default Notarization Route (SAT + XLM + XRP), v1.0

**Established:** 2026-10-22, per Leon (chat authorization, ~02:37 CT) — "the major focus is
on SAT, XLM, and XRP... make that the default as the setup."
**Scope stamp:** triad_route_v1.0_2026-10-22. Supersedes nothing; promotes an existing
proven configuration (TL-1, PAT-1 both ran this exact trio) to standing default.

## 1. Doctrine

Every STANDARD notarization event = one triad fire. Three rails, three consensus
engines, three roles:

| Member | Role | Engine | SLO | Fee doctrine |
|--------|------|--------|-----|--------------|
| **SAT (BTC)** | Notary anchor — the immovable substrate | SHA-256 PoW | ~1 block (~10 min) expected; **hard deadline 3 blocks (~30 min)** | dynamic sats/vB from mempool.space, **ceiling 30 sat/vB hard stop** |
| **XLM** | Display rail — human-readable named entry | Stellar SCP | included ≤ 3 ledgers (~12s) | static 100 stroops |
| **XRP** | Attestation rail — redundant fast institutional anchor | XRPL consensus | validated ≤ 3 ledgers (~12s) | static 10 drops (20 only on terQUEUED) |

## 2. Why these three (and not others)

1. **No shared failure mode.** SCP, XRPL consensus, and PoW are three independent
   engines run by three disjoint operator populations. If a fast rail halts, the other
   fast rail plus SAT still carry the event; if both fast rails halt, SAT finality is
   untouched. No other trio on the roster has this property at this cost.
2. **Stable fees.** None of the three runs a base-fee auction market. The speed-sim's
   one real defect was exactly that pathology (ETH legacy gas vs base fee). The triad
   has no analogous defect surface: fees are static (XLM/XRP) or capped (SAT).
3. **Complementary surfaces.** XLM `manage_data` renders as a named, human-readable
   entry (viewer-friendly, the public face); XRP memos are the institutional attestation;
   SAT is the notary-grade epoch stamp nobody can rewrite. Read, Verify, Learn, Check —
   the viewer already speaks all three.
4. **Cost.** Full triad at current fees: ~800 sats + 100 stroops + 10 drops ≈ **under
   $0.10 per event.** Cheapest reliable unit on the roster.
5. **Proven.** TL-1 (trustable lock) and PAT-1 (patent lock) both ran this exact trio
   byte-exact. This is promotion of a working configuration, not a new experiment.

## 3. Hardened rules (standing, enforceable in `triad_fire.py`)

**Write-path failover pairs (15s timeout, 3 attempts before failover):**
- SAT: mempool.space `/tx` → blockstream.info `/api/tx`
- XLM: horizon.stellar.org (single canonical public endpoint; 3x retry, 10s backoff;
  on catastrophic failure the event holds at SAT finality and XLM refires on recovery)
- XRP: xrplcluster.com → s1.ripple.com (full submit failover, sequence re-fetched per endpoint)

**Read-path (dual, byte-exact, 10s timeout, 3 attempts):**
- SAT: mempool.space + blockstream.info
- XLM: horizon.stellar.org (operations endpoint) + stellar.expert
- XRP: xrplcluster.com (tx) + api.xrpscan.com (raw data)

**Idempotency:** the envelope registry plus `TRIAD_LEGS.json` — a fired digest never
refires without a new ceremony tag. UTXO/spend check before every SAT leg.

**Inclusion poll:** fast rails 2s cadence to validated/included; SAT 60s cadence to
30-minute hard deadline; miss = escalate to operator, never silent.

**Readback gate:** 3/3 byte-exact on dual endpoints = PASS. Any miss = fail-closed,
escalate, no partial credit.

**Envelope doctrine unchanged:** version byte marks ceremony class (0x0D BTC-specific
epoch, 0x0F PAT, 0x10 route speed-sim, 0x06 MCR-class); the triad is a ROUTE, not a
new ceremony class.

## 4. When the triad is NOT enough

- **Major epoch events** (MCR-class corpus seals, patent locks with full proof spread)
  still fan out to the wider mesh (12 rails) for maximal cross-domain proof.
- **HBAR** joins as a fourth member on the standing alias once funded + certified
  (T1 probe → T2 training leg → T3 per the roster protocol); expected ~3s aBFT.
- Minor rails (ALGO/SOL/AVAX/DOT/ATOM/ADA/LTC/DOGE) remain certified and callable
  but are no longer part of the DEFAULT configuration.

## 5. Disposition

The triad is now the default notarization configuration of record. ROSTER v1.2
carries it as `DEFAULT ROUTE`. First hardened proof run: TRIAD-SIM-1 (2026-10-22),
receipts in `triad/`.
