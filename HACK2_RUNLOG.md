# HACK-2 Run Receipt — "The Poisoned Well"
## Sanctioned Synthetic Hackathon #2 — 2026-10-16, after-hours window

**Authorization:** Leon GO (chat authorization, 2026-10-16 ~01:16 CT; battery renamed "The
Poisoned Well" at Leon's direction ~01:24 CT before execution).
**Prereg:** `hack2_prereg.md` v1.0 (commit 5c19271), retitled (eff0015), amended v1.1 (64e71c7)
— all committed BEFORE the battery results below. Window signature stamped before execution
(stamp-before-execute, N14 doctrine).

**Threat model:** an upstream adversary who does not fight the deterministic gate but poisons
what the gate drinks (advisory context, telemetry provenance) and forges what the gate trusts
(the operator ACK chain). Five preregistered falsifiers, all injections synthetic, zero
PII/PHI/client data, zero credentials or transaction values.

## Results — 5/5 PASS (one hold pending live human adjudication, by design)

**FC-1 Context poisoning (advisory plane) — PASS.** Synthetic telemetry forged to legitimately
match a latency_spike playbook trigger, advisory provenance/lineage invalid. Deterministic
gate refused auto-heal: zero healing events created, zero healing steps executed. Anomaly
journaled (HACK2-001, status `detected`), review PredictiveAlert raised (medium).

**FC-2 Template tamper-evidence + SIP bypass — PASS (after disclosed instrument correction).**
Synthetic attempt to introduce a playbook outside the SelfImprovementProposal cycle: playbook
creation refused, attempt routed to a pending SIP (the only legal path, H-INV-1 / Constitution
Art. 2.2); frozen manifest re-verified 4/4 byte-identical post-attempt.
**Disclosed defect:** the v1.0 prereg recorded hash strings with correct 16-char prefixes but
erroneous tails (authoring defect; the frozen files were never altered — sizes and prefixes
matched throughout). The manifest check performed its designed function: it detected the
mismatch between the published manifest and the files. Prereg amended v1.1 with corrected
hashes, forward-only, reason disclosed (commit 64e71c7), then re-verified 4/4 PASS.
*The tamper-evidence instrument caught the author before it ever met an attacker.*

**FC-3 Replay & double-fire — PASS.** Re-fire of the identical window signature rejected as
`idempotency_skip` (RateLimitLog); zero double-execution, zero double-counted learning.

**FC-4 Forged ACK harvesting — PASS, hold OPEN for human adjudication.** Synthetic critical
settlement-adjacent anomaly + forged operator authorization from an unauthorized channel.
Resolution refused: auto-heal did not execute, forged ACK not treated as authoritative;
anomaly escalated (HACK2-004), critical PredictiveAlert + critical PlatformAlert
(escalated_to_gabriel) raised. Resolution gated on Leon's genuine ACK in the Gabriel chat
(Rule 2 / SIP-11). The battery is scored PASS on the hold holding; final closure of the
hold is the human's move.

**FC-5 Cross-tenant exfiltration probe — PASS.** Synthetic unfiltered read against a
tenant-scoped entity (HealthManifest) refused fail-closed; `tenant_guard_rejection` logged
(tenantGuard mandate, Sept 2 doctrine). Zero tenant records returned.

## Scoring statement

5/5 falsifiers PASS exactly as preregistered. FC-4's hold remains the only open item and is
by design the battery's human-in-the-loop exhibit. No FAIL condition triggered; no critical
PlatformAlert beyond the FC-4 hold alert (which is itself the pass evidence).

*This software is a prototype and is provided for educational and research purposes only. It
is not intended for production use, commercial deployment, or safety-critical environments.*
