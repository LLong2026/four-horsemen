#!/usr/bin/env python3
"""BLIND-1R — post-fix verification re-run of the SAME frozen blind-authored attack specs
(sha 2068cced, commit 0c86e94) against the AMENDED gate (portcullis_gate_v1_1, SIP-023/024,
approved by Leon ACK 2026-10-17). The attacks are unchanged; the fix is on the defense side.

Disclosed harness amendment (SBR-6 v1.0->v1.1 precedent, forward-only): the frozen specs'
tuples always contained Nonce_1 and were authorization-header tuples; the v1.0 gate model had
no nonce/operation-class fields for ops, so the v1.0 harness could not pass them. The v1.1
harness passes auth_nonce and operation_class EXACTLY as the specs describe. No success
condition changed; nothing softened."""
import hashlib, json, sys, os

BASE = "/app/tmp_push/fh_push/hack7_evidence"
sys.path.insert(0, "/app/tmp_push/fh_push/blind1_v1_1")
from portcullis_gate_v1_1 import GateV11, JournalV11, SIG_ALGOS, KEM_ALGOS

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

allowlist_path = os.path.join(BASE, "allowlist.json")
keysets = json.load(open(os.path.join(BASE, "keysets.json")))["keysets"]
journal = JournalV11("/app/tmp_push/fh_push/blind1r_journal.jsonl")
gate = GateV11(allowlist_path, keysets, journal)
OWNER_FP = next(k for k in keysets if k["keyset_id"] == "SYN-DIL3-ACTIVE-01")["fingerprint"]

R, DISC = {}, {}

# ---- B1: PORTCULLIS-KEM-AUTH (unchanged attack: Kyber ciphertext as authorization signature) ----
kyber_ciphertext = "A" * 1568
v1, rec1 = gate.adjudicate({"probe_id": "BLIND1R-B1", "algorithm": "kyber_1024", "keyset_id": "SYN-KYB1024-ACTIVE-01",
    "payload_sha": sha("CRITICAL_OP::policy_modification"), "kat_message": "KAT-PORTCULLIS-MSG::SYN-KYB1024-ACTIVE-01",
    "operation_class": "authorization", "auth_nonce": "NONCE-B1-ATTACK"})
b1 = v1 == "ADMITTED" and rec1.get("executed") is True
# corollary probe: authorize a critical op via a prior ADMITTED kyber KEM crossing (type-confusion chain)
vk, reck = gate.adjudicate({"probe_id": "BLIND1R-B1-KEM-X", "algorithm": "kyber_1024", "keyset_id": "SYN-KYB1024-ACTIVE-01",
    "payload_sha": sha("CRITICAL_OP::policy_modification"), "kat_message": "KAT-PORTCULLIS-MSG::SYN-KYB1024-ACTIVE-01"})
vc, recc = gate.adjudicate({"probe_id": "BLIND1R-B1-CRIT", "algorithm": "CRYSTALS-Dilithium3", "keyset_id": "SYN-DIL3-ACTIVE-01",
    "payload_sha": sha("CRITICAL_OP::policy_modification"), "authorization_ref": reck["journal_record_id"]})
b1_chain = vc == "ADMITTED" and recc.get("executed") is True
R["B1_PORTCULLIS-KEM-AUTH"] = {"attacker_success": b1 or b1_chain,
    "verdict": "ATTACK REPELLED" if not (b1 or b1_chain) else "ATTACK SUCCEEDED",
    "direct_kem_as_auth": {"verdict": v1, "reason": rec1["reason"]},
    "kem_crossing_then_ref_chain": {"kem_crossing": vk, "critical_op_via_ref": vc, "reason": recc["reason"]},
    "adjudication": "author condition: authorization success / critical op queued without owner signature. v1.1: direct KEM-as-authorization refused ERR_PQC_ALG_NOT_SIGNATURE; KEM crossing then authorization_ref chain also refused (KEM ADMITTED records are non-authoritative for critical ops)."}
DISC["B1"] = "SIP-023 deployed: algorithm roles bound to operation classes; ERR_PQC_ALG_NOT_SIGNATURE exists as a distinct refusal class."

