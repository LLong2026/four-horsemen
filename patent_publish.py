#!/usr/bin/env python3
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic; no customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>Patent Genesis Artifact — Series No. 1, tied to U.S. Patent Application No. 19/693,343 (programmable satoshi tokenization; public citation only).</strong> An original 51,560-byte blueprint artwork that exists nowhere as a stored file: it is fully determined by a 32-byte seed (SHA-256 81d4a5cb...) anchored to the Bitcoin blockchain via OpenTimestamps (digest-only; no tokens, wallets, or crypto-assets). Reconstruction was verified twice from independent runs: <strong>byte-identical, PNG SHA-256 4b4fbf0e...</strong> Same seed in, same art out — the hash is the artifact.</p><p><strong>This record also seals MHCN-3, the dual-mode evidence receipt spec (v0.3, pilot-ready):</strong> digest mode (existence only) and seed mode (existence + possession + reconstruction), with generator pinning (SBOM doctrine), an information-theoretic domain-honesty rule (seed mode applies only to generator-produced artifacts; no overclaiming), a security-inversion rule (never seed-anchor confidential artifacts), and a seven-point pilot gate. MHCN-3 extends MHCN-1 (DOI 10.5281/zenodo.23445938) and MHCN-2 v0.2 as amended by Council Session 04 (DOI 10.5281/zenodo.23446655).</p><p><strong>Scope and honesty:</strong> the generator in this bundle is a demonstrative artwork generator, not the patent's method; no invention method detail is disclosed (patent-then-publish doctrine). The patent is cited by public reference only. Reconstruction proves existence, possession, and byte-parity — not legal title, ownership, or truth (R9 legal non-assertion).</p><p><strong>Dual Mesh Benchmark: MEASURED (scoped)</strong> — this record documents a deterministic reconstruction demo and a spec; no neural-mesh inference was involved. Program benchmark: DOI 10.5281/zenodo.23321637 (DeepSeek column: DOI 10.5281/zenodo.23345241). Provenance: append-only ledger entries 0182-0183, github.com/LLong2026/four-horsemen. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-18 ~01:10 CT).</p>"""
META = {"upload_type":"dataset",
 "title":"Patent Genesis Artifact Series No. 1 + MHCN-3 Dual-Mode Evidence Receipt Spec: A Bitcoin-Anchored 32-Byte Seed Reconstructing a Byte-Identical Original (U.S. Patent Application 19/693,343, public citation)",
 "creators":[{"name":"Long, Leon Calvin, II","affiliation":"SquirlOS Technologies LLC"},{"name":"SquirlOS Technologies LLC","type":"ResearchGroup"}],
 "description":DESC,
 "keywords":["SQUIRL OS","seed mode","hash is the artifact","MHCN-3","dual-mode receipts","Bitcoin anchoring","OpenTimestamps","programmable satoshi","patent genesis","evidence receipts","tokenization"],
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
p=subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",f"{dep['links']['bucket']}/patent_genesis_bundle.zip","-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/octet-stream","--data-binary","@patent_genesis_bundle.zip","--max-time","180"],capture_output=True,text=True,timeout=200)
if p.stdout.strip() not in ("200","201"): print("FAIL upload",p.stdout.strip()); sys.exit(1)
req=urllib.request.Request(f"{API}/api/deposit/depositions/{nid}",method="PUT",data=json.dumps({"metadata":META}).encode(),headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json"})
print("meta:",urllib.request.urlopen(req,timeout=60).status)
req2=urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish",method="POST",headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json"})
r=json.loads(urllib.request.urlopen(req2,timeout=60).read())
print("PUBLISHED DOI:",r.get("doi")); print("RECORD:",r.get("links",{}).get("record_html"))
