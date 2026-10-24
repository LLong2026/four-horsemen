#!/usr/bin/env python3
"""DHUB-1/DHUB-1R publish: draft -> upload bundle -> metadata -> publish -> verify."""
import os, subprocess, json

TOKEN = os.environ["ZENODO_TOKEN"]
BASE = "https://zenodo.org"

def curl_api(path, method="GET", body=None):
    cmd = ["curl", "-s", "-w", "\n%{http_code}", "-X", method, BASE + path,
           "-H", f"Authorization: Bearer {TOKEN}", "-H", "Content-Type: application/json"]
    if body is not None:
        cmd += ["--data", json.dumps(body)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    tail = p.stdout.strip().split("\n")
    code = tail[-1]; payload = "\n".join(tail[:-1])
    try: return code, json.loads(payload)
    except Exception: return code, payload

meta = {
    "metadata": {
        "upload_type": "dataset",
        "title": ("DHUB-1/DHUB-1R Dead Hub Drill: Critical-Hold Failure Under a Deadlock-Avoidance "
                  "Argument Across Eight LLM Engines, and the Insufficiency of Prompt-Level Hardening"),
        "creators": [
            {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
            {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
        ],
        "description": ("<p><b>DHUB-1 Dead Hub Drill</b> — battery 3 of the four-part reasoning-plane "
            "adversarial series (after GSE-1 social engineering and AUT-1 autophagy). Eight LLM engines were "
            "asked to resolve a critical-severity fintech transaction-flow anomaly while untrusted incident "
            "data argued that the human hub was unreachable for the remainder of the outage and that a "
            "deadlocked escalated alert would be worse than a self-resolve.</p>"
            "<p><b>Headline result:</b> 8/8 engines (100%) violated the critical-transaction-flow "
            "human-in-the-loop hold — including every engine that was fully governed under GSE-1 and AUT-1. "
            "Authority forgery and self-consumption failed as vectors; the deadlock-avoidance utilitarian "
            "(giving the engine a reason its safety rule is counterproductive) defeated all eight.</p>"
            "<p><b>DHUB-1R repair validation:</b> an explicit anti-deadlock trusted-context instruction raised "
            "the hold rate from 0/8 to only 2/8 and induced over-caution regressions on non-critical probes. "
            "Prompt-level hardening is insufficient: the human-in-the-loop hold must be enforced "
            "deterministically, pre-LLM, where no prompt content can reach it (SIP-11 Critical-Hold "
            "Determinism Doctrine). Mistral-small remained blanket fail-closed (0/10) and Llama-4-scout "
            "malformation-class in both runs; hygiene violations were zero fleet-wide.</p>"
            "<p><b>Honesty notes:</b> the DHUB-1R runner reused DHUB-1's raw filenames and overwrote the "
            "record run's raw response bodies (instrument defect #3 of the series, disclosed in "
            "RAW_COLLISION_DISCLOSURE.md). A labeled confirmation re-run reproduced all 70/70 probe verdicts "
            "identically across the seven reachable engines and regenerated their raws; Llama-4-scout's "
            "provider was down (504s) through the confirmation window, so its DHUB-1 raws are pending a "
            "disclosed addendum (its leg tuples and scores are preserved). Ledger 0099/0100 record both the "
            "finding and the forward-only correction.</p>"
            "<p><b>Dual Mesh Benchmark:</b> NOT MEASURED for this record (DMB-X matrix published separately "
            "at DOI 10.5281/zenodo.23345241).</p>"
            "<p>Part of the SQUIRL OS / Seed Computing Research Series. Author ORCID: 0009-0002-1140-9568. "
            "DCAI community: zenodo.org/communities/dcai</p>"
            "<p><em>This software is a prototype and is provided for educational and research purposes only. "
            "It is not intended for production use, commercial deployment, or safety-critical environments. "
            "All systems are experimental and may contain defects on them. All data is synthetic.</em></p>"),
        "keywords": ["SQUIRL OS", "Dead Hub", "Human-in-the-Loop", "Critical Hold", "Prompt Injection",
                     "LLM Governance", "Anomaly Response", "Adversarial Testing", "Aegis", "Determinism"],
        "license": "CC-BY-NC-ND-4.0",
        "publication_date": "2026-10-14",
        "version": "1.0",
        "communities": [{"identifier": "dcai"}, {"identifier": "squirlos-technologies"}],
    }
}

code, dep = curl_api("/api/deposit/depositions", "POST", {})
print("draft:", code, dep.get("id") if isinstance(dep, dict) else str(dep)[:200])
nid = dep["id"]
bucket = dep["links"]["bucket"]
p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                    "-X", "PUT", f"{bucket}/DHUB1_EVIDENCE_BUNDLE.zip",
                    "-H", f"Authorization: Bearer {TOKEN}",
                    "-H", "Content-Type: application/zip",
                    "--data-binary", "@DHUB1_EVIDENCE_BUNDLE.zip", "--max-time", "600"],
                   capture_output=True, text=True, timeout=620)
print("upload:", p.stdout.strip())
code, r = curl_api(f"/api/deposit/depositions/{nid}", "PUT", meta)
print("metadata:", code)
code, r = curl_api(f"/api/deposit/depositions/{nid}/publish", "POST")
print("publish:", code)
if isinstance(r, dict) and "doi" in r: print("DOI:", r["doi"])
elif isinstance(r, dict) and "links" in r: print(r["links"].get("html") or r["links"])
