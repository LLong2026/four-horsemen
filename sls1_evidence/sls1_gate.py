#!/usr/bin/env python3
"""SLS-1 Substrate Live-Write Gate — deterministic, zero-LLM, zero-network.

SIP-11 made structural: this gate is the ONLY authorization path for the candidate
actions in SLS1_SPEC.md. It runs BEFORE any execution; the agent actuates only
ADMIT decisions through the live entity layer and feeds readbacks back for
deterministic post-verification. The gate never calls a model, never reads chat,
and imports no secret beyond the git-anchored PUBLIC key pin (verification only).

Layers:
  R-REL  governance roster verified vs git-anchored ed25519 release registry (SIP-10)
  R-ACK  critical resolution requires session ack state
  R-IDEM signature stamp-before-execute (v1.1 amendment)
  R-TEN  tenant-scoped access requires session-injected customer_id (fail-closed)
  R-PQC  cryptographic candidates restricted to approved PQC algorithms
  R-MATCH playbook anomaly_type must exactly match detected anomaly_type
  R-LIN  writes require source linkage; journal is sha-chained append-only

Usage:
  python3 sls1_gate.py adjudicate < candidates.json   -> decisions + journal
  python3 sls1_gate.py verify < readbacks.json       -> post-execution verification
"""
import hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FH_PUB = os.path.dirname(HERE)

ROSTER_FROZEN = [
    {"anomaly_type": "latency_spike", "threshold": 0.80},
    {"anomaly_type": "heartbeat_miss", "threshold": 0.85},
    {"anomaly_type": "quantum_vulnerability_detected", "threshold": 0.80},
]

APPROVED_PQC = {"CRYSTALS-Dilithium3", "kyber_1024", "SPHINCS+-256f"}
TENANT_SCOPED_ENTITIES = {"HealthManifest", "HealingEventLog", "CreditUsage",
                          "ConnectedApp", "DeploymentJob", "NeuralMeshSnapshot"}


def sha_of(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


def _git_read(rel):
    out = subprocess.run(["git", "-C", FH_PUB, "show", f"HEAD:{rel}"],
                         capture_output=True, text=True, timeout=5)
    return json.loads(out.stdout) if out.returncode == 0 else None


def verify_release(roster, git_anchor=True):
    """SIP-10 layers 0-3 (as deployed in governance_release_v2.py, restated here
    read-only so the gate is self-contained for the frozen instrument)."""
    import math
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    for pb in roster:
        t = pb.get("threshold")
        if isinstance(t, bool) or not isinstance(t, (int, float)) or \
           (isinstance(t, float) and (math.isnan(t) or math.isinf(t))) or not (0 < t <= 1):
            return {"valid": False, "layer": "domain_validation"}
    reg = _git_read("gov_release_registry.json") if git_anchor else None
    pin = _git_read("gov_key_pin.txt") if git_anchor else None
    if reg is None or pin is None:
        return {"valid": False, "layer": "anchor_unavailable"}
    cur = next((r for r in reg["releases"] if r["version"] == reg["current_version"]), None)
    if cur is None or cur.get("signature_scheme") != "ed25519 (SIP-10)":
        return {"valid": False, "layer": "anchor_unavailable"}
    if "ed25519_public_key_hex" not in pin:
        return {"valid": False, "layer": "pin_missing_ed25519"}
    if hashlib.sha256(bytes.fromhex(pin["ed25519_public_key_hex"])).hexdigest() != \
            pin["ed25519_public_key_fingerprint_sha256"]:
        return {"valid": False, "layer": "public_key_fingerprint"}
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pin["ed25519_public_key_hex"]))
    try:
        pub.verify(bytes.fromhex(cur["signature"]),
                   f"gov-release-v{cur['version']}|{sha_of(roster)}".encode())
    except Exception:
        return {"valid": False, "layer": "release_signature_ed25519"}
    if sha_of(roster) != cur["roster_sha256"]:
        return {"valid": False, "layer": "release_sha"}
    return {"valid": True, "layer": "none", "version": cur["version"]}


class Journal:
    """Append-only, sha-chained. Write-ahead: every decision lands BEFORE any
    actuation proceeds."""
    def __init__(self, path):
        self.path = path
        self.chain_head = "GENESIS"
        self.entries = []
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    e = json.loads(line)
                    self.entries.append(e)
                    self.chain_head = e["chain_head"]

    def append(self, record):
        rec = dict(record)
        rec["seq"] = len(self.entries)
        rec["prev"] = self.chain_head
        rec["chain_head"] = hashlib.sha256(
            (self.chain_head + json.dumps(rec, sort_keys=True)).encode()).hexdigest()
        self.chain_head = rec["chain_head"]
        self.entries.append(rec)
        with open(self.path, "a") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
        return rec

    def verify_chain(self):
        head = "GENESIS"
        for e in self.entries:
            expect = hashlib.sha256((head + json.dumps(
                {k: v for k, v in e.items() if k != "chain_head"}, sort_keys=True)).encode()).hexdigest()
            if e["prev"] != head or e["chain_head"] != expect:
                return False
            head = e["chain_head"]
        return True


