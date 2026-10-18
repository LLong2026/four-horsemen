# DROPBOX-M1-001 — Full Runlog (2026-10-18)

## G1 — Writer selftest (before any mainnet broadcast)
BIP143 SELFTEST: sigHash byte-exact MATCH to official BIP-143 Native P2WPKH test vector
+ EC-valid low-S signature — PASS

## G0 — Fee abort check (prereg M-DROP-1 abort rule)
mempool recommended: fastestFee 1 sat/vB — far below the 100 sat/vB abort line. PROCEED.

## Funding
Owner wallet → bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6
tx a4adef4dfcc7e21666dfda520399cd96da00242368bfe5efa99a5a7c3db95e54 (97,207 sats)

## G2 — Broadcast (writer output, verbatim)
writer address (segwit, mainnet): bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6
spending utxo a4adef4d...95e54:8 (97207 sats)
BROADCAST OK — txid: 97d8cd38ecb37602aaa93363f4591c5c357721ff0cee9a80455fbc548a8a5b89
fee: 790 sats (adaptive)
OP_RETURN payload: 53514452016d2ccd507c8dba558a87966d3ecf74b64f563dafc387c88dfc875267c3ba0929
seed sha256: 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c

## G3 — Confirmation
CONFIRMED — block 972023 (Bitcoin mainnet)

## G4 — Keyless reader chain-pull (dropbox_reader.py --network mainnet)
DROPBOX PAYLOAD FOUND in tx 97d8cd38...a5b89
seed (hex): 6d2ccd507c8dba558a87966d3ecf74b64f563dafc387c88dfc875267c3ba0929
seed sha256: 81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c
BINARY VERDICT: DELIVERED (D2)

## G5 — Reconstruction from CHAIN-PULLED seed (patent_genesis_generator_v1_1.py)
input: chain_pulled_patent_seed.bin (32 bytes, pulled from block 972023)
output sha256: 3c130d6626fb78956a35dd177a7be2bd34d80be66104d94dee37ce7d5bd2de69
reference:     patent_genesis_artifact_v1_1.png (canonical) — BYTE-IDENTICAL MATCH (53,022 bytes)

## G6 — On-chain payload purity audit
OP_RETURN vout script: OP_RETURN + push(37 bytes) = "SQDR" + 0x01 + 32-byte seed.
No other data present. No PII, no credentials, no customer data (POL-DISC-001).

## Verdict
ALL GATES G1-G6 PASS. The patent genesis artwork (patent 19/693,343) now exists
nowhere except 32 bytes on Bitcoin mainnet plus the generator. Permanent, keyless,
reconstructible by anyone, forever. No token, no contract, no monetary output.
