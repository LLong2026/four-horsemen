#!/usr/bin/env python3
"""SIP-034..037 chain-of-custody graph publish (dcai + squirlos-technologies)."""
import os, subprocess, json, sys, time, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic. No customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>A deterministic chain-of-custody graph binding an AI governance corpus to the Bitcoin blockchain — with self-healing re-anchoring and fail-closed reconciliation.</strong> While the 'everything on chain' wave puts data and logic on-chain, this record documents the opposite design: an append-only AI governance corpus (ledger, monitoring feed, preregistrations, receipts) whose integrity is notarized by Bitcoin proof-of-work via OpenTimestamps — <strong>only 32-byte SHA-256 digests cross the boundary; no tokens, wallets, or non-digest data touch any chain</strong>, and cryptographic authority remains in a separate post-quantum layer (CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f; the existence/authority split is disclosed by design).</p><p><strong>The novel contribution is the closed loop.</strong> Three deterministic services (no LLM in any decision path): STAMP (hash-only notarization, dual-calendar redundancy), RECOVER (drift detection with automatic re-anchoring that retires superseded stamps to history as retained proof — never deleted), and RECONCILE (a fail-closed gate classifying every receipt as LIVE MATCH / CERTIFIED STATE / ORPHAN). Benchmarking the gate against its own live ledger caught <strong>two genuine drift events on its first two runs</strong>, the second revealing a structural property we formalize as the <strong>tip-lag corollary</strong> (INV-1-C): an append-only log's tip is always ahead of its most recent stamp — mirroring Bitcoin checkpoint semantics — solved with certified state snapshots so every receipt reconciles deterministically.</p><p><strong>Disclosed self-correction (audit-and-correction doctrine):</strong> a benchmark-PASS claim was sealed in ledger entry 0165 <em>before</em> the gate returned; the gate returned FAIL. Entry 0166 corrects the record — premature claim disclosed, root cause structural, fix disclosed, nothing scrubbed — and the correction is itself an entry in the notarized ledger. Final verdict: PASS — 3/3 live and certified receipts matched, 1 historical retained, 0 orphans.</p><p><strong>Scoped novelty claim:</strong> hash-anchoring itself is established prior art (OpenTimestamps, RFC 3161, Chainpoint, Proof of Existence — cited, not claimed). To our knowledge, this is the first reported end-to-end automated chain-of-custody system for an AI governance corpus integrating hash-only PoW notarization, deterministic drift re-anchoring with historical retention, fail-closed reconciliation gating, and a disclosed self-correction of its own benchmark record. Independent verification trusts no party: <code>pip install opentimestamps-client; ots upgrade; ots verify</code>.</p><p><strong>Scope caveat (load-bearing):</strong> anchoring notarizes existence, not authority; Bitcoin's signatures are not post-quantum (hence INV-4). Prototype software; all payloads synthetic. <strong>Dual Mesh Benchmark status: NOT MEASURED in this record</strong> (no neural-mesh inference involved); program benchmark DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241). Provenance: append-only public ledger entries 0162-0166, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17, 22:23-22:50 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "A Deterministic Chain-of-Custody Graph for an AI Governance Corpus: Bitcoin Hash-Anchoring, Self-Healing Re-Anchoring, and Fail-Closed Reconciliation — With Two Live Drift Catches and a Disclosed Self-Correction (SIP-034..037)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "chain of custody", "blockchain anchoring", "OpenTimestamps", "Bitcoin",
               "hash notarization", "AI governance", "deterministic gates", "self-healing systems",
               "append-only ledger", "fail-closed reconciliation", "post-quantum cryptography",
               "transparency", "preregistration"],
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
if not isinstance(dep, dict) or "id" not in dep:
    print("FAIL draft", str(dep)[:200]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{bucket}/chain_of_custody_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/octet-stream","--data-binary","@chain_of_custody_bundle.zip","--max-time","180"],
    capture_output=True, text=True, timeout=200)
if p.stdout.strip() not in ("200","201"):
    print("FAIL upload", p.stdout.strip()); sys.exit(1)
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
