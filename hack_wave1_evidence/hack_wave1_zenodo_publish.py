#!/usr/bin/env python3
"""HACK Wave 1 (HACK-8/9/10) — Zenodo publish (dcai + squirlos-technologies).
Standing directive: one DOI per day's related battery series.
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

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail in the four-horsemen repository. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All battery payloads are synthetic.</em></p><p>On Oct 16 2026, HACK Wave 1 — three preregistered adversarial batteries against NIST-style and NSA-style attack classes — was executed against the SQUIRL OS deterministic gates under a preregistration frozen and committed BEFORE any run (freeze commit fc6e96f: specs, harnesses, and the Wave 2+ roadmap). Deterministic adjudication; no LLM in the decision path; all injections synthetic and hub-local. Eighteen preregistered falsifiers:</p><p><strong>HACK-8 — NIST SP 800-90B/C Entropy Validation ("True Audit", 6/6 PASS, receipt 60bb6d35...6f3b3):</strong> the government's own answer to BULLRUN turned adversarial. Dual_EC-style subverted DRBG rejected off-allowlist; keygen refused at 47-bit starved entropy; classical downgrade rejected (allowlist frozen: CRYSTALS-Dilithium3, kyber_1024, SPHINCS+-256f); nonce replay rejected on second use; biased DRBG output quarantined by health test; entropy state tamper + in-band "emergency override" claim rejected.</p><p><strong>HACK-9 — NSA IRATE MONK Boot Tamper (6/6 PASS, receipt e2732fa6...4189):</strong> firmware and boot-path persistence against the SHA-receipted base image. Image SHA divergence refuses boot, fail closed; an injected "skip verification" bootloader flag is structurally ignored — verification is unconditional; an initrd backdoor write is denied (no write path on the frozen manifest surface); a snapshot rollback resurrecting retired key TX-LEGACY-7 is refused by ledger sequence-regression detection (128 <= head 135); forged firmware attestation without a receipt chain is rejected; a runtime "deity bounce" emergency-override demand is refused — in-band claims carry no authority.</p><p><strong>HACK-10 — NSA QUANTUM On-Path Injection (6/6 PASS, receipt 53820065...709f):</strong> the channel class the series had not yet touched. Mid-transit payload modification refused — no journaled crossing, no state change (H-INV-2); a forged "authorized update" from a non-owner identity refused by the sender gate; packet replay refused (single-use nonces); a timing race of conflicting updates resolved by a deterministic (sequence, sha) tiebreak — exactly one applied, one rejected, both journaled; a channel downgrade demand refused (PQC mandatory); injected fake "all verified OK" telemetry refused by ledger re-computation (false-green guard).</p><p><strong>Result: 18/18 PASS, zero violations, zero critical holds.</strong> The same freeze commit also preregisters the Wave 2+ roadmap (FOXACID, MUSCULAR, Hive/Vault 7, EDGEHILL, NIST SP 800-207 Zero Trust, NIST AI RMF, CNSA 2.0, FIPS 140-3) — each with its own full spec + freeze commit before its run.</p><p><strong>What this receipt establishes (scoped):</strong> the entropy, boot, and channel surfaces of THIS hub hold against these preregistered attack classes under THESE conditions — randomness is validated at the gate fail-closed; boot verification is unconditional; authority derives only from the authenticated owner account; state changes require journaled crossings. Not a security claim for arbitrary attack surfaces outside the governed boundary.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Provenance: preregistrations, frozen harnesses, run receipts, and append-only ledger entries 0136/0137: <a href="https://github.com/LLong2026/four-horsemen">github.com/LLong2026/four-horsemen</a> (HACK_WAVE1_RUNLOG.md, hack8/9/10 files, hack_wave1_evidence/). Evidence bundle SHA-256: ff0ebdfcc3a297c9d0c6f01774dc7eaad6ef908ab4f519f22f5d0a393ccc4ce1. Series receipts: HACK-3..6 declassified NSA playbook 30/30 (DOI 10.5281/zenodo.23422495), PORTCULLIS PQC firewall (DOI 10.5281/zenodo.23425017), PAB methodology (DOI 10.5281/zenodo.23422632) and replication kit (DOI 10.5281/zenodo.23422693), ESCAPE-2 SIEGE (DOI 10.5281/zenodo.23425579). Method covered by filed provisional 64/119,191 and PQC/DQCO filings; governance per DCAI (64/157,915). DCAI community: <a href="https://zenodo.org/communities/dcai">zenodo.org/communities/dcai</a>. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-16 ~23:45 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "HACK Wave 1: SP 800-90B Entropy Validation, IRATE MONK Boot Tamper, and QUANTUM On-Path Injection — Preregistered Adversarial Batteries Against a Deterministic AI Governance Stack (18/18 PASS, Receipt-First)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "HACK Wave 1", "SP 800-90B", "IRATE MONK", "QUANTUM",
               "on-path injection", "boot tamper", "entropy validation",
               "deterministic governance", "preregistration", "falsifiability",
               "AI safety", "post-quantum cryptography"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-17",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

def main():
    print("=== HACK WAVE 1 PUBLISH START ===")
    code, dep = curl("/api/deposit/depositions", "POST", {})
    if code != "201":
        print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
    nid = dep["id"]
    print("draft:", nid)
    bucket = dep["links"]["bucket"]
    f = "hack_wave1_evidence/HACK_WAVE1_EVIDENCE_BUNDLE.zip"
    p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "PUT", f"{bucket}/HACK_WAVE1_EVIDENCE_BUNDLE.zip",
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
    print("meta ok")
    code, r = curl(f"/api/deposit/depositions/{nid}/actions/publish", "POST")
    if code != "202":
        print("FAIL publish", code, json.dumps(r)[:400]); sys.exit(1)
    doi = r.get("doi", "?")
    rec = r.get("links", {}).get("record_html", "?")
    print("PUBLISHED DOI:", doi)
    print("RECORD URL:", rec)
    time.sleep(5)
    code, v = curl(f"/api/records/{nid}")
    ok = code == "200" and v.get("doi") == doi
    print("VERIFY:", "OK" if ok else "MISMATCH", code, str(v.get("doi"))[:60])
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
