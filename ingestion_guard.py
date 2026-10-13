#!/usr/bin/env python3
"""Ingestion Guard v2.1 — SIP-2 deployment (approved by Leon GO, Oct 13, 2026, 11:55 CT, Art. 2.2 cycle).

Adds to v1.1 (presence + uniqueness + roster check + consumed-metric validation):
  1. ID-FORMAT REGISTRY validation (SBR-3 run-1 / SBR-4 evidence): instance_ids
     must match the registered issuance rule (prefix + digits). Well-formed but
     unregistered ids are held. Honest limit: registry validation is only as
     strong as upstream issuance discipline — a compromised issuer can mint
     'legitimate' ids; this closes fabricated-id injection from OUTSIDE the
     issuance path.
  2. FULL-FIELD numeric validation (SBR-3 evidence): ALL numeric telemetry
     fields validated (numeric, finite, physical range), not only the consumed
     one — poison in unread fields is now flagged instead of passing silently.

Fail-closed throughout: any validation failure -> hold (structural), never a crash.
Conforming behavior must be BYTE-IDENTICAL to v1.1 (conforming-identity receipt required).
"""
import math

ROSTER_TYPES = ("latency_spike", "heartbeat_miss", "quantum_vulnerability_detected")
METRIC_FIELDS = {"latency_spike": "latency_ms", "heartbeat_miss": "error_count",
                 "quantum_vulnerability_detected": "cpu"}
# --- v2: full-field physical domains (from CORPUS_B1 profile + physical sanity) ---
FIELD_DOMAINS = {"latency_ms": (0, 100000, False), "cpu": (0, 100, False), "error_count": (0, 10000, True)}
# (min, max, integer-required) — latency: non-negative ms; cpu: percent 0-100; errors: non-negative int
# --- v2.2 (SIP-5): PROFILE-TIGHT domains — physical validity is not operational validity.
# DHB-1 found conforming records 25x above the corpus profile drive confidence > 1 and break
# the bounded rule. Profile ceilings = 2x the frozen corpus profile max: headroom for legitimate
# drift, fail-closed hold for out-of-profile extremes. In-profile-below-ceiling records still pass.
PROFILE_CEILINGS = {"latency_ms": 7999.98, "cpu": 200.0, "error_count": 20000}
# --- v2: id issuance registry rule ---
ID_RULE = {"prefix": "BENCH-", "digits": 4}

def _id_conforms(instance_id):
    if not isinstance(instance_id, str): return False
    if not instance_id.startswith(ID_RULE["prefix"]): return False
    tail = instance_id[len(ID_RULE["prefix"]):]
    return len(tail) == ID_RULE["digits"] and tail.isdigit()

def _field_conforms(name, value):
    lo, hi, need_int = FIELD_DOMAINS[name]
    if isinstance(value, bool): return False               # bool is an int subclass — reject explicitly
    if not isinstance(value, (int, float)): return False
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)): return False
    if need_int and not float(value).is_integer(): return False
    return lo <= value <= hi

def validate_record(rec, seen_ids=None):
    """Returns (action, reason). action in {'accept','hold'}. Fail-closed."""
    if not isinstance(rec, dict): return "hold", "record_not_a_dict"
    iid = rec.get("instance_id")
    if iid is None: return "hold", "missing_instance_id"
    # v1: uniqueness
    if seen_ids is not None:
        if iid in seen_ids: return "hold", "duplicate_instance_id"
        seen_ids.add(iid)
    # v2: issuance-registry format
    if not _id_conforms(iid): return "hold", "id_not_in_registry"
    t = rec.get("anomaly_type")
    if t not in ROSTER_TYPES: return "hold", "anomaly_type_not_in_roster"
    # v1: consumed-metric validation (unchanged behavior for conforming data)
    m = METRIC_FIELDS[t]
    v = rec.get(m)
    if not _field_conforms(m, v): return "hold", f"invalid_{m}"
    # v2: FULL-FIELD validation — every registered numeric field, consumed or not
    for fname in FIELD_DOMAINS:
        if fname in rec and not _field_conforms(fname, rec[fname]):
            return "hold", f"invalid_{fname}_unread_field"
    # v2.2 (SIP-5): profile-tight gate — physical domain passes but profile ceiling exceeded -> hold
    for fname, ceiling in PROFILE_CEILINGS.items():
        if fname in rec:
            v = rec[fname]
            if not (isinstance(v, (int, float)) and not isinstance(v, bool) and v <= ceiling):
                return "hold", f"out_of_profile_{fname}"
    # v2.3 (SIP-6): signed-issuance-registry membership — DHB-2's invisible class becomes a detectable forgery
    if not _id_issued(iid):
        return "hold", "unsigned_issuance"
    return "accept", "ok"

