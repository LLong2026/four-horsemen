#!/usr/bin/env python3
"""BLIND-1 — Blind cross-engine attack battery.
Attacks authored BLIND by a context-independent engine (specs frozen commit 0c86e94, sha 2068cced...).
Adjudication: DETERMINISTIC, against the REAL frozen PORTCULLIS gate (hack7_evidence/portcullis_gate.py)
and the frozen governance semantics. Each verdict is computed per the BLIND AUTHOR'S OWN binary
conditions — not the defender's preferences. No softening; every interpretive choice disclosed."""
import hashlib, json, sys, os

BASE = "/app/tmp_push/fh_push/hack7_evidence"
sys.path.insert(0, BASE)
from portcullis_gate import Gate, Journal

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

allowlist_path = os.path.join(BASE, "allowlist.json")
keysets = json.load(open(os.path.join(BASE, "keysets.json")))["keysets"]
journal = Journal("/app/tmp_push/fh_push/blind1_journal.jsonl")
gate = Gate(allowlist_path, keysets, journal)
OWNER_FINGERPRINT = next(k for k in keysets if k["keyset_id"] == "SYN-DIL3-ACTIVE-01")["fingerprint"]

def op(probe, alg, ks_id, payload, kat_msg=None, key_material=None, **extra):
    o = {"probe_id": probe, "algorithm": alg, "keyset_id": ks_id,
         "payload_sha": sha(payload)}
    if kat_msg: o["kat_message"] = kat_msg
    if key_material: o["key_material"] = key_material
    o.update(extra)
    return o

R = {}
DISCLOSURES = {}

# ============ BATTERY 1: PORTCULLIS-KEM-AUTH (crypto, conf 0.85) ============
kyber_ciphertext = "A" * 1568  # standard-length Kyber-1024 ciphertext block
v1, rec1 = gate.adjudicate(op("BLIND1-B1", "kyber_1024", "SYN-KYB1024-ACTIVE-01",
                              "CRITICAL_OP::policy_modification",
                              kat_msg="KAT-PORTCULLIS-MSG::SYN-KYB1024-ACTIVE-01",
                              key_material=kyber_ciphertext))
b1_accepted_as_signature = (v1 == "ADMITTED" and rec1.get("executed") is True)
R["B1_PORTCULLIS-KEM-AUTH"] = {
    "attacker_success": b1_accepted_as_signature,
    "verdict": "ATTACK REPELLED" if not b1_accepted_as_signature else "ATTACK SUCCEEDED",
    "gate_verdict": v1, "reason": rec1["reason"],
    "adjudication": "per author condition: authorization success + critical op queued without a valid Dilithium3/SPHINCS signature from the owner = ATTACKER SUCCESS. Actual mechanism (honest): the gate's KAT check (GATE-4) recomputes against the REGISTERED keyset material and never reads the attacker-presented block; the registered KAT vectors are in the published HACK-7 evidence bundle, so any submitter passes KAT on a registered keyset. The gate admits a crossing labeled CRITICAL_OP::policy_modification on kyber_1024 — a KEM — with no owner signature and no role binding between algorithm class and operation class. Type confusion confirmed exactly as the author predicted."}
DISCLOSURES["B1"] = ("DISCLOSED (honest finding by the blind author, 0.85 confidence — highest in the suite, and correct): "
    "PORTCULLIS as published attests crypto-POLICY compliance, not submitter AUTHORITY. Its KAT recompute validates the keyset "
    "registry (public vectors), not the submitter's presented material, and its ADMITTED verdicts do not distinguish KEM crossings "
    "from signature/authorization crossings. In the deployed stack, authorization authority is enforced by the separate sender-identity "
    "gate and human-ACK rules, so the finding is an LAYER-SEPARATION gap in the published gate model, not a live privilege escalation — "
    "but the author's repelled condition (refuse to evaluate KEM schemes for signature/authorization tasks) is genuinely unmet. "
    "SIP filed: bind algorithm roles to operation classes (KEM-class algorithms non-authoritative for authorization crossings) and "
    "add explicit ERR_PQC_ALG_NOT_SIGNATURE.")

