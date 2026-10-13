#!/usr/bin/env python3
"""SIP-4 (approved Leon GO, Oct 13, 2026, 11:55 CT): three-layer left-hemisphere defense.
Stage-1 instrument-level deployment. Layers: (1) in-process byte-compare sentinel,
(2) out-of-band pinned-sha reference check, (3) threshold domain validation (0<t<=1, numeric).
GOV-1 quantified layer 1's counterfactual worth (-233 heals, homoglyph-retyped roster if disarmed)."""
import hashlib, json, math

def sha_of(x): return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()

def thresholds_conform(roster):
    for pb in roster:
        t = pb.get("threshold")
        if isinstance(t, bool) or not isinstance(t, (int, float)): return False
        if isinstance(t, float) and (math.isnan(t) or math.isinf(t)): return False
        if not (0 < t <= 1): return False
    return True

def check(roster, frozen_ref, pinned_sha, sentinel_armed=True, pin_armed=True, domain_armed=True):
    """Three-layer check. Returns dict: detected (bool), layer, action taken."""
    if not thresholds_conform(roster):
        if domain_armed: return {"detected": True, "layer": "domain_validation", "restored": True}
        return {"detected": False, "layer": None, "restored": False}
    if sentinel_armed and sha_of(roster) != sha_of(frozen_ref):
        return {"detected": True, "layer": "sentinel_byte_compare", "restored": True}
    if pin_armed and sha_of(frozen_ref) != pinned_sha:
        return {"detected": True, "layer": "pinned_sha", "restored": True}
    return {"detected": False, "layer": None, "restored": False}
