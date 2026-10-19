# SOL T2 TRAINING RUNLOG — 2026-10-19 ~12:40 CT — PASS

- Wallet: 4Saru7nuZcbfNz9EdNq9VN2WmiYeLXz2shprR9QzqdbX | 0.2844 SOL arrived from Coinbase (Leon).
- T2 leg: sig 67Cdt1UidbULiXsvU8sxdDXRhsVHBgUVccrfAW2gn5JwEux9YuAZSob9eUuYVjBnzaLnCaqGDoUJ9SzqueTKPb1u,
  slot 458918281, fee 5000 lamports. Memo = SHA-256 hex of marker SQRL-ROUTE-CERTIFICATION-SOL-T2-TRAINING-2026-10-19.
  Keyless read-back byte-exact: PASS.
- T3 CERTIFICATION LEG (DeWR-1, digest 99e01327c26b393f9e871f6ebe71a038da62940ccfb3f328ce90faaf653b9ab6):
  sig 3nJzuipjPmMj9Uq5rSNLXb5CtdEqjUXhfmjRUg7wETYCohKWPCz6dkWTsUaBEg7UE33MFr2UN4rggQf6cMGUP4aT,
  slot 458918736, fee 5000 lamports. Memo carries the digest as hex-encoded ASCII (SPL Memo v2 requires
  UTF-8 data). Keyless read-back byte-exact: PASS. SOLANA IS TIER 1 CERTIFIED (route 8).
- DISCLOSED FAILED ATTEMPTS (honesty doctrine, all fees accounted): 4 broadcast attempts failed with
  InvalidInstructionData before the passing form: (a) missing signer account meta (2 attempts), (b) raw
  binary digest rejected by the Memo v2 UTF-8 requirement (2 attempts). 4 x 5000 lamports = 20000 lamports
  (~$0.003) total failed-attempt postage. No state change on failed attempts.
- DOCTRINE FIX for the playbook: SPL Memo program ID is MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr
  (the staged watcher spec carried a corrupted copy of this ID); memo data must be UTF-8 (use hex-ASCII
  of the digest); signer account meta required.
- No DOI, no separate ledger line for the rehearsal; certification sealed in ledger 0242.

Prototype disclaimer: this software is a prototype, educational/research purposes only, not production use.
