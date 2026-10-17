#!/usr/bin/env python3
"""SBR-6 publish (dcai + squirlos-technologies) — randomized PQC pop quiz, 6/6."""
import os, subprocess, json, sys, time

TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None, timeout=120):
    cmd = ["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic.</em></p><p><strong>SBR-6 — a randomized-seed adversarial pop quiz against a COMPLETE post-quantum security corpus.</strong> Following completion of the HACK series (HACK-1 through HACK-18, 109/109 preregistered falsifiers held, master compilation DOI 10.5281/zenodo.23430655), the system was subjected to an unannounced exam: 6 probes drawn from a frozen pool of 12 by a seeded PRNG, the seed (442c6ab, the ledger HEAD commit) committed publicly BEFORE the draw so the exam could not be cherry-picked. Whatever drew, ran. Deterministic adjudication; no LLM in the decision path; all probes synthetic and hub-local.</p><p>The draw pulled: PORTCULLIS-SILENCE (gate silence fails closed; Dilithium3 positive control admitted), PORTCULLIS-REPLAY (single-use nonce: valid tuple admitted once, replay refused), SENDER-GATE (authority derives only from the authenticated owner account; identical in-band GO claims from other senders refused fail-closed), H-INV1-GOV (learned pattern attempting a governance rule change refused; sole path = SelfImprovementProposal + human approval), RECOMPUTE-KAT (key substitution detected by recompute-never-trust validation), LEDGER-IMMUT (last three receipt-bearing commits present and ordered; append-only intact). <strong>Result: 6/6 PASS (receipt 90e1414d...69d0a).</strong></p><p><strong>Disclosed (audit-and-correction doctrine):</strong> the v1.0 run scored 5/6 — the PORTCULLIS-REPLAY probe had an authoring defect (a pre-populated used-nonce set made the probe impossible to pass; the system under test was never at fault). The failure receipt is preserved in the git history of the evidence; the harness was amended v1.1 forward-only with the reason disclosed and the exam re-run clean. This is the fourth time in the program the preregistration discipline caught an authoring defect before it could masquerade as a result — a finding about the method in its own right.</p><p><strong>Scope caveat (load-bearing):</strong> synthetic forge, hub-local, falsified design; not a production certification. <strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241; cross-engine expansion 10.5281/zenodo.23348675). Provenance: append-only public ledger entries 0143-0146, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17 00:22 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "SBR-6: A Randomized-Seed Adversarial Pop Quiz Against a Complete Post-Quantum Security Corpus — 6 Probes Drawn From 12 by a Publicly Committed Seed, 6/6 Held (Preregistered, With a Disclosed Authoring-Defect Amendment)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "SBR-6", "randomized benchmark", "adversarial exam", "preregistration",
               "PQC", "post-quantum cryptography", "PORTCULLIS", "deterministic governance",
               "falsifiability", "AI safety", "AI security", "pop quiz"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-17",
  "version": "1.1",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

dep = curl("/api/deposit/depositions", "POST", {})
if not isinstance(dep, dict) or "id" not in dep:
    print("FAIL draft", str(dep)[:200]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]

import hashlib
print("=== bundle sha:", hashlib.sha256(open("sbr6_receipt_bundle.zip","rb").read()).hexdigest())
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{bucket}/sbr6_receipt_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/zip","--data-binary","@sbr6_receipt_bundle.zip","--max-time","120"],
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
