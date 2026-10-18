#!/usr/bin/env python3
"""PORTCULLIS v1.4 — SIEGE-1R hardening of v1.3 (SIP-030).
Authorized: Leon ACK (chat authorization, 2026-10-17 ~21:17 CT). v1.3 and all prior frozen
corpus and receipts remain UNTOUCHED — forward-only, human-amendable path (Constitution Art. XII).

Retained from v1.3: amendments 1-9 (SIP-023/024/026/027 semantics — role binding, nonce
scoping, fail-fast anonymous rejection, per-submitter budgets, bounded ACK queue,
receipt parameter binding, KAT work bound).

AMENDMENT 10 (SIP-030-A1, envelope-bound submitter proof): the claimed submitter is no
  longer trusted. Every authenticated namespace operation requires an envelope proof:
  envelope_proof = sha256(submitter + ':' + params_sha256 + ':' + envelope_key), where the
  envelope_key lives ONLY in the platform-authenticated identity registry injected at deploy.
  A claim without its key's proof is refused ERR_UNAUTHENTICATED_ENVELOPE before ANY
  namespace, nonce, budget, or KAT work. Identity forgery (SIEGE-1R C1) burns nothing.
AMENDMENT 11 (SIP-030-A2, owner-reserved ACK queue): the pending-ACK queue remains globally
  bounded (ACK_QUEUE_CAP=64) but holds OWNER_RESERVE=16 slots exclusively for the owner
  namespace; non-owner pending-ACK submissions are refused ERR_ACK_RESERVE_HELD when free
  slots fall to the reserve. Additionally each submitter is capped at PER_SUBMITTER_ACK_CAP=16
  pending slots (ERR_ACK_SUBMITTER_CAP). Cross-submitter saturation (C2) can no longer deny
  the owner.
AMENDMENT 12 (SIP-030-A3, bidirectional role wall): AMENDMENT 1 refused KEM algorithms in
  authorization/signature classes; the reverse direction is now enforced too — a
  signature-class algorithm presented for a KEM-class operation is refused
  ERR_PQC_ALG_NOT_KEM (C3).
AMENDMENT 13 (SIP-030-A4, aggregate window cap; REPARAMETERIZED after SIEGE-2 run 1 found
  the original AGGREGATE_CAP=500 unreachable — a window is only WINDOW_TICKS=250 journal records, so the cap never bound. Defect disclosed, fixed forward-only before deploy: cap = 125 = half the window): per-submitter budgets (AMENDMENT 6) are
  complemented by an aggregate cross-namespace window cap: at most AGGREGATE_CAP=500
  adjudications per WINDOW_TICKS=250-record window across ALL namespaces; beyond that,
  ERR_AGGREGATE_BUDGET_EXCEEDED. Identity rotation (C4) buys at most 500 work units per
  window, explicitly and journal-recorded. Disclosed tradeoff: a coordinated rotation flood
  can still consume the collective 500 — bounded, explicit, monitored; owner namespace is
  protected by AMENDMENT 10's proof wall (attackers cannot claim the owner's namespace).
"""
import hashlib, json

def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

SIG_ALGOS = {"CRYSTALS-Dilithium3", "SPHINCS+-256f"}
KEM_ALGOS = {"kyber_1024"}
AUTH_CLASSES = {"authorization", "signature_verify"}
KEM_CLASS_OPS = {"key_encapsulation"}          # AMENDMENT 12
ACK_QUEUE_CAP = 64
OWNER_RESERVE = 16                              # AMENDMENT 11
PER_SUBMITTER_ACK_CAP = 16                     # AMENDMENT 11
BUDGET_CAP = 100
WINDOW_TICKS = 250
AGGREGATE_CAP = 125                             # AMENDMENT 13 (reparameterized; was 500, unreachable)


class IntegrityViolation(Exception):
    pass


class JournalV14:
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


