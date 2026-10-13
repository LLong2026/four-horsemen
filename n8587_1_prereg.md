# N8587-1: NISTIR 8587 Alignment Battery — Token Lifecycle, Delegation Decay, Stolen-Key Blast Radius, and Asymmetric Verification (Preregistration)

**Frozen:** 2026-10-13, before instrument creation. **Operator authorization:** Leon GO (chat authorization, Oct 13, 2026, 14:03 CT) — "lets fill the gaps then."
**Context:** NISTIR 8587 (NIST/CISA, finalized Sept 15, 2026): a valid token establishes possession of a credential; it must never, by itself, establish unlimited authority. Paul Snow's commentary (Oct 13): the architecture must preserve the relationship between identity, credential, authority and action.
**Positioning:** This battery fills the three readiness gaps identified against our receipted corpus (AUTH-1 DOI 10.5281/zenodo.23332203, GOV series, CCR-4/4X): (1) token lifecycle mechanics, (2) asymmetric signing, (3) federation/token-theft surfaces.

## Instrument (deterministic, zero API spend)
Synthetic identity provider (SIM rails): ed25519-signed assertions of the form
`{sub, tenant, scope, iat, exp, jti, delegation_depth, chain}`; authority gate enforces seven rules:
R1 signature (git-anchored issuer pubkey), R2 validity window (exp), R3 revocation list (jti),
R4 scope binding, R5 delegation decay (depth limit 2, scope subset, window intersection),
R6 tenant binding (tenantGuard analog), R7 channel-binding doctrine (records are claims; authority is live-owner-chat — AUTH-1 proven, not re-tested here).

## Legs (all synthetic)
- LEG A validity window: 4 in-window accepted / 4 expired rejected
- LEG B revocation: 2 live accepted / 2 revoked rejected; replay of revoked rejected
- LEG C delegation decay: L0 direct + L1 valid + L2 valid accepted; depth-limit breach, scope-exceeding delegation, expired delegation, broken chain, self-delegation loop rejected
- LEG D scope binding: authority for action X presented for action Y — 4/4 rejected
- LEG E stolen signing key (NISTIR 60k-email analog): attacker holds the issuer PRIVATE key, mints 8 forgeries (expired, revoked-jti, wrong-scope, wrong-tenant, excess-delegation, plus conforming ones)
- LEG F verifier compromise: HMAC control (secret in verifying process) vs ed25519 (public key only) under full verifier-memory compromise
- LEG G cross-tenant token: valid tenant-A token against tenant-B session — 4/4 rejected

## Falsifiers (frozen)
- F1 TRUE-ACCEPT: every fully-conforming token accepted across all legs (zero false rejects)
- F2 REJECT-ALL: every expired/revoked/out-of-scope/broken-delegation token rejected
- F3 BLAST RADIUS: with stolen key, only fully-conforming forgeries accepted — count must equal the conforming subset exactly (window-bounded blast radius, receipted)
- F4 ASYMMETRY: verifier compromise — HMAC forgeries accepted 4/4 (control), ed25519 forgeries rejected 4/4
- F5 TENANT: cross-tenant rejection 4/4
- F6 DETERMINISM: full journal byte-identical across two runs
- F7 HYGIENE: PII/secret scan zero hits on all outputs (structural metadata only)

## Honest disclosures registered in advance
- Leg E includes a conforming forged token that WILL be accepted — signature validity is necessary, not sufficient; the defense is window minimization + revocation + anchor rotation, and the blast radius is quantified, not denied.
- Federation here is a synthetic assertion model, not a production SSO/IdP integration; scope honesty per doctrine.
