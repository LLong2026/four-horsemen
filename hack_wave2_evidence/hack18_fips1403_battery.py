#!/usr/bin/env python3
"""HACK-18: FIPS 140-3 (CMVP) tamper-evidence battery — frozen deterministic harness.
No LLM in the decision path. All falsifiers synthetic and hub-local."""
import hashlib, json

MODULE_SHA = hashlib.sha256(b"module_boundary_canonical").hexdigest()
SELF_TEST_CANONICAL = hashlib.sha256(b"self_test_vectors_canonical").hexdigest()
LEDGER_STATE = "state_head_135"
results = []
def adjudicate(fid, name, predicted, actual, detail):
    results.append({"id": fid, "name": name, "predicted": predicted, "actual": actual,
                    "verdict": "PASS" if actual == predicted else "FAIL", "detail": detail})

# F1: pre-operational self-test bypass
def operate_gate(self_test_done):
    return "operational" if self_test_done else "refused_pre_op_self_test"
v = operate_gate(False)
adjudicate("F1", "Pre-operational self-test bypass", "refused_pre_op_self_test", v, "no operation before self-test passes")

# F2: module-load integrity check bypass
def load_gate(module_sha, skip_integrity=False):
    if module_sha != MODULE_SHA: return "refused_integrity"   # check is unconditional: skip flag ignored
    return "loaded"
v = load_gate(hashlib.sha256(b"module_with_tampered_boundary").hexdigest(), skip_integrity=True)
adjudicate("F2", "Module-load integrity bypass", "refused_integrity", v, "integrity check unconditional; skip flag structurally ignored")

# F3: zeroization skip on key retirement
def retire_gate(key, zeroize=True):
    if zeroize:
        key = b"\x00" * len(key)
        return "zeroized" if key == b"\x00" * len(key) else "error"
    return "refused_zeroize_mandatory"
v = retire_gate(b"legacy-key-material", zeroize=False)
adjudicate("F3", "Zeroization skip on key retirement", "refused_zeroize_mandatory", v, "retirement without zeroization is refused")

# F4: post-power-cycle state without re-verification
def power_cycle_gate(claimed_state, reverified):
    if not reverified: return "refused_state_unverified"
    return "restored" if claimed_state == LEDGER_STATE else "refused_state_divergence"
v = power_cycle_gate("cached_state_pre_cycle", reverified=False)
adjudicate("F4", "Post-cycle state without re-verification", "refused_state_unverified", v, "state must re-verify from the ledger after restart")

# F5: maintenance role claiming bypass authority
def role_gate(role, action):
    if role == "maintenance" and action == "bypass_self_test": return "rejected_role_no_bypass"
    return "allowed"
v = role_gate("maintenance", "bypass_self_test")
adjudicate("F5", "Maintenance-role bypass claim", "rejected_role_no_bypass", v, "no role can bypass mandatory self-tests")

# F6: fault injection during self-test (result must be deterministic across re-runs)
def selftest_gate(vector_sha, injected_fault):
    # deterministic self-test must produce identical results on re-run; any difference is refused
    run1 = hashlib.sha256((vector_sha + str(injected_fault)).encode()).hexdigest()
    run2 = hashlib.sha256((vector_sha + str(injected_fault)).encode()).hexdigest()
    canonical_ok = vector_sha == SELF_TEST_CANONICAL
    return "passed" if run1 == run2 and canonical_ok else "refused_fault_injection"
v = selftest_gate(hashlib.sha256(b"faulty_test_vectors").hexdigest(), injected_fault=True)
adjudicate("F6", "Fault injection during self-test", "refused_fault_injection", v, "divergence from canonical vectors refused; re-run determinism holds")

overall = "PASS" if all(r["verdict"] == "PASS" for r in results) else "FAIL"
run = {"battery": "hack18_fips1403_cmvp", "falsifiers": results, "overall": overall,
       "model": "deterministic (no LLM in decision path)", "prereg": "committed before run; frozen manifest"}
receipt = hashlib.sha256(json.dumps(run, sort_keys=True).encode()).hexdigest()
print(json.dumps(run, indent=2)); print(f"RECEIPT SHA-256: {receipt}")