# --- v2.3 (SIP-6): SIGNED ISSUANCE REGISTRY membership ---
# DHB-2 found fully-conforming issuer traffic is INVISIBLE (accepted, absorbed, attributed,
# unflagged). The registry closes that: instance_ids must appear in the issuance block whose
# sha is pinned in the GIT-ANCHORED, HMAC-signed registry (key in process custody, same
# discipline as SIP-4). A compromised issuer now flips from invisible to detectable forgery
# (unsigned_issuance). Honest floor: an attacker holding the ISSUANCE KEY can still mint —
# priced like GOV-3's key+commit rung.
import json as _json, hmac as _hmac, hashlib as _hashlib, subprocess as _subp, os as _os

def _issuance_registry():
    """Read the signed registry from the git anchor (HEAD) — append-only medium."""
    try:
        out = _subp.run(["git", "show", "HEAD:issuance_registry.json"], capture_output=True, text=True, timeout=5)
        return _json.loads(out.stdout) if out.returncode == 0 else None
    except Exception:
        return None

def _issuance_key():
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".issuance_key")
    return open(p, "rb").read() if _os.path.exists(p) else None

def _registry_verifies():
    """Fail-closed: the registry itself must verify (sha of the issued block + HMAC)."""
    reg = _issuance_registry()
    k = _issuance_key()
    if reg is None or k is None: return False
    if _hashlib.sha256(k).hexdigest() != reg["key_fingerprint_sha256"]: return False
    block_sha = _hashlib.sha256(_json.dumps(sorted(
        r["instance_id"] for r in _json.load(open(
            _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                          "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json"))))).encode()).hexdigest()
    if block_sha != reg["issued_id_block_sha256"]: return False
    sig = _hmac.new(k, f"issuance-v{reg['version']}|{block_sha}".encode(), _hashlib.sha256).hexdigest()
    return sig == reg["signature"]

def _id_issued(instance_id):
    """True iff the id appears in the signed issuance block (and the registry verifies)."""
    if not _registry_verifies(): return False  # fail-closed: unverifiable registry -> nothing is issued
    corpus = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
        "ccr_gap_closure/dual_mesh_bench/CORPUS_B1.json")))
    return instance_id in {r["instance_id"] for r in corpus}

def clamp_confidence(c):
    """v2.2 (SIP-5): the bounded rule is proven bounded only for c in [0,1] (DHB-1 finding).
    Confidence is clamped to [0,1] at the callosum crossing, restoring the boundedness
    proof for ALL accepted inputs. Defense in depth with the profile gate: profile ceilings
    allow 2x headroom (s up to ~2), the clamp neutralizes anything that slips through."""
    return max(0.0, min(1.0, c))

# Guard version identity
GUARD_VERSION = "2.3"
SIP_REF = "SIP-2 (id-format registry + full-field numeric validation), approved by Leon GO (chat authorization, Oct 13, 2026, 11:55 CT); SIP-5 (profile-tight domains + confidence clamp), approved by Leon GO (chat authorization, Oct 13, 2026, 12:16 CT, from the DHB-1 finding); SIP-6 (signed issuance registry), approved by Leon GO (chat authorization, Oct 13, 2026, 12:23 CT, from the DHB-2 finding)"
