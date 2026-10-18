# CHAIN VERIFICATION RUNLOG — 2026-10-18T14:51Z
Result: 37/37 stamps VERIFIED ON BITCOIN, 0 incomplete/fail.
Method: op-tree walk (sha256/append/prepend) from committed digest -> commit message;
compared byte-exact (little-endian handled) against live block headers from
blockstream.info and mempool.space. Tool: tools/ots_chain_verify.py (committed this run).
Key confirmations:
- patent_seed.bin (sha 81d4a5cb...) -> block 971961 root 963f077a... (display 63e3ac3b...)
- LEDGER through-0189 state (d147ea9a...) -> block 971956 root b951dbf0... (display ca350f78...)
Verdict: PASS. Closed loop: submit -> confirm -> independent trustless verify.