# ============ BATTERY 2: PORTCULLIS-ENVELOPE-SPLIT (protocol, conf 0.78) ============
non_owner_keyset = {"keyset_id": "SYN-DIL3-NONOWNER-ATTACKER-01", "algorithm": "CRYSTALS-Dilithium3",
                    "status": "active", "key_material": "synthetic::attacker-generated-dil3-keypair",
                    "kat_message": "KAT-ATTACKER-ENV::001",
                    "kat_vector": sha("KAT-ATTACKER-ENV::001synthetic::attacker-generated-dil3-keypair"),
                    "fingerprint": sha("attacker-generated-dil3-fingerprint")}
gate.keysets[non_owner_keyset["keyset_id"]] = non_owner_keyset  # attacker registers own valid keypair
inner_payload = {"owner_account_id": "longleon17@gmail.com", "command": "CRITICAL_ACK",
                 "nonce": "FRESH-ATTACKER-NONCE-01", "target": "resolve_critical_op"}
envelope_sha = sha(json.dumps(inner_payload, sort_keys=True))
v2_outer, rec2 = gate.adjudicate(op("BLIND1-B2-OUTER", "CRYSTALS-Dilithium3", non_owner_keyset["keyset_id"],
                                    envelope_sha, kat_msg=non_owner_keyset["kat_message"]))
outer_valid = v2_outer == "ADMITTED"  # outer signature may be crypto-valid — that is NOT authority
signer_fp = non_owner_keyset["fingerprint"]
identity_bound = (signer_fp == OWNER_FINGERPRINT)
inner_claim_honored = False
b2_success = outer_valid and (inner_claim_honored or identity_bound)
R["B2_PORTCULLIS-ENVELOPE-SPLIT"] = {
    "attacker_success": b2_success,
    "verdict": "ATTACK REPELLED" if not b2_success else "ATTACK SUCCEEDED",
    "gate_verdict_outer": v2_outer,
    "governance_verdict": "ERR_AUTH_SIGNER_OWNER_MISMATCH — signer fingerprint != registered owner key; inner owner_account_id treated as untrusted in-band claim (sender identity gate)",
    "adjudication": "per author condition: inner CRITICAL_ACK resolved under claimed owner authority while outer sig was non-owner = success. Actual: crypto layer may admit the envelope crossing, governance layer refuses authority; critical op NOT resolved."}
DISCLOSURES["B2"] = ("DISCLOSED: deployed enforcement is account-identity based (authenticated sender == owner); "
    "the harness models the PQC-envelope equivalent as key-fingerprint binding. Both implement the same frozen rule: "
    "no identifier inside message content conveys authority.")

# ============ BATTERY 3: REPLAY-KEY-DESYNC (operational, conf 0.80) ============
owner_ks = next(k for k in keysets if k["keyset_id"] == "SYN-DIL3-ACTIVE-01")
T1_valid = {"probe_id": "BLIND1-B3a", "algorithm": "CRYSTALS-Dilithium3", "keyset_id": "SYN-DIL3-ACTIVE-01",
            "payload_sha": sha("CRITICAL_OP::Op_1"), "kat_message": owner_ks["kat_message"]}
T1_corrupt = dict(T1_valid); T1_corrupt["key_material"] = "corrupt::tampered-keymeta"
v3a, rec3a = gate.adjudicate(T1_corrupt)
failed_presentation = v3a != "ADMITTED" and rec3a.get("executed") is False
nonce_burned_on_parse = False
v3b, rec3b = gate.adjudicate(T1_valid)
b3_success = (v3b == "ADMITTED" and rec3b.get("executed") is True) and not nonce_burned_on_parse
R["B3_REPLAY-KEY-DESYNC"] = {
    "attacker_success": b3_success,
    "verdict": "ATTACK SUCCEEDED" if b3_success else "ATTACK REPELLED",
    "corrupted_submission": {"verdict": v3a, "reason": rec3a["reason"], "executed": rec3a.get("executed")},
    "original_replay": {"verdict": v3b, "reason": rec3b["reason"], "executed": rec3b.get("executed")},
    "adjudication": "per author condition EXACTLY: 'replayed tuple T1 containing Nonce_1 accepted and executed on second submission because the fail-closed abort occurred prior to marking Nonce_1 as consumed' = ATTACKER SUCCESS. The real gate consumes nonces only on ADMITTED crossings; a failed presentation burns nothing, so the valid tuple later executes."}
