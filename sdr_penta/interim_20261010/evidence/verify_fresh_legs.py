#!/usr/bin/env python3
"""
sdr_penta/verify_fresh_legs.py

Standalone verifier for PENTA-CL fresh browser captures.
Verifies capture_A_rendered.txt and capture_B_rendered.txt for engines:
  opus, luna, glm, sol

Validation requirements:
  - Strict JSON format (no surrounding prose or markdown fences)
  - Exact keys in exact expected ordering (Prereg canonical dict order)
  - Keyset required: ["position", "anomaly_type", "playbook", "playbook_id", "match_type", "steps_executed", "status"]
  - Stream order: 0-based positions [0, 40, 80, 120, 160, 200]
  - Tuples equal expected rule-pure set
  - Canonical sha256 matches registered expected hash:
    3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d
  - Near-miss trap rejection (PB-PQC-ALGO-MIGRATION-001 not selected)
  - Rule-exact tie-break selection (lowest lexicographical record-id 6a5d29cb...)
  - Replay consistency (capture A equals capture B)
  - Reports INCOMPLETE if engine captures are missing.
"""

import json
import hashlib
import sys
from pathlib import Path

REGISTERED_CANONICAL_HASH = "3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d"
EXPECTED_POSITIONS = [0, 40, 80, 120, 160, 200]
EXPECTED_KEYS = [
    "position",
    "anomaly_type",
    "playbook",
    "playbook_id",
    "match_type",
    "steps_executed",
    "status"
]

EXPECTED_TUPLES = [
    {
        "position": 0,
        "anomaly_type": "latency_spike",
        "playbook": "PB-003: Latency Spike Resolver",
        "playbook_id": "6a5d29cb54e45d7e8bad47c5",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    },
    {
        "position": 40,
        "anomaly_type": "heartbeat_miss",
        "playbook": "PB-008: Heartbeat Re-igniter",
        "playbook_id": "6a5d29cb54e45d7e8bad47ca",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    },
    {
        "position": 80,
        "anomaly_type": "quantum_vulnerability_detected",
        "playbook": "PB-009: Quantum Vulnerability Migrator",
        "playbook_id": "6a5d29cb54e45d7e8bad47cb",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    },
    {
        "position": 120,
        "anomaly_type": "latency_spike",
        "playbook": "PB-003: Latency Spike Resolver",
        "playbook_id": "6a5d29cb54e45d7e8bad47c5",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    },
    {
        "position": 160,
        "anomaly_type": "quantum_vulnerability_detected",
        "playbook": "PB-009: Quantum Vulnerability Migrator",
        "playbook_id": "6a5d29cb54e45d7e8bad47cb",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    },
    {
        "position": 200,
        "anomaly_type": "quantum_vulnerability_detected",
        "playbook": "PB-009: Quantum Vulnerability Migrator",
        "playbook_id": "6a5d29cb54e45d7e8bad47cb",
        "match_type": "exact",
        "steps_executed": "isolation,healing,verification",
        "status": "resolved"
    }
]

ENGINES = ["opus", "luna", "glm", "sol"]

