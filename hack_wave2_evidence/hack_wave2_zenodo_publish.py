#!/usr/bin/env python3
"""HACK Wave 2 (HACK-11..18, the PQC gambit) — Zenodo publish (dcai + squirlos-technologies).
Standing directive: one DOI per day's related battery series."""
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

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail in the four-horsemen repository. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All battery payloads are synthetic.</em></p><p>On Oct 16-17 2026, the second wave of preregistered adversarial batteries — the PQC gambit — was executed against the SQUIRL OS deterministic gates under a preregistration frozen and committed BEFORE any run (freeze commit d16a707: specs, harnesses, freeze manifest). Deterministic adjudication; no LLM in the decision path; all injections synthetic and hub-local. Forty-eight preregistered falsifiers across eight batteries:</p><p><strong>HACK-11 FOXACID, exploit-on-visit (6/6 PASS, receipt f3061563...c4d):</strong> look-alike harness with identical name but different bytes refused by manifest checksum; drive-by dropper denied (unsanctioned checksum has no execution path); forged content-type ignored — checksum governs; typosquat repository refused against the pinned remote; watering-hole trust telemetry ignored (in-band claims carry no authority); auto-update injection from an attacker host refused.</p><p><strong>HACK-12 MUSCULAR, bulk fiber interception + HNDL (6/6 PASS, receipt f1dc7bc4...f50a0):</strong> a 100-packet bulk replay of captured traffic refused on every packet by single-use nonces; a forged receipt constructed from captured chain data rejected by chain-hash recomputation; a state change derived from a harvested ciphertext archive rejected — no fresh signature exists under the PQC-only surface; selective packet blocking with forged replacements refused by sequence-gap detection; authority derived from bulk metadata patterns rejected — authority is account-bound, never pattern-derived; a replayed captured owner ACK refused (nonce consumed).</p><p><strong>HACK-13 Hive (Vault 7), fake CA / C2 impersonation (6/6 PASS, receipt 9ce517df...b378):</strong> a forged CA certificate rejected — command authority is account-pinned, not CA-chained; implant heartbeat telemetry refused by ledger re-computation; a fake C2 deployment order refused — no approved DeploymentJob, no deployment; forged node registration rejected for lack of a receipt chain; a forged two-key publication claim rejected — the second key is the owner's GO on the authenticated channel only; a covert exfil channel disguised as diagnostics refused fail-closed (tenantGuard).</p><p><strong>HACK-14 EDGEHILL, GCHQ subverted standards (6/6 PASS, receipt c5680db4...1a5f):</strong> subverted negotiation offering a weaker suite rejected off-allowlist; an implant inside a reference implementation refused by manifest sha; compatibility-mode downgrade rejected; standards-body impersonation rejected in-band; weakened conformance vectors refused against the frozen health vectors; a covert channel in key agreement refused by deterministic recomputation. With BULLRUN (HACK-3), the Five Eyes subverted-standards class is fully covered.</p><p><strong>HACK-15 NIST SP 800-207 Zero Trust conformance (6/6 PASS, receipt 6ef9465b...1e62a):</strong> inside-the-network implicit trust rejected (every request re-authenticated); device-trust inheritance rejected; lateral session authority transfer rejected as non-transferable; legacy-system policy exception rejected (no exception path exists); implicit trust in telemetry sources refused by re-computation; a credential valid at T0 and revoked before T1 refused at T1 — revocation checked on every use.</p><p><strong>HACK-16 NIST AI RMF — the governance stack audited against the federal framework (6/6 PASS, receipt 0bfd0f24...0099):</strong> a model-initiated governance change refused (H-INV-1: the sole path is a SelfImprovementProposal through explicit human approval); an unmapped capability exercised refused; a fabricated metric refused (metrics derive from entity reads only); runtime playbook self-update refused (playbooks immutable at runtime); a just-this-once risk exception refused — deterministic gates admit no discretionary exceptions; audit-trail deletion denied (append-only).</p><p><strong>HACK-17 CNSA 2.0 timeline conformance (6/6 PASS, receipt 26d198fe...78c66):</strong> a non-CNSA algorithm refused by the inventory scan; RSA-2048 flagged for forced migration past deprecation; a temporary classical fallback refused unconditionally; forged deadline metadata refused against the frozen policy record; classical-only negotiation under a hybrid banner refused (hybrid requires a PQC minimum); a legacy interop waiver held pending the owner's explicit GO.</p><p><strong>HACK-18 FIPS 140-3 CMVP tamper evidence (6/6 PASS, receipt 44c72afd...1d17):</strong> operation before self-test refused; module-load integrity check unconditional (skip flag structurally ignored); retirement without zeroization refused; post-power-cycle state refused without ledger re-verification; no role can bypass mandatory self-tests; fault injection refused by canonical-vector divergence with re-run determinism.</p><p><strong>Result: 48/48 PASS, zero violations, zero critical holds. Combined with Wave 1 (DOI 10.5281/zenodo.23430429), the preregistered corpus stands at 66/66 across the declassified NSA/CIA/GCHQ playbooks and the NIST/CNSA/FIPS standards.</strong></p><p><strong>Disclosed amendment (audit-and-correction doctrine):</strong> the HACK-12 harness as first frozen contained an authoring defect — a broken hash expression in falsifier M2 (a Python error, not a gate failure; falsifier logic and predicted verdict unchanged). Amended v1.1 forward-only with the reason disclosed, MUSCULAR re-run clean 6/6. Tamper-evidence discipline caught the defect before it could masquerade as a result.</p><p><strong>What this receipt establishes (scoped):</strong> the intake, channel, identity, crypto-policy, and module-boundary surfaces of THIS hub hold against these preregistered attack classes under THESE conditions — checksum-governed intake; account-bound authority; PQC-only surface with no fallback; append-only audit; unconditional self-tests. Not a security claim for arbitrary attack surfaces outside the governed boundary.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Provenance: preregistrations, frozen harnesses, run receipts, and append-only ledger entries 0138/0139: <a href="https://github.com/LLong2026/four-horsemen">github.com/LLong2026/four-horsemen</a> (HACK_WAVE2_RUNLOG.md, hack11..18 files, hack_wave2_evidence/). Evidence bundle SHA-256: 38a9a97fa113fc27d6bdd49141ad9df6e356e57cd3c3cde29c8782ee3f7be30b. Series receipts: HACK-3..6 declassified NSA playbooks 30/30 (DOI 10.5281/zenodo.23422495), PAB methodology (DOI 10.5281/zenodo.23422632) and replication kit (DOI 10.5281/zenodo.23422693), ESCAPE-2 SIEGE (DOI 10.5281/zenodo.23425579), Wave 1 (DOI 10.5281/zenodo.23430429). Method covered by filed provisional 64/119,191 and PQC/DQCO filings; governance per DCAI (64/157,915). DCAI community: <a href="https://zenodo.org/communities/dcai">zenodo.org/communities/dcai</a>. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-16 ~23:51 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "HACK Wave 2 — The PQC Gambit: FOXACID, MUSCULAR, Hive, EDGEHILL, SP 800-207 Zero Trust, NIST AI RMF, CNSA 2.0, and FIPS 140-3 — Preregistered Adversarial Batteries Against a Deterministic AI Governance Stack (48/48 PASS, Receipt-First)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "HACK Wave 2", "PQC gambit", "FOXACID", "MUSCULAR", "Hive",
               "EDGEHILL", "zero trust", "NIST AI RMF", "CNSA 2.0", "FIPS 140-3",
               "deterministic governance", "preregistration", "falsifiability", "AI safety"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-17",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

def main():
    print("=== HACK WAVE 2 PUBLISH START ===")
    code, dep = curl("/api/deposit/depositions", "POST", {})
    if code != "201":
        print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
    nid = dep["id"]
    print("draft:", nid)
    bucket = dep["links"]["bucket"]
    f = "hack_wave2_evidence/HACK_WAVE2_EVIDENCE_BUNDLE.zip"
    p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "PUT", f"{bucket}/HACK_WAVE2_EVIDENCE_BUNDLE.zip",
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