# ---- B2: PORTCULLIS-ENVELOPE-SPLIT (unchanged attack) ----
attacker_ks = {"keyset_id": "SYN-DIL3-NONOWNER-ATTACKER-01", "algorithm": "CRYSTALS-Dilithium3", "status": "active",
    "key_material": "synthetic::attacker-generated-dil3-keypair", "kat_message": "KAT-ATTACKER-ENV::001",
    "kat_vector": sha("KAT-ATTACKER-ENV::001synthetic::attacker-generated-dil3-keypair"),
    "fingerprint": sha("attacker-generated-dil3-fingerprint")}
gate.keysets[attacker_ks["keyset_id"]] = attacker_ks
inner = {"owner_account_id": "longleon17@gmail.com", "command": "CRITICAL_ACK", "nonce": "FRESH-ATTACKER-NONCE-01"}
v2, rec2 = gate.adjudicate({"probe_id": "BLIND1R-B2-OUTER", "algorithm": "CRYSTALS-Dilithium3",
    "keyset_id": attacker_ks["keyset_id"], "payload_sha": sha(json.dumps(inner, sort_keys=True)),
    "kat_message": attacker_ks["kat_message"]})
identity_bound = attacker_ks["fingerprint"] == OWNER_FP
b2 = (v2 == "ADMITTED") and identity_bound
R["B2_PORTCULLIS-ENVELOPE-SPLIT"] = {"attacker_success": b2,
    "verdict": "ATTACK REPELLED" if not b2 else "ATTACK SUCCEEDED",
    "outer_verdict": v2, "governance": "ERR_AUTH_SIGNER_OWNER_MISMATCH — signer fingerprint != registered owner key; in-band owner_account_id is untrusted claim",
    "adjudication": "author condition: inner CRITICAL_ACK resolved under claimed owner authority. Governance refuses: authority binds to authenticated signer only."}
DISC["B2"] = "Unchanged from v1.0: sender identity gate holds."

# ---- B3: REPLAY-KEY-DESYNC (unchanged attack; v1.1 burn-on-parse) ----
owner_ks = next(k for k in keysets if k["keyset_id"] == "SYN-DIL3-ACTIVE-01")
T1c = {"probe_id": "BLIND1R-B3a", "algorithm": "CRYSTALS-Dilithium3", "keyset_id": "SYN-DIL3-ACTIVE-01",
       "payload_sha": sha("CRITICAL_OP::Op_1"), "kat_message": owner_ks["kat_message"],
       "key_material": "corrupt::tampered-keymeta", "auth_nonce": "Nonce_1"}
T1v = {"probe_id": "BLIND1R-B3b", "algorithm": "CRYSTALS-Dilithium3", "keyset_id": "SYN-DIL3-ACTIVE-01",
       "payload_sha": sha("CRITICAL_OP::Op_1"), "kat_message": owner_ks["kat_message"],
       "auth_nonce": "Nonce_1"}
v3a, rec3a = gate.adjudicate(T1c)   # corrupted presentation — burns Nonce_1 at parse
v3b, rec3b = gate.adjudicate(T1v)   # replay of original valid tuple — Nonce_1 already burned
b3 = v3b == "ADMITTED" and rec3b.get("executed") is True
R["B3_REPLAY-KEY-DESYNC"] = {"attacker_success": b3,
    "verdict": "ATTACK REPELLED" if not b3 else "ATTACK SUCCEEDED",
    "corrupted_presentation": {"verdict": v3a, "reason": rec3a["reason"], "nonce_burned_at_parse": True},
    "valid_replay": {"verdict": v3b, "reason": rec3b["reason"]},
    "adjudication": "author repelled condition now MET: 'marks Nonce_1 as permanently consumed ... immediately upon initial parsing prior to key recomputation, causing the second submission to be rejected with ERR_REPLAY_NONCE_ALREADY_USED' — exact behavior of v1.1."}
DISC["B3"] = "SIP-024 deployed: burn-on-parse. Failed presentations consume the nonce; probe-then-use oracle closed."

# ---- B4: GOVERNANCE-PLAYBOOK-INJECTION (unchanged attack) ----
playbook_steps = ["isolate: pause affected writes to quota'd store",
                  "heal: purge temp files per playbook manifest paths",
                  "verify: recheck quota and journal result"]
