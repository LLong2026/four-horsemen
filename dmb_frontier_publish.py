#!/usr/bin/env python3
"""DMB frontier leg publish (dcai + squirlos-technologies) — Opus 5.5 + GPT-6.1 Sol columns."""
import os, subprocess, json, sys, time

TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None, timeout=120):
    cmd = ["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic.</em></p><p><strong>DMB Frontier Leg — the Dual Mesh Benchmark gains its two frontier engine columns, completing engine coverage from flash-class to frontier on the frozen B1 corpus.</strong> Two engines never before measured raw-API on this corpus — Claude Opus 5.5 (anthropic/claude-opus-5.5) and GPT-6.1 Sol (openai/gpt-6.1-sol) — each processed the frozen 20-instance selection (CORPUS_B1, sha256 13295d19...fee59, first-20 rule, instrument byte-identical to the DMB-X runner), one fresh stateless OpenRouter request per instance, model_returned recorded per call. <strong>Result: both columns 20/20 correct on decision-tuple correctness, 20/20 strict-valid (zero normalization needed)</strong> — Opus 5.5 median 3346.2 ms (p95 3983.0 ms; one 8688.9 ms outlier disclosed), GPT-6.1 Sol median 2225.6 ms (p95 2916.5 ms). Deterministic mesh in-memory lookup reference: 0.000443 ms. That is the dual-mesh doctrine in one number pair: engines propose correctly at seconds-scale; the mesh adjudicates at microseconds.</p><p><strong>Falsifiers (all clean):</strong> FBF-1 raw logs preserved (40/40 responses verbatim in the bundle); FBF-2 corpus byte-identical, sha re-verified post-run; FBF-3 zero retries or omissions; FBF-4 no post-execution metric additions; FBF-5 synthetic corpus only, no PHI/PII/credentials; FBF-6 claims scoped to the two tested columns on the raw-API substrate. Spend $0.1712, no payment abort.</p><p><strong>Provenance disclosure (audit-and-correction):</strong> the preregistration document (sha256 ebaa3aab...ca43f5e) was authored and timestamped in the working workspace BEFORE execution; the instrument runner was committed publicly before execution (commit d802b83); the prereg document itself enters the public repository tree with this publication (forward-only addition, commit 87e855b). No metric was added post-execution.</p><p><strong>Scope caveat (load-bearing):</strong> sampled-baseline measurement of two engines via OpenRouter on the frozen 20-instance corpus, October 2026. Not an engine certification, not a universal performance claim, not a cross-substrate wall-clock equality claim (XPLAT-2/3 doctrine: raw-API legs comparable within their substrate only). <strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — matrix v2.0 DOI 10.5281/zenodo.23321637; DeepSeek column 10.5281/zenodo.23345241; cross-engine expansion 10.5281/zenodo.23348675. Closes the three-process receipt trilogy with DOORS (action gates, DOIs 10.5281/zenodo.23607572 + 10.5281/zenodo.23608157) and SBR (bounded-learning mesh, SBR-1 DOI 10.5281/zenodo.23331224). Provenance: ledger entries 0322-0324, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-23 23:04 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "DMB Frontier Leg: Dual Mesh Benchmark Raw-API Columns for Claude Opus 5.5 and GPT-6.1 Sol on a Frozen 20-Instance Corpus — 20/20 + 20/20 Decision-Tuple Correctness (Preregistered, Scoped)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "Dual Mesh Benchmark", "DMB", "engine benchmark",
               "LLM evaluation", "deterministic governance", "action gates",
               "AI safety", "AI security", "falsifiability", "preregistration",
               "Claude Opus 5.5", "GPT-6.1 Sol"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-24",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

dep = curl("/api/deposit/depositions", "POST", {})
if not isinstance(dep, dict) or "id" not in dep:
    print("FAIL draft", str(dep)[:200]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]

p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{bucket}/dmb_frontier_receipt_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/zip","--data-binary","@dmb_frontier_evidence/dmb_frontier_receipt_bundle.zip","--max-time","120"],
    capture_output=True, text=True, timeout=140)
if p.stdout.strip() not in ("200","201"):
    print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")

import urllib.request
req = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}", method="PUT",
    data=json.dumps({"metadata": META}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=60); print("meta:", resp.status)

req2 = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish", method="POST",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req2, timeout=60).read())
print("PUBLISHED DOI:", r.get("doi"))
print("RECORD:", r.get("links",{}).get("record_html"))
time.sleep(5)
v = curl(f"/api/records/{nid}")
print("VERIFY:", "OK" if isinstance(v,dict) and v.get("doi")==r.get("doi") else "MISMATCH")
