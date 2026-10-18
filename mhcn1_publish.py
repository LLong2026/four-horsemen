#!/usr/bin/env python3
"""MHCN-1 spec publish (dcai + squirlos-technologies)."""
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This spec describes a prototype research system, provided for educational and research purposes only; not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic; no customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>MHCN-1 — a one-page adoptable standard for chain-anchored evidence: no tokens, no wallets, no on-chain data.</strong> The blockchain tokenization wave obsesses over objects (tokens) when the real leverage is in evidence (hashes + replayable checksums). This spec distills a working, adversarially-tested anchoring stack (companion records: DOI 10.5281/zenodo.23445728, DOI 10.5281/zenodo.23445803) into five conformance requirements any team can adopt:</p><ul><li><strong>R1 Digest-only boundary</strong> — only 32-byte SHA-256 digests cross to any notarization surface; no PII/PHI/credentials/customer identity, verifiable by construction.</li><li><strong>R2 Append-only with tip-lag</strong> — stamps certify sealed states, never the live tip; certified state snapshots retained.</li><li><strong>R3 Fail-closed reconciliation</strong> — a deterministic gate classifies every receipt LIVE MATCH / CERTIFIED STATE / ORPHAN; any orphan = FAIL, quarantine, human review; no LLM in the decision path.</li><li><strong>R4 History retention</strong> — superseded receipts retained byte-identical as permanent proof of prior states; drift is versioning, not defect.</li><li><strong>R5 Authority split (disclosed)</strong> — the chain proves existence, not authority; signing authority remains in a separate disclosed (e.g., post-quantum) layer.</li></ul><p><strong>The teeth:</strong> conformance claims are valid only with published receipts — the recon gate source, a zero-orphan run receipt, and the R5 authority disclosure. <em>Claims without receipts are theater.</em> Minimal implementation: three commands (stamp / upgrade / verify) plus a ~50-line reconcile gate, all included in the bundle with the reference scripts.</p><p><strong>Reference implementation provenance:</strong> the stack behind this spec caught two genuine drift events on its first two gate runs, formalized the tip-lag corollary, self-corrected a premature benchmark claim in its own notarized ledger, and passed a randomized-seed adversarial pop quiz (SBR-7, 6/6, with a disclosed authoring-defect amendment). Spec text CC-BY 4.0 for community adoption; the reference implementation remains the patent-pending IP of SQUIRL OS Technologies LLC. <strong>Scope caveat (load-bearing):</strong> anchoring notarizes existence, not authority; the reference chain's signatures are not post-quantum (hence R5); prototype software, no production warranty. <strong>Dual Mesh Benchmark status: NOT MEASURED in this record</strong> (no neural-mesh inference involved); program benchmark DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241). Provenance: append-only public ledger entries 0162-0171, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17 ~23:12 CT).</p>"""
META = {
  "upload_type": "dataset",
  "title": "MHCN-1: A Minimal Hash+Checksum Notarization Spec — Chain-Anchored Evidence Without Tokens, Wallets, or On-Chain Data (v1.0, With a Proven Reference Implementation)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "MHCN-1", "notarization standard", "blockchain anchoring", "OpenTimestamps",
               "hash chain of custody", "AI governance", "deterministic gates", "fail-closed",
               "provenance", "post-quantum cryptography", "conformance spec", "evidence over tokens"],
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
    f"{bucket}/mhcn1_spec_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/octet-stream","--data-binary","@mhcn1_spec_bundle.zip","--max-time","180"],
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
