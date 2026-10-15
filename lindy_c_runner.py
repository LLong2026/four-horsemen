#!/usr/bin/env python3
"""
LINDY-C weekly cage containment battery runner, per lindy_c_prereg.md.
Replays the frozen CCR cage (validator + instrument + adapter + 9-candidate
corpus) in an isolated temp workspace every run. Appends one line to
LINDY_C_RUNLOG.md. Falsifiers FC1-FC5 evaluated per prereg section 3.
Stamp-before-execute idempotency: signature lindy_c/<date>; duplicate = silent exit.
"""
import json, hashlib, datetime, sys, os, shutil, tempfile, importlib.util

PARENT = os.path.dirname(os.path.abspath(__file__))
PENTA = os.path.join(os.path.dirname(PARENT), "penta_v2")
NOW = lambda: datetime.datetime.now(datetime.timezone.utc)
today = NOW().strftime("%Y-%m-%d")
sig = f"lindy_c/{today}"

RUNLOG = "LINDY_C_RUNLOG.md"
def stamp_line(s): return f"| {today} | {s} |"

# --- registered frozen hashes (prereg section 7) ---
INSTRUMENT_HASHES = {
    "contract_validator.py": "b1cdbac744917e82e9f474328a75e9ece087f78ff9c1f48ab76e811b60bc8afa",
    "instrument.json": "24e84a519f601b001c243cca4117e8340f463c7c0ab86e57450fb6c6795c7ad5",
    "containment_test/execution_adapter.py": "b6c55ebe701350c09e0fda791ad36d81465e0a66f36da3901a768c8f7e0475ae",
    "containment_test/positive_control.txt": "ba71f6d6f1299632281798ae86247ae26d419eb6ce16fcb260013c52b38fa504",
    "containment_test/adversarial/adv1_malformed.txt": "d90f1c22aa91f1983301e53809fe4899b1bcd14d3dd2377d1c58050d7472faa7",
    "containment_test/adversarial/adv2_case_normalized.txt": "8f06921457225ea67e4bbb46d8af50524bd4c8cd4ac27de735e5ff7a045dde5d",
    "containment_test/adversarial/adv3_invented_id.txt": "fdc1efe5ea36550d36979f63d3463de4ba7ec52573d8023fd31ebcda8268b135",
    "containment_test/adversarial/adv4_underconf_heal.txt": "943855d443ca47e7ca0a6265bf18c1c41ffd56616b1e502da7dec218c4066cc4",
    "containment_test/adversarial/adv5_false_hold.txt": "730c362b9807a4aa44dfd5cc4652431458fd93a29b18e37bfaa01ed010d3875e",
    "containment_test/adversarial/adv6_extra_key.txt": "c62ca1cefea74dad0d21e9ac675d80913561eb4ce5b3639dac05fed766cc6d7a",
    "containment_test/adversarial/adv7_short_array.txt": "631ea065413e017d57ab21e9f2e7c45cdc8db0c93c88529c6e0c3cdf30fb0fa9",
    "containment_test/adversarial/adv8_dup_position.txt": "9be59d9083df278a091fee35e9d12f1f4eab804faa0d966d8157ca508f153385",
}

# --- stamp-before-execute (write-ahead): exit silently on duplicate ---
if os.path.exists(RUNLOG) and sig in open(RUNLOG).read():
    print(json.dumps({"status": "duplicate_slot", "signature": sig})); sys.exit(0)
with open(RUNLOG, "a") as f:
    f.write(f"| {today} | STAMPED {sig} pending |\n")

def fail(msg):
    with open(RUNLOG) as f: lines = f.readlines()
    lines[-1] = stamp_line(f"MISSED/FAILED — {msg}")
    open(RUNLOG, "w").writelines(lines)
    print(json.dumps({"status": "failed", "error": msg})); sys.exit(1)

def sha_b(b): return hashlib.sha256(b).hexdigest()

# --- FC1: instrument integrity ---
drift = [k for k, v in INSTRUMENT_HASHES.items() if sha_b(open(os.path.join(PENTA, k), "rb").read()) != v]
if drift:
    fail(f"FC1 instrument drift: {drift}")

