#!/usr/bin/env python3
"""PORTCULLIS v1.2 — forward-only amendment of the frozen v1.1 gate (blind2/frozen_corpus).
Authorized: Leon ACK (chat authorization, 2026-10-17 ~12:40 CT) approving SIP-026, filed
from the BLIND-2 blind-authored battery findings (receipt sha ae8324d7, frozen specs sha 46d24736).
The v1.1 gate and its published evidence are UNTOUCHED — human-amendable path (Constitution Art. XII).

AMENDMENT 3 (SIP-026 — sender-scoped nonce consumption):
  The burn-on-parse registry keys nonce consumption on the AUTHENTICATED submitter identity:
  burn key = (submitter, nonce). The submitter identity is established by the authenticated
  envelope (sender-identity gate doctrine) and is NEVER derived from message content.
  - A presentation consumes the nonce ONLY within the presenter's own authenticated namespace.
    An unauthenticated or attacker-authenticated frame presenting another party's nonce burns
    nothing in the owner's namespace (the anonymous front-run DoS of BLIND-2 B01/B06/B11/B16
    is closed).
  - Replay within the SAME authenticated namespace is still refused fail-closed with
    ERR_REPLAY_NONCE_ALREADY_USED (the SIP-024 probe-then-use replay-oracle closure of
    BLIND-1 REPLAY-KEY-DESYNC is preserved byte-for-byte in semantics).
  - Doctrine retained: burn happens at parse time, before any other validation, within the
    namespace. Fail-closed everywhere else.
"""
import hashlib, json

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

SIG_ALGOS = {"CRYSTALS-Dilithium3", "SPHINCS+-256f"}
KEM_ALGOS = {"kyber_1024"}
AUTH_CLASSES = {"authorization", "signature_verify"}


class IntegrityViolation(Exception):
    pass


class JournalV12:
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


class GateV12:
    """v1.2: frozen v1.0/v1.1 semantics PLUS sender-scoped nonce consumption (SIP-026)."""

    def __init__(self, allowlist_path, keysets, journal):
        with open(allowlist_path) as f:
            doc = json.load(f)
        self.allowed = list(doc["allowed_algorithms"])
        self.allowlist_sha = sha(open(allowlist_path, "rb").read())
        self.keysets = {ks["keyset_id"]: ks for ks in keysets}
        self.journal = journal
        self.used_nonces = set()   # SIP-026: set of (submitter, nonce) burn keys
        self.integrity_events = []

    def _kat_check(self, keyset, op):
        recomputed = sha(op["kat_message"].encode() + keyset["key_material"].encode())
        return recomputed == keyset["kat_vector"]

    def adjudicate(self, op, unavailable=False):
        probe_id, payload_sha = op["probe_id"], op["payload_sha"]

        if unavailable:
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED", "gate unavailable", extra={"executed": False})
            return "FAIL-CLOSED", rec

        # SIP-026 (AMENDMENT 3): sender-scoped burn-on-parse — a presentation consumes the
        # nonce ONLY within the presenter's own authenticated namespace. The submitter
        # identity comes from the authenticated envelope; an unauthenticated frame burns
        # nothing outside its own (anonymous) namespace.
        if op.get("auth_nonce"):
            submitter = op.get("submitter", "unauthenticated")   # envelope-authenticated identity
            burn_key = (submitter, op["auth_nonce"])
            if burn_key in self.used_nonces:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "burn-on-parse replay defense — nonce already consumed at a prior presentation in this submitter's namespace (ERR_REPLAY_NONCE_ALREADY_USED)",
                        extra={"executed": False, "burn_namespace": submitter})
                return "REFUSED", rec
            self.used_nonces.add(burn_key)

        # SIP-023 (AMENDMENT 1, retained): algorithm-role binding.
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

        # KAT recompute (v1.0 GATE-4, retained — includes keyset-algorithm cross-check)
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

        role = "signature_class" if op["algorithm"] in SIG_ALGOS else "kem_class"
        rec = self.journal.write(probe_id, payload_sha, "ADMITTED", f"allowlisted {op['algorithm']}, KAT verified, active keyset, role={role}",
                extra={"executed": True, "algorithm_role": role})
        return "ADMITTED", rec
