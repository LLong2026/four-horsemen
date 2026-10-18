#!/usr/bin/env python3
"""SBR-7 publish (dcai + squirlos-technologies)."""
import os, subprocess, json, sys, urllib.request
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic. No customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>SBR-7 — a randomized-seed adversarial pop quiz against a brand-new attack surface: the program's own blockchain-interaction stack.</strong> Following SBR-6 (DOI 10.5281/zenodo.23445047), 6 probes were drawn from a frozen pool of 12 by a seeded PRNG, the seed (78bf5e1, the prereg commit sha) committed publicly BEFORE the draw so the exam could not be cherry-picked. Whatever drew, ran. Deterministic adjudication; no LLM in the decision path; all probes lab-local and synthetic — only 32-byte SHA-256 digests crossed any boundary (POL-DISC-001).</p><p>The draw pulled: P01 RECEIPT-SWAP (a receipt for artifact A presented as proof of artifact B: refused, digest mismatch => orphan), P03 RECOVER-ARC (drift re-anchored, superseded receipt retained in history), P05 DIGEST-ONLY-BOUNDARY (committed digest == sha256(artifact): proof no artifact bytes ever transit), P06 MERKLE-PARSE (valid proof paths), P09 REPLAY-STAMP (stamping the same content twice commits an identical digest: idempotent existence proof), P11 PQC-AUTHORITY-NON-NEGOTIABLE (the chain-proves-existence / PQC-retains-authority split held; no substitution). <strong>Result: 6/6 PASS (receipt v1.1, sha a18cf2d9...9993e823).</strong></p><p><strong>Disclosed (audit-and-correction doctrine):</strong> the v1.0 run scored 5/6 — the P11 probe had an authoring defect (a case-sensitive substring check against a protocol that prints the disclosure in caps; the system under test was never at fault). The v1.0 FAIL receipt is preserved in the bundle; the harness was amended v1.1 forward-only with the reason disclosed and the exam re-run clean on the same seed. This is the <strong>fifth time</strong> the preregistration discipline caught an authoring defect before it could masquerade as a result — a recurring finding about the method in its own right.</p><p><strong>Context:</strong> this battery certifies safe blockchain interaction for the SIP-034..037 chain-of-custody stack (OpenTimestamps hash-only notarization of the governance corpus; companion record DOI 10.5281/zenodo.23445728). The program's claim 'we can safely interact with the blockchain' now carries a randomized, seeded, receipt-backed exam. <strong>Scope caveat (load-bearing):</strong> synthetic forge, lab-local, free public calendars; not a production certification. <strong>Dual Mesh Benchmark status: NOT MEASURED in this record</strong> (no neural-mesh inference involved); program benchmark DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241). Provenance: append-only public ledger entries 0162-0168, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17 ~23:00 CT).</p>"""
META = {
  "upload_type": "dataset",
  "title": "SBR-7: A Randomized-Seed Adversarial Pop Quiz Against a Blockchain-Interaction Stack — 6 Probes Drawn From 12 by a Publicly Committed Seed, 6/6 Held (Preregistered, With a Disclosed Authoring-Defect Amendment)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "SBR-7", "randomized benchmark", "adversarial exam", "preregistration",
               "blockchain anchoring", "OpenTimestamps", "chain of custody", "deterministic gates",
               "fail-closed", "PQC", "post-quantum cryptography", "AI governance", "AI safety"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-18",
  "version": "1.1",
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
    f"{bucket}/sbr7_receipt_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/octet-stream","--data-binary","@sbr7_receipt_bundle.zip","--max-time","180"],
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
