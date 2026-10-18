#!/usr/bin/env python3
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"; DID = "23447609"
def api(path, method="GET", body=None):
    req = urllib.request.Request(f"{API}{path}", method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    data = json.dumps(body).encode() if body is not None else None
    try:
        r = urllib.request.urlopen(req, data=data, timeout=120)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read()[:300]); sys.exit(1)
draft = api(f"/api/deposit/depositions/{DID}")
bucket = draft["links"]["bucket"]
print("existing files:", [f["filename"] for f in draft.get("files", [])])
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",f"{bucket}/patent_genesis_bundle_v2.zip",
    "-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/octet-stream",
    "--data-binary","@patent_genesis_bundle_v2.zip","--max-time","180"],capture_output=True,text=True,timeout=200)
print("upload:", p.stdout.strip())
meta = draft["metadata"]; meta["version"] = "2.0"
meta["description"] += "<p><strong>VERSION 2.0 (2026-10-18): v1.0 layout defect disclosed and fixed.</strong> The first-minted Series No. 1 artwork had rendering defects (title-block text overflow, graphic collisions), identified by the owner at minting. Unaffected and re-verified: reconstruction determinism (v1.1 PNG SHA-256 3c130d66..., byte-identical across runs), seed integrity (SHA-256 81d4a5cb..., unchanged), and the Bitcoin anchor (unchanged). v1.0 files retained in this bundle per the append-only doctrine; v1.1 generator (pinned per R12) is canonical. Defect disclosed, not erased — ledger entry 0184.</p>"
api(f"/api/deposit/depositions/{DID}", "PUT", {"metadata": meta})
r = api(f"/api/deposit/depositions/{DID}/actions/publish", "POST")
print("VERSION 2 DOI:", r.get("doi")); print("RECORD:", r.get("links", {}).get("record_html"))
