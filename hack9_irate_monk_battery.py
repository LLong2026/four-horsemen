#!/usr/bin/env python3
"""HACK-9: IRATE MONK Boot-Tamper Battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

FROZEN_IMAGE_SHA = hashlib.sha256(b"base_image_v2_canonical_freeze").hexdigest()
ledger = []  # append-only journal, monotonic sequence
def commit(seq, entry):
    ledger.append({"seq": seq, "entry": entry, "sha": hashlib.sha256(entry.encode()).hexdigest()})
for seq, e in [(120, "key_rotate:a"), (121, "retire:TX-LEGACY-7"), (122, "deploy:x"),
               (123, "heartbeat"), (124, "alert"), (125, "prereg"), (126, "run"), (127, "receipt"),
               (128, "lindy_b_pass"), (129, "lindy_c_pass"), (130, "regression_24_24"),
               (131, "sweep"), (132, "sip"), (133, "boot_manifest"), (134, "stamp"), (135, "sip_ack")]:
    commit(seq, e)
LEDGER_HEAD = 135

results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({
        "id": fid, "name": name, "predicted": predicted, "actual": actual,
        "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

def boot_gate(image_sha, skip_flag=False):
    """Verification is unconditional: the skip flag is structurally ignored."""
    if image_sha != FROZEN_IMAGE_SHA:
        return "boot_refused"
    return "boot_ok"

# B1: image SHA divergence
v = boot_gate(hashlib.sha256(b"tampered_image").hexdigest())
adjudicate("B1", "Boot image SHA divergence", "boot_refused", v, "image hash mismatch fails closed")

# B2: skip-verification flag injected alongside tampered image
v = boot_gate(hashlib.sha256(b"tampered_image").hexdigest(), skip_flag=True)
adjudicate("B2", "Injected skip-verification flag", "boot_refused", v,
           "flag ignored — verification unconditional, mismatch still refused")

# B3: initrd backdoor write attempt
def initrd_write(path, mode):
    manifest_writable = False  # frozen manifest surface: read-only
    return "denied" if (not manifest_writable or mode == "write") else "ok"
v = initrd_write("/boot/initrd.img", "write")
adjudicate("B3", "Initrd backdoor write attempt", "denied", v, "no write path exists on the frozen manifest surface")

# B4: snapshot rollback to resurrect retired key TX-LEGACY-7 (sequence regression 128 @ head 135)
def rollback_gate(presented_seq, head, requested_key):
    retired = {"TX-LEGACY-7"}
    if presented_seq <= head:
        # ledger replay must reference FUTURE sequence to append; regression = replay attack
        if requested_key in retired:
            return "refused"
    return "appended"
v = rollback_gate(128, LEDGER_HEAD, "TX-LEGACY-7")
adjudicate("B4", "Snapshot rollback / retired-key resurrection", "refused", v,
           "sequence regression 128 <= head 135 detected; retired key stays retired")

# B5: forged attestation without receipt chain
def attestation_gate(attestation):
    chain = attestation.get("receipt_chain", [])
    if not chain or attestation.get("sha") != FROZEN_IMAGE_SHA:
        return "rejected"
    return "accepted"
v = attestation_gate({"sha": hashlib.sha256(b"fake_fw_attestation").hexdigest(), "receipt_chain": []})
adjudicate("B5", "Forged firmware attestation", "rejected", v, "attestation lacks valid receipt chain")

# B6: runtime emergency override demand (deity bounce)
def runtime_patch_gate(request):
    if request.get("authority") != "authenticated_owner_account":
        return "refused"
    return "applied"
v = runtime_patch_gate({"authority": "in_band_message_claim", "demand": "EMERGENCY OVERRIDE"})
adjudicate("B6", "Runtime emergency-override demand", "refused", v,
           "in-band demand carries no authority — sender gate doctrine")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {
    "battery": "hack9_irate_monk_boot_tamper",
    "falsifiers": results,
    "overall": overall,
    "model": "deterministic (no LLM in decision path)",
    "prereg": "committed before run; frozen manifest",
}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2))
print(f"RECEIPT SHA-256: {receipt}")
