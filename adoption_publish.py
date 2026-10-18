#!/usr/bin/env python3
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic; no customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>The complete, working stack for chain-anchored evidence — five deterministic services plus a four-part adoption program aimed at the tokenization field.</strong> This record publishes the full corpus built and adversarially tested in a single session: the STAMP / RECOVER / RECONCILE / GRAPH / BLOCK-TRACK anchor services (SIP-034..038, scripts included, runnable), the <strong>Examiner Mode</strong> (SIP-039) that compiles a zero-trust evidence file from live gate verdicts, and the tokenization adoption program: <strong>MHCN-2 draft</strong> (RWA evidence lifecycle receipts: event-time anchoring, authority chaining, redactable-artifact/provable-existence), <strong>EVM mirror concept</strong> (read-only Merkle-root bridge so smart contracts can verify Bitcoin anchors — no tokens, no custody; deployment gated on owner decisions, honestly recorded as not deployed), and <strong>SBOM anchoring with a working self-referential demo</strong> (an SPDX-2.3 SBOM of the stack, stamped on Bitcoin and admitted to the reconciliation gate).</p><p><strong>Provenance, disclosed in full:</strong> during assembly the reconciliation gate caught four genuine drift events (ledger advancing through sealed entries; the block registry rewriting itself tracking new receipts) — all absorbed by the certified-state mechanism, nothing deleted, nothing scrubbed — and the program's own ledger required one self-correction (entry 0174 claimed PASS while the gate returned FAIL; corrected in entry 0175 with the error left visible). The Examiner Mode's first output file faithfully recorded the FAIL verdict while the ledger claim was wrong — the tool being more honest than its operator is the strongest evidence this stack works. Conformance doctrine: claims without receipts are theater.</p><p><strong>Companion records:</strong> MHCN-1 standard DOI 10.5281/zenodo.23445938; chain-of-custody graph DOI 10.5281/zenodo.23445728; SBR-7 randomized audit DOI 10.5281/zenodo.23445803. <strong>Dual Mesh Benchmark status: NOT MEASURED in this record</strong> (no neural-mesh inference involved; deterministic services only); program benchmark DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241). <strong>Scope caveats (load-bearing):</strong> anchoring notarizes existence, not authority (PQC authority split retained; reference chain signatures are not post-quantum); MHCN-2 and the EVM mirror are sealed concepts, not deployed integrations; prototype software, no production warranty. Provenance: append-only public ledger entries 0168-0176, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17 ~23:31 CT).</p>"""
META = {
  "upload_type": "dataset",
  "title": "A Complete Hash-Anchoring Stack for AI Governance Evidence: STAMP/RECOVER/RECONCILE/GRAPH/BLOCK-TRACK Services, Zero-Trust Examiner Mode, and a Four-Part Tokenization-Field Adoption Program (MHCN-2 RWA Evidence, EVM Mirror, SBOM Anchoring)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "hash anchoring", "OpenTimestamps", "blockchain notarization", "AI governance",
               "chain of custody", "deterministic gates", "fail-closed", "examiner mode", "RWA tokenization",
               "SBOM", "software supply chain", "post-quantum cryptography", "evidence over tokens"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-18",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}
def curl(path, method="GET", body=None, timeout=120):
    cmd = ["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout
dep = curl("/api/deposit/depositions", "POST", {})
nid = dep.get("id") if isinstance(dep, dict) else None
if not nid: print("FAIL draft", str(dep)[:200]); sys.exit(1)
print("draft:", nid)
bucket = dep["links"]["bucket"]
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{bucket}/adoption_stack_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/octet-stream","--data-binary","@adoption_stack_bundle.zip","--max-time","180"],
    capture_output=True, text=True, timeout=200)
if p.stdout.strip() not in ("200","201"): print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")
req = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}", method="PUT",
    data=json.dumps({"metadata": META}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
print("meta:", urllib.request.urlopen(req, timeout=60).status)
req2 = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish", method="POST",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req2, timeout=60).read())
print("PUBLISHED DOI:", r.get("doi"))
print("RECORD:", r.get("links",{}).get("record_html"))