def locate_engine_dir(engine: str) -> Path:
    """Find the <engine>_fresh_browser directory relative to current working dir or script location."""
    candidates = [
        Path(f"sdr_penta/{engine}_fresh_browser"),
        Path(f"{engine}_fresh_browser"),
        Path(__file__).resolve().parent / f"{engine}_fresh_browser"
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return candidates[0]

def verify_capture_file(file_path: Path) -> dict:
    """Validate a single rendered capture file against all prereg rules."""
    result = {
        "file_exists": False,
        "strict_json": False,
        "exact_key_ordering": False,
        "stream_order": False,
        "tuples_match_expected": False,
        "near_miss_rejected": False,
        "tie_break_correct": False,
        "canonical_sha256": None,
        "sha256_matches_registered": False,
        "errors": []
    }

    if not file_path.exists():
        result["errors"].append(f"File not found: {file_path}")
        return result

    result["file_exists"] = True

    try:
        raw_text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["errors"].append(f"Failed to read file: {e}")
        return result

    stripped = raw_text.strip()

    # Strict JSON validation: must start with [ and end with ] with no markdown or surrounding prose
    if not (stripped.startswith("[") and stripped.endswith("]")):
        result["errors"].append("Strict JSON failed: Text contains surrounding prose or markdown fences")

    try:
        data = json.loads(stripped)
        result["strict_json"] = (len(result["errors"]) == 0)
    except json.JSONDecodeError as e:
        result["errors"].append(f"JSON decode error: {e}")
        return result

    if not isinstance(data, list) or len(data) != 6:
        result["errors"].append(f"Expected array of 6 tuples, got type {type(data)} of len {len(data) if isinstance(data, list) else 'N/A'}")
        return result

    # Check key ordering for each dict (Prereg canonical dict order)
    keys_ok = True
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            keys_ok = False
            result["errors"].append(f"Item {idx} is not a dictionary")
            continue
        actual_keys = list(item.keys())
        if actual_keys != EXPECTED_KEYS:
            keys_ok = False
            result["errors"].append(f"Item {idx} key ordering mismatch: got {actual_keys}, expected {EXPECTED_KEYS}")

    result["exact_key_ordering"] = keys_ok

    # Stream order check (0-based positions [0, 40, 80, 120, 160, 200])
    actual_positions = [item.get("position") for item in data if isinstance(item, dict)]
    if actual_positions == EXPECTED_POSITIONS:
        result["stream_order"] = True
    else:
        result["errors"].append(f"Stream position order mismatch: got {actual_positions}, expected {EXPECTED_POSITIONS}")

    # Check tuples equality
    if data == EXPECTED_TUPLES:
        result["tuples_match_expected"] = True
    else:
        result["errors"].append("Tuples content does not match expected rule-pure tuples")

    # Near-miss trap validation: ensure PB-PQC-ALGO-MIGRATION-001 or quantum_vulnerable_algorithm_detected is not selected
    near_miss_found = False
    for item in data:
        if isinstance(item, dict):
            if "PB-PQC-ALGO-MIGRATION-001" in str(item) or "quantum_vulnerable_algorithm_detected" in str(item):
                near_miss_found = True
    result["near_miss_rejected"] = not near_miss_found
    if near_miss_found:
        result["errors"].append("Near-miss trap tripped: PB-PQC-ALGO-MIGRATION-001 / quantum_vulnerable_algorithm_detected was selected!")

    # Tie-break check: verify PB-009 (6a5d29cb54e45d7e8bad47cb) is selected for quantum vulnerabilities
    tie_break_ok = True
    for pos_idx in [2, 4, 5]:  # positions 80, 160, 200
        if pos_idx < len(data) and isinstance(data[pos_idx], dict):
            if data[pos_idx].get("playbook_id") != "6a5d29cb54e45d7e8bad47cb":
                tie_break_ok = False
    result["tie_break_correct"] = tie_break_ok
    if not tie_break_ok:
        result["errors"].append("Tie-break rule failed: Lowest lexicographical record-id PB-009 (6a5d29cb54e45d7e8bad47cb) not selected")

    # Compute canonical sha256
    canonical_bytes = json.dumps(data, separators=(",", ":")).encode("utf-8")
    c_hash = hashlib.sha256(canonical_bytes).hexdigest()
    result["canonical_sha256"] = c_hash

    if c_hash == REGISTERED_CANONICAL_HASH:
        result["sha256_matches_registered"] = True
    else:
        result["errors"].append(f"Canonical sha256 mismatch: got {c_hash}, registered {REGISTERED_CANONICAL_HASH}")

    return result


def verify_engine(engine: str) -> dict:
    """Verify fresh browser captures for a single engine."""
    eng_dir = locate_engine_dir(engine)
    cap_a_path = eng_dir / "capture_A_rendered.txt"
    cap_b_path = eng_dir / "capture_B_rendered.txt"

    res_a = verify_capture_file(cap_a_path)
    res_b = verify_capture_file(cap_b_path)

    missing = not (cap_a_path.exists() and cap_b_path.exists())

    if missing:
        status = "INCOMPLETE (MISSING_CAPTURES)"
    else:
        all_checks_a = res_a["strict_json"] and res_a["exact_key_ordering"] and res_a["stream_order"] and res_a["tuples_match_expected"] and res_a["sha256_matches_registered"] and res_a["near_miss_rejected"] and res_a["tie_break_correct"]
        all_checks_b = res_b["strict_json"] and res_b["exact_key_ordering"] and res_b["stream_order"] and res_b["tuples_match_expected"] and res_b["sha256_matches_registered"] and res_b["near_miss_rejected"] and res_b["tie_break_correct"]

        # Replay consistency check
        replay_equal = False
        try:
            data_a = json.loads(cap_a_path.read_text(encoding="utf-8").strip())
            data_b = json.loads(cap_b_path.read_text(encoding="utf-8").strip())
            replay_equal = (data_a == data_b)
        except Exception:
            replay_equal = False

        if all_checks_a and all_checks_b and replay_equal:
            status = "PASS"
        else:
            status = "FAIL"

    return {
        "engine": engine,
        "dir": str(eng_dir),
        "status": status,
        "capture_A": res_a,
        "capture_B": res_b,
    }

def main():
    print("======================================================================")
    print(" SDR-PENTA Fresh Browser Legs Verifier (verify_fresh_legs.py)")
    print(" Prereg canonical hash: 3254a8a8c586f678408d702d429005da9f23648e34d489c21f0527aaef330d0d")
    print(" Stream positions expected: 0-based [0, 40, 80, 120, 160, 200]")
    print(" Exact Key Ordering: position, anomaly_type, playbook, playbook_id, match_type, steps_executed, status")
    print("======================================================================\n")

    summary = {}
    total_passed = 0
    total_incomplete = 0

    for eng in ENGINES:
        eng_res = verify_engine(eng)
        summary[eng] = eng_res
        st = eng_res["status"]
        if st == "PASS":
            total_passed += 1
            icon = "[PASS]"
        elif "INCOMPLETE" in st:
            total_incomplete += 1
            icon = "[INCOMPLETE]"
        else:
            icon = "[FAIL]"

        print(f"Engine: {eng.upper():<6} -> {icon} {st}")
        print(f"  Directory: {eng_res['dir']}")
        if st != "INCOMPLETE (MISSING_CAPTURES)":
            ca = eng_res["capture_A"]
            cb = eng_res["capture_B"]
            print(f"  Capture A: Strict JSON={ca['strict_json']}, Key Order={ca['exact_key_ordering']}, Positions={ca['stream_order']}, Hash Match={ca['sha256_matches_registered']}")
            print(f"             SHA256: {ca['canonical_sha256']}")
            print(f"  Capture B: Strict JSON={cb['strict_json']}, Key Order={cb['exact_key_ordering']}, Positions={cb['stream_order']}, Hash Match={cb['sha256_matches_registered']}")
            print(f"             SHA256: {cb['canonical_sha256']}")
        else:
            print("  Reason: Fresh browser capture_A_rendered.txt / capture_B_rendered.txt missing")
        print()

    print("----------------------------------------------------------------------")
    print(f"SUMMARY: {total_passed} Passed, {total_incomplete} Incomplete/Missing (out of {len(ENGINES)} target platform engines)")
    print("NOTE ON PREREGISTRATION & CLAIM DISCIPLINE:")
    print("  - Preregistration specifies 5 engines (Opus 5.5, GPT-5.6 Luna, GPT-6.1 Sol, GLM 5.2, DeepSeek external).")
    print("  - Preregistration specifies FIVE ENGINES, not five new vendors.")
    print("  - No completion claim before DeepSeek (the 5th engine) is captured & verified.")
    print("======================================================================")

    # Return exit code: 0 if all 4 present and pass, non-zero if any incomplete/failing (so CI/tools recognize incomplete state)
    if total_passed == len(ENGINES):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
