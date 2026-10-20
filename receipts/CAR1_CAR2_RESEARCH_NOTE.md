# The Covenant Carrier: CAR-1 & CAR-2 — What We Learned
**SQUIRL OS Technologies — Research Note | 2026-10-20 | Ledgers 0269, 0270 | RAILS v1 frozen**

## The problem we were solving
Anchoring proof on Bitcoin is final but slow and priced like real estate; the fast
rails are cheap but hold no value. Liquidity, gas fees, and global routing were three
separate problems. CAR-1 and CAR-2 close all three with one architecture:

1. **Liquidity** — the satoshi itself is the estate. A 330-sat P2TR covenant output
   carries the 1,920-leaf corpus root inside its output key (SAT-2). It never moves
   to prove something; it commits in place.
2. **Gas fees** — the sat's *identity* travels instead of the sat. A 32-byte composite
   digest SHA256(outpoint ‖ root) rides the fast rails: 100 stroops on Stellar, 10
   drops on XRP — **~$0.00003 total per carrier send**.
3. **Global routing** — every repaired route from CFR-9, MCR-1/2, SAT-1/2 and SBR-1 is
   now frozen into a one-command kit (RAILS v1: `rails/RAILS_FROZEN_v1.md` +
   `rails/squirrel_rails.py`). No more repairing. That is the scale unlock.

## What we learned, measured
| | CAR-1 (first construction) | CAR-2 (frozen kit) |
|---|---|---|
| Build time | ~1 hour (manual construction) | one command, zero repairs |
| XLM leg | 4.7s (ledger 65045996) | 5.4s (ledger 65046560) |
| XRP leg | 1.5s (ledger 107787805) | **0.8s** (ledger 107788499) |
| Cost | ~$0.00003 | ~$0.00003 |
| Verification | keyless, byte-exact both rails | keyless, byte-exact both rails |

- The pointer is a claim; the chain is the truth. Every step of verification recomputes
  from public data alone — no trust in us required (G0/G1/G2 gates, all PASS).
- **Dual security, no fail**: any carrier transaction can be followed two ways — the
  sat itself on Bitcoin (follow the outpoint), and the hash on Stellar (follow the
  entry). Two independent networks must both lie for the record to break.
- Staleness is a feature: any covenant move renders old pointers stale by design, and
  the tamper watch re-arms the carrier with a fresh outpoint‖root digest automatically.

## Does it get faster with use? Yes — in the ways that matter
The ledger close times are physics (XLM ~5s, XRP ~4s per ledger) and we will never
beat a clock with a command. What compounds is everything around the clock:
- **Zero repair**: CAR-1 took an hour to construct; CAR-2 took one command. The next
  send takes one command too, forever. That is the real speedup, and it is permanent.
- **Parallel firing**: the kit's legs are independent — fired concurrently, total time
  approaches the *slowest* leg, not the sum. SBR-1 already proved 8 anchors in ~4s.
- **The learning loop feeds the routes**: every new rail lesson (DOT's post-2025 XCM,
  Cardano's CBOR pair order, XRP's readback shape) is now a frozen route, not tribal
  knowledge. Each ceremony makes the next one cheaper in operator time — which is
  the only cost left.

## The receipts (gold, as requested)
- **The covenant satoshi (Bitcoin, block 972280):**
  https://mempool.space/tx/1f6d4b53b386cddc9d47890f2738673246166379b6a19102b2f344f4371be19c
- **CAR-1 — Stellar transport (ledger 65045996):**
  https://stellar.expert/explorer/public/tx/582fe3360bb24eb8d51a980d81c57c6adfb46208cc9ae23844dac0b1d5a89f6a
- **CAR-1 — XRP anchor of record (ledger 107787805):**
  https://livenet.xrpl.org/transactions/5DA9404FA5C142CE3B8AF4FD044C0774C7D9A92000A3F7137216A900A0F7BE9C
- **CAR-2 — Stellar transport (ledger 65046560):**
  https://stellar.expert/explorer/public/tx/2e8b59fe668cf67e5e0329b3a6a1e18dc284c7e3086bfb867019245bd6343b30
- **CAR-2 — XRP anchor of record (ledger 107788499):**
  https://livenet.xrpl.org/transactions/4389BE1CF80FBFC1E0CD02170F4918DF76DABCF5FCBEEBC4491C31BA0CD26F82
- **Ledger entries 0269/0270:** https://github.com/LLong2026/four-horsemen

All five records are now live in the Satoshi Track app (SAT-COV-2, CAR-1, CAR-2
HashRecords) — the sat tracker makes every future ceremony leg followable by
the sat on Bitcoin and the hash on Stellar, dual-verified.

## The last frontier: universal smart routing through SWIFT
The honest read: SWIFT is a member-owned cooperative. Touching it directly requires
being a licensed, supervised financial institution with a BIC — a certification we
do not hold and should not pretend to hold. But the *message standard* it runs on,
ISO 20022, is public, and the Universal Bridge already speaks it fluently (patent
pending, 64/094,360 / 19/693,343 family).

So the smart play is exactly the two Leon named, and we recommend the second:
- **Wait for the right sponsor.** A member bank or licensed fintech partner can plug
  the bridge into SWIFT without us ever being the member. Our ISO 20022 demonstration
  corpus (Universal Seed → deterministic routing → canonical settlement receipts) is
  the asset that makes a sponsor say yes — the value is *being sponsor-ready*, not
  in chasing a certification we cannot use alone.
- **Until then, leave it alone.** The public rails already prove the routing thesis
  end to end, keylessly, for three hundredths of a cent. The frontier is not a door
  we knock on; it is a door that opens when someone with a BIC wants what is on the
  other side of it. The record shows the capability. The sponsor brings the keys.

Engraved proofs pointing at wallets would technically work today — but nobody would
understand them. The sends are how people *see* anchoring until anchoring speaks for
itself. And now that we still have to send something, we send it in one command,
with zero repairs, at stroop prices.

---
*This software is a prototype and is provided for educational and research purposes
only. It is not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.*
