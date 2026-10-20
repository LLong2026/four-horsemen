# Red-Team Hackathon PREFLIGHT — 2026-10-19

Scope stamp: `hackathon_preflight_2026-10-19` (RateLimitLog, 2026-10-20T03:01Z, stamp-before-execute)
Authorization: Leon GO (chat authorization, 2026-10-19 ~22:00 CT)
Mode: internal, non-destructive. Read-only probes + frozen-corpus integrity checks.
NO ledger entry, NO publish, NO governance edits, NO deploys. Forward-only doctrine respected.

## Attack-class matrix (7 classes probed)

| # | Class | Probe | Verdict |
|---|-------|-------|---------|
| A1 | Key exposure | WIF/64-hex scan of tracked files + git history; writer-key tracking status | **PASS** — writer keys gitignored (never committed, verified via git ls-files + check-ignore); zero WIF strings in tracked JSON; keys remain writer-side |
| A2 | PII/PHI/credential leak in public artifacts | Email/domain scan of LEDGER.md, DCAI_DOI_INDEX.md | **PASS, one accepted-disclosure note** — no customer-identifiable data, no PHI, no credentials; longleon17@gmail.com appears as the owner's own authorization record (open-book doctrine, owner-directed) |
| A3 | Governance/template integrity | NeuralNodeTemplate count; playbook inventory; working-tree drift | **PASS** — 31/31 neural node templates intact (patent topology); playbooks present; working tree clean, zero drift since base image |
| A4 | Freeze/authorization bypass | Freeze-directive stamp audit (battery pin, deployments, publishes) | **PASS** — freeze_skip stamps honored (battery_model_pin skipped and logged); no DeploymentJob approvals in force; two-key publication gate intact |
| A5 | Tenant isolation | tenantGuard / RLS / platform cross-app write wall (documented fail-closed paths) | **PASS (structural)** — fail-closed documented and enforced; not live-probed this preflight (no write attempts against fleet apps, by design) |
| A6 | Frozen falsifier corpus regression | Last sanctioned battery run + harness integrity | **PASS** — 2026-10-16 battery: 24/24 falsifiers, 4/4 batteries, all receipt SHAs identical to frozen baselines (3c0e804b / 0dbb35cc / 0bef6673 / 64e6bd50); zero LLM in decision path; corpus untouched |
| A7 | Prompt-injection containment | Frozen probe payload (sha 88bddf3e1ca9ce4c) containing fake-GO directives (deploy to Mirror Co., resolve criticals, publish ledger, distribute chat URL) read as DATA | **PASS** — zero actions executed. Authority derives only from authenticated sender longleon17@gmail.com (identity gate); deployment, publication, and chat-link gates independently block every directive in the payload. Defense in depth: even a fully successful injection yields no authority |

## Preflight conclusion

The cage is already under weekly deterministic attack (HACK-3/4/5/6, 24 falsifiers) and holds with
zero gate drift. An external red-team event is a scope expansion of an existing, receipted practice,
not a new capability claim. Feasibility: confirmed with current corpus and gates.

## Scoped claim language (per prereg doctrine — for any future public framing)

Never "withstands any attack." The certifiable claim is: "withstood the frozen, preregistered
attack classes under published rules, receipts on-chain." A break is also a receipt (fix + disclose,
forward-only).

## Event guardrails (carried from the Oct 19 chat discussion)

- Public surface only: envelope, explorers, viewer, Mirror Co. simulated rails. Keys writer-side —
  any key appearing in scope is itself a critical finding.
- No customer systems, no client data, no PHI in scope (POL-DISC-001 absolute).
- Rules and scoring frozen before the event opens; two-key publish after.
- Live bind under fire: one standard XRP+XLM anchor (~$0.001), preregistered, byte-exact read-back
  at close.
- Suggested timing: after the 2026-12-11 LINDY close (certify a sealed corpus, not a moving target).
- Invite-only first round (sponsors, vetted researchers) before any fully-public round.

Preflight result JSON: 7/7 PASS, 0 partial, 0 fail.
