#!/usr/bin/env bash
# ANCHOR-BLOCKS v1.0 (SIP-038) — Bitcoin block registry tracker for the transparency anchor.
# Upgrades receipts (fetches on-chain confirmations from calendars), then records block
# height + block hash for every confirmed stamp into ANCHOR-BLOCK-REGISTRY.json.
# Idempotent: registry entries are never overwritten once a block hash is captured.
# Usage: ./anchor_blocks.sh   (run on any cadence; safe to re-run)
set -uo pipefail
python3 - <<'PYEOF'
import json, subprocess, os, hashlib, urllib.request, time
reg_path = "anchors/ANCHOR-BLOCK-REGISTRY.json"
reg = {"updated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "receipts": {}}
if os.path.exists(reg_path):
    old = json.load(open(reg_path)); reg["receipts"] = old.get("receipts", {})
pending = confirmed = 0
for ots in sorted(os.listdir("anchors")):
    if not ots.endswith(".ots"): continue
    path = f"anchors/{ots}"
    subprocess.run(["ots","upgrade",path],capture_output=True,text=True,timeout=90)
    info = subprocess.run(["ots","info",path],capture_output=True,text=True,timeout=60).stdout
    height = None
    for l in info.splitlines():
        if "Bitcoin block height" in l:
            try: height = int(l.split(":")[-1].strip())
            except ValueError: pass
    entry = reg["receipts"].get(ots, {})
    entry["receipt_sha256"] = hashlib.sha256(open(path,'rb').read()).hexdigest()
    if height:
        entry["block_height"] = height
        entry["status"] = "confirmed_onchain"
        if "block_hash" not in entry:
            try:
                bh = urllib.request.urlopen(f"https://blockstream.info/api/block-height/{height}",timeout=30).read().decode()
                entry["block_hash"] = bh
            except Exception as e:
                entry["block_hash"] = f"lookup_failed: {e}"
        confirmed += 1
    else:
        entry["status"] = "pending"
        pending += 1
    reg["receipts"][ots] = entry
json.dump(reg, open(reg_path,"w"), indent=1)
print(f"BLOCK REGISTRY: confirmed={confirmed} pending={pending} -> {reg_path}")
for name, e in sorted(reg["receipts"].items()):
    line = f"  {name}: {e['status']}"
    if e.get("block_height"): line += f" @ block {e['block_height']} ({str(e.get('block_hash',''))[:20]}...)"
    print(line)
PYEOF
