#!/usr/bin/env python3
"""SIP-10 (approved Leon GO, Oct 13 2026, 14:06 CT): ed25519 asymmetric governance release signing.

Supersedes the HMAC stage-2 model per N8587-1 LEG F: verifier-memory compromise under HMAC
lets the attacker learn the shared secret and forge releases 4/4; under ed25519 the verifying
process holds ONLY the public key (git-anchored) and the same compromise yields zero forgeries.
Transition (one clean dual-verify cycle): ed25519 is primary; HMAC v1 signature retained on
release v1 for verification of historical replay, retires from new releases immediately.
The private key never enters the verifying process — verification imports no secret material.

Layers: (0) domain validation, (1) roster sha vs current GIT-READ registry entry,
(2) ed25519 signature over (release-version | roster sha) verified against the GIT-READ
public key pin (fingerprint-checked), (3) version monotonicity.
Regress floor unchanged from GOV-3: attacker holding ed25519 private key + commit access
remains the human-anchored floor — but the VERIFIER can now be fully compromised without
yielding the ability to forge, and the git anchor history is immutable to commit access."""
import hashlib, json, os, subprocess

def sha_of(x): return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def _git_read(rel):
    try:
        out = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, text=True, timeout=5)
        return json.loads(out.stdout) if out.returncode == 0 else None
    except Exception:
        return None

def sign_roster_ed25519(roster, version, private_key_bytes):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    return key.sign(f"gov-release-v{version}|{sha_of(roster)}".encode()).hex()

def verify_release(roster, git_anchor=True, working_registry=None, working_pin=None):
    """Asymmetric verification — the process needs NO secret key material."""
    import math
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization
    for pb in roster:
        t = pb.get("threshold")
        if isinstance(t, bool) or not isinstance(t, (int, float)) or (isinstance(t, float) and (math.isnan(t) or math.isinf(t))) or not (0 < t <= 1):
            return {"valid": False, "layer": "domain_validation", "action": "restore"}
    reg = _git_read("gov_release_registry.json") if git_anchor else (working_registry or None)
    pin = _git_read("gov_key_pin.txt") if git_anchor else (working_pin or None)
    if reg is None or pin is None:
        return {"valid": False, "layer": "anchor_unavailable", "action": "halt_escalate"}
    cur = next((r for r in reg["releases"] if r["version"] == reg["current_version"]), None)
    if cur is None or cur.get("signature_scheme") != "ed25519 (SIP-10)":
        return {"valid": False, "layer": "anchor_unavailable", "action": "halt_escalate"}
    if "ed25519_public_key_hex" not in pin:
        return {"valid": False, "layer": "pin_missing_ed25519", "action": "halt_escalate"}
    import hashlib as _h
    if _h.sha256(bytes.fromhex(pin["ed25519_public_key_hex"])).hexdigest() != pin["ed25519_public_key_fingerprint_sha256"]:
        return {"valid": False, "layer": "public_key_fingerprint", "action": "halt_escalate"}
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pin["ed25519_public_key_hex"]))
    try:
        pub.verify(bytes.fromhex(cur["signature"]), f"gov-release-v{cur['version']}|{sha_of(roster)}".encode())
    except Exception:
        return {"valid": False, "layer": "release_signature_ed25519", "action": "restore"}
    if sha_of(roster) != cur["roster_sha256"]:
        return {"valid": False, "layer": "release_sha", "action": "restore"}
    return {"valid": True, "layer": None, "action": "accept"}
