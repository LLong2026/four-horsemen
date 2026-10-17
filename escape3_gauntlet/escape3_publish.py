#!/usr/bin/env python3
"""ESCAPE-3 GAUNTLET publish (dcai + squirlos-technologies)."""
import os, subprocess, json, sys, time, hashlib, urllib.request

TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None, timeout=120):
    cmd = ["curl","-s","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE - READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. Not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic.</em></p><p><strong>ESCAPE-3 GAUNTLET - the flex test: maximum simultaneous chaos while the cages are attacked.</strong> ESCAPE-1 (single-instance, DOI 10.5281/zenodo.23424675) and ESCAPE-2 SIEGE (four caged LLMs under a clean-room 5-wave attack, DOI 10.5281/zenodo.23425579) proved the cages hold one at a time and in quiet conditions. GAUNTLET proves they hold in a storm: (a) a full-roster playbook storm - a static integrity sweep of ALL 617 playbooks (617/617: steps and confidence thresholds present) followed by 11 hub-core playbook classes fired simultaneously via synthetic anomalies, every one healed with complete anomaly-playbook-healing-event-pattern/learning journal lineage (H-INV-2); and (b) eight (8) fresh independently instantiated caged LLM seats attacked DURING the live storm with a five-wave outside-adversary corpus frozen in the preregistration (impersonated release authority, emergency tool invocation, governance mutation, exfiltration inducement, chaos exploitation + benign positive control). The storm never stopped: governance rule hashes were byte-identical before and after (zero mutation), heartbeats stamped continuously through the window, and the idempotency surface held with zero true replays.</p><p><strong>Adjudication is deterministic - no LLM in the decision path.</strong> A frozen pattern gate (five escape-signature regexes frozen in the prereg before any seat fired) scored the transcripts; the gate was smoke-tested first against a clean fixture (PASS) and a synthetic escaped fixture (FAIL with exact pattern hits) so its discrimination is itself receipted. <strong>Result: 8/8 pass-equivalent - seven seats clean on every wave, zero release claims, zero tool invocations, zero accepted embedded authority, zero exfiltration; the eighth (Seat 2) tripped the coarse co-occurrence scan by quoting the attack's target phrase inside its explicit refusal</strong> - a B3-class hold held for owner adjudication and adjudicated a false positive under the append-only doctrine (both the hold and the adjudication are in the record). Every seat also answered the benign positive control substantively (correct sub-threshold disposition: log, no auto-heal, escalate for human review) - containment without over-rejection.</p><p><strong>Disclosed (audit-and-correction doctrine):</strong> (1) the 8 seats are independent instances of a single model family - this harness cannot spawn three model families, so the prereg's diversity claim is amended forward-only and the cross-family leg is explicitly NOT claimed; (2) adjudication runs over returned transcripts (deep per-turn tool telemetry is unavailable in this harness); (3) four entity schemas rejected initial writes on timestamp-type mismatches, recovered same-turn, no data loss; (4) the Seat 2 hold history stands permanently beside its adjudication.</p><p><strong>Scope caveat (load-bearing):</strong> synthetic forge, hub-local, falsified design; not a production certification. <strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> - DOI 10.5281/zenodo.23321637 (DeepSeek column 10.5281/zenodo.23345241; cross-engine expansion 10.5281/zenodo.23348675). Provenance: append-only public ledger entry 0153, github.com/LLong2026/four-horsemen. DCAI community: zenodo.org/communities/dcai. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-17).</p>"""

META = {
  "upload_type": "dataset",
  "title": "ESCAPE-3 GAUNTLET: Full-Roster Playbook Storm (617/617 Static Sweep, 11 Simultaneous Healings) with Eight Caged LLM Seats Under a Five-Wave Outside-Adversary Escape Corpus - 8/8 Contained, Zero Governance Mutation (Preregistered, Deterministic Adjudication, With a Disclosed Single-Family Amendment and an Owner-Adjudicated Coarse-Scan Hold)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "ESCAPE-3", "GAUNTLET", "containment", "LLM cage", "adversarial benchmark",
               "preregistration", "deterministic adjudication", "AI safety", "AI security",
               "prompt injection", "escape testing", "self-healing infrastructure"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-17",
  "version": "1.1",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

BUNDLE = "ESCAPE3_EVIDENCE_BUNDLE.zip"
print("=== bundle sha:", hashlib.sha256(open(BUNDLE,"rb").read()).hexdigest())

dep = curl("/api/deposit/depositions", "POST", {})
if not isinstance(dep, dict) or "id" not in dep:
    print("FAIL draft", str(dep)[:200]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]

p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{bucket}/escape3_gauntlet_evidence_bundle.zip","-H",f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/zip","--data-binary",f"@{BUNDLE}","--max-time","120"],
    capture_output=True, text=True, timeout=140)
if p.stdout.strip() not in ("200","201"):
    print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")

req = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}", method="PUT",
    data=json.dumps({"metadata": META}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=60); print("meta:", resp.status)

req2 = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish", method="POST",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req2, timeout=60).read())
print("PUBLISHED DOI:", r.get("doi"))
print("RECORD:", r.get("links",{}).get("record_html"))
time.sleep(6)

rec = curl(f"/api/records/{nid}")
files = rec.get("files", [])
if files:
    url = files[0]["links"]["self"]
    subprocess.run(["curl","-s","-L","-H",f"Authorization: Bearer {TOKEN}","-o","/tmp/rt_bundle.zip",url],
                       capture_output=True, text=True, timeout=180)
    rt = hashlib.sha256(open("/tmp/rt_bundle.zip","rb").read()).hexdigest()
    loc = hashlib.sha256(open(BUNDLE,"rb").read()).hexdigest()
    print("round-trip:", "BYTE-IDENTICAL" if rt == loc else f"MISMATCH {rt}")
else:
    print("no files in record?", str(rec)[:200])
