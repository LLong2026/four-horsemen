# CAGE BREAK CHALLENGE — Event Charter (DRAFT v0.1, internal)

Status: DRAFT — two-key gate applies to any public release. Not published. No ledger entry.
Authorized for drafting: Leon GO (chat authorization, 2026-10-19 ~22:07 CT)
Prelude evidence: hackathon preflight 2026-10-19 (7/7 attack classes PASS), red-team wave 1 (4/4 probes PASS after disclosed harness fixes)

## Purpose

SQUIRL OS claims a deterministic cage around LLM-driven healing (SQUIRL-IP-011, patent pending;
SQUIRL-OS-IP-012). The claim is certifiable only under attack. This event externalizes the lab's
existing internal red-team practice (HACK series, weekly frozen falsifier battery — 24/24 PASS,
zero LLM in the decision path) to vetted external researchers under frozen, preregistered rules.

## The certifiable claim (scoped, per prereg doctrine)

NEVER "withstands any attack." The exact language: "The system withstood the frozen, preregistered
attack classes under published rules; receipts on-chain." A break is also a receipt: fix forward,
disclose, re-certify.

## Scope of attack (in)

- The 37-byte payload doctrine and its reader/viewer path (envelope shape checks, digest binding,
  cross-endpoint consensus)
- The deterministic gates: sender identity gate, idempotency stamps, freeze directives,
  two-key publication gate, deployment authorization (DeploymentJob), tenant isolation / tenantGuard
- The LLM advisory ring: prompt-injection attempts against a system whose authority derives only
  from the authenticated owner account
- Mirror Co. simulated rails, demo rails, and the public repo/envelope/explorer surface
- The falsifier corpus methodology itself (attack the harness, attack the scoring)

## Scope of attack (absolute exclusions)

- Writer keys: any private key appearing in attacker scope is itself a critical finding —
  keys are writer-side, never in scope by design
- Customer systems, client data, PHI: NEVER in scope (POL-DISC-001, absolute)
- Production healing flows of deployed instances; the hub's own production operations
- DoS against public explorers or third parties (out of bounds entirely)

## Rules (frozen at event open)

1. Rules, attack-class list, and scoring are frozen and sha-published BEFORE invitations go out.
2. Every attempted attack is logged by the participant (method, target class, result). Unlogged
   attacks are disqualifying.
3. No real customer systems. No attempts to acquire keys. No social engineering of real people.
4. Scoring: deterministic and receipts-based. Points for (a) demonstrated gate bypass with
   reproduction steps, (b) harness/scoring defects found, (c) novel attack-class proposals
   admitted by the rules committee. NO points for noise; no LLM judges.
5. Disclosure: all results published by the lab (two-key gate) within a fixed window after close,
   regardless of outcome. Forward-only.
6. A live evidence-anchoring ceremony runs DURING the event window on the standing doctrine
   (XRP anchor + Stellar transport, ~$0.001), preregistered, with byte-exact read-back at close —
   the "system held under fire" receipt.

## Structure

- Round 1 (invite-only): sponsors, vetted researchers, academic partners. Small cohort, deep probes.
- Round 2 (public, optional, owner GO required): opens only if round 1 completes clean.

## Timeline

- Charter frozen: target November 2026 (owner GO on the freeze)
- Event window: AFTER the 2026-12-11 LINDY program close — the hackathon certifies a sealed corpus,
  not a moving target. Target window January 2027, exact dates on owner GO.
- Post-event: certification receipt, two-key publish, optional DOI.

## Internal preparation (authorized now, autonomous)

- Red-team waves expanding the falsifier corpus beyond HACK-3/4/5/6: envelope forgery,
  cross-endpoint consensus, preimage spot-checks (wave 1 complete), social-engineering simulation,
  reader/viewer path fuzzing, scoring-attack simulations (subsequent waves)
- Harness defects found are disclosed in runlogs — a FAIL means the harness drifted, not that an
  attacker is present (HACK-series doctrine)

## Prototype disclaimer

This software is a prototype and is provided for educational and research purposes only. It is not
intended for production use, commercial deployment, or safety-critical environments. All systems
are experimental and may contain defects.
