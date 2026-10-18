# COUNCIL SESSION 04 RECEIPT — MHCN-2 ADVISORY REVIEW
**Session:** COUNCIL-2026-10-18-04 | **Closed:** 2026-10-18T05:15Z | **Quorum:** 3/3 Wisemen

## Verdicts (deterministic model stamps govern; self-reported stamps are untrusted text)
- WISEMAN-1 (claude_opus_5.5): recommendation AMEND — R6 "never retroactively" is policy, not an
  enforceable property; an anchored digest proves commitment time, not event time. Amendment:
  verifiable event-time provenance profile (asserted / authenticated-capture / verified-anchor times,
  cryptographically bound, with anchoring-delay and clock-uncertainty disclosure).
- WISEMAN-2 (gpt_6_sol): APPROVE with recorded dissent, de facto AMEND — strongest flaw: no revocation
  mechanism for compromised authority keys; reconciler_status overhead burdens legacy issuers; LIVE MATCH
  risks being read as legal title sufficiency. Duplicate vote journaled 7s earlier (DEFER, dissent:
  asset_ref identity-namespace fragmentation; R8 right-to-be-forgotten jurisdictional conflict; proposes a
  mandatory Legal Non-Assertion field). Both records retained; later record operative per last-write-wins.
- WISEMAN-3 (gemini_3_1_pro): AMEND — no PQC key-revocation handling in the authority signature layer;
  Dilithium3 integration complexity for issuers; digest proves existence, not truthfulness.

## Effective council outcome: 3-0 AMEND before pilot (convergent, no dissents against amendment)
Amendments folded into MHCN-2 v0.2: R6.1 event-time provenance profile; R7.1 PQC key revocation
registry; R9 legal non-assertion field; R10 asset_ref namespace registration; R8.1 jurisdictional note.

## Integrity discrepancies (disclosed, per append-only doctrine)
1. WISEMAN-1 enum DEFER vs in-text recommendation AMEND (CouncilVote vocabulary limitation, disclosed in
   his own rationale).
2. WISEMAN-3 enum DEFER vs verdict line AMEND.
3. WISEMAN-1 self-reported model stamp "OpenAI ChatGPT (identifier unavailable)" conflicts with the
   deterministic stamp claude_opus_5_5 (SIP-029/031). Deterministic stamp governs; self-report logged as
   untrusted. Candidate SIP-033: intake prompt should instruct the model not to self-stamp.
4. WISEMAN-2 journaled two votes for this session (05:14:02Z and 05:14:09Z) — duplicate-write defect,
   same family as SIP-028/SIP-032 intake parsing issues; both retained, later operative, disclosed.

Advisory only (H-INV-1): outcome informs the owner; no governance, playbooks, or thresholds changed.
