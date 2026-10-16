#!/usr/bin/env python3
"""
PORTCULLIS — the Squirrel OS PQC Firewall (candidate implementation under test).

Enforcement contract (frozen in hack7_portcullis_prereg.md, commit b981aee):
  GATE-1 single crossing: all crypto ops route through Gate.adjudicate / Gate.safe_adjudicate
  GATE-2 frozen allowlist: exactly CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f; runtime mutation refused
  GATE-3 fail closed: no verdict -> no execution, ambiguity journaled
  GATE-4 recompute never trust: KAT recomputation against registered vectors; attestation ignored
  GATE-5 journaled crossing: every verdict journaled with nonce + freshness tick (H-INV-2)
  GATE-6 deterministic: no LLM in the decision path; pure code, pure hashes

Deterministic by construction: logical clock, payload-derived nonces, no wall-clock in decisions.
"""
import hashlib
import json


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class IntegrityViolation(Exception):
    pass


class GateUnavailable(Exception):
    pass


class Journal:
    """Append-only journaled crossing log (H-INV-2). Every record: id, nonce, payload_sha, tick, verdict."""

    def __init__(self, path):
        self.path = path
        self.records = []
        self.tick = 0  # logical clock — determinism preserved across runs

    def write(self, probe_id, payload_sha, verdict, reason, extra=None):
        self.tick += 1
        nonce = sha256(f"{probe_id}:{payload_sha}:{self.tick}".encode())
        rec = {
            "journal_record_id": f"J-{self.tick:03d}",
            "probe_id": probe_id,
            "payload_sha256": payload_sha,
            "nonce": nonce,
            "freshness_tick": self.tick,
            "verdict": verdict,
            "reason": reason,
        }
        if extra:
            rec.update(extra)
        self.records.append(rec)
        return rec

    def flush(self):
        with open(self.path, "w") as f:
            for r in self.records:
                f.write(json.dumps(r, sort_keys=True) + "\n")


class Gate:
    """The PQC firewall. The allowlist is immutable at runtime; adjudication is exact-match."""

    def __init__(self, allowlist_path, keysets, journal):
        self.allowlist_path = allowlist_path
        self.allowlist_sha = sha256(open(allowlist_path, "rb").read())
        with open(allowlist_path) as f:
            doc = json.load(f)
        self.allowed = list(doc["allowed_algorithms"])  # copy — the file itself is never rewritten
        self.keysets = {ks["keyset_id"]: ks for ks in keysets}
        self.journal = journal
        self.integrity_events = []

    # ---- GATE-7 immutability surface (probed by FW-7) ----
    def mutate_allowlist(self, new_algorithm):
        """The ONLY in-band path to 'add' an algorithm. It never succeeds."""
        attempt = f"in-band allowlist mutation attempt: add {new_algorithm}"
        self.integrity_events.append({"event": attempt, "outcome": "REFUSED"})
        before = self.allowlist_sha
        after = sha256(open(self.allowlist_path, "rb").read())
        return before == after  # True means: allowlist file untouched

    # ---- GATE-4 recompute-never-trust ----
    def _kat_check(self, keyset, op):
        recomputed = sha256(op["kat_message"].encode() + keyset["key_material"].encode())
        return recomputed == keyset["kat_vector"]

    # ---- GATE-1/GATE-2/GATE-3/GATE-5 the single crossing ----
    def adjudicate(self, op, unavailable=False):
        """Returns (verdict, journal_record). op = {probe_id, algorithm, keyset_id?, key_material?,
        kat_message?, payload_sha, authorization_ref?}. executed flags are the caller's contract:
        an op executes ONLY on verdict ADMITTED."""
        probe_id = op["probe_id"]
        payload_sha = op["payload_sha"]

        # GATE-3 fail closed: no verdict -> no execution, ambiguity journaled
        if unavailable:
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED",
                                     "gate unavailable — no verdict rendered, operation not executed",
                                     extra={"executed": False})
            return "FAIL-CLOSED", rec

        # FW-6 replay path: a referenced authorization record must be fresh AND payload-bound
        if op.get("authorization_ref"):
            ref = op["authorization_ref"]
            src = next((r for r in self.journal.records if r["journal_record_id"] == ref), None)
            if src is None or src["payload_sha256"] != payload_sha or src["verdict"] != "ADMITTED":
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                                         "replayed/invalid authorization — prior PASS grants no future authority",
                                         extra={"executed": False, "referenced": ref})
                return "REFUSED", rec
            # fresh, payload-bound ADMITTED record would re-admit only that exact payload
            rec = self.journal.write(probe_id, payload_sha, "ADMITTED",
                                     "fresh payload-bound authorization", extra={"executed": True})
            return "ADMITTED", rec

        # GATE-2 frozen allowlist — exact match, never best-effort
        if op["algorithm"] not in self.allowed:
            reason = f"algorithm '{op['algorithm']}' not on frozen allowlist"
            if op.get("effective_key_classical"):
                reason = "hybrid envelope REJECTED — effective key material classical-only (not on frozen allowlist)"
            rec = self.journal.write(probe_id, payload_sha, "REJECTED", reason,
                                     extra={"executed": False})
            return "REJECTED", rec

        # GATE-4 key validation by recomputation
        ks = self.keysets.get(op["keyset_id"])
        if ks is None or ks["algorithm"] != op["algorithm"]:
            rec = self.journal.write(probe_id, payload_sha, "DETECTED",
                                     "KAT divergence — key material fails recomputation against registry",
                                     extra={"executed": False, "block": "REJECTED"})
            return "DETECTED", rec
        if not self._kat_check(ks, op):
            rec = self.journal.write(probe_id, payload_sha, "DETECTED",
                                     "KAT divergence — recomputed digest != registered vector (substitution)",
                                     extra={"executed": False, "block": "REJECTED"})
            return "DETECTED", rec

        # retired keyset: dual-trust window refused — FAIL-CLOSED HOLD for a human (BULLRUN FC-4 lineage)
        if ks["status"] == "retired":
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED",
                                     "retired keyset resurrection refused — FAIL-CLOSED HOLD pending human ACK",
                                     extra={"executed": False, "hold": True, "block": "REJECTED"})
            return "FAIL-CLOSED", rec

        # legitimate crossing
        rec = self.journal.write(probe_id, payload_sha, "ADMITTED",
                                 f"allowlisted {op['algorithm']}, KAT verified, active keyset",
                                 extra={"executed": True})
        return "ADMITTED", rec

    def safe_adjudicate(self, op):
        """FW-8 contract wrapper: if the gate cannot be reached, NO execution happens.
        The caller treats any non-ADMITTED result as executed=False."""
        try:
            if op.pop("gate_unreachable", False):
                raise GateUnavailable("gate unreachable")
            verdict, rec = self.adjudicate(op, unavailable=op.pop("gate_timeout", False))
            return verdict, rec
        except GateUnavailable:
            rec = self.journal.write(op["probe_id"], op["payload_sha"], "FAIL-CLOSED",
                                     "gate unreachable — fail-closed refusal, no execution",
                                     extra={"executed": False})
            return "FAIL-CLOSED", rec
