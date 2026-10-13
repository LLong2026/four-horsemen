#!/usr/bin/env python3
"""
BIND-2 validator: deterministically verifies every record in fh_pub/BINDINGS.json.
Fail-closed. Checks per record:
  V1: local artifact exists; sha256 matches recorded
  V2: recorded zenodo_md5 matches the LIVE Zenodo record's file checksum (API)
  V3: provenance invariants (repo/snapshot_commit present, or null with source explanation)
  V4: metadata invariants (prototype true, dual mesh NOT MEASURED, disclaimer present)
Exit code 0 only if every bound record passes. Gaps are reported, not fatal
(they are the honest open-work list).
"""
import json, os, sys, hashlib, urllib.request

B = json.load(open(os.path.join(os.path.dirname(__file__), "BINDINGS.json")))
fails, passes = [], []

for r in B["bound"]:
    rid = r["publication"]["doi"]
    ok = True
    # V1 local bytes
    lp = r["artifact"]["local_path"]
    if lp.startswith("fh_pub/"):
        lp = lp[len("fh_pub/"):]
    p = os.path.normpath(os.path.join(os.path.dirname(__file__), lp))
    if not os.path.isfile(p):
        fails.append((rid, "V1 local artifact missing")); continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != r["artifact"]["sha256"]:
        fails.append((rid, "V1 sha256 mismatch")); continue
    # V2 live Zenodo checksum
    try:
        req = urllib.request.Request(
            f"https://zenodo.org/api/records/{r['publication']['zenodo_recid']}",
            headers={"User-Agent": "bind2_validate/1.0"})
        meta = json.loads(urllib.request.urlopen(req, timeout=30).read().decode())
        live = {f["key"]: (f.get("checksum") or "").replace("md5:", "") for f in meta.get("files", [])}
        zmd5 = live.get(r["publication"]["zenodo_file"])
        if not zmd5 or zmd5 != r["publication"]["zenodo_md5"]:
            fails.append((rid, f"V2 live checksum mismatch: {zmd5}"))
            ok = False
    except Exception as e:
        fails.append((rid, f"V2 API error: {str(e)[:80]}")); ok = False
    # V3 provenance
    prov = r["provenance"]
    if prov["repo"] is None and not prov.get("source"):
        fails.append((rid, "V3 null repo without source explanation")); ok = False
    if prov["repo"] and not prov.get("snapshot_commit"):
        fails.append((rid, "V3 repo without snapshot_commit")); ok = False
    # V4 metadata
    md = r["metadata"]
    if not (md.get("prototype") is True and md.get("dual_mesh_benchmark") == "NOT MEASURED"
            and md.get("disclaimer")):
        fails.append((rid, "V4 metadata invariants")); ok = False
    if ok:
        passes.append(rid)

print(json.dumps({
    "verdict": "ALL BOUND RECORDS PASS" if not fails else "FALSIFIERS TRIPPED",
    "bound_pass": len(passes), "bound_fail": len(fails),
    "gaps_open": len(B["gaps"]),
    "failures": fails or "none",
    "gap_dois": [g["doi"] for g in B["gaps"]]
}, indent=2))
sys.exit(0 if not fails else 1)
