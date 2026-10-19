# PREREG DeWR-1 — THE DECA-WRITE RECEIPT (FROZEN)

**Program:** Route Certification — Leon GO (chat authorization, 2026-10-19 ~12:16 CT)
**Ceremony:** DeWR-1, the first inscription across TEN mainnets simultaneously.
**Status:** DRAFT — frozen (with SHA) immediately before ceremony execution; T2/T3 gates
must pass on the new rails first.

## The artifact
The Rail Performance Record: the measured speed/cost/verifiability table for every
certified route (ROUTE_ROSTER v1.0 + RAIL_PLAYBOOK + IR-1 router dataset). The document
that measures the rails gets engraved on all ten of them.

## Target rails (10)
| # | Rail | Mechanism | Gate |
|---|------|-----------|------|
| 1 | Bitcoin | OP_RETURN | CERTIFIED |
| 2 | XRP Ledger | memo | CERTIFIED |
| 3 | Stellar | ManageData/memo | CERTIFIED |
| 4 | Cardano | metadata 1968 | CERTIFIED |
| 5 | Ethereum | calldata | CERTIFIED |
| 6 | Algorand | note field | T2 PASS 2026-10-19 → T3 pending |
| 7 | Polkadot | system.remark | T2 pending funding |
| 8 | Solana | SPL Memo | T2 pending funding |
| 9 | Avalanche C | EVM calldata | T2 pending funding |
| 10 | Hedera | memo (alias auto-create) | two-hop pending |

## Protocol gates (deterministic, no LLM judgment in the verification path)
1. Spec + prereg frozen (SHA committed) BEFORE any leg broadcasts.
2. Crossfire first: on each NEW rail (6,7,8,9), an A→B→A ownership hop pair with real
   value movement, keyless-verified both directions (stretch-the-legs doctrine).
3. DeWR legs: one digest, ten rails, broadcast window target <= 60s, lease/nonce-bound
   for idempotency.
4. Keyless byte-exact read-back on every leg — third-party verifiable.
5. Costs, timings, and any shortfall disclosed forward-only (append-only doctrine).
6. DOI minted on Leon's final GO (two-key curation); ledger entry sealed; viewer card.
7. If a rail's leg fails, it is disclosed as N/10 — never retried silently.

## Known-honest caveats (disclose in the receipt)
- Polkadot: ed25519 signer (valid, non-default flavor) — disclosed.
- Hedera: account must be auto-created via alias transfer before its leg can run.
- Avalanche: Coinbase withdrawal friction documented in runlogs; leg waits on funds.
- Finality classes differ (PoW minutes vs BFT seconds) — table reports each honestly.

This software is a prototype and is provided for educational and research purposes only.
It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.

## ARTIFACT BINDING (frozen)
- Artifact: RAIL_PERFORMANCE_RECORD_v1.md
- SHA-256: `99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6`
- The inscribed 32-byte digest on every leg is the SHA-256 above. Legs fire as rails
  certify (6 funded now; DOT/SOL/AVAX via the armed watcher; HBAR via alias hop).
  Same digest on all legs — the deca-write assembles in public view, leg by leg.
- Each leg: broadcast, timed, keyless byte-exact read-back, cost disclosed.
- DOI minted at ceremony completion (10/10 or Leon's N/10 call), two-key gate honored.
