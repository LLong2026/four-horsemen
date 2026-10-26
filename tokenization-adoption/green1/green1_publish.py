#!/usr/bin/env python3
"""Publish GREEN-1 (Trust Is the Pollutant) to Zenodo — new deposition."""
import os, subprocess, json, sys, urllib.request

TOKEN = os.environ["ZENODO_TOKEN"]; API = "https://zenodo.org"
PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GREEN1_PAPER_v1.0.pdf")
PDF_SHA = "c3adb09bd9d50a18e79cae253435446a49acd11ab56520fb74987ad99c8dca31"

DESC = """<p><strong>SQUIRL OS RESEARCH DISCLOSURE — READ FIRST:</strong> AI-assisted, receipt-first research program (open-book doctrine: audit-and-correction, versioned amendments, append-only public ledger). Errors are disclosed, not erased. <em>This software is a prototype and is provided for educational and research purposes only. It is not intended for production use, commercial deployment, or safety-critical environments. All payloads synthetic or owner-generated; no customer-identifiable data appears in this record (POL-DISC-001).</em></p><p><strong>"Trust Is the Pollutant: Witness Receipts, Content-Addressed Storage, and the Environmental Case Against Redundant Copies."</strong> Global data centres consumed ~415 TWh in 2024 (~1.5% of world electricity, IEA Energy and AI 2025), projected past 1,000 TWh by 2030 in the Base Case. Not all of that energy buys information; some of it buys reassurance: the same artifact is routinely held hot by many parties because no party can cheaply prove any other party's copy is unaltered. This paper separates storage redundancy into availability-driven duplication (legitimate, retained) and trust-driven duplication (mechanically removable), and reports the measured production cost floor of removing the trust component with chain-witnessed content addressing: a 3,377-file corpus folded to an 80-byte Merkle root (MCR-4, root 38089f07...e8daaa) tri-chain anchored on Bitcoin OP_RETURN, Stellar manage-data, and XRP memo; a three-way fractional ownership transfer (FRACTAL-2, doi:10.5281/zenodo.23655614) witnessed byte-exact on three mainnets for $0.2509 measured ($0.1254 at the 1 sat/vB trough); and ~1.9 cents per receipt amortized via weekly BTC batching (SOV-B1, doi:10.5281/zenodo.23628676). Verification is keyless — any browser, any public explorer, no account, no platform, no custodian. Honest scoping: receipts shrink copies, not bytes; the canonical copy must still exist and be retrievable; retrieval becomes a commodity market ("who serves this hash cheapest") and every provider can win. UK/EU resonance: NESO-scoped UK data-centre demand growing from 3.6 TWh/yr (2020) toward 13–35 TWh/yr by 2050, and Great Britain's demand-connection queue rising from 41 GW (Nov 2024) to ~125 GW (June 2025), make connection-efficient dedup a grid resource; witness-verified cold-tiering is a measurable, auditable net-zero reduction whose proof is publicly verifiable rather than self-attested.</p><p><strong>Scope and honesty:</strong> prior art disclosed — content-addressed storage is established (Git, BitTorrent Merkle pieces, IPFS, Venti and deduplicating-archival lineage). NOT claimed: inventing content addressing or dedup, or "fewer data centres" as a blanket prediction. Claimed (scoped): the measured cents-per-anchor tri-chain witness cost floor that makes custodian-free cross-party verification cheaper than the first guarded replica it displaces; the chain-as-witness architecture (doi:10.5281/zenodo.23649741) applied to shared-storage trust; the environmental framing of trust-driven duplication as purchased, avoidable energy; and receipts-first disclosure practice. The Section 5 savings illustration is labeled illustrative and scales with the true size of the trust-driven fraction, which this paper does not measure; the cost floor is measured. Dual Mesh Benchmark: MEASURED (scoped) — determinism receipts per doi:10.5281/zenodo.23321637; no LLM in any decision path. Provenance: append-only ledger, github.com/LLong2026/four-horsemen. Two-key curation: drafted and vetted by the system (Gabriel), published on the owner's explicit GO (Leon GO, chat authorization, 2026-10-26 00:34 CT).</p>"""

META = {"upload_type": "publication", "publication_type": "article",
 "title": "Trust Is the Pollutant: Witness Receipts, Content-Addressed Storage, and the Environmental Case Against Redundant Copies (SQUIRL OS GREEN-1)",
 "creators": [{"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
              {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"}],
 "description": DESC,
 "keywords": ["content-addressed storage", "witness receipts", "merkle mountain", "data centre energy",
              "deduplication", "post-quantum", "blockchain anchoring", "net zero", "green computing",
              "SQUIRL OS"],
 "license": "cc-by-4.0", "publication_date": "2026-10-26", "version": "1.0",
 "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}]}

def curl(path, method="GET", body=None):
    cmd = ["curl", "-s", "-X", method, f"{API}{path}", "-H", f"Authorization: Bearer {TOKEN}"]
    if body is not None: cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try: return json.loads(p.stdout)
    except Exception: return p.stdout

dep = curl("/api/deposit/depositions", "POST", {})
if isinstance(dep, dict) and "id" in dep:
    nid = dep["id"]; print("draft id:", nid)
else:
    print("FAIL draft:", str(dep)[:300]); sys.exit(1)

p = subprocess.run(["curl","-s","-o","/dev/null","-w","%{http_code}","-X","PUT",
    f"{dep['links']['bucket']}/GREEN1_PAPER_v1.0.pdf",
    "-H", f"Authorization: Bearer {TOKEN}",
    "-H","Content-Type: application/octet-stream",
    "--data-binary","@"+PDF,"--max-time","180"], capture_output=True, text=True, timeout=200)
if p.stdout.strip() not in ("200","201"): print("FAIL upload", p.stdout.strip()); sys.exit(1)
print("file uploaded")

req = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}", method="PUT",
    data=json.dumps({"metadata": META}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
print("meta status:", urllib.request.urlopen(req, timeout=60).status)

req2 = urllib.request.Request(f"{API}/api/deposit/depositions/{nid}/actions/publish", method="POST",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
r = json.loads(urllib.request.urlopen(req2, timeout=60).read())
print("PUBLISHED DOI:", r.get("doi"))
print("RECORD:", r.get("links", {}).get("record_html"))
json.dump({"doi": r.get("doi"), "record": r.get("links", {}).get("record_html"),
           "title": META["title"], "pdf_sha256": PDF_SHA, "deposit_id": nid,
           "published_at": "2026-10-26",
           "authorization": "Leon GO (chat authorization, 2026-10-26 00:34 CT)"},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "GREEN1_ZENODO_RECEIPT.json"), "w"), indent=1)
print("receipt saved")
