#!/usr/bin/env python3
"""DROPBOX-M1-001 — Zenodo publish (dcai + squirlos-technologies).
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

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail in the four-horsemen repository. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects.</em></p><p><strong>DROPBOX-M1-001: the first permanent mainnet seed drop.</strong> On Oct 18 2026, under preregistration M-DROP-1 (frozen BEFORE funding and broadcast, sha 95c322ea...785de), the 32-byte genesis seed of the Patent Genesis Series No. 1 artwork (filed provisional 19/693,343) was sealed into a 37-byte OP_RETURN on Bitcoin mainnet — tx <a href="https://mempool.space/tx/97d8cd38ecb37602aaa93363f4591c5c357721ff0cee9a80455fbc548a8a5b89">97d8cd38...a5b89</a>, CONFIRMED BLOCK 972023, total cost 790 sats of postage. A keyless reader (no keys, no wallet, no signing) pulled the seed straight off the blockchain, and the canonical v1.1 generator reconstructed the artwork from that chain-pulled seed byte-identically (SHA-256 3c130d66...de69, MATCH). The artwork now exists nowhere except 32 bytes on Bitcoin mainnet plus the generator — permanent, reconstructible by anyone, forever.</p><p><strong>This record documents a working reduction-to-practice of the seed-mode architecture</strong> (dual-mode evidence receipts; prior technical report DOI 10.5281/zenodo.23448010): transfer-only storage (delivers, retains nothing), binary verification (DELIVERED (D2) or not), postage-only economics (no monetary output, no token, no contract, no counterparty), writer-side-only key custody, deterministic payload (marker || version || seed). All six preregistered gates passed: G1 BIP-143 vector-proven signing (byte-exact vs the official Native P2WPKH test vector), G2 broadcast, G3 block confirmation (972023), G4 keyless chain-pull (pulled seed SHA-256 81d4a5cb...c456c, exact match to the target frozen in the prereg), G5 byte-identical reconstruction from the chain-pulled seed, G6 on-chain payload purity audit (OP_RETURN contains marker + version + seed only; no PII, no credentials, no customer data).</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Anyone can verify, three ways: (1) browser — pull the tx and reconstruct the artifact in the public Genesis Viewer (deterministic-code-dsos.base44.app/genesis-viewer, hash 81d4a5cb...c456c); (2) examiner — run the included keyless reader and generator on the included chain-pulled seed; (3) skeptic — re-implement from the spec: fetch the block, parse the OP_RETURN, hash what you find. Trustless by construction.</p><p>Provenance: prereg, frozen gates, runlog, and append-only ledger entries 0191/0192: <a href="https://github.com/LLong2026/four-horsemen">github.com/LLong2026/four-horsemen</a> (receipts/DROPBOX_M1_001_2026-10-18.md, dropbox/PREREG_M-DROP-1.md). Evidence bundle SHA-256: b0cf41f956ab475112e4a56371fa5ce5347f5472e2b6aa605894948b3422220a. Series: testnet4 proof-of-loop DROPBOX-T4-001 (ledger 0191); SIP-042 invariants (sha 25a45075); Patent Genesis Series No. 1 DOI 10.5281/zenodo.23447609. DCAI community: <a href="https://zenodo.org/communities/dcai">zenodo.org/communities/dcai</a>. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (chat authorization, 2026-10-18 ~11:40 CT).</p>"""

META = {
  "upload_type": "dataset",
  "title": "DROPBOX-M1-001: First Permanent Mainnet Seed Drop — Patent Genesis Artwork Reconstructed Byte-Identically From a Bitcoin OP_RETURN by a Keyless Reader (SIP-042, Preregistered, All Gates G1-G6 PASS)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["SQUIRL OS", "DROPBOX", "seed mode", "OP_RETURN", "Bitcoin",
               "keyless recovery", "reduction to practice", "seed-reconstructed originals",
               "the hash is the artifact", "deterministic", "preregistration",
               "falsifiability", "receipt-first"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-18",
  "version": "1.0",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}

code, dep = curl("/api/deposit/depositions", "POST", {})
if code != "201":
    print("FAIL draft", code, str(dep)[:300]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
bucket = dep["links"]["bucket"]
f = "DROPBOX_M1_EVIDENCE_BUNDLE.zip"
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
print("PUBLISHED DOI:", r.get("doi"))