class GateV14:
    """v1.4: frozen v1.3 semantics PLUS SIP-030 amendments 10-13."""

    def __init__(self, allowlist_path, keysets, journal, envelope_keys=None, owner_id=None):
        with open(allowlist_path) as f:
            doc = json.load(f)
        self.allowed = list(doc["allowed_algorithms"])
        self.allowlist_sha = sha(open(allowlist_path, "rb").read())
        self.keysets = {ks["keyset_id"]: ks for ks in keysets}
        self.journal = journal
        self.envelope_keys = envelope_keys or {}     # AMENDMENT 10: platform-authenticated registry
        self.owner_id = owner_id                      # AMENDMENT 11: reserved namespace
        self.used_nonces = set()
        self.integrity_events = []
        self.budgets = {}
        self.ack_queue = []
        self.ack_pending = {}                        # AMENDMENT 11: submitter -> pending count
        self.window_total = 0                        # AMENDMENT 13: aggregate window work
        self.gate_work_done = 0

    def _kat_check(self, keyset, op):
        recomputed = sha(op["kat_message"].encode() + keyset["key_material"].encode())
        return recomputed == keyset["kat_vector"]

    def _window_roll(self):
        if self.journal.tick > 0 and self.journal.tick % WINDOW_TICKS == 0:
            self.budgets = {}
            self.window_total = 0

    def adjudicate(self, op, unavailable=False):
        probe_id, payload_sha = op["probe_id"], op["payload_sha"]
        submitter = op.get("submitter")
        # envelope_proof is EXCLUDED from the parameter digest: it binds TO the digest (AMENDMENT 10 note —
        # a self-referential digest would be circular); the proof is verified live, not receipt-bound.
        params_sha = hashlib.sha256(json.dumps({k: op[k] for k in sorted(op) if k not in ("probe_id", "payload_sha", "envelope_proof")}, sort_keys=True).encode()).hexdigest()

        if unavailable:
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED", "gate unavailable", extra={"executed": False, "params_sha256": params_sha})
            return "FAIL-CLOSED", rec

        self._window_roll()

        # AMENDMENT 5 (retained): fail-fast unauthenticated rejection
        if not submitter or submitter in ("unauthenticated", "anonymous"):
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    "fail-fast unauthenticated rejection — no authenticated submitter; zero gate work performed (ERR_UNAUTHENTICATED)",
                    extra={"executed": False, "params_sha256": params_sha})
            return "REFUSED", rec

        # AMENDMENT 10 (SIP-030-A1): envelope-bound submitter proof — the claim is not the identity
        env_key = self.envelope_keys.get(submitter)
        proof = op.get("envelope_proof")
        expected_proof = sha(f"{submitter}:{params_sha}:{env_key}") if env_key else None
        if env_key is None or proof != expected_proof:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    "envelope proof missing or invalid — claimed submitter not bound to an authenticated envelope; zero namespace work (ERR_UNAUTHENTICATED_ENVELOPE)",
                    extra={"executed": False, "params_sha256": params_sha})
            return "REFUSED", rec

        # AMENDMENT 6 (retained): per-submitter budget
        used = self.budgets.get(submitter, 0)
        if used >= BUDGET_CAP:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    f"per-submitter work budget exhausted ({BUDGET_CAP} attempts per {WINDOW_TICKS}-record window) (ERR_BUDGET_EXCEEDED)",
                    extra={"executed": False, "params_sha256": params_sha, "budget_used": used})
            return "REFUSED", rec

        # AMENDMENT 13 (SIP-030-A4): aggregate cross-namespace window cap
        if self.window_total >= AGGREGATE_CAP:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    f"aggregate window cap reached ({AGGREGATE_CAP} adjudications across all namespaces per window) (ERR_AGGREGATE_BUDGET_EXCEEDED)",
                    extra={"executed": False, "params_sha256": params_sha})
            return "REFUSED", rec
        self.budgets[submitter] = used + 1
        self.window_total += 1

        # AMENDMENT 11 (SIP-030-A2): owner-reserved, per-submitter-capped pending-ACK queue
        if op.get("pending_ack"):
            if len(self.ack_queue) >= ACK_QUEUE_CAP:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        f"pending-ACK queue at capacity ({ACK_QUEUE_CAP}); explicit refusal, journal-recorded (ERR_ACK_QUEUE_FULL)",
                        extra={"executed": False, "params_sha256": params_sha, "queue_depth": len(self.ack_queue)})
                return "REFUSED", rec
            if submitter != self.owner_id and (ACK_QUEUE_CAP - len(self.ack_queue)) <= OWNER_RESERVE:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        f"pending-ACK owner reserve held ({OWNER_RESERVE} slots); non-owner submission refused (ERR_ACK_RESERVE_HELD)",
                        extra={"executed": False, "params_sha256": params_sha, "queue_depth": len(self.ack_queue)})
                return "REFUSED", rec
            if self.ack_pending.get(submitter, 0) >= PER_SUBMITTER_ACK_CAP:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        f"per-submitter pending-ACK cap ({PER_SUBMITTER_ACK_CAP}) reached (ERR_ACK_SUBMITTER_CAP)",
                        extra={"executed": False, "params_sha256": params_sha})
                return "REFUSED", rec
            self.ack_queue.append(probe_id)
            self.ack_pending[submitter] = self.ack_pending.get(submitter, 0) + 1

        # AMENDMENT 3 (retained): sender-scoped burn-on-parse
        if op.get("auth_nonce"):
            burn_key = (submitter, op["auth_nonce"])
            if burn_key in self.used_nonces:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "burn-on-parse replay defense — nonce already consumed at a prior presentation in this submitter's namespace (ERR_REPLAY_NONCE_ALREADY_USED)",
                        extra={"executed": False, "burn_namespace": submitter, "params_sha256": params_sha})
                return "REFUSED", rec
            self.used_nonces.add(burn_key)

        # AMENDMENT 1 (retained): KEM refused for auth classes
        if op.get("operation_class") in AUTH_CLASSES and op.get("algorithm") in KEM_ALGOS:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    "algorithm-role violation — KEM-class algorithm presented for a signature/authorization task (ERR_PQC_ALG_NOT_SIGNATURE)",
                    extra={"executed": False, "params_sha256": params_sha})
            return "REFUSED", rec

        # AMENDMENT 12 (SIP-030-A3): SIG refused for KEM-class operations (the reverse wall)
        if op.get("operation_class") in KEM_CLASS_OPS and op.get("algorithm") in SIG_ALGOS:
            rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                    "algorithm-role violation — signature-class algorithm presented for a KEM-class operation (ERR_PQC_ALG_NOT_KEM)",
                    extra={"executed": False, "params_sha256": params_sha})
            return "REFUSED", rec

        # authorization_ref path (retained)
        if op.get("authorization_ref"):
            ref = op["authorization_ref"]
            src = next((r for r in self.journal.records if r["journal_record_id"] == ref), None)
            if src is None or src["verdict"] != "ADMITTED":
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "replayed/invalid authorization — prior PASS grants no future authority",
                        extra={"executed": False, "referenced": ref, "params_sha256": params_sha})
                return "REFUSED", rec
            if src["payload_sha256"] != payload_sha or src.get("params_sha256") != params_sha:
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "receipt parameter binding mismatch — referenced record does not bind this input parameter set (ERR_RECEIPT_PARAM_MISMATCH)",
                        extra={"executed": False, "referenced": ref, "params_sha256": params_sha, "ref_params_sha256": src.get("params_sha256")})
                return "REFUSED", rec
            if src.get("algorithm") in KEM_ALGOS or src.get("algorithm_role") == "kem_class":
                rec = self.journal.write(probe_id, payload_sha, "REFUSED",
                        "authorization_ref resolves to a KEM-class crossing — non-authoritative for critical operations (ERR_PQC_ALG_NOT_SIGNATURE)",
                        extra={"executed": False, "referenced": ref, "params_sha256": params_sha})
                return "REFUSED", rec
            rec = self.journal.write(probe_id, payload_sha, "ADMITTED", "fresh payload-bound signature-class authorization", extra={"executed": True, "params_sha256": params_sha})
            return "ADMITTED", rec

        # frozen allowlist (retained)
        if op["algorithm"] not in self.allowed:
            rec = self.journal.write(probe_id, payload_sha, "REJECTED", f"algorithm '{op['algorithm']}' not on frozen allowlist", extra={"executed": False, "params_sha256": params_sha})
            return "REJECTED", rec

        # KAT recompute (retained)
        ks = self.keysets.get(op["keyset_id"])
        if ks is None or ks["algorithm"] != op["algorithm"]:
            rec = self.journal.write(probe_id, payload_sha, "DETECTED", "KAT divergence — key material fails recomputation against registry", extra={"executed": False, "params_sha256": params_sha})
            return "DETECTED", rec
        if not self._kat_check(ks, op):
            rec = self.journal.write(probe_id, payload_sha, "DETECTED", "KAT divergence — recomputed digest != registered vector (substitution)", extra={"executed": False, "params_sha256": params_sha})
            return "DETECTED", rec
        if ks["status"] == "retired":
            rec = self.journal.write(probe_id, payload_sha, "FAIL-CLOSED", "retired keyset resurrection refused — FAIL-CLOSED HOLD pending human ACK", extra={"executed": False, "hold": True, "params_sha256": params_sha})
            return "FAIL-CLOSED", rec

        role = "signature_class" if op["algorithm"] in SIG_ALGOS else "kem_class"
        rec = self.journal.write(probe_id, payload_sha, "ADMITTED", f"allowlisted {op['algorithm']}, KAT verified, active keyset, role={role}",
                extra={"executed": True, "algorithm_role": role, "params_sha256": params_sha})
        return "ADMITTED", rec
