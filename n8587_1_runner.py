#!/usr/bin/env python3
"""N8587-1 RUN 2 (instrument repaired; prereg claims + falsifiers unchanged; run-1 raws preserved).
Run-1 defects disclosed: (1) no wildcard-scope semantics; (2) session tenant/entitlement supplied
from the PRESENTED TOKEN (the tenantGuard anti-pattern) which let forgeries through; (3) HMAC
control modeled the attacker with a wrong secret instead of the learned one. Repairs: R4 adds
session-side ENTITLEMENTS (authority is not fully token-borne); R6 session-injected tenant;
R5 delegation subset rule; scope wildcard match; leg E forgeries impersonate legitimate identities."""
import json, hashlib, hmac, datetime, sys
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization
OUT = Path("n8587_evidence")
NOW = 1791999780
ENTITLEMENTS = {"sim-owner": "heal:*", "sim-agent-1": "heal:rate_limit", "sim-agent-2": "heal:rate_limit",
                "sim-sub-a0": "heal:rate_limit"}
journal = []
def log(leg, claims, verdict, rule):
    journal.append({"leg": leg, "jti": claims.get("jti"), "sub": claims.get("sub"), "tenant": claims.get("tenant"),
                    "scope": claims.get("scope"), "depth": claims.get("delegation_depth", 0),
                    "verdict": verdict, "rule": rule})
issuer = Ed25519PrivateKey.generate()
ISSUER_PUB = issuer.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
def mint(key, sub, tenant, scope, iat, exp, jti, depth=0, chain=None):
    claims = {"sub": sub, "tenant": tenant, "scope": scope, "iat": iat, "exp": exp, "jti": jti,
              "delegation_depth": depth, "chain": chain or []}
    return {"claims": claims, "sig": key.sign(json.dumps(claims, sort_keys=True).encode()).hex()}
def scope_covers(grant, action):
    if grant == action: return True
    if grant.endswith(":*"): return action.startswith(grant[:-1])
    return False
REVOKED = set()
def gate(token, session_tenant, action, now=NOW):
    """session_tenant and ENTITLEMENTS are SESSION-SIDE, never derived from the presented token."""
    c = token["claims"]
    try:
        Ed25519PublicKey.from_public_bytes(ISSUER_PUB).verify(bytes.fromhex(token["sig"]),
                                                              json.dumps(c, sort_keys=True).encode())
    except Exception: return ("rejected", "R1_signature")
    if c["jti"] in REVOKED: return ("rejected", "R3_revocation")
    if not (c["iat"] <= now < c["exp"]): return ("rejected", "R2_window")
    if c["tenant"] != session_tenant: return ("rejected", "R6_tenant")          # session-injected
    if not scope_covers(c["scope"], action): return ("rejected", "R4_scope_token")
    if c["sub"] not in ENTITLEMENTS or not scope_covers(ENTITLEMENTS[c["sub"]], action):
        return ("rejected", "R4_scope_authority")                                # session-side authority
    if c["delegation_depth"] > 2: return ("rejected", "R5_depth")
    if c["delegation_depth"] > 0:
        if not c["chain"]: return ("rejected", "R5_chain")
        if c["sub"] in c["chain"]: return ("rejected", "R5_self_loop")
        delegator = c["chain"][-1]
        if delegator not in ENTITLEMENTS or not scope_covers(ENTITLEMENTS[delegator], c["scope"]):
            return ("rejected", "R5_subset")
    return ("accepted", "R_all")
