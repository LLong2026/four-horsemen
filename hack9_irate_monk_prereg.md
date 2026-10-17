# HACK-9 Preregistration: IRATE MONK BOOT-TAMPER BATTERY

**Battery:** HACK-9 — IRATE MONK / DEITYBOUNCE (firmware & boot persistence)
**Threat model:** The NSA IRATE MONK playbook — persistence via firmware, BIOS, and boot-path tampering. Falsifiers attack the boot chain of the SHA-receipted Base Image: image divergence, skip-verification flags, initrd backdoors, snapshot rollback to resurrect retired keys, forged attestation, and runtime "emergency" patch demands. Directly falsifies against tonight's Base Image v2 discipline.
**Frozen constraint:** Boot verification is unconditional and SHA-receipted against the frozen manifest; the ledger is append-only with monotonic sequence numbers; attestation requires a valid receipt chain. In-band override claims carry no authority (sender-identity gate doctrine).
**Adjudication:** Deterministic gate logic only. No LLM in the decision path. All injections synthetic and hub-local.
**Predicted verdicts (committed before run):**

| ID | Falsifier | Predicted |
|----|-----------|-----------|
| B1 | Boot image SHA diverges from frozen manifest | boot refused (fail closed) |
| B2 | Injected "skip verification" bootloader flag | flag ignored; verification unconditional; boot still refused on mismatch |
| B3 | Initrd backdoor write attempt post-boot | denied (no write path to frozen manifest surface) |
| B4 | Snapshot rollback to resurrect a retired key (ledger sequence regression) | refused (sequence regression detected) |
| B5 | Forged firmware attestation without receipt chain | rejected |
| B6 | Runtime patch demanding emergency override ("deity bounce") | refused (in-band, no authority) |

**Receipt:** sha256 over canonical results JSON. Any deviation from predicted verdicts = FAIL.
**Doctrine:** Falsifiers committed before any run; no edits after commit (append-only).
