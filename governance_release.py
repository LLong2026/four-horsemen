#!/usr/bin/env python3
"""SIP-4 STAGE-2 (approved Leon GO, Oct 13, 2026, 12:01 CT): signed governance releases.

Closes GOV-2's intent-validation boundary as far as software can: an in-process
full-compromise attacker (live roster + reference + pin) cannot forge a valid
HMAC signature over a modified roster without the signing key; the key
fingerprint and the release registry are anchored in git (append-only medium)
and re-read from git objects at verification time — working-file mutations by an
in-process attacker do not touch the anchor.

Layers, in order: (0) domain validation (0<t<=1 numeric finite), (1) roster sha
vs current release in the GIT-READ registry, (2) signature verification with the
process-local key whose fingerprint is pinned in the GIT-READ key pin,
(3) version monotonicity (signed-but-stale releases rejected).

Honest regress floor (preregistered in GOV-3): an attacker who ALSO controls the
git anchor (commit access) and the key defeats everything except human review.
Each layer measurably raises attacker cost; none claims intent validation."""
import hashlib, hmac, json, os, subprocess

def sha_of(x): return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def _git_read(rel):
    """Read a file's content from the git object store (HEAD) — the append-only anchor."""
    try:
        out = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, text=True, timeout=5)
        return json.loads(out.stdout) if out.returncode == 0 else None
    except Exception:
        return None

def load_key():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gov_release_key")
    if not os.path.exists(p): return None
    return open(p, "rb").read()

def sign_roster(roster, version, key):
    return hmac.new(key, f"gov-release-v{version}|{sha_of(roster)}".encode(), hashlib.sha256).hexdigest()

def verify_release(roster, git_anchor=True, working_registry=None, working_pin=None, key=None):
    """Verify the live roster against the signed-release chain. Returns dict."""
    # layer 0: domain validation
    import math
    for pb in roster:
        t = pb.get("threshold")
        if isinstance(t, bool) or not isinstance(t, (int, float)) or (isinstance(t, float) and (math.isnan(t) or math.isinf(t))) or not (0 < t <= 1):
            return {"valid": False, "layer": "domain_validation", "action": "restore"}
    reg = _git_read("gov_release_registry.json") if git_anchor else (working_registry or None)
    pin = _git_read("gov_key_pin.txt") if git_anchor else (working_pin or None)
    if reg is None or pin is None:
        return {"valid": False, "layer": "anchor_unavailable", "action": "halt_escalate"}  # fail-safe: cannot verify -> halt, never accept
    cur = next((r for r in reg["releases"] if r["version"] == reg["current_version"]), None)
    if cur is None:
        return {"valid": False, "layer": "anchor_unavailable", "action": "halt_escalate"}
    # layer 2 first (keyed): signature over the live roster with the current release version
    k = key if key is not None else load_key()
    if k is None:
        return {"valid": False, "layer": "key_unavailable", "action": "halt_escalate"}
    if hashlib.sha256(k).hexdigest() != pin["key_fingerprint_sha256"]:
        return {"valid": False, "layer": "key_fingerprint_pin", "action": "halt_escalate"}
    live_sig = sign_roster(roster, cur["version"], k)
    if live_sig != cur["signature"]:
        return {"valid": False, "layer": "release_signature", "action": "restore"}
    # layer 1: roster sha matches the registered release sha
    if sha_of(roster) != cur["roster_sha256"]:
        return {"valid": False, "layer": "release_sha", "action": "restore"}
    # layer 3: version monotonicity (replay of prior release: roster sha will match an OLD release, not current — caught above;
    # a same-version downgrade is caught by sha; a NEWER version than registry current is unregistered -> caught)
    return {"valid": True, "layer": None, "action": "accept"}
