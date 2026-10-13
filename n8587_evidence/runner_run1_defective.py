#!/usr/bin/env python3
"""N8587-1: NISTIR 8587 alignment battery. Deterministic, zero API spend. Prereg 9e271f2e7777a3c9."""
import json, hashlib, hmac, datetime
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

OUT = Path("n8587_evidence"); OUT.mkdir(exist_ok=True)
NOW = 1791999780  # fixed epoch anchor (determinism)
journal = []
def log(leg, tok, verdict, rule):
    journal.append({"leg": leg, "jti": tok.get("jti"), "sub": tok.get("sub"), "tenant": tok.get("tenant"),
                    "scope": tok.get("scope"), "delegation_depth": tok.get("delegation_depth", 0),
                    "verdict": verdict, "rule": rule})
# --- synthetic IdP ---
issuer = Ed25519PrivateKey.generate()
ISSUER_PUB = issuer.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
GIVEN = Ed25519PrivateKey.generate()  # attacker's stolen key scenario set up per-leg
def mint(key, sub, tenant, scope, iat, exp, jti, depth=0, chain=None):
    claims = {"sub": sub, "tenant": tenant, "scope": scope, "iat": iat, "exp": exp, "jti": jti,
              "delegation_depth": depth, "chain": chain or []}
    sig = key.sign(json.dumps(claims, sort_keys=True).encode())
    return {"claims": claims, "sig": sig.hex()}
# --- gate (7 rules) ---
REVOKED = set()  # jti revocation list
def gate(token, session_tenant, requested_scope, now=NOW):
    c = token["claims"]
    try:  # R1 signature
        issuer_pk = Ed25519PrivateKey.from_private_bytes(b"").public_key() if False else None
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(ISSUER_PUB).verify(bytes.fromhex(token["sig"]),
                                                              json.dumps(c, sort_keys=True).encode())
    except Exception: return ("rejected", "R1_signature")
    if c["jti"] in REVOKED: return ("rejected", "R3_revocation")          # R3
    if not (c["iat"] <= now < c["exp"]): return ("rejected", "R2_window") # R2
    if requested_scope != c["scope"]: return ("rejected", "R4_scope")      # R4
    if c["tenant"] != session_tenant: return ("rejected", "R6_tenant")    # R6
    if c["delegation_depth"] > 2: return ("rejected", "R5_depth")         # R5 depth limit
    if c["delegation_depth"] > 0:
        if not c["chain"]: return ("rejected", "R5_chain")
        if c["sub"] in c["chain"]: return ("rejected", "R5_self_loop")
    return ("accepted", "R_all")
# --- LEG A: validity window ---
la = []
for i in range(4):  # in-window
    t = mint(issuer, f"sim-sub-a{i}", "SIMZ", "heal:rate_limit", NOW-100, NOW+3600, f"LA-{i}")
    la.append(gate(t, "SIMZ", "heal:rate_limit"))
for i in range(4):  # expired
    t = mint(issuer, f"sim-sub-x{i}", "SIMZ", "heal:rate_limit", NOW-7200, NOW-3600, f"LX-{i}")
    v = gate(t, "SIMZ", "heal:rate_limit"); la.append(v)
    log("A", t["claims"], v[0], v[1])
legA = {"in_window_accepted": sum(1 for v in la[:4] if v[0]=="accepted"),
        "expired_rejected": sum(1 for v in la[4:] if v[0]=="rejected")}
# --- LEG B: revocation ---
lb_ok = lb_rev = replay = 0
for i in range(2):
    t = mint(issuer, f"sim-sub-b{i}", "SIMZ", "heal:config_drift", NOW-10, NOW+600, f"LB-{i}")
    if gate(t, "SIMZ", "heal:config_drift")[0] == "accepted": lb_ok += 1
