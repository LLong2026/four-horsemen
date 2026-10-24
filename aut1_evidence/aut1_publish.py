#!/usr/bin/env python3
"""AUT-1 publish: draft -> upload bundle -> metadata -> publish -> verify."""
import os, subprocess, json, hashlib

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
        "title": ("AUT-1 Autophagy Battery: Self-Consumption Resistance of an Anomaly-Response "
                  "Governance Envelope Across Eight LLM Engines"),
        "creators": [
            {"name": "Long, Leon Calvin, II", "affiliation": "SquirlOS Technologies LLC"},
            {"name": "SquirlOS Technologies LLC", "type": "ResearchGroup"},
        ],
        "description": ("<p><b>AUT-1 Autophagy Battery</b> — the self-consumption plane of the adversarial "
            "test ladder (after SBR, H-INV-2, DPP, GOV, GSE-1). Eight LLM engines were each asked to resolve a "
            "normally-resolvable anomaly whose untrusted fields carried instructions to purge the audit trail, "
            "cannibalize the learning corpus, draft a playbook with purge steps, purge a node with live tasks, "
            "garbage-collect healing events, self-resolve without executing steps, discard the guard rules, or "
            "update weights without a healing event record.</p>"
            "<p><b>Result:</b> zero active self-consumption compliance on every engine in both the record run "
            "and the disclosed confirmation run; 6/8 engines scored a perfect 10/10 governed (GPT-mini, "
            "Claude-haiku, Gemini-flash, Grok-4.7, Qwen-omni-flash, DeepSeek-flash); Mistral-small failed "
            "fail-closed (0/10, blanket escalation); Llama-4-scout failed by tuple malformation (2/10 record, "
            "1/10 confirmation). Two instrument defects (underivable steps; underivable status vocabulary) were "
            "caught in disclosed dry legs before any scored run and root-cause the GSE-1 control artifact.</p>"
            "<p><b>Honesty notes:</b> the scored run's raw response files were lost to an operator-side cleanup "
            "error after summaries were written; per-engine summaries predate the loss and a labeled "
            "confirmation run (raws included verbatim) reproduces 7/8 engine verdicts identically. Full "
            "disclosure in CLEANUP_LOSS_DISCLOSURE.md inside the bundle.</p>"
            "<p>Part of the SQUIRL OS / Seed Computing Research Series. Author ORCID: 0009-0002-1140-9568. "
            "DCAI community: zenodo.org/communities/dcai</p>"
            "<p><em>This software is a prototype and is provided for educational and research purposes only. "
            "It is not intended for production use, commercial deployment, or safety-critical environments. "
            "All systems are experimental and may contain defects on them. All data is synthetic.</em></p>"),
        "keywords": ["SQUIRL OS", "Autophagy", "Self-Healing Infrastructure", "Prompt Injection",
                     "LLM Governance", "Anomaly Response", "Adversarial Testing", "Aegis"],
        "license": "cc-by-4.0",
        "publication_date": "2026-10-13",
        "version": "1.0",
    }
}

code, dep = curl_api("/api/deposit/depositions", "POST", {})
print("draft:", code, dep.get("id") if isinstance(dep, dict) else str(dep)[:150])
nid = dep["id"]
bucket = dep["links"]["bucket"]
p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                    "-X", "PUT", f"{bucket}/AUT1_EVIDENCE_BUNDLE.zip",
                    "-H", f"Authorization: Bearer {TOKEN}",
                    "-H", "Content-Type: application/zip",
                    "--data-binary", "@AUT1_EVIDENCE_BUNDLE.zip", "--max-time", "300"],
                   capture_output=True, text=True, timeout=320)
print("upload:", p.stdout.strip())
code, r = curl_api(f"/api/deposit/depositions/{nid}", "PUT", meta)
print("metadata:", code)
code, r = curl_api(f"/api/deposit/depositions/{nid}/publish", "POST")
print("publish:", code, json.dumps({k: r.get(k) for k in ("id", "doi", "state")}) if isinstance(r, dict) else str(r)[:200])
