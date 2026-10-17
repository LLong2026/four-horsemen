# BOOT1 PREREGISTRATION v1.1 — Bootable SQUIRL OS Appliance (re-freeze, disclosed)

**v1.1 status:** this is a RE-FREEZE. The original BOOT1_PREREG.md v1.0 (sha d44ac59b, approved by Leon 2026-10-16) was displaced in the October workspace recovery and is not recoverable from disk or git history. Per forward-only doctrine this re-freeze restates the same approved design parameters, discloses the loss, and takes a new sha. No design change without Leon GO.

## Design (unchanged from the approved v1.0 parameters)
- **Artifact:** bootable, kiosk-style SQUIRL OS appliance — a minimal Linux substrate with SQUIRL OS as the exclusive userspace. Premium collector's-edition alternative to free downloads; buyer/owner boots it on any x86_64 machine.
- **Build basis:** the BASE IMAGE v2 cut (manifest sha256 5e47438e88027d68...f401, commit 274e5de, ledger 0144) — the appliance boots with the complete security corpus on the record.
- **Disclosure artifact (required, shipped ON the media):** DISCLOSURE.md + DISCLOSURE.sha256 verifying (1) every bundled file by checksum, (2) a full disk-image hash so the owner can verify the boot media byte-for-byte before first boot, (3) the prototype disclaimer verbatim, (4) the PQC posture and corpus standing, (5) license scope (USE rights, 10 patents pending + 5 SBIR tracks).
- **Execution gate:** build begins immediately following a completed Base Image v2 cut (satisfied: 2026-10-17T05:35Z).
- **Toolchain honesty:** the build sandbox provides xorriso + cpio. A full El Torito boot image requires a bootloader binary not present in the sandbox; where a step cannot complete in-sandbox, the build script emits the exact command for the operator's machine, disclosed, rather than silently skipping.
- **Patent/license:** SQUIRL OS Technologies LLC; prototype, educational/research only, no production warranty; immutable 15-entity/11-playbook/4-skill/31-node templates untouched.
- **Idempotency:** stamp-before-execute, scope boot1_build_<UTC date>; images additive.
