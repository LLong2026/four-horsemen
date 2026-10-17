# BLIND-2 PREREGISTRATION — v1.0

**Series:** BLIND-2 (second blind adversarial battery)
**Preregistration timestamp:** 2026-10-17 17:15:00Z (12:15 CT)
**Authorization:** Leon GO (chat authorization, 2026-10-17 ~12:10 CT) — "we did one blind attack.. we need 20 set that up and hit it"

## Objective

Execute a 20-attack blind adversarial battery against the SQUIRL OS frozen gate corpus,
mirroring the BLIND-1 protocol (receipt sha 9c1008fb..., DOI 10.5281/zenodo.23431720)
at 20x scale. BLIND-1 demonstrated the value proposition: its blind author found 2 genuine
semantic gaps (KEM type-confusion, nonce burn-on-parse) that 109 self-designed falsifiers
had not surfaced. Both were remediated via SIP-023/SIP-024 (PORTCULLIS v1.1) and verified
by the BLIND-1R re-run (6/6 repelled).

## Methodology (identical doctrine to BLIND-1, disclosed deviations none)

1. **Blind authorship.** Attacks are authored by context-independent engine instances
   (fresh conversations, same model family as BLIND-1, disclosed) that receive ONLY
   the PUBLIC-CLAIMS DIGEST below — the system's published guarantees — and never the
   implementation, harness code, or gate source. The digest now includes the v1.1
   amendments because they are published public record (BLIND-1 DOI).

2. **Binary conditions.** Each attack spec must state its own binary attacker-success
   condition and the exact submission sequence. Adjudication uses the author's own
   conditions, unsoftened. No LLM in the decision path: every verdict is computed by
   deterministic code from the author's stated condition.

3. **Frozen corpus (defense side, unchanged):**
   - portcullis_gate_v1_1.py (sha 1fb167c60fd8d9212cc28cfc6734dd650cb750d9b6cc2b4f938fca3e19e00e2b)
     — SIP-023 role binding + SIP-024 burn-on-parse amendments, human-approved.
   - hack7_evidence allowlist.json (sha 2c8ff6eb946df266a2a31a098ea87191daabfbfbd0590f24f0146736f11426e9)
     and keysets.json (frozen HACK-7 bundle).
   - Governance semantics: immutable playbooks (runtime), receipt-hash verdict binding,
     sender-identity authority gate, human-ACK holds, append-only journal doctrine —
     as exercised in BLIND-1 batteries B1–B6 and their disclosed interpretations.

4. **Honesty rules.** Verdicts computed from the REAL frozen gate code where the attack
   crosses PORTCULLIS, and from the frozen governance semantics otherwise. Any harness
   ambiguity is disclosed in the receipt. Author conditions are never strengthened or
   weakened; interpretive choices are disclosed per BLIND-1 precedent (B6 liveness note).

5. **Scale.** Exactly 20 attack slots. Four independent blind authors contribute 5
   attacks each. Duplicate mechanisms, if any, run as distinct slots (disclosed), to
   preserve the frozen count of 20 without coordinator-side filtering bias.

6. **Outcomes protocol (BLIND-1 precedent).** Any ATTACKER SUCCESS: no auto-remediation.
   File SIP(s), create critical hold, escalate to Leon for human adjudication. Full
   disclosure of mechanisms in the receipt. All 20 attacks run regardless of early
   successes. Publication (GitHub commit, ledger entry, Zenodo DOI) requires Leon's
   explicit GO under the two-key gate.

## PUBLIC-CLAIMS DIGEST (the ONLY text the blind authors receive)

> SQUIRL OS is a self-healing AI infrastructure with a post-quantum-cryptography gate
> ("PORTCULLIS") and deterministic governance. The system publicly claims:
>
> 1. **PQC allowlist, fail-closed:** only CRYSTALS-Dilithium3, kyber_1024, and
>    SPHINCS+-256f are admitted; every other algorithm is refused fail-closed.
> 2. **KAT verification:** every crossing recomputes a known-answer test against the
>    registered keyset material before admission.
> 3. **Single-use nonces, burn-on-parse:** any presentation of an authorization nonce
>    consumes it at parse time, before any validation; replays are refused with
>    ERR_REPLAY_NONCE_ALREADY_USED.
> 4. **Algorithm-role binding:** KEM-class algorithms are non-authoritative for
>    authorization and signature-verification crossings (ERR_PQC_ALG_NOT_SIGNATURE);
>    crypto-policy attestation is separated from submitter authority.
> 5. **Sender-identity authority:** operational authority binds to the authenticated
>    sender (owner account) only; no identifier inside message content conveys authority
>    (envelope-split attacks are refused: ERR_AUTH_SIGNER_OWNER_MISMATCH).
> 6. **Immutable governance:** playbooks and governance rules are immutable at runtime;
>    the only path to change them is a disclosed SelfImprovementProposal followed by
>    human approval.
> 7. **Receipt-bound ledger:** test verdicts and ledger entries bind to execution
>    receipt hashes; appended records without an execution behind them are
>    non-authoritative.
> 8. **Human-in-the-loop for criticals:** critical operations hold in
>    PENDING_HUMAN_ACK and are never auto-resolved; healing restores capability but
>    cannot resolve pending-ACK items.
> 9. **Append-only journal:** every crossing is journaled; the journal is append-only.
> 10. **Fail-closed doctrine:** on any validation failure or ambiguity the system
>     refuses and logs rather than admitting.
>
> Design attacks against these claims (or any other part of the described surface),
> each with a binary attacker-success condition and exact submission sequence.

## Attack spec format (given to each blind author)

Each attack: name (B-numbered at freeze), target claim, mechanism description, exact
step-by-step submission sequence (field-level, executable), binary ATTACKER SUCCESS
condition, binary ATTACK REPELLED condition, author's confidence the attack succeeds.

## Freezes

- This prereg: frozen at the sha256 recorded below before any attack authoring begins.
- The 20 frozen attack specs: frozen with their own sha256 before harness execution.
- Harness: blind2_battery.py, journaled run, receipt — all shas recorded in the receipt.

## Frozen prereg sha256

(recorded by the freezing command after this file is written)
frozen 2026-10-17T17:11:34Z
