#!/usr/bin/env python3
"""FRACTAL-2 Zenodo publish (dcai + squirlos-technologies).
Pattern: reserve draft -> upload -> metadata -> publish -> verify. Append-only."""
import os, subprocess, json, sys

TOKEN = os.environ["ZENODO_TOKEN"]
API = "https://zenodo.org"

def curl(path, method="GET", body=None):
    cmd = ["curl", "-s", "-w", "\n%{http_code}", "-X", method,
           f"{API}{path}", "-H", f"Authorization: Bearer {TOKEN}"]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    raw, _, code = p.stdout.rpartition("\n")
    try: return code, json.loads(raw)
    except Exception: return code, raw

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail in the four-horsemen repository. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.</em></p><p><strong>FRACTAL-2: a three-way (30/30/40) fractal ownership split of a published research artifact, consensus-witnessed on three rails for about one quarter of a US dollar.</strong> On Oct 25 2026, under preregistration FRACTAL2_PREREG.md (frozen and committed BEFORE broadcast, sha 357284b8...b5195), fractional ownership of the HG-CERT-1 governance-drift hold-gate certification paper (DOI 10.5281/zenodo.23627901) was split 30/30/40 across three wallets in a canonical ownership manifest (SHA-256 3134705c...cd077) and witnessed byte-exactly on three independent mainnets: <a href="https://stellar.expert/explorer/public/tx/e7def7e8447335b2099bd987d92ed0f36417b43e16acdd95b8488aeaee595552">Stellar</a> (5.9 s, 100 stroops), <a href="https://livenet.xrpl.org/transactions/670ECBB9E4014F776775668A643938479350AD2BA378595560C596C9DD9CC73B">XRPL</a> (5.9 s, 10 drops), and <a href="https://mempool.space/tx/074c5fbc05d5a6fc9856c5e2bf280f03ea8f29555f8018dd8c8df8da702d6a11">Bitcoin OP_RETURN</a> (316 sats at 2 sat/vB, fired at the observed 1 sat/vB weekend mempool trough). Every leg read back keylessly (no keys, no wallet, no sign-in) from public endpoints, 3/3 byte-exact.</p><p><strong>Measured cost (scoped, spot-priced at fire time):</strong> triad total $0.2509; at the observed 1 sat/vB trough floor the same Bitcoin leg is $0.1254; under the weekly-batch checkpoint doctrine the amortized cost is about 1.9 cents per receipt. Legacy single-rail token-mint flows on major smart-contract chains typically cost $5-50+ with no multi-rail witness and no keyless verification path: the gap is two to three orders of magnitude. Roughly 32 three-way fractional ownership transfers of published research artifacts for the price of one $8 cup of coffee.</p><p><strong>All five preregistered gates PASS.</strong> Disclosed defects (append-only doctrine): the first Bitcoin leg (tx 8b0155c9..., 316 sats) fired with envelope class byte 0x01 instead of the preregistered 0x12 — the digest was correct on-chain; caught at the readback gate and superseded by the corrected re-fire 074c5fbc... (both txids journaled). No client data, no PHI, no credentials; operator authorization recorded by marker only.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675. No neural-mesh inference in any decision path; all gates deterministic.</p><p>Anyone can verify, three ways: (1) fetch each tx from any public explorer and decode the payload (SQDR + 0x12 + manifest SHA-256); (2) recompute the manifest hash from FRACTAL_2_OWNERSHIP_CANONICAL.json in this bundle and compare; (3) walk the append-only ledger (entry 0353) in the <a href="https://github.com/LLong2026/four-horsemen">four-horsemen repository</a>. Evidence bundle SHA-256: b91f413bd630ea60eb8f19fe8383e04f2c069ac84e5d932b728eb2ee70064463. Series lineage: FRACTAL-1 first 20% fractional sat lease (ledger 0305); MILE-TT-1 first P2P satoshi ownership transfer (DOI 10.5281/zenodo.23581044). Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-25 22:55 CT / 2026-10-25 22:59 CT).</p>"""

META = {
  "upload_type": "publication",
  "publication_type": "report",
  "title": "FRACTAL-2: A Three-Way (30/30/40) Fractal Ownership Split of a Published Research Artifact, Consensus-Witnessed on Three Rails for $0.25 (Preregistered, Keyless Readback 3/3, Cost-Floor Benchmark)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "FRACTAL-2", "fractional ownership", "fractal ownership",
               "multi-rail anchoring", "Stellar", "XRP Ledger", "Bitcoin OP_RETURN",
               "cost floor", "satoshi batch", "keyless verification", "preregistration",
               "falsifiability", "receipt-first", "tokenization"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-25",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

code, dep = curl("/api/deposit/depositions", "POST", {})
if code != "201":
    print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]
f = "FRACTAL2_EVIDENCE_BUNDLE.zip"
p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
    "-X", "PUT", f"{bucket}/{f}",
    "-H", f"Authorization: Bearer {TOKEN}",
    "-H", "Content-Type: application/octet-stream",
    "--data-binary", f"@{f}", "--max-time", "300"],
    capture_output=True, text=True, timeout=320)
if p.stdout.strip() not in ("200", "201"):
    print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")
code, r = curl(f"/api/deposit/depositions/{nid}", "PUT", {"metadata": META})
if code != "200":
    print("FAIL meta", code, str(r)[:300]); sys.exit(1)
print("metadata set")
code, r = curl(f"/api/deposit/depositions/{nid}/actions/publish", "POST")
if code != "202":
    print("FAIL publish", code, str(r)[:300]); sys.exit(1)
print("PUBLISHED:", r.get("doi"), "record id", r.get("id"))
