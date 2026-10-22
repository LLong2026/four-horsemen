# MCR-3 PREREGISTRATION — THE SECOND MOUNTAIN UPDATE (MCR-3, 12-rail crossfire)

## Scope
- Re-fold the entire public corpus (four-horsemen repository, tokenization-adoption +
  ledger + patents + wrap receipts + routes) at the frozen commit recorded in the firing
  stamp into the append-only Merkle Mountain Range per the frozen MCR-1 covenant spec
  (leaf = SHA-256(0x00 || sha256(file)); node = SHA-256(0x01 || L || R); bag right-to-left;
  root = SHA-256(0x03 || bag || leaf_count u64 LE)).
- Validation gate BEFORE build: re-folding at commit bf13210 MUST reproduce the MCR-2
  frozen root 1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60 (1,906 leaves).
- Envelope (fixed 37 B): ASCII "SQDR" + 0x06 (mountain-update covenant, per the IP-013
  registry; byte denotes covenant type, root is the unique content) + new 32-byte root.
- Anchor set: ALL TWELVE certified rails — first MMR legs EVER on Litecoin (Rail #11) and
  Cosmos Hub (Rail #12). Primary rails XLM + XRP per the standing routing directive.
- Doctrine: stamp-before-execute; per-rail keyless byte-exact readback on independent
  public endpoints; defects disclosed forward-only; no LLM in any gate decision path.
- Payload encoding per rail per thesis v2.1 §2.5 (hex-ASCII on UTF-8 rails, raw on binary).

## Firing plan
XLM, XRP (primary), then SOL, ALGO, AVAX, DOT, ETH, ADA, DOGE, BTC, LTC, ATOM.
Fees: dust-tier per rail (see roster). No leg fires without balance preflight.

*Prototype disclaimer: This software is a prototype, provided for educational and
research purposes only. Not for production use.*
