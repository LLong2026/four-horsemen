#!/usr/bin/env python3
"""SIP-7 external verification leg (approved Leon GO, Oct 13, 2026, 12:34 CT).

The run-end audit compares LIVE anchor file shas against the DOI-bound
ANCHOR_BINDINGS record. With keys+commit, local git falls — the DOI-bound
record does not. A divergence is a DETECTED forgery; an unverifiable binding
record is fail-closed (treat as: NOT detected locally, escalate to human)."""
import json, hashlib, os

def sha_bytes(b): return hashlib.sha256(b).hexdigest()

def load_binding(path=None):
    p = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "ANCHOR_BINDINGS.json")
    if not os.path.exists(p): return None
    try: return json.load(open(p))
    except Exception: return None

def check_anchor(file, live_sha, binding=None):
    """Returns dict: detected (bool) + reason. detected=True means FORGERY CAUGHT."""
    b = binding or load_binding()
    if b is None: return {"detected": False, "reason": "binding_record_unavailable_fail_closed_escalate"}
    a = next((x for x in b["anchors"] if x["file"] == file), None)
    if a is None: return {"detected": False, "reason": "anchor_not_bound"}
    if live_sha != a["sha256_git_head"]:
        return {"detected": True, "reason": "anchor_fingerprint_divergence_from_doi_bound_record", "bound": a["sha256_git_head"], "live": live_sha}
    return {"detected": False, "reason": "anchor_matches_doi_bound_record"}

def verify_all():
    """Run-end audit leg: check every bound anchor's live sha."""
    b = load_binding()
    if b is None: return {"ok": False, "reason": "binding_record_unavailable"}
    out = {}
    for a in b["anchors"]:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), a["file"])
        live = sha_bytes(open(p,"rb").read()) if os.path.exists(p) else None
        out[a["file"]] = check_anchor(a["file"], live, b)
    return {"ok": all(not v["detected"] and v["reason"] == "anchor_matches_doi_bound_record" for v in out.values()), "anchors": out}
