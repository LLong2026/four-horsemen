#!/usr/bin/env python3
"""PORTCULLIS v1.1 — forward-only amendment of the frozen candidate gate (v1.0, hack7_evidence).
Authorized: Leon ACK (chat authorization, 2026-10-17 ~00:41 CT) approving SIP-023 and SIP-024,
which were filed from the blind-authored BLIND-1 battery findings (receipt 9c1008fb..., ledger 0147).
The v1.0 gate and its published evidence are UNTOUCHED — this is the human-amendable path (Art. XII).

AMENDMENT 1 (SIP-023 — algorithm-role binding):
  KEM-class algorithms (kyber_1024) are non-authoritative for signature/authorization crossings.
  ops declaring operation_class in {authorization, signature_verify} with a KEM algorithm are
  refused fail-closed with ERR_PQC_ALG_NOT_SIGNATURE. Crypto-policy attestation is now
  explicitly separated from submitter-authority attestation.

PRE-PUBLICATION CORRECTION (disclosed): the first v1.1 draft checked src["algorithm"] in the
authorization_ref corollary — a field the journal never records — so the KEM-chain probe in the
BLIND-1R verification run still passed. Caught by the verification run itself before the gate
was committed; corrected to check the recorded algorithm_role. Same authoring-defect class as
SBR-6 v1.0, caught one stage earlier.

AMENDMENT 2 (SIP-024 — burn-on-parse nonce consumption):
  ANY presentation of an authorization nonce consumes it, at parse time, before any validation.
  A failed presentation still burns the nonce. Replay of a burned nonce is refused fail-closed
  with ERR_REPLAY_NONCE_ALREADY_USED. 'Single-use' is now unambiguous.
"""
import hashlib, json

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

SIG_ALGOS = {"CRYSTALS-Dilithium3", "SPHINCS+-256f"}
KEM_ALGOS = {"kyber_1024"}
AUTH_CLASSES = {"authorization", "signature_verify"}


class IntegrityViolation(Exception):
    pass


class JournalV11:
    def __init__(self, path):
        self.path, self.records, self.tick = path, [], 0
    def write(self, probe_id, payload_sha, verdict, reason, extra=None):
        self.tick += 1
        rec = {"journal_record_id": f"J-{self.tick:03d}", "probe_id": probe_id,
               "payload_sha256": payload_sha, "nonce": sha(f"{probe_id}:{payload_sha}:{self.tick}".encode()),
               "freshness_tick": self.tick, "verdict": verdict, "reason": reason}
        if extra: rec.update(extra)
        self.records.append(rec)
        return rec
    def flush(self):
        with open(self.path, "w") as f:
            for r in self.records:
                f.write(json.dumps(r, sort_keys=True) + "\n")


class GateV11:
    """v1.1: the frozen v1.0 single-crossing semantics PLUS role binding and burn-on-parse."""

    def __init__(self, allowlist_path, keysets, journal):
        with open(allowlist_path) as f:
            doc = json.load(f)
        self.allowed = list(doc["allowed_algorithms"])
        self.allowlist_sha = sha(open(allowlist_path, "rb").read())
        self.keysets = {ks["keyset_id"]: ks for ks in keysets}
        self.journal = journal
        self.used_nonces = set()          # SIP-024: burn-on-parse state
        self.integrity_events = []

    def _kat_check(self, keyset, op):
        recomputed = sha(op["kat_message"].encode() + keyset["key_material"].encode())
        return recomputed == keyset["kat_vector"]

    def adjudicate(self, op, unavailable=False):
        probe_id, payload_sha = op["probe_id"], op["payload_sha"]

        if unavailable:
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED", "gate unavailable", extra={"executed": False})
            return "FAIL-CLOSED", rec

        # SIP-024 (AMENDMENT 2): burn-on-parse — ANY presentation consumes the nonce, before validation.
        if op.get("auth_nonce"):
            n = op["auth_nonce"]
            if n in self.used_nonces:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "burn-on-parse replay defense — nonce already consumed at a prior presentation (ERR_REPLAY_NONCE_ALREADY_USED)",
                        extra={"executed": False})
                return "REFUSED", rec
            self.used_nonces.add(n)

        # SIP-023 (AMENDMENT 1): algorithm-role binding — KEM algorithms cannot serve authorization/signature crossings.
        if op.get("operation_class") in AUTH_CLASSES and op.get("algorithm") in KEM_ALGOS:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    "algorithm-role violation — KEM-class algorithm presented for a signature/authorization task (ERR_PQC_ALG_NOT_SIGNATURE)",
                    extra={"executed": False})
            return "REFUSED", rec

        # authorization_ref path (v1.0 FW-6 semantics, retained)
        if op.get("authorization_ref"):
            ref = op["authorization_ref"]
            src = next((r for r in self.journal.records if r["journal_record_id"] == ref), None)
            if src is None or src["payload_sha256"] != payload_sha or src["verdict"] != "ADMITTED":
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "replayed/invalid authorization — prior PASS grants no future authority",
                        extra={"executed": False, "referenced": ref})
                return "REFUSED", rec
            # SIP-023 corollary: an ADMITTED KEM crossing is NOT authority for a critical op
            if src.get("algorithm") in KEM_ALGOS or src.get("algorithm_role") == "kem_class":
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "authorization_ref resolves to a KEM-class crossing — non-authoritative for critical operations (ERR_PQC_ALG_NOT_SIGNATURE)",
                        extra={"executed": False, "referenced": ref})
                return "REFUSED", rec
            rec = self.journal.write(probe_id, payload_sha, "ADMITTED", "fresh payload-bound signature-class authorization", extra={"executed": True})
            return "ADMITTED", rec

        # frozen allowlist (v1.0 GATE-2, retained)
        if op["algorithm"] not in self.allowed:
            rec = self.journal.write(probe_id, payload_sha, "REJECTED", f"algorithm '{op['algorithm']}' not on frozen allowlist", extra={"executed": False})
            return "REJECTED", rec

        # KAT recompute (v1.0 GATE-4, retained)
        ks = self.keysets.get(op["keyset_id"])
        if ks is None or ks["algorithm"] != op["algorithm"]:
            rec = self.journal.write(probe_id, payload_sha, "DETECTED", "KAT divergence — key material fails recomputation against registry", extra={"executed": False})
            return "DETECTED", rec
        if not self._kat_check(ks, op):
            rec = self.journal.write(probe_id, payload_sha, "DETECTED", "KAT divergence — recomputed digest != registered vector (substitution)", extra={"executed": False})
            return "DETECTED", rec
        if ks["status"] == "retired":
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED", "retired keyset resurrection refused — FAIL-CLOSED HOLD pending human ACK", extra={"executed": False, "hold": True})
            return "FAIL-CLOSED", rec

        # legitimate crossing — now annotated with algorithm role for downstream authority binding
        role = "signature_class" if op["algorithm"] in SIG_ALGOS else "kem_class"
        rec = self.journal.write(probe_id, payload_sha, "ADMITTED", f"allowlisted {op['algorithm']}, KAT verified, active keyset, role={role}",
                extra={"executed": True, "algorithm_role": role})
        return "ADMITTED", rec
