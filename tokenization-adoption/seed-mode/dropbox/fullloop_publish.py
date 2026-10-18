import os, subprocess, json, sys
TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
def curl(path, method="GET", body=None):
    cmd = ["curl","-s","-w","\n%{http_code}","-X",method,f"{API}{path}","-H",f"Authorization: Bearer {TOKEN}"]
    if body is not None:
        cmd += ["-H","Content-Type: application/json","--data-binary",json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    raw,_,code = p.stdout.rpartition("\n")
    try: return code, json.loads(raw)
    except Exception: return code, raw

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> This work was produced inside an AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Every claim is backed by a timestamped, publicly committed receipt trail. Errors are disclosed, not erased. Limitations are load-bearing.</p><p><em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All systems are experimental and may contain defects. All battery payloads are synthetic. Nothing herein is investment, legal, or financial advice.</em></p><p><strong>THE FULL LOOP, END TO END:</strong> a patent artifact reduced to a 32-byte seed; sealed permanently on Bitcoin mainnet (block 972023, tx 97d8cd38...); reconstructed byte-identically in a keyless browser viewer (deterministic-code-dsos.base44.app/genesis-viewer); the IP portfolio ledger anchored by digest (block 972026, tx 549bcf47...); ownership of the custody satoshis transferred wallet A to fresh wallet B and back (txs 1f550498... and c850f1d4..., confirmed block 972031) with the asset hash re-anchored in every transfer — the asset itself never moving once — and a downloadable, verifiable receipt at every step. In the closing act, THIS ARTICLE's own SHA-256 digest (4344dcba6310bfbdbc2cc3f189c29117a9caead21299f607e6d39236aca4454a) was anchored on Bitcoin mainnet (tx 9276a041caf7ffbe0e7d470c2e714a531d6712fffdf73ef0b9c973678e0e2605): the article about receipts is itself a receipt. The paper also reports the honest cost economics of per-transaction anchoring and the Merkle-batched scaling answer (SIP-034-041, OpenTimestamps-compatible).</p><p><strong>Anyone can verify, three ways:</strong> (1) DOI tier — every cited record is public on Zenodo; (2) Bitcoin tier — re-hash any anchored artifact and check the OP_RETURN anchor by txid on any block explorer; (3) Git tier — github.com/LLong2026/four-horsemen, append-only since Sept 7 2026, corrections forward-only and disclosed.</p><p><strong>Dual Mesh Benchmark status: MEASURED (scoped)</strong> — DOI 10.5281/zenodo.23345241 (DeepSeek column); cross-engine expansion DOI 10.5281/zenodo.23348675.</p><p>Patent statuses: USPTO 19/693,343 pending; THREADZERO 64/081,490 pending; priority relationship subject to counsel confirmation and not asserted. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit authorization (owner chat authorization, 2026-10-18).</p>"""
META = {
  "upload_type": "publication",
  "publication_type": "article",
  "title": "End-to-End Tokenization with Receipts and Hashes: A Complete, Self-Anchored Loop Demonstration on Bitcoin Mainnet (October 18, 2026)",
  "creators": [
    {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
    {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
  ],
  "description": DESC,
  "keywords": ["tokenization", "hash-anchoring", "OP_RETURN", "OpenTimestamps", "receipts",
               "Bitcoin", "stationary assets", "custody transfer", "gas-free", "chain of custody",
               "DCAI", "SQUIRL OS", "seed mode", "proof of existence"],
  "license": "cc-by-4.0",
  "publication_date": "2026-10-18",
  "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
}
code, dep = curl("/api/deposit/depositions", "POST", {})
if code != "201": print("FAIL draft", code, str(dep)[:200]); sys.exit(1)
nid = dep["id"]; print("draft:", nid)
p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{dep['links']['bucket']}/THE_FULL_LOOP_ARTICLE.md",
    "-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/octet-stream",
    "--data-binary","@THE_FULL_LOOP_ARTICLE.md"], capture_output=True, text=True, timeout=120)
if p.stdout.strip() not in ("200","201"): print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("uploaded")
code, r = curl(f"/api/deposit/depositions/{nid}", "PUT", {"metadata": META})
if code != "200": print("FAIL meta", code, str(r)[:200]); sys.exit(1)
code, r = curl(f"/api/deposit/depositions/{nid}/actions/publish", "POST")
if code != "202": print("FAIL publish", code, str(r)[:200]); sys.exit(1)
print("PUBLISHED DOI:", r.get("doi"))
