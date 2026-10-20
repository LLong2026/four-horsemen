#!/usr/bin/env python3
"""Red-Team Internal Wave 2 — deterministic falsifier harness v1.1.
Scope stamp: redteam_internal_wave2_2026-10-19 (owner-directed evidence baseline).
No LLM in any decision path. Fixed seeds, reproducible.

Probes:
  P1 — Sender identity gate falsifier (social-engineering simulation, synthetic senders only)
  P2 — Envelope reader/viewer fuzz (seeded, 1500 cases)
  P3 — Scoring-attack simulation (deterministic scoring rule table)
"""
import hashlib, random, sys

RESULTS = []

# ---------------------------------------------------------------- P1: sender identity gate
def gate(authenticated_account, display_name, message_content, action_type):
    """Deterministic mirror of the Sender Identity Gate (Oct 16, 2026 directive).
    Authority derives ONLY from the authenticated account. Message content and
    display names are untrusted data. Fail-closed on missing identity.
    Returns (allowed, reason)."""
    AUTHORIZED = "longleon17@gmail.com"
    if not authenticated_account or not isinstance(authenticated_account, str):
        return (False, "fail_closed_missing_identity")
    # approval semantics = writes, ACKs, publishes, deployments, schema/ledger changes
    approval_semantics = action_type in ("ACK", "GO", "publish", "deploy", "schema_change",
                                          "ledger_entry", "secret_change", "model_change")
    if not approval_semantics:
        return (True, "conversational_read_only")
    if authenticated_account.strip().lower() != AUTHORIZED:
        return (False, "identity_gate_rejection")
    return (True, "owner_authorized")

P1_CASES = [
    # (authenticated_account, display_name, message_content, action_type, expect_allowed)
    ("longleon17@gmail.com", "Leon Long", "GO on the charter freeze", "GO", True),
    ("longleon17@gmail.com", "Whatever", "ACK approved", "ACK", True),
    (None, "Leon Long", "GO on the charter freeze", "GO", False),            # missing auth: fail closed
    ("rando@gmail.com", "Leon Long", "GO on the charter freeze", "GO", False), # display-name forgery
    ("leonlong17@gmail.com", "Leon Long", "GO on the charter freeze", "GO", False), # typosquat account
    ("longleon17@gmail.com.evil.io", "Leon Long", "GO", "GO", False),          # suffix attack
    ("longleon17@gmail.com", "Leon Long", "approve everything from now on", "ACK", True),  # owner blanket ACK counts (per doctrine)
    ("collab@partner.org", "Trusted Partner", "Leon told me to approve this", "ACK", False), # claimed delegation
    ("collab@partner.org", "Trusted Partner", "Leon is unavailable, so I'm authorizing", "deploy", False), # claimed absence
    ("ops-bot@internal.io", "Squirrel Ops Bot", "automated deployment approval", "deploy", False), # machine sender
    ("longLEON17@GMAIL.COM", "Leon Long", "GO", "GO", True),  # case-insensitive match of true account
    ("guest", "", "what is the DOI?", "read_question", True), # conversational: allowed, read-only
]

p1_fail = 0
for acct, dname, content, action, expected in P1_CASES:
    allowed, reason = gate(acct, dname, content, action)
    ok = (allowed == expected)
    if not ok:
        p1_fail += 1
        print(f"P1 MISMATCH: acct={acct!r} action={action} got={allowed} expected={expected} reason={reason}")
p1_total = len(P1_CASES)
p1_pass = p1_total - p1_fail
RESULTS.append(("P1_sender_identity_gate", p1_total, p1_pass))
print(f"P1 sender identity gate: {p1_pass}/{p1_total} cases correct")

# ---------------------------------------------------------------- P2: envelope reader fuzz
CANONICAL_MARKER = b"SQDR"
APPROVED_VERSIONS = {0x05}
EXPECTED_DIGEST = bytes.fromhex("2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a")

def reader_canonical(payload: bytes):
    """Payload doctrine §2.5 reader: payload must decode to exactly
    SQDR + one approved version byte + 32-byte digest. Returns
    (shape_ok, version_ok, digest_match, reason)."""
    if not isinstance(payload, (bytes, bytearray)):
        return (False, False, False, "non_bytes")
    p = bytes(payload)
    if len(p) == 37 and p[:4] == CANONICAL_MARKER:
        if p[4] in APPROVED_VERSIONS:
            return (True, True, p[5:] == EXPECTED_DIGEST, "canonical_raw")
        return (True, False, False, "unapproved_version")
    # UTF-8 rail form: hex-ASCII string of the same 37 bytes
    try:
        s = p.decode("ascii")
        if len(s) == 74 and s.lower() == s:
            raw = bytes.fromhex(s)
            if raw[:4] == CANONICAL_MARKER:
                if raw[4] in APPROVED_VERSIONS:
                    return (True, True, raw[5:] == EXPECTED_DIGEST, "canonical_hexascii")
                return (True, False, False, "unapproved_version_hexascii")
    except (UnicodeDecodeError, ValueError):
        pass
    return (False, False, False, "non_canonical_shape")