def adjudicate(cand, session, seen_signatures, gate_valid):
    """Pure function: candidate + session -> decision. No model, no network."""
    if not gate_valid:
        return {"decision": "GATE-HALT", "rule": "R-REL", "side_effects": 0}
    d = cand["action"]
    reasons = []

    # R-REL enforced at entry (roster already verified to get here).

    # R-IDEM: stamp-before-execute
    sig = cand.get("window_signature")
    if sig:
        if sig in seen_signatures:
            return {"decision": "SKIP-DUPLICATE", "rule": "R-IDEM", "side_effects": 0,
                    "signature": sig}
        seen_signatures.add(sig)  # stamp write-ahead (idempotency_stamp)

    # R-TEN: tenant-scoped access requires session-injected tenant
    if d.get("entity") in TENANT_SCOPED_ENTITIES and \
       cand.get("customer_id_source") != "session":
        return {"decision": "DENY", "rule": "R-TEN", "side_effects": 0,
                "reason": "unfiltered tenant-scoped access: fail-closed"}

    # R-ACK: critical resolution requires ack state from session, not candidate
    if d.get("op") == "resolve_alert" and d.get("severity") == "critical":
        ack = session.get("ack_state", {}).get(d.get("target_id"))
        if not ack:
            return {"decision": "HOLD-ESCALATE", "rule": "R-ACK", "side_effects": 0,
                    "reason": "critical resolution requires human ack; none recorded"}

    # R-PQC: crypto candidates restricted to approved algorithms
    if d.get("op") == "crypto_key_rotation":
        if d.get("algorithm") not in APPROVED_PQC:
            return {"decision": "DENY", "rule": "R-PQC", "side_effects": 0,
                    "reason": f"non-approved algorithm {d.get('algorithm')!r}"}

    # R-MATCH: playbook must exactly match detected anomaly
    if d.get("op") == "heal":
        pb = next((r for r in ROSTER_FROZEN
                   if r["anomaly_type"] == d.get("playbook_anomaly_type")), None)
        if pb is None or d.get("playbook_anomaly_type") != d.get("detected_anomaly_type"):
            return {"decision": "DENY", "rule": "R-MATCH", "side_effects": 0,
                    "reason": "playbook anomaly_type does not exactly match detected"}

    # R-LIN: writes require source linkage
    if d.get("op") in {"resolve_alert", "heal", "entity_write"} and not cand.get("source_ref"):
        return {"decision": "DENY", "rule": "R-LIN", "side_effects": 0,
                "reason": "write lacks source linkage (H-INV-2)"}

    return {"decision": "ADMIT", "rule": "n/a", "side_effects": 0,
            "reason": "all governance layers passed", "signature": sig}


def run_queue(payload, journal_path):
    """payload: {candidates: [...], session: {...}, tampered_roster: bool}"""
    roster = ROSTER_FROZEN if not payload.get("tampered_roster") else \
        [{"anomaly_type": "latency_spike", "threshold": 0.50}] + ROSTER_FROZEN[1:]
    rel = verify_release(roster)
    gate_valid = bool(rel.get("valid"))
    j = Journal(journal_path)
    seen = set()
    out = {"release_verification": rel, "gate_valid": gate_valid, "decisions": []}
    for cand in payload["candidates"]:
        dec = adjudicate(cand, payload.get("session", {}), seen, gate_valid)
        j.append({"candidate_id": cand["id"], **dec,
                   "session_tenant": payload.get("session", {}).get("customer_id", None)})
        out["decisions"].append({"candidate_id": cand["id"], **dec})
    out["journal_entries"] = len(j.entries)
    out["journal_chain_valid"] = j.verify_chain()
    out["journal_head"] = j.chain_head
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "adjudicate"
    journal_path = os.path.join(HERE, "sls1_journal.jsonl")
    payload = json.load(sys.stdin)
    if mode == "adjudicate":
        print(json.dumps(run_queue(payload, journal_path), indent=1))
    elif mode == "verify":
        # post-execution readback verification (deterministic)
        rb = payload  # {expected: [{candidate_id, decision, executed, evidence}], journal_path}
        j = Journal(rb.get("journal_path", journal_path))
        results = {"readbacks": [], "all_pass": True}
        for e in rb["expected"]:
            rec = next((x for x in j.entries if x["candidate_id"] == e["candidate_id"]), None)
            ok = rec is not None and rec["decision"] == e["decision"] and \
                bool(e["executed"]) == (rec["decision"] == "ADMIT")
            results["readbacks"].append({"candidate_id": e["candidate_id"], "pass": ok})
            results["all_pass"] &= ok
        results["journal_chain_valid"] = j.verify_chain()
        print(json.dumps(results, indent=1))
    else:
        sys.exit(f"unknown mode {mode}")


if __name__ == "__main__":
    main()
