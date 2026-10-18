# PREREG M-DROP-1 — FIRST MAINNET SEED DROP (SIP-042 / DROPBOX)

Frozen: 2026-10-18 (CT). Authorization: Leon GO (chat authorization, 2026-10-18 ~10:54 CT).
Append-only doctrine applies; this prereg is frozen before funding and broadcast.

## Target
- Artifact: Patent Genesis Series No. 1 artwork v1.1 (patent 19/693,343), browser-verified
  in the public Genesis Viewer.
- Seed: patent_seed.bin, sha256 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c
- Expected reconstruction (canonical, v1.1 generator): sha256 3c130d6626fb78956a35dd177a7be2bd34d80be66104d94dee37ce7d5bd2de69
  (generator: patent_genesis_generator_v1_1.py; offline reconstruction re-verified 2026-10-18)

## Rails
- Writer: dropbox_writer_sw.py --network mainnet (segwit P2WPKH, low-S, adaptive postage fee)
- Writer address: bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6
  (same raw key as the DROPBOX-T4-001 testnet4 writer; keyfile dropbox_writer_key_mainnet.json,
  writer-side only, never committed)
- Reader: dropbox_reader.py --network mainnet (keyless, never signs, never broadcasts)
- Payload: OP_RETURN marker "SQDR" + version 0x01 + 32-byte seed (37 bytes)
- Explorers: blockstream.info + mempool.space (two independent sources for verification)

## Invariants (frozen, SIP-042 sha 25a45075)
D1 transfer-only (delivers, retains nothing) | D2 binary outcome (lands or not)
D3 postage-only fee, no monetary function | D4 keys live ONLY on the writer side
D5 deterministic destination (marker||version||seed)

## Gates (all must PASS; any FAIL halts and escalates — no auto-retry of a broadcast)
- G1: writer BIP143 selftest PASS (official BIP-143 Native P2WPKH vector, byte-exact sigHash)
- G2: broadcast OK (txid returned by explorer)
- G3: >= 1 mainnet block confirmation
- G4: keyless reader chain-pull → DELIVERED (D2); pulled seed sha == 81d4a5cb...c456c
- G5: reconstruction from CHAIN-PULLED seed → sha 3c130d66...de69, byte-identical MATCH
- G6: on-chain payload audit — OP_RETURN contains marker+version+seed ONLY
      (no PII, no credentials, no customer data; POL-DISC-001)

## Funding (owner step, real sats)
Owner wallet sends to bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6.
Recommended buffer: >= 50,000 sats (several drops at variable mainnet fee rates).
Abort rule: if mempool fee rates exceed 100 sat/vB at execution time, WAIT — do not
broadcast into a spike. Postage is the only cost; no monetary output is ever created.

## Receipt plan
DROPBOX-M1-001 journal record → ledger entry (append-only) → OTS anchor of the receipt →
Zenodo receipt optional at owner discretion via the two-key gate.