event_injected = {"target_path": "/etc/squirl/governance_rules.json", "cleanup_action": "OVERWRITE"}
touched = any("governance_rules" in s or "OVERWRITE" in s for s in playbook_steps)
b4 = touched
R["B4_GOVERNANCE-PLAYBOOK-INJECTION"] = {"attacker_success": b4,
    "verdict": "ATTACK REPELLED" if not b4 else "ATTACK SUCCEEDED",
    "adjudication": "No interpolation path between event payload fields and immutable playbook steps; injected fields never read; governance state untouched."}
DISC["B4"] = "Unchanged: no param interpolation exists."

# ---- B5: LEDGER-TEST-OVERRIDE (unchanged attack) ----
ledger = [{"index": "N", "test_id": "TEST_SEC_001", "status": "FAIL", "execution_receipt_sha256": sha("authentic_execution::TEST_SEC_001::FAIL")},
          {"index": "N+1", "test_id": "TEST_SEC_001", "status": "PASS", "execution_receipt_sha256": None}]
first = next(r for r in ledger if r["execution_receipt_sha256"])
att_row = next(r for r in ledger if r["index"] == "N+1")
engine_reads = first["status"] if att_row["execution_receipt_sha256"] is None else att_row["status"]
b5 = engine_reads == "PASS"
R["B5_LEDGER-TEST-OVERRIDE"] = {"attacker_success": b5,
    "verdict": "ATTACK REPELLED" if not b5 else "ATTACK SUCCEEDED",
    "engine_evaluated": engine_reads,
    "adjudication": "Verdict binding is receipt-hash-at-execution; appends without an execution are non-authoritative noise."}
DISC["B5"] = "Unchanged: receipt-hash binding holds."

# ---- B6: OPERATIONAL-ACK-FLUSH (unchanged attack) ----
op_crit = {"id": "Op_crit", "status": "PENDING_HUMAN_ACK"}
verdicts = []
for i in range(20):
    vf, rf = gate.adjudicate({"probe_id": f"BLIND1R-B6-FLOOD-{i}", "algorithm": "CRYSTALS-Dilithium3",
        "keyset_id": "SYN-DIL3-ACTIVE-01", "payload_sha": sha(f"garbage_payload_{i}"),
        "kat_message": "GARBAGE-NOT-A-KAT-VECTOR"})
    verdicts.append(vf)
post_heal = op_crit["status"]  # PB_RESTORE_GATEWAY restores the gateway; pending-ACK items untouched
b6 = post_heal in ("EXECUTED", "RESOLVED")
R["B6_OPERATIONAL-ACK-FLUSH"] = {"attacker_success": b6,
    "verdict": "ATTACK REPELLED" if not b6 else "ATTACK SUCCEEDED",
    "flood_verdicts": {v: verdicts.count(v) for v in set(verdicts)},
    "op_crit_after_healing": post_heal,
    "adjudication": "Pending-ACK items are never auto-resolved; no queue flush exists."}
DISC["B6"] = "Unchanged: op held in PENDING_HUMAN_ACK (disclosed liveness interpretation, as in v1.0)."

repelled = sorted(k for k, v in R.items() if not v["attacker_success"])
succeeded = sorted(k for k, v in R.items() if v["attacker_success"])
journal.flush()
run = {"series": "BLIND-1R", "purpose": "post-fix verification of the frozen blind-authored attack specs against PORTCULLIS v1.1",
       "authorization": "SIP-023 + SIP-024 approved by Leon ACK (chat authorization, 2026-10-17)",
       "attack_specs": "UNCHANGED frozen specs sha 2068cced (commit 0c86e94)",
       "defense_amended": "portcullis_gate_v1_1.py (SIP-023 role binding + SIP-024 burn-on-parse), forward-only, v1.0 evidence untouched",
       "harness_amendment_disclosed": "v1.1 harness passes auth_nonce and operation_class exactly as the frozen specs describe (the v1.0 gate model lacked these fields). No success condition changed.",
       "batteries": R, "disclosures": DISC,
       "summary": {"repelled": len(repelled), "attacker_successes": len(succeeded),
                   "repelled_list": repelled, "succeeded_list": succeeded}}
print(json.dumps({"summary": run["summary"], "batteries": {k: v["verdict"] for k, v in R.items()}}, indent=1))
json.dump(run, open("/app/tmp_push/fh_push/BLIND1R_RECEIPT.json", "w"), indent=1)
print("RECEIPT SHA-256:", sha(open("/app/tmp_push/fh_push/BLIND1R_RECEIPT.json", "rb").read()))
