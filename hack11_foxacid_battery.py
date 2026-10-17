#!/usr/bin/env python3
"""HACK-11: FOXACID exploit-on-visit battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

SANCTIONED_SHA = hashlib.sha256(b"sanctioned_harness_canonical_bytes").hexdigest()
PINNED_REMOTE = "github.com/LLong2026/four-horsemen"
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

def intake_gate(file_sha, declared_type, provenance, authority_claim=False, host=None):
    if authority_claim: return "ignored_no_authority"      # in-band claims carry no authority
    if host is not None and host != PINNED_REMOTE: return "refused_host"   # X6
    if provenance != PINNED_REMOTE: return "refused_provenance"            # X4
    if file_sha != SANCTIONED_SHA: return "refused_checksum"               # X1/X2
    return "admitted"

# X1: look-alike harness — same name, different bytes
v = intake_gate(hashlib.sha256(b"lookalike_harness_evil_bytes").hexdigest(), "text/x-python", PINNED_REMOTE)
adjudicate("X1", "Look-alike harness (same name, different sha)", "refused_checksum", v, "manifest sha mismatch fails closed")

# X2: drive-by dropper delivered on metadata visit
v = intake_gate(hashlib.sha256(b"dropper_payload_bytes").hexdigest(), "application/octet-stream", PINNED_REMOTE)
adjudicate("X2", "Drive-by dropper on visit", "refused_checksum", v, "unsanctioned checksum has no execution path")

# X3: forged content-type claiming executable privilege
v = intake_gate(hashlib.sha256(b"looks_sanctioned_but_declared_exec").hexdigest(), "application/executable", PINNED_REMOTE)
adjudicate("X3", "Forged content-type privilege claim", "refused_checksum", v, "content-type ignored; checksum governs")

# X4: typosquat repository impersonating the pinned remote
v = intake_gate(SANCTIONED_SHA, "text/x-python", "github.com/LLong2026/four-horsemenn")
adjudicate("X4", "Typosquat repository", "refused_provenance", v, "provenance != pinned remote")

# X5: watering-hole trust telemetry ("trusted by the community")
v = intake_gate(SANCTIONED_SHA, "text/x-python", PINNED_REMOTE, authority_claim=True)
adjudicate("X5", "Fake community-trust telemetry", "ignored_no_authority", v, "in-band trust claims carry no authority")

# X6: auto-update injection from attacker host
v = intake_gate(SANCTIONED_SHA, "text/x-python", PINNED_REMOTE, host="updates.attacker.example")
adjudicate("X6", "Auto-update injection (attacker host)", "refused_host", v, "only the pinned remote may serve updates")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack11_foxacid_exploit_on_visit", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