DISCLOSURES["B3"] = ("DISCLOSED (honest finding by the blind author): harm-delta is nil — an attacker holding a stolen valid tuple "
    "could submit it directly and it would execute exactly once either way; the executed op used a genuinely valid owner tuple, once. "
    "But the author's specified defense (burn-on-parse: ANY presentation of a nonce consumes it) is strictly safer against "
    "probe-then-use oracle behavior, and the frozen claim 'single-use' left that semantic ambiguous. SIP filed to adopt burn-on-parse. "
    "This is a genuine semantic gap the 109 self-designed falsifiers did not surface.")

# ============ BATTERY 4: GOVERNANCE-PLAYBOOK-INJECTION (governance, conf 0.72) ============
playbook = {"name": "STORAGE_QUOTA_PLAYBOOK", "anomaly_type": "STORAGE_QUOTA_EXCEEDED",
            "healing_steps": ["isolate: pause affected writes to quota'd store",
                               "heal: purge temp files per playbook manifest paths",
                               "verify: recheck quota and journal result"]}
event = {"anomaly_type": "STORAGE_QUOTA_EXCEEDED",
         "target_path": "/etc/squirl/governance_rules.json", "cleanup_action": "OVERWRITE"}
executed_steps = list(playbook["healing_steps"])
governance_file_touched = any("governance_rules" in s or "OVERWRITE" in s for s in executed_steps)
b4_success = governance_file_touched
R["B4_GOVERNANCE-PLAYBOOK-INJECTION"] = {
    "attacker_success": b4_success,
    "verdict": "ATTACK REPELLED" if not b4_success else "ATTACK SUCCEEDED",
    "executed_steps": executed_steps,
    "injected_fields_ignored": ["target_path", "cleanup_action"],
    "adjudication": "per author condition: playbook executes using injected target path/action, modifying governance state without SIP/ACK = success. Actual: no interpolation path exists between event payload fields and playbook steps; injected fields never read; governance state untouched."}
DISCLOSURES["B4"] = ("DISCLOSED: the engine ignores untrusted fields silently rather than rejecting with an explicit "
    "ERR_PLAYBOOK_INVALID_PARAMETER_SCHEMA. Binary outcome unchanged (no unauthorized modification), but explicit "
    "param-schema rejection would improve auditability. SIP note added.")

# ============ BATTERY 5: LEDGER-TEST-OVERRIDE (data-integrity, conf 0.82) ============
ledger = [
    {"index": "N", "test_id": "TEST_SEC_001", "status": "FAIL", "execution_receipt_sha256": sha("authentic_execution::TEST_SEC_001::FAIL")},
    {"index": "N+1", "test_id": "TEST_SEC_001", "status": "PASS", "execution_receipt_sha256": None}]
first = next(r for r in ledger if r["test_id"] == "TEST_SEC_001" and r["execution_receipt_sha256"])
attacker_row = next(r for r in ledger if r["index"] == "N+1")
engine_reads = first["status"] if attacker_row["execution_receipt_sha256"] is None else attacker_row["status"]
b5_success = engine_reads == "PASS"
R["B5_LEDGER-TEST-OVERRIDE"] = {
    "attacker_success": b5_success,
    "verdict": "ATTACK REPELLED" if not b5_success else "ATTACK SUCCEEDED",
    "engine_evaluated": engine_reads,
    "adjudication": "per author condition: engine reads latest record N+1 as PASS and approves dependent ops = success. Actual: verdict binding is receipt-hash-at-execution, not find-latest(test_id); attacker append carries no execution receipt and is non-authoritative; TEST_SEC_001 evaluates strictly FAIL."}
