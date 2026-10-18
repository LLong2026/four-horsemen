#!/usr/bin/env python3
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic or owner-authored; no customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>Technical report formalizing seed mode for evidence receipts.</strong> Digest-only blockchain notarization proves existence but not possession: once an artifact is deleted it cannot be re-examined. For artifacts produced by a deterministic generator, this report closes the gap: the notarized value becomes a 32-byte generative seed from which any party can reconstruct the original byte-identically at any time — the hash is the artifact. Formalizes MHCN-3 dual-mode receipts (R11), generator pinning (R12), an information-theoretic domain-honesty rule (R13), a security-inversion rule (R14), and a seven-point pilot gate (R15). Reports two Bitcoin-anchored demonstrations (an 8,858-byte structured document and a 51,560-byte patent-citation artwork, U.S. Patent Application 19/693,343 cited publicly only), a disclosed-and-fixed first-mint rendering defect as a preregistration case study, and a public zero-trust browser examiner station where any visitor reconstructs the artifact from its published fingerprint and verifies the canonical hash locally. Extends MHCN-1 (DOI 10.5281/zenodo.23445938), the evidence stack (DOI 10.5281/zenodo.23446098), and the Council Session 04 review (DOI 10.5281/zenodo.23446655). Series No. 1 bundle: DOI 10.5281/zenodo.23447609.</p><p><strong>Dual Mesh Benchmark: MEASURED (scoped)</strong> — deterministic generators and hashes only; no neural-mesh inference in any result. Program benchmark: DOI 10.5281/zenodo.23321637 (DeepSeek column: DOI 10.5281/zenodo.23345241).</p><p>Try it: paste fingerprint <code>81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c</code> into the public Genesis Viewer hash drop (Deterministic Coding site, linked from the Squirl OS Vault Public Links page) and verify in your own browser.</p>"""
META = {"upload_type":"publication","publication_type":"technical_note",
 "title":"The Hash Is the Artifact: Dual-Mode Evidence Receipts with Seed-Reconstructed Originals, Notarized on the Bitcoin Blockchain",
 "creators":[{"name":"Long, Leon Calvin, II","affiliation":"SquirlOS Technologies LLC","orcid":"0000-0002-8893-7854"}],
 "description":DESC,
 "keywords":["seed mode","hash is the artifact","dual-mode receipts","MHCN-3","Bitcoin anchoring","OpenTimestamps","zero-trust verification","evidence receipts","tokenization","deterministic reconstruction","SQUIRL OS"],
 "license":"cc-by-4.0","publication_date":"2026-10-18","version":"1.0",
 "communities":[{"identifier":"dcai"},{"identifier":"squirlos-technologies"}]}
def curl(path, method="GET", body=None):
    cmd=["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd+=["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout
dep=curl("/api/deposit/depositions","POST",{})
nid=dep.get("id") if isinstance(dep,dict) else None
if not nid: print("FAIL draft",str(dep)[:200]); sys.exit(1)
p=subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",f"{dep['links']['bucket']}/hash_is_the_artifact_paper.zip","-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/octet-stream","--data-binary","@hash_is_the_artifact_paper.zip","--max-time","180"],capture_output=True,text=True,timeout=200)
if p.stdout.strip() not in ("200","201"): print("FAIL upload",p.stdout.strip()); sys.exit(1)
req=urllib.request.Request(f"{API}/api/deposit/depositions/{nid}",method="PUT",data=json.dumps({"metadata":META}).encode(),headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json"})
print("meta:",urllib.request.urlopen(req,timeout=60).status)
req2=urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish",method="POST",headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json"})
r=json.loads(urllib.request.urlopen(req2,timeout=60).read())
print("PUBLISHED DOI:",r.get("doi")); print("RECORD:",r.get("links",{}).get("record_html"))
