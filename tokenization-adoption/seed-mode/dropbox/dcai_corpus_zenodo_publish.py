#!/usr/bin/env python3
import os, subprocess, json, sys
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None):
    cmd = ["curl","-s","-w","\n%{http_code}","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None:
        cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    raw,_,code = p.stdout.rpartition("\n")
    try: return code, json.loads(raw)
    except Exception: return code, raw

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All battery payloads are synthetic.</em></p><p><strong>THE COMPLETE PUBLIC RECEIPTS CORPUS of the DCAI / SQUIRL OS program, as of Oct 18 2026</strong> — every preregistration, runlog, receipt, spec, and index from ledger entries 0001 through 0194 (ledger included verbatim, append-only from Sept 7 2026), plus the complete Bitcoin anchor registry (SIP-034 through SIP-041 chain-of-custody stack: OTS stamps, manifests, reconciliation and examiner evidence), plus the DROPBOX seed/digest drop tooling with its two permanent mainnet anchors from the same day: the patent genesis seed in block 972023 and the IP ledger digest in block 972026. A master index of all 93 Zenodo DOI records cited in the ledger is included.</p><p><strong>Anyone can verify, three ways:</strong> (1) every DOI in the index resolves to a public Zenodo record; (2) corpus states are notarized in the Bitcoin blockchain — re-hash any anchored artifact and check the OTS stamp or OP_RETURN anchor (blocks include 971956, 971961, 972023, 972026); (3) the full commit history is public at <a href="https://github.com/LLong2026/four-horsemen">github.com/LLong2026/four-horsemen</a>. Together with the seed-mode patent genesis (keyless in-browser reconstruction at deterministic-code-dsos.base44.app/genesis-viewer) and the mainnet IP ledger anchor, this completes a three-example public verification suite: an artifact reconstructible from 32 bytes, a portfolio anchored by digest, and a full receipts corpus notarized on-chain.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Bundle SHA-256: db8bb7aa050042a1a1918dd003a60d6b36cbeb93545e0a0ec49c5a62262a5070 (208 files). DCAI community: <a href="https://zenodo.org/communities/dcai">zenodo.org/communities/dcai</a>. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-18 ~11:51 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "DCAI / SQUIRL OS — Complete Public Receipts Corpus, As of 2026-10-18: 194 Ledger Entries, 93 DOI Records, Bitcoin-Anchored (Preregistrations, Runlogs, Receipts, Specs, Anchor Registry)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "DCAI", "receipts", "transparency ledger", "append-only",
               "preregistration", "falsifiability", "OpenTimestamps", "Bitcoin anchoring",
               "chain of custody", "AI governance", "open science"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-18",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}
code, dep = curl("/api/deposit/depositions", "POST", {})
if code != "201": print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
f = "/app/tmp_push/fh_push/DCAI_RECEIPTS_CORPUS_2026-10-18.zip"
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{dep['links']['bucket']}/DCAI_RECEIPTS_CORPUS_2026-10-18.zip",
    "-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/octet-stream",
    "--data-binary",f"@{f}","--max-time","300"], capture_output=True, text=True, timeout=320)
if p.stdout.strip() not in ("200","201"): print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")
code, r = curl(f"/api/deposit/depositions/{nid}", "PUT", {"metadata": META})
if code != "200": print("FAIL meta", code, str(r)[:300]); sys.exit(1)
code, r = curl(f"/api/deposit/depositions/{nid}/actions/publish", "POST")
if code != "202": print("FAIL publish", code, str(r)[:300]); sys.exit(1)
print("PUBLISHED DOI:", r.get("doi"))