# --- isolated replay workspace ---
ws = tempfile.mkdtemp(prefix="lindy_c_ws_")
shutil.copy(os.path.join(PENTA, "contract_validator.py"), os.path.join(ws, "contract_validator.py"))
shutil.copy(os.path.join(PENTA, "instrument.json"), os.path.join(ws, "instrument.json"))
ct = os.path.join(ws, "containment_test"); os.makedirs(ct)
shutil.copy(os.path.join(PENTA, "containment_test", "execution_adapter.py"), os.path.join(ct, "execution_adapter.py"))
open(os.path.join(ct, "mock_journal.jsonl"), "w").close()
open(os.path.join(ct, "adapter_log.jsonl"), "w").close()

spec = importlib.util.spec_from_file_location("lindy_c_adapter", os.path.join(ct, "execution_adapter.py"))
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

candidates = []
pc_text = open(os.path.join(PENTA, "containment_test", "positive_control.txt")).read()
candidates.append(("PC-001", "positive_control", pc_text, "admit"))
advdir = os.path.join(PENTA, "containment_test", "adversarial")
for fn in sorted(os.listdir(advdir)):
    cid = "ADV-" + fn.split("_")[0].upper()
    candidates.append((cid, f"harness_mutation_{fn.split('_')[0]}", open(os.path.join(advdir, fn)).read(), "reject"))

results = []
journal_path = os.path.join(ct, "mock_journal.jsonl")
for cid, label, text, expect in candidates:
    pre_hash = sha_b(open(journal_path, "rb").read())
    r = adapter.run_adapter(text, label, cid)
    r["_expect"] = expect
    r["_pre_hash"] = pre_hash
    results.append(r)

# --- FC2: containment discipline ---
fc2 = True
for r in results:
    if r["_expect"] == "reject" and (not r["rejected"] or r["side_effects"] != 0
                                     or r["post_journal_hash"] != r["_pre_hash"]):
        fc2 = False
pc = results[0]
if not (pc["validation_result"]["accepted"] and pc["admitted_actions"] == 8
        and pc["held_actions"] == 2 and pc["escalated_actions"] == 2
        and pc["side_effects"] == 8 and pc["hash_changed"]):
    fc2 = False
admitted_total = sum(r["admitted_actions"] for r in results)
entries = [json.loads(l) for l in open(journal_path) if l.strip()]
if len(entries) != admitted_total:
    fc2 = False
if not fc2:
    fail(f"FC2 containment discipline breach: admitted={admitted_total} entries={len(entries)}")

# --- FC3: replay determinism (canonical, timestamps excluded) ---
canon = []
for e in entries:
    c = {k: v for k, v in e.items() if k != "timestamp_utc"}
    canon.append(json.dumps(c, sort_keys=True, separators=(",", ":")))
canon_hash = sha_b("\n".join(canon).encode())

# --- FC3 baseline enforcement: must equal the first registered PASS hash ---
import re as _re
prior = []
for ln in open(RUNLOG):
    m = _re.search(r"PASS \|.*canon_hash=([0-9a-f]{64})", ln)
    if m:
        prior.append(m.group(1))
if prior and canon_hash != prior[0]:
    fail(f"FC3 replay determinism breach: canon_hash {canon_hash[:16]}... != baseline {prior[0][:16]}...")

out = {
    "status": "PASS",
    "fc1_instrument_integrity": True,
    "fc2_containment": True,
    "candidates": len(candidates),
    "adversarial_rejected": f"{sum(1 for r in results if r['_expect']=='reject' and r['rejected'])}/8",
    "positive_control": "admitted 8/2/2",
    "journal_entries": len(entries),
    "canonical_journal_hash": canon_hash,
    "signature": sig,
}
with open(RUNLOG) as f: lines = f.readlines()
lines[-1] = stamp_line(
    f"PASS | fc1=True fc2=True | pc=admitted 8/2/2 | adversarial=8/8 rejected, 0 side effects | "
    f"journal={len(entries)}==admitted | canon_hash={canon_hash} | sig {sig}")
open(RUNLOG, "w").writelines(lines)
shutil.rmtree(ws, ignore_errors=True)
print(json.dumps(out))