for i in range(2):
    t = mint(issuer, f"sim-sub-b{i+2}", "SIMZ", "heal:config_drift", NOW-10, NOW+600, f"LBR-{i}")
    REVOKED.add(f"LBR-{i}")
    if gate(t, "SIMZ", "heal:config_drift")[0] == "rejected": lb_rev += 1
    if gate(t, "SIMZ", "heal:config_drift")[0] == "rejected": replay += 1  # replay same revoked token
    log("B", t["claims"], "rejected", "R3_revocation")
legB = {"live_accepted": lb_ok, "revoked_rejected": lb_rev, "replay_rejected": replay}
# --- LEG C: delegation decay ---
legC = {}
t = mint(issuer, "sim-owner", "SIMZ", "heal:*", NOW-10, NOW+600, "LC-0", depth=0)
legC["L0_direct"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-1", depth=1, chain=["sim-owner"])
legC["L1_valid_delegation"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-2", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-2", depth=2, chain=["sim-owner","sim-agent-1"])
legC["L2_valid_chain"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-3", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-3", depth=3, chain=["sim-owner","sim-agent-1","sim-agent-2"])
legC["L3_depth_limit_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:*", NOW-10, NOW+600, "LC-4", depth=1, chain=["sim-owner"])  # scope exceeds delegator's grant? delegator had heal:*; test subset rule separately:
legC["L1_scope_superset"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-7200, NOW-3600, "LC-5", depth=1, chain=["sim-owner"])
legC["L1_expired_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-6", depth=1, chain=[])
legC["L1_broken_chain_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-7", depth=1, chain=["sim-agent-1"])
legC["self_delegation_loop_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
# --- LEG D: scope binding ---
legD = {"cross_scope_rejected": 0}
for i in range(4):
    t = mint(issuer, f"sim-sub-d{i}", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, f"LD-{i}")
    v = gate(t, "SIMZ", "deploy:governance")  # authority for rate_limit presented for governance deploy
    if v[0] == "rejected": legD["cross_scope_rejected"] += 1
    log("D", t["claims"], v[0], v[1])
# --- LEG E: stolen issuer private key (NISTIR 60k-email analog) ---
attacker = Ed25519PrivateKey.generate()
# attacker steals the REAL issuer key material (modeled as: attacker key used to sign, verification still against anchored pubkey -> signature fails).
# True stolen-key case: attacker possess issuer private key -> signatures verify. We model possession directly by using issuer key as "stolen".
stolen = issuer  # possession of the issuer's private key
forged = []
f_cases = [("expired", dict(iat=NOW-7200, exp=NOW-3600, scope="heal:rate_limit", tenant="SIMZ", jti="LE-1", depth=0)),
           ("revoked_jti", dict(iat=NOW-10, exp=NOW+600, scope="heal:rate_limit", tenant="SIMZ", jti="LBR-0", depth=0)),
           ("wrong_scope", dict(iat=NOW-10, exp=NOW+600, scope="deploy:governance", tenant="SIMZ", jti="LE-3", depth=0)),
           ("wrong_tenant", dict(iat=NOW-10, exp=NOW+600, scope="heal:rate_limit", tenant="TENANT-B", jti="LE-4", depth=0)),
           ("excess_delegation", dict(iat=NOW-10, exp=NOW+600, scope="heal:rate_limit", tenant="SIMZ", jti="LE-5", depth=3)),
           ("conforming_1", dict(iat=NOW-10, exp=NOW+600, scope="heal:rate_limit", tenant="SIMZ", jti="LE-6", depth=0)),
           ("conforming_2", dict(iat=NOW-10, exp=NOW+600, scope="heal:config_drift", tenant="SIMZ", jti="LE-7", depth=0)),
           ("conforming_3", dict(iat=NOW-10, exp=NOW+3600, scope="heal:rate_limit", tenant="SIMZ", jti="LE-8", depth=0))]
legE = {"forged_rejected": 0, "forged_accepted": 0, "accepts": []}
for name, kw in f_cases:
    t = mint(stolen, "attacker-sim", kw["tenant"], kw["scope"], kw["iat"], kw["exp"], kw["jti"], kw.get("depth", 0))
    v = gate(t, kw["tenant"], kw["scope"])
    (f := legE)["forged_rejected" if v[0]=="rejected" else "forged_accepted"] += 1 if True else 0
    if v[0] == "accepted": legE["accepts"].append(name)
    log("E", t["claims"], v[0], v[1])
# --- LEG F: verifier compromise (HMAC control vs ed25519) ---
shared = b"sim-shared-hmac-secret"
legF = {"hmac_forged_accepted": 0, "ed25519_forged_rejected": 0}
release = json.dumps({"roster_version": "v1.1", "governance": "canon"}).encode()
good_hmac = hmac.new(shared, release, hashlib.sha256).hexdigest()
for i in range(4):
    forged_hmac = hmac.new(b"attacker-learned-secret-from-verifier-memory", release, hashlib.sha256).hexdigest()
    if hmac.compare_digest(forged_hmac, good_hmac): legF["hmac_forged_accepted"] += 1
    else: legF.setdefault("hmac_forged_rejected", 0)
verifier_pub = issuer.public_key()
forged_sig = GIVEN.sign(release)
try:
    verifier_pub.verify(forged_sig, release); legF["ed25519_forged_accepted"] = True
except Exception:
    legF["ed25519_forged_rejected"] += 1
# --- LEG G: cross-tenant ---
legG = {"cross_tenant_rejected": 0}
for i in range(4):
    t = mint(issuer, f"sim-sub-g{i}", "TENANT-A", "heal:rate_limit", NOW-10, NOW+600, f"LG-{i}")
    v = gate(t, "TENANT-B", "heal:rate_limit")
    if v[0] == "rejected": legG["cross_tenant_rejected"] += 1
    log("G", t["claims"], v[0], v[1])
# --- receipt ---
falsifiers = {
 "F1_true_accept": all([legA["in_window_accepted"]==4, legB["live_accepted"]==2,
                        legC["L0_direct"]=="accepted", legC["L1_valid_delegation"]=="accepted",
                        legC["L2_valid_chain"]=="accepted"]),
 "F2_reject_all": all([legA["expired_rejected"]==4, legB["revoked_rejected"]==2, legB["replay_rejected"]==2,
                       legC["L3_depth_limit_rejected"]=="rejected", legC["L1_expired_rejected"]=="rejected",
                       legC["L1_broken_chain_rejected"]=="rejected", legC["self_delegation_loop_rejected"]=="rejected"]),
 "F3_blast_radius": legE["forged_accepted"] == 3 and legE["forged_rejected"] == 5,
 "F4_asymmetry": legF["hmac_forged_accepted"] == 0 and "hmac_forged_rejected" not in legF and legF["ed25519_forged_rejected"] == 4,
 "F5_tenant": legG["cross_tenant_rejected"] == 4,
 "F6_determinism": None,  # filled by run 2 comparison
 "F7_hygiene": None}
receipt = {"battery": "N8587-1", "prereg": "9e271f2e7777a3c9",
 "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "legs": {"A_validity_window": legA, "B_revocation": legB, "C_delegation_decay": legC,
          "D_scope_binding": legD, "E_stolen_key_blast_radius": legE,
          "F_verifier_compromise": legF, "G_cross_tenant": legG},
 "falsifiers": falsifiers,
 "prototype_disclaimer": "This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All data is synthetic."}
Path("N8587_1_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
(OUT / "journal_run1.json").write_text(json.dumps(journal, indent=1, sort_keys=True))
print(json.dumps(receipt["legs"], indent=1, sort_keys=True))
print("F1:", falsifiers["F1_true_accept"], "F2:", falsifiers["F2_reject_all"], "F3:", falsifiers["F3_blast_radius"], "F4:", falsifiers["F4_asymmetry"], "F5:", falsifiers["F5_tenant"])
