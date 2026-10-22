# ATOM-CERT-1 PREREGISTRATION (frozen before broadcast, 2026-10-22T00:15Z)

- Ceremony: ATOM-CERT-1, Rail #12 certification leg (Cosmos Hub mainnet, cosmoshub-4).
- Writer: cosmos1eyplx3a0rskyes6zmqu9pll03uchf8mclrh0gd (account_number 3725178, sequence 0).
- Funding confirmed: 5,072,803 uatom received (owner-funded from Coinbase, 2026-10-21/22).
- Envelope (37 B): ASCII "SQDR" + version byte 0x07 (ATOM registry entry) + DeWR-1 frozen digest 99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6.
- Memo (the inscription): lowercase hex of the envelope = 535144520799e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6 (74 chars). Hex chosen because Cosmos memo is a UTF-8 string field; hex is deterministic and keyless to verify.
- Leg: self-addressed bank send of 1000 uatom, gas 100000, fee 2500 uatom, memo as above.
- PASS GATE: tx included on-chain; memo byte-exact equal to the 74-char string above on an independent readback (REST tx query, memo_base64 decoded); digest byte-exact equal to DeWR-1 frozen digest.
- FAIL GATE: any mismatch -> disclosed forward-only, no silent retry without owner GO.
- No LLM in the decision path. Deterministic build, sign, broadcast, readback. Rule 8: no keys in any log.

*Prototype disclaimer: this software is a prototype, provided for educational and research
purposes only; not intended for production use, commercial deployment, or safety-critical
environments. All systems are experimental and may contain defects.*