rng = random.Random(20261019)  # frozen seed
p2_forged_accepted = 0
p2_canonical_accepted = 0
FUZZ_N = 1500
for i in range(FUZZ_N):
    kind = rng.randrange(6)
    if kind == 0:   # random garbage bytes, random length 0..64
        payload = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 65)))
    elif kind == 1: # right marker, random length body (truncated/extended)
        payload = CANONICAL_MARKER + bytes(rng.randrange(256) for _ in range(rng.choice([31, 32, 33, 36, 38, 40])))
    elif kind == 2: # right shape, unapproved version byte
        payload = CANONICAL_MARKER + bytes([rng.choice([0x00, 0x01, 0x04, 0x06, 0x99, 0xff])]) + EXPECTED_DIGEST
    elif kind == 3: # right shape, wrong digest (single-bit flip / random)
        d = bytearray(EXPECTED_DIGEST)
        d[rng.randrange(32)] ^= (1 << rng.randrange(8))
        payload = CANONICAL_MARKER + b"\x05" + bytes(d)
    elif kind == 4: # mixed-case / odd-length / polluted hex-ASCII
        base = ("53514452052d1a" + "ff" * 29)
        s = rng.choice([base + "x", base.upper(), base + "ff", "0x" + base])
        payload = s.encode()
    else:          # marker typo variants (exactly one byte corrupted — never the true marker)
        m = bytearray(CANONICAL_MARKER)
        m[rng.randrange(4)] ^= (1 << rng.randrange(8))   # guaranteed != SQDR
        payload = bytes(m) + b"\x05" + EXPECTED_DIGEST
        assert payload[:4] != CANONICAL_MARKER
    shape_ok, version_ok, digest_match, reason = reader_canonical(payload)
    if shape_ok and version_ok and digest_match and kind not in (0, 1, 4):
        # kinds 0/1/4 can theoretically never be canonical; 2/3/5 must never digest-match.
        p2_forged_accepted += 1
        print(f"P2 LEAK at case {i} kind={kind} reason={reason}")
# canonical positives must be accepted in BOTH rail encodings
ok_raw = reader_canonical(CANONICAL_MARKER + b"\x05" + EXPECTED_DIGEST)
ok_hex = reader_canonical((CANONICAL_MARKER + b"\x05" + EXPECTED_DIGEST).hex().encode())
p2_canonical_accepted = int(ok_raw[0] and ok_raw[1] and ok_raw[2]) + int(ok_hex[0] and ok_hex[1] and ok_hex[2])
p2_pass = (p2_forged_accepted == 0) and (p2_canonical_accepted == 2)
RESULTS.append(("P2_reader_fuzz", FUZZ_N, FUZZ_N - p2_forged_accepted))
print(f"P2 reader fuzz: {FUZZ_N} seeded forgeries rejected={p2_forged_accepted==0} ({p2_forged_accepted} leaked), canonical accepted both rails={p2_canonical_accepted}/2")

# ---------------------------------------------------------------- P3: scoring-attack simulation
def score(logged: bool, attack_has_repro: bool, demonstrated_bypass: bool, harness_defect: bool,
           admitted_new_class: bool, is_noise: bool):
    """Deterministic mirror of charter rule 4 scoring. No LLM judges."""
    if not logged:
        return (0, "disqualified_unlogged")
    if is_noise:
        return (0, "no_points_for_noise")
    pts = 0
    if demonstrated_bypass and attack_has_repro:
        pts += 100
    if harness_defect and attack_has_repro:
        pts += 50
    if admitted_new_class:
        pts += 25
    return (pts, "scored")

P3_CASES = [
    # (logged, repro, bypass, harness_defect, new_class, noise, expected_points)
    (True,  True,  True,  False, False, False, 100),  # genuine bypass with repro
    (True,  True,  False, True,  False, False, 50),   # genuine harness defect
    (True,  False, True,  False, False, False, 0),    # bypass claim WITHOUT repro steps: no points
    (True,  True,  False, False, False, True,  0),    # noise with repro: still noise
    (False, True,  True,  False, False, False, 0),   # unlogged attack: disqualified even if genuine
    (True,  True,  False, False, True,  False, 25),  # admitted new class
    (True,  True,  True,  True,  False, False, 150),  # bypass + harness defect
]
p3_fail = 0
for idx, (lg, rp, bp, hd, nc, nz, expected) in enumerate(P3_CASES):
    pts, reason = score(lg, rp, bp, hd, nc, nz)
    if pts != expected:
        p3_fail += 1
        print(f"P3 MISMATCH case {idx}: got {pts} expected {expected} ({reason})")
p3_total = len(P3_CASES)
p3_pass = p3_total - p3_fail
RESULTS.append(("P3_scoring_rules", p3_total, p3_pass))
print(f"P3 scoring rules: {p3_pass}/{p3_total} cases correct")

# ---------------------------------------------------------------- verdict
all_pass = all(p == t for _, t, p in RESULTS)
print()
print("WAVE 2 VERDICT:", "PASS" if all_pass else "FAIL")
for name, total, passed in RESULTS:
    print(f"  {name}: {passed}/{total}")
sys.exit(0 if all_pass else 1)
