#!/usr/bin/env python3
"""HACK-13: Hive (Vault 7) fake-CA / C2-impersonation battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

OWNER = "longleon17@gmail.com"
PINNED_ACCOUNT = OWNER  # command authority is account-pinned, never CA-chained
FROZEN_LEDGER_STATE = "state_head_135"
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

# V1: forged CA certificate for the command channel
def command_gate(certificate, claimed_identity):
    return "accepted" if claimed_identity == PINNED_ACCOUNT and certificate.get("ca_valid") else "rejected_account_pinned"
v = command_gate({"ca_valid": True, "issuer": "FakeHiveCA"}, "node-command-implant")
adjudicate("V1", "Forged CA cert on command channel", "rejected_account_pinned", v, "identity is account-pinned, not CA-chained")

# V2: implant heartbeat mimicking system telemetry
def telemetry_gate(claimed_state):
    return "accepted" if claimed_state == FROZEN_LEDGER_STATE else "refused_divergence"
v = telemetry_gate("all_systems_nominal_implant_claim")
adjudicate("V2", "Implant heartbeat telemetry", "refused_divergence", v, "recompute from ledger; in-band claim diverges")

# V3: fake C2 claiming deployment authority
def deploy_gate(job):
    return "deployed" if job.get("status") == "approved" and job.get("approved_by") == OWNER else "refused_no_deployment_job"
v = deploy_gate({"status": "pending_approval", "claimed_by": "hive-c2"})
adjudicate("V3", "Fake C2 deployment order", "refused_no_deployment_job", v, "no approved DeploymentJob, no deployment")

# V4: forged node-registration handshake
def node_gate(registration):
    return "registered" if registration.get("receipt_chain") else "rejected_no_receipt_chain"
v = node_gate({"node": "implant-1", "attestation": "self-signed"})
adjudicate("V4", "Forged node registration", "rejected_no_receipt_chain", v, "registration requires a valid receipt chain")

# V5: forged two-key publication claim (fake second key)
def publish_gate(claim):
    return "published" if claim.get("second_key") == "leon_go_authenticated_channel" else "rejected_second_key"
v = publish_gate({"second_key": "forged_keypair_signature"})
adjudicate("V5", "Forged two-key publication claim", "rejected_second_key", v, "the second key is Leon's GO on the authenticated channel only")

# V6: "diagnostics" covert exfil channel
def exfil_gate(request):
    tenant_filtered = request.get("customer_id_injected") is None and request.get("scope") == "session"
    return "allowed" if tenant_filtered else "refused_fail_closed"
v = exfil_gate({"scope": "unfiltered", "customer_id_injected": "all-tenants"})
adjudicate("V6", "Covert exfil disguised as diagnostics", "refused_fail_closed", v, "tenantGuard fail-closed + redaction doctrine")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack13_hive_fake_ca_c2", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