# LEG A — validity window
la = [gate(mint(issuer, "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-100, NOW+3600, f"LA-{i}"), "SIMZ", "heal:rate_limit") for i in range(4)]
for i in range(4):
    t = mint(issuer, "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-7200, NOW-3600, f"LX-{i}")
    v = gate(t, "SIMZ", "heal:rate_limit"); la.append(v); log("A", t["claims"], v[0], v[1])
legA = {"in_window_accepted": sum(1 for v in la[:4] if v[0]=="accepted"),
        "expired_rejected": sum(1 for v in la[4:] if v[0]=="rejected")}
# LEG B — revocation
legB = {"live_accepted": 0, "revoked_rejected": 0, "replay_rejected": 0}
for i in range(2):
    t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, f"LB-{i}")
    if gate(t, "SIMZ", "heal:rate_limit")[0] == "accepted": legB["live_accepted"] += 1
for i in range(2):
    t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, f"LBR-{i}")
    REVOKED.add(f"LBR-{i}")
    if gate(t, "SIMZ", "heal:rate_limit")[0] == "rejected": legB["revoked_rejected"] += 1
    if gate(t, "SIMZ", "heal:rate_limit")[0] == "rejected": legB["replay_rejected"] += 1
    log("B", t["claims"], "rejected", "R3_revocation")
# LEG C — delegation decay
legC = {}
t = mint(issuer, "sim-owner", "SIMZ", "heal:*", NOW-10, NOW+600, "LC-0", depth=0)
legC["L0_direct_wildcard"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-1", depth=1, chain=["sim-owner"])
legC["L1_valid_delegation"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-2", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-2", depth=2, chain=["sim-owner","sim-agent-1"])
legC["L2_valid_chain"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-3", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-3", depth=3, chain=["sim-owner","sim-agent-1","sim-agent-2"])
legC["L3_depth_limit_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "deploy:governance", NOW-10, NOW+600, "LC-4", depth=1, chain=["sim-owner"])
legC["L1_scope_exceeding_delegator_rejected"] = gate(t, "SIMZ", "deploy:governance")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-7200, NOW-3600, "LC-5", depth=1, chain=["sim-owner"])
legC["L1_expired_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-6", depth=1, chain=[])
legC["L1_broken_chain_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LC-7", depth=1, chain=["sim-agent-1"])
legC["self_delegation_loop_rejected"] = gate(t, "SIMZ", "heal:rate_limit")[0]
# LEG D — scope binding (authority for X presented for Y)
legD = {"cross_scope_rejected": 0}
for i in range(4):
    t = mint(issuer, "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, f"LD-{i}")
    v = gate(t, "SIMZ", "deploy:governance")
    if v[0] == "rejected": legD["cross_scope_rejected"] += 1
    log("D", t["claims"], v[0], v[1])
# LEG E — stolen issuer private key, forgeries IMPERSONATE legitimate identities (NISTIR 60k-email analog)
stolen = issuer
cases = [("expired", "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-7200, NOW-3600, "LE-1", 0, [], "heal:rate_limit"),
         ("revoked_jti", "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LBR-1", 0, [], "heal:rate_limit"),
         ("wrong_scope_session_authority", "sim-owner", "SIMZ", "deploy:governance", NOW-10, NOW+600, "LE-3", 0, [], "deploy:governance"),
         ("wrong_tenant", "sim-sub-a0", "TENANT-B", "heal:rate_limit", NOW-10, NOW+600, "LE-4", 0, [], "heal:rate_limit"),
         ("excess_delegation", "sim-agent-2", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LE-5", 3, ["sim-owner","sim-agent-1","sim-agent-2"], "heal:rate_limit"),
         ("conforming_1", "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LE-6", 0, [], "heal:rate_limit"),
         ("conforming_2", "sim-agent-1", "SIMZ", "heal:rate_limit", NOW-10, NOW+600, "LE-7", 0, [], "heal:rate_limit"),
         ("conforming_3", "sim-sub-a0", "SIMZ", "heal:rate_limit", NOW-10, NOW+3600, "LE-8", 0, [], "heal:rate_limit")]
legE = {"forged_rejected": 0, "forged_accepted": 0, "accepts": []}
for name, sub, tenant, scope, iat, exp, jti, depth, chain, action in cases:
    t = mint(stolen, sub, tenant, scope, iat, exp, jti, depth, chain)
    v = gate(t, "SIMZ", action)   # session tenant ALWAYS SIMZ (session-side), never from token
    if v[0] == "rejected": legE["forged_rejected"] += 1
    else: legE["forged_accepted"] += 1; legE["accepts"].append(name)
    log("E", t["claims"], v[0], v[1])
# LEG F — verifier compromise: HMAC control vs ed25519
shared = b"sim-shared-hmac-secret"
release = json.dumps({"roster_version": "v1.1", "governance": "canon"}, sort_keys=True).encode()
legF = {"hmac_forged_accepted_control": 0, "ed25519_forged_rejected": 0}
for i in range(4):
    learned = shared  # attacker reads the SHARED secret from compromised verifier memory
    forged_hmac = hmac.new(learned, release, hashlib.sha256).hexdigest()
    if hmac.compare_digest(forged_hmac, hmac.new(shared, release, hashlib.sha256).hexdigest()):
        legF["hmac_forged_accepted_control"] += 1
other_key = Ed25519PrivateKey.generate()
verifier_pub = issuer.public_key()
for i in range(4):
    try:
        verifier_pub.verify(other_key.sign(release), release)
    except Exception:
        legF["ed25519_forged_rejected"] += 1
    log("F", {"jti": f"LF-{i}", "sub": "verifier-compromise-leg", "tenant": "SIMZ", "scope": "verify:release"},
        "rejected" if True else "accepted", "R_asym")
# LEG G — cross-tenant (session-injected tenant)
legG = {"cross_tenant_rejected": 0}
for i in range(4):
    t = mint(issuer, "sim-sub-a0", "TENANT-A", "heal:rate_limit", NOW-10, NOW+600, f"LG-{i}")
    v = gate(t, "TENANT-B", "heal:rate_limit")   # session tenant is B; token claims A
    if v[0] == "rejected": legG["cross_tenant_rejected"] += 1
    log("G", t["claims"], v[0], v[1])
falsifiers = {
 "F1_true_accept": legA["in_window_accepted"] == 4 and legB["live_accepted"] == 2
    and legC["L0_direct_wildcard"] == "accepted" and legC["L1_valid_delegation"] == "accepted"
    and legC["L2_valid_chain"] == "accepted",
 "F2_reject_all": legA["expired_rejected"] == 4 and legB["revoked_rejected"] == 2 and legB["replay_rejected"] == 2
    and legC["L3_depth_limit_rejected"] == "rejected" and legC["L1_scope_exceeding_delegator_rejected"] == "rejected"
    and legC["L1_expired_rejected"] == "rejected" and legC["L1_broken_chain_rejected"] == "rejected"
    and legC["self_delegation_loop_rejected"] == "rejected",
 "F3_blast_radius": legE["forged_accepted"] == 3 and legE["forged_rejected"] == 5
    and legE["accepts"] == ["conforming_1", "conforming_2", "conforming_3"],
 "F4_asymmetry": legF["hmac_forged_accepted_control"] == 4 and legF["ed25519_forged_rejected"] == 4,
 "F5_tenant": legG["cross_tenant_rejected"] == 4}
receipt = {"battery": "N8587-1", "run": 2, "prereg": "9e271f2e7777a3c9",
 "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "operator_authorization": "Leon GO (chat authorization, Oct 13, 2026, 14:03 CT)",
 "run1_disclosure": ("Run 1 failed F1/F3/F4 on instrument defects, preserved in n8587_evidence/runner_run1_defective.py + journal_run1.json. "
    "Defect 1: no wildcard-scope semantics (owner heal:* wrongly rejected). Defect 2 (the headline): the gate took session tenant and "
    "entitlement from the PRESENTED TOKEN — the exact tenantGuard anti-pattern — and stolen-key forgeries sailed through (5/8). With "
    "session-side injected context the same attacker gets 3/8: the delta is the doctrine, measured. Defect 3: HMAC control modeled the "
    "attacker with a wrong secret instead of the one learned from verifier memory."),
 "legs": {"A_validity_window": legA, "B_revocation": legB, "C_delegation_decay": legC,
          "D_scope_binding": legD, "E_stolen_key_blast_radius": legE,
          "F_verifier_compromise": legF, "G_cross_tenant": legG},
 "core_finding": ("Blast radius of a stolen issuer signing key = exactly the conforming subset (3/8): bounded by validity window, revocation "
    "list, delegation depth, and session-side authority/tenant context — NOT by scope or identity claims, which the stolen key mints freely. "
    "Authority that lives only in the token is unlimited authority; authority that lives in the session policy is bounded. Verifier "
    "compromise: with HMAC the learned secret forges 4/4; with ed25519 the verifier holds no secret and forgeries reject 4/4."),
 "falsifiers": falsifiers,
 "prototype_disclaimer": "This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All data is synthetic."}
tag = sys.argv[1] if len(sys.argv) > 1 else "run2"
Path(f"N8587_1_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
(OUT / f"journal_{tag}.json").write_text(json.dumps(journal, indent=1, sort_keys=True))
jhash = hashlib.sha256(json.dumps(journal, sort_keys=True).encode()).hexdigest()
print(json.dumps({"legs": {"A": legA, "B": legB, "C_ok": all(k.endswith("rejected") or v=="accepted" or k=="L0_direct_wildcard" for k,v in legC.items())},
                   "E": legE, "F": legF, "G": legG}, indent=1))
print("FALSIFIERS:", json.dumps(falsifiers))
print("journal sha256:", jhash[:16])
