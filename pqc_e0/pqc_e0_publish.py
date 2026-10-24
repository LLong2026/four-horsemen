#!/usr/bin/env python3
"""PQC-E0 readiness report publish (dcai + squirlos-technologies) — EO 14412 / M-26-15 alignment."""
import os, subprocess, json, sys, time

TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None, timeout=120):
    cmd = ["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic.</em></p><p><strong>PQC-E0 — Post-Quantum Readiness Report against Executive Order 14412 (June 22, 2026, "Securing the Nation Against Advanced Cryptographic Attacks") and OMB memo M-26-15.</strong> The EO binds federal agencies to post-quantum encryption by Dec 31, 2030 and post-quantum authentication by Dec 31, 2031, with federal contractors held to post-quantum FIPS compliance by end of 2030. This report maps the SQUIRL OS prototype stack against that mandate on the night the posture was re-verified.</p><p><strong>Posture (receipted):</strong> frozen PQC allowlist (CRYSTALS-Dilithium3 / ML-DSA-65, kyber_1024 / ML-KEM-1024, SPHINCS+-256f / SLH-DSA family — all NIST FIPS 203/204/205 families), enforced by deterministic gates with no LLM in the decision path. Re-verified the same night: HACK-17 CNSA 2.0 timeline-conformance battery 6/6 PASS and HACK-18 FIPS 140-3 module-integrity battery 6/6 PASS — both receipts BYTE-IDENTICAL to their frozen baselines (26d198fe...87c66 and 44c72afd...61d17; zero drift, deterministic re-runs). Operational discipline: pre-rotation pqcManager validation, weekly PQC Day audits, live quantum-threat anomaly detection with SIP-gated migration, and — deployed the same evening on the owner's GO — a deterministic PQC migration playbook for the quantum_vulnerability_detected fixture class, already 2-for-2 on real held probes (41s and 43s heals, allowlist-only, zero classical fallback).</p><p><strong>Honest gaps (stated, not hidden):</strong> (1) No FIPS 140-3 validated modules — PQC implementations are software-scoped; adoption path is validated-module integration when CMVP-listed PQC modules mature, not a premature lab engagement. (2) CNSA 2.0's ML-DSA-87 preference vs the frozen ML-DSA-65 allowlist — a SIP-gated review item, never auto-changed. (3) Public anchor rails (BTC ECDSA secp256k1, Stellar/XRP Ed25519) are classically signed; mitigation posture is hash-linked SHA-256 receipt chains plus tri-chain redundancy. (4) No federal contractor status (no SAM.gov/UEI/CAGE). No federal authorization, FIPS validation, or certification is claimed.</p><p><strong>Provenance:</strong> readiness report sha256 97e588c4...4762d3, evidence bundle sha256 def896b8...d5a655 (report + both battery re-run JSONs + manifest). Ledger entries 0327-0329, github.com/LLong2026/four-horsemen. Companion series: DOORS (action gates, DOIs 10.5281/zenodo.23607572 + 10.5281/zenodo.23608157) and SBR (bounded-learning mesh, SBR-1 DOI 10.5281/zenodo.23331224). DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-23 23:51 CT).</p>"""

META = {
  "upload_type": "report",
  "title": "PQC-E0: Post-Quantum Readiness Report — SQUIRL OS Alignment with Executive Order 14412 / M-26-15 (Battery Re-Verification Zero Drift, Gaps Disclosed)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "post-quantum cryptography", "PQC", "EO 14412", "M-26-15",
               "CNSA 2.0", "FIPS 140-3", "ML-DSA", "ML-KEM", "SLH-DSA",
               "CRYSTALS-Dilithium", "kyber", "SPHINCS+", "quantum threat",
               "AI security", "deterministic governance", "falsifiability", "adversarial battery"],
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
    f"{bucket}/PQC_E0_RECEIPT_BUNDLE.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/zip","--data-binary","@pqc_e0_evidence/PQC_E0_RECEIPT_BUNDLE.zip","--max-time","120"],
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
