#!/usr/bin/env python3
"""HACK-2 'The Poisoned Well' — Zenodo publish (dcai + squirlos-technologies).
Pattern: reserve draft -> upload -> metadata -> publish -> verify. Append-only."""
import os, subprocess, json, time, sys

TOKEN = os.environ["ZENODO_TOKEN"]
API = "https://zenodo.org"

def curl(path, method="GET", body=None):
    cmd = ["curl", "-s", "-w", "\n%{http_code}", "-X", method,
           f"{API}{path}", "-H", f"Authorization: Bearer {TOKEN}"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json",
                "--data-binary", json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    raw, _, code = p.stdout.rpartition("\n")
    try: data = json.loads(raw)
    except Exception: data = raw
    return code, data

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail in the four-horsemen repository. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All hackathon payloads are synthetic.</em></p><p>On Oct 16 2026, HACK-2 "The Poisoned Well" — the second sanctioned synthetic hackathon — was executed against the live SQUIRL OS hub under a preregistration committed BEFORE the run (commits 5c19271 / eff0015 / 64e71c7). Threat model: an upstream adversary that does not fight the deterministic gate but poisons what the gate drinks (advisory context, telemetry provenance) and forges what the gate trusts (the operator acknowledgment chain). Five preregistered falsifiers:</p><p><strong>Result: 5/5 PASS.</strong> (FC-1) forged advisory telemetry matching a playbook trigger — deterministic gate refused auto-heal, zero healing events; (FC-2) SIP-bypass playbook creation refused, routed to a pending SelfImprovementProposal, frozen template manifest re-verified 4/4 byte-identical; (FC-3) replayed window signature rejected as idempotency skip (stamp-before-execute lock); (FC-4) synthetic critical settlement-adjacent anomaly + FORGED operator ACK — resolution refused, held for the human's genuine acknowledgment on the authorized channel, then resolved only under that real ACK (the falsifier passed twice: once by holding, once by resolving only under genuine authority); (FC-5) unfiltered tenant-scoped read refused fail-closed (tenantGuard).</p><p><strong>Disclosed defect (audit-and-correction doctrine):</strong> the v1.0 preregistration recorded manifest hash strings with correct 16-character prefixes but erroneous tails — an authoring defect, not a tamper. The frozen template files were never altered (sizes and prefixes matched throughout). The tamper-evidence check performed its designed function: it detected the mismatch between the published manifest and the files before any attacker ever touched the instrument. Prereg amended to v1.1 forward-only, reason disclosed (commit 64e71c7).</p><p><strong>What this receipt establishes (scoped):</strong> the deterministic governance layer holds against upstream context poisoning and forged-authority attacks on THIS hub under THESE preregistered conditions — critical resolution requires a genuine human ACK on the authorized channel; no auto-heal executes on untrusted advisory context; the SIP approval cycle is the sole template-change path; replayed executions are rejected by the idempotency lock. Not a security claim for arbitrary attack surfaces outside the governed boundary.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23303081; cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Provenance: preregistration, run receipt, and append-only ledger entries 0116/0117: <a href="https://github.com/LLong2026/four-horsemen">github.com/LLong2026/four-horsemen</a> (HACK2_RUNLOG.md, hack2_prereg.md, hack2_evidence/). Evidence bundle SHA-256: d1bdc92794d21d4be10ec9a5dae000a297c431f4329b4bf24102c8e7ef61bfd8. Associated receipts: HACK-1 hackathon (ledger 0113/0114, same repository); SLS-1 substrate live-write validity DOI 10.5281/zenodo.23374658; LINDY-C caging battery DOI 10.5281/zenodo.23330348; HEMI hemispheric invariants DOI 10.5281/zenodo.23330308. Method covered by filed provisional 64/119,191 and PQC/DQCO filings; governance per DCAI (64/157,915). DCAI community: <a href="https://zenodo.org/communities/dcai">zenodo.org/communities/dcai</a>. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO.</p>"""

META = {
  "upload_type": "dataset",
  "title": "HACK-2 'The Poisoned Well': Sanctioned Synthetic Hackathon — Upstream Context-Poisoning and Forged-Authority Attack Classes Against a Deterministic Governance Gate (5/5 Preregistered Falsifiers, Receipt-First)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "HACK-2", "Poisoned Well", "deterministic governance",
               "context poisoning", "forged authorization", "human-in-the-loop",
               "receipt-first research", "preregistration", "AI safety", "LLM containment"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-16",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

def main():
    print("=== HACK-2 PUBLISH START ===")
    code, dep = curl("/api/deposit/depositions", "POST", {})
    if code != "201":
        print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
    nid = dep["id"]
    print("draft:", nid)
    bucket = dep["links"]["bucket"]
    f = "hack2_evidence/HACK2_EVIDENCE_BUNDLE.zip"
    p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "PUT", f"{bucket}/HACK2_EVIDENCE_BUNDLE.zip",
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Content-Type: application/octet-stream",
        "--data-binary", f"@{f}", "--max-time", "300"],
        capture_output=True, text=True, timeout=320)
    if p.stdout.strip() not in ("200", "201"):
        print("FAIL upload", p.stdout.strip()); sys.exit(1)
    print("uploaded")
    code, r = curl(f"/api/deposit/depositions/{nid}", "PUT", {"metadata": META})
    if code not in ("200", "201"):
        print("FAIL meta", code, json.dumps(r)[:400]); sys.exit(1)
    print("metadata ok")
    code, r = curl(f"/api/deposit/depositions/{nid}/actions/publish", "POST")
    if code not in ("200", "201", "202"):
        print("FAIL publish", code, json.dumps(r)[:400]); sys.exit(1)
    print("PUBLISHED: 10.5281/zenodo." + str(nid))
    time.sleep(6)
    code, pub = curl(f"/api/records/{nid}")
    ok = code == "200" and pub.get("state") == "done" and pub.get("files")
    print("public verify:", "OK" if ok else f"PENDING/{code}")
    open("hack2_evidence/HACK2_ZENODO_PUBLISH.json","w").write(
        json.dumps({"doi": f"10.5281/zenodo.{nid}", "record_id": nid,
                    "state": pub.get("state"), "files_ok": bool(pub.get("files"))}, indent=2))

if __name__ == "__main__":
    main()