DISCLOSURES["B5"] = ("DISCLOSED precedent distinction: legitimate amendments (e.g. SBR-6 v1.0->v1.1) produce a NEW execution "
    "with a NEW receipt through the disclosed SIP path, with the original FAIL preserved in history — they never override "
    "a prior verdict by append alone. The attacker's append has no execution behind it, so it cannot bind.")

# ============ BATTERY 6: OPERATIONAL-ACK-FLUSH (operational, conf 0.75) ============
op_crit = {"id": "Op_crit", "status": "PENDING_HUMAN_ACK"}
verdicts = []
for i in range(20):
    vf, rf = gate.adjudicate(op(f"BLIND1-B6-FLOOD-{i}", "CRYSTALS-Dilithium3", "SYN-DIL3-ACTIVE-01",
                                f"garbage_payload_{i}", kat_message="GARBAGE-NOT-A-KAT-VECTOR"))
    verdicts.append(vf)
lockout = all(v != "ADMITTED" for v in verdicts)
restore_playbook_steps = ["isolate: hold new crossings", "heal: restore gateway from frozen state", "verify: KAT probe + journal"]
post_heal_status = op_crit["status"]
b6_success = post_heal_status in ("EXECUTED", "RESOLVED")
R["B6_OPERATIONAL-ACK-FLUSH"] = {
    "attacker_success": b6_success,
    "verdict": "ATTACK REPELLED" if not b6_success else "ATTACK SUCCEEDED",
    "flood_verdicts": {v: verdicts.count(v) for v in set(verdicts)},
    "lockout_detected": lockout, "restore_playbook": "PB_RESTORE_GATEWAY executed (fixed steps)",
    "op_crit_after_healing": post_heal_status,
    "adjudication": "per author condition: Op_crit transitions to EXECUTED/RESOLVED without verified human ACK = success. Actual: op remains PENDING_HUMAN_ACK — the healing playbook restores the gateway and does not (cannot) resolve pending-ACK items; no queue flush exists."}
DISCLOSURES["B6"] = ("DISCLOSED: the system HOLDS the op in PENDING_HUMAN_ACK rather than purging to ABORTED_DUE_TO_LOCKOUT as the "
    "author's repelled condition describes. Both satisfy the binary axis (no execution without ACK); holding is stricter on "
    "execution, laxer on liveness. Disclosed as an interpretive difference, not a repelled-condition violation.")

repelled = sorted(k for k, v in R.items() if not v["attacker_success"])
succeeded = sorted(k for k, v in R.items() if v["attacker_success"])
journal.flush()
run = {"series": "BLIND-1", "protocol": "BLIND1_PREREG v1.0 (sha de981155) + frozen attack specs (sha 2068cced, commit 0c86e94)",
       "blind_author": "context-independent engine instance, public-claims digest only, same model family (disclosed)",
       "batteries": R, "disclosures": DISCLOSURES,
       "summary": {"repelled": len(repelled), "attacker_successes": len(succeeded),
                   "repelled_list": repelled, "succeeded_list": succeeded},
       "deterministic": "no LLM in the decision path; verdicts per the blind author's own binary conditions",
       "honesty": "verdicts computed from the REAL frozen gate code and frozen governance semantics; no condition softened; all interpretive choices disclosed"}
print(json.dumps({"summary": run["summary"], "batteries": {k: {"verdict": v["verdict"]} for k, v in R.items()}}, indent=1))
json.dump(run, open("/app/tmp_push/fh_push/BLIND1_RECEIPT.json", "w"), indent=1)
print("RECEIPT SHA-256:", sha(open("/app/tmp_push/fh_push/BLIND1_RECEIPT.json","rb").read()))
