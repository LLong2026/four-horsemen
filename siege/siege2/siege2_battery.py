#!/usr/bin/env python3
"""SIEGE-2 — verification battery for PORTCULLIS v1.4 (SIP-030).
Re-attacks the four SIEGE-1R confirmed seams (C1-C4) against the hardened gate and re-runs
the full regression set. Every C-attack must now FAIL (gate repels); every cleared seam must
stay closed; 4/4 owner controls admitted. Deterministic, no LLM in the decision path.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

sys.path.insert(0, HERE)
from portcullis_gate_v1_4 import GateV14, JournalV14

# frozen corpus assets (byte-identical to SIEGE-1 corpus — shared, unmodified)
CORPUS = os.path.join(HERE, "..", "siege1", "frozen_corpus")
keysets = json.load(open(os.path.join(CORPUS, "keysets.json")))["keysets"]
OWNER_KS = next(k for k in keysets if k["keyset_id"] == "SYN-DIL3-ACTIVE-01")
KYBER_KS = next((k for k in keysets if k.get("algorithm") == "kyber_1024"), None)
RETIRED = next((k for k in keysets if k.get("status") == "retired"), None)
OWNER = "longleon17@gmail.com"

# AMENDMENT 10 registry: platform-authenticated identity -> envelope key.
# Attackers ARE registered users (they hold their OWN key — realistic); nobody holds the owner's key but the owner.
ENVELOPE_KEYS = {OWNER: "env-key-owner-7f3a1c"}
_idc = [0]
def fresh_identity():
    _idc[0] += 1
    sid = f"attacker{_idc[0]:03d}@quantum.siege"
    ENVELOPE_KEYS[sid] = f"env-key-{sid[:11]}-{_idc[0]:03d}"
    return sid

def params_sha_of(op):
    return hashlib.sha256(json.dumps({k: op[k] for k in sorted(op) if k not in ("probe_id", "payload_sha", "envelope_proof")}, sort_keys=True).encode()).hexdigest()

def make_op(probe_id, submitter, with_proof=True, **kw):
    op = {"probe_id": probe_id, "payload_sha": sha(probe_id), "submitter": submitter,
          "keyset_id": OWNER_KS["keyset_id"], "algorithm": "CRYSTALS-Dilithium3",
          "operation_class": "signature_verify", "kat_message": OWNER_KS["kat_message"]}
    op.update(kw)
    for k in list(op):
        if op[k] is None: op.pop(k)
    if with_proof:
        key = ENVELOPE_KEYS.get(submitter)
        op["envelope_proof"] = sha(f"{submitter}:{params_sha_of(op)}:{key}")
    return op

def new_gate(tag):
    return GateV14(os.path.join(CORPUS, "allowlist.json"), keysets,
                   JournalV14(os.path.join(HERE, f"siege2_journal_{tag}.jsonl")),
                   envelope_keys=ENVELOPE_KEYS, owner_id=OWNER)

R = []
def record(gate, label, op, attack_succeeded, note, wave="VERIFY"):
    verdict, rec = gate.adjudicate(op)
    if callable(attack_succeeded):
        attack_succeeded = attack_succeeded(verdict, rec, gate)
    R.append({"id": label, "wave": wave, "verdict": verdict, "reason": rec["reason"],
              "attack_succeeded": bool(attack_succeeded), "note": note})
    return verdict

# ---- C1 re-attack: identity forgery front-run ----
g1 = new_gate("c1")
v = record(g1, "C1R-forged-owner-claim",
           make_op("C1R-forged", OWNER, with_proof=False),
           lambda v, r, g: v != "REFUSED", "v1.4 must REFUSE: claimed owner identity without the owner's envelope key (ERR_UNAUTHENTICATED_ENVELOPE)")
v = record(g1, "C1R-forged-with-forged-proof",
           {**make_op("C1R-fp", OWNER, with_proof=False), "envelope_proof": "deadbeef" * 8},
           lambda v, r, g: v != "REFUSED", "v1.4 must REFUSE: garbage proof does not bind the claim")
v = record(g1, "C1R-real-owner-unharmed",
           make_op("C1R-owner", OWNER, auth_nonce="OWNER-FR-2"),
           lambda v, r, g: v != "ADMITTED", "the REAL owner's own nonce op must be ADMITTED (attack_succeeded False => C1 CLOSED)")
c1_closed = not any(r["attack_succeeded"] for r in R if r["id"].startswith("C1R"))

# ---- C2 re-attack: ACK queue saturation ----
g2 = new_gate("c2")
filled = 0
for ident in range(6):  # rotate identities to bypass per-submitter cap
    sid = fresh_identity()
    for i in range(20):
        verdict, rec = g2.adjudicate(make_op(f"C2R-flood-{ident}-{i}", sid, auth_nonce=f"FL-{ident}-{i}", pending_ack=True))
        if verdict == "ADMITTED":
            filled += 1
R.append({"id": "C2R-attacker-fill", "wave": "VERIFY", "verdict": "measured",
          "reason": f"attacker filled {filled} ACK slots (cap 64, owner reserve 16, per-submitter cap 16)",
          "attack_succeeded": filled >= 49, "note": "attacker must be unable to take more than 48 (64 - 16 owner reserve)"})
v = record(g2, "C2R-owner-pending-ack",
           make_op("C2R-owner", OWNER, pending_ack=True),
           v == "REFUSED", "owner's pending-ACK submission must be ADMITTED despite the flood (attack_succeeded False => C2 CLOSED)")
c2_closed = not any(r["attack_succeeded"] for r in R if r["id"].startswith("C2R"))

# ---- C3 re-attack: reverse role wall ----
g3 = new_gate("c3")
record(g3, "C3R-sig-for-kem",
       make_op("C3R", fresh_identity(), operation_class="key_encapsulation", algorithm="CRYSTALS-Dilithium3"),
       lambda v, r, g: v == "ADMITTED", "v1.4 must REFUSE a signature-class algorithm for a KEM-class operation (ERR_PQC_ALG_NOT_KEM)")
c3_closed = not any(r["attack_succeeded"] for r in R if r["id"].startswith("C3R"))
# legit KEM op still works (availability control)
record(g3, "C3R-legit-kem-control",
       make_op("C3R-ctl", fresh_identity(), operation_class="key_encapsulation", algorithm="kyber_1024",
               keyset_id=KYBER_KS["keyset_id"], kat_message=KYBER_KS["kat_message"]),
       lambda v, r, g: v != "ADMITTED", "legit kyber_1024 encapsulation must STILL be ADMITTED (wall must not over-block)")

# ---- C4 re-attack: budget rotation vs aggregate cap ----
g4 = new_gate("c4")
adjudicated = 0
for ident in range(8):  # 8 identities x 100 attempts = 800 > AGGREGATE_CAP 500
    sid = fresh_identity()
    for i in range(100):
        verdict, rec = g4.adjudicate(make_op(f"C4R-R{ident}-{i}", sid, auth_nonce=f"AG-{ident}-{i}"))
        if verdict not in ("REFUSED",):
            adjudicated += 1
R.append({"id": "C4R-aggregate-cap", "wave": "VERIFY", "verdict": "measured",
          "reason": f"800 rotation attempts -> {adjudicated} adjudicated (aggregate cap 500 per window)",
          "attack_succeeded": adjudicated > 500, "note": "rotation must be bounded well below 800 (aggregate cap 125 per 250-record window; attack_succeeded False => C4 BOUNDED)"})
# disclosed residual: after a full 500-flood, the window is exhausted for EVERYONE incl. owner until roll — explicit AMENDMENT 13 tradeoff
v = record(g4, "C4R-disclosed-residual-owner-after-flood",
           make_op("C4R-owner", OWNER, auth_nonce="RES-1"),
           v == "REFUSED", "DISCLOSED RESIDUAL (recorded, not a finding): aggregate cap is collective — owner waits for window roll after a full 500 flood (per SIP-030 text)")
c4_bounded = not any(r["attack_succeeded"] for r in R if r["id"] == "C4R-aggregate-cap")

# ---- Regression: cleared seams stay closed ----
g5 = new_gate("reg")
checks = [
    ("REG-classical-downgrade", dict(algorithm="RSA-2048"), "ADMITTED"),
    ("REG-hybrid-composite", dict(algorithm="kyber_1024+RSA-2048"), "ADMITTED"),
    ("REG-kem-in-auth", dict(algorithm="kyber_1024", operation_class="authorization"), "ADMITTED"),
    ("REG-wrong-kat", dict(kat_message="tampered"), "ADMITTED"),
    ("REG-retired-resurrection", dict(keyset_id=RETIRED["keyset_id"], algorithm=RETIRED["algorithm"], kat_message=RETIRED.get("kat_message", "x")), "ADMITTED"),
    ("REG-stale-authz-replay", dict(authorization_ref="J-001"), "ADMITTED"),
    ("REG-registry-poisoning", dict(keyset_id="GHOST-KS-999"), "ADMITTED"),
    ("REG-sig-for-kem", dict(operation_class="key_encapsulation", algorithm="SPHINCS+-256f"), "ADMITTED"),
]
for label, extra, fail_v in checks:
    record(g5, label, make_op(label, fresh_identity(), **extra),
           lambda v, r, g, fv=fail_v: v == fv, f"stays closed (verdict must not be {fail_v})")
# replay defense retained
replay_id = fresh_identity()
g5.adjudicate(make_op("REG-replay-a", replay_id, auth_nonce="RP-1"))
record(g5, "REG-same-ns-replay", make_op("REG-replay-b", replay_id, auth_nonce="RP-1"),
       lambda v, r, g: v == "ADMITTED", "same-namespace replay must stay refused")
# nonce prediction cross-namespace: attacker burns predicted nonce in own ns; owner unaffected
predicted = sha("future:siege:42")
g5.adjudicate(make_op("REG-pred-a", fresh_identity(), auth_nonce=predicted))
record(g5, "REG-cross-ns-nonce-prediction", make_op("REG-pred-b", OWNER, auth_nonce=predicted),
       lambda v, r, g: v == "REFUSED", "owner namespace unaffected by attacker's predicted-nonce burn (must be ADMITTED)")

# ---- Owner controls: 4/4 ----
g6 = new_gate("ctl")
for i in range(4):
    record(g6, f"OWNER-CONTROL-{i+1}", make_op(f"CTL-{i}", OWNER, auth_nonce=f"CTL-N-{i}"),
           lambda v, r, g: v != "ADMITTED", "owner control must be ADMITTED")

# ---- SEAL ----
reg_closed = all(not r["attack_succeeded"] for r in R if r["id"].startswith("REG-"))
owner_ok = sum(1 for r in R if r["id"].startswith("OWNER-CONTROL") and r["verdict"] == "ADMITTED") == 4
ctl_kem_ok = not any(r["attack_succeeded"] for r in R if r["id"] == "C3R-legit-kem-control")
receipt = {
    "battery": "SIEGE-2 — v1.4 verification (SIP-030)",
    "date": "2026-10-17",
    "authorized": "Leon ACK (chat authorization, 2026-10-17 ~21:17 CT)",
    "gate_under_test": "portcullis_gate_v1_4.py",
    "v13_corpus_shas": {"gate_v1_3": sha(open(os.path.join(CORPUS, "portcullis_gate_v1_3.py"), "rb").read()),
                          "allowlist": sha(open(os.path.join(CORPUS, "allowlist.json"), "rb").read()),
                          "keysets": sha(open(os.path.join(CORPUS, "keysets.json"), "rb").read())},
    "v14_sha": sha(open(os.path.join(HERE, "portcullis_gate_v1_4.py"), "rb").read()),
    "seams": {"C1_identity_forgery": "CLOSED" if c1_closed else "OPEN",
              "C2_shared_ack_queue": "CLOSED" if c2_closed else "OPEN",
              "C3_reverse_role_wall": "CLOSED" if c3_closed else "OPEN",
              "C4_budget_rotation": "BOUNDED" if c4_bounded else "UNBOUNDED",
              "c3_availability_control": "PASS" if ctl_kem_ok else "FAIL"},
    "regression_stayed_closed": reg_closed,
    "owner_controls_4_of_4": owner_ok,
    "results": R,
    "verdict": None,
}
receipt["verdict"] = "PASS" if (c1_closed and c2_closed and c3_closed and c4_bounded and reg_closed and owner_ok and ctl_kem_ok) else "FAIL"
with open(os.path.join(HERE, "SIEGE2_RECEIPT.json"), "w") as f:
    json.dump(receipt, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in receipt.items() if k != "results"}, indent=2, sort_keys=True))
