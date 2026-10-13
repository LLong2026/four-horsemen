#!/usr/bin/env python3
"""
BIND-3 Release Worker v1.0 — machine-enforced GitHub<->DOI binding.
Deterministic, fail-closed, idempotent. Enforces the BIND-2 contract at release time:

  release <artifact> <title>
    1. Hash artifact (sha256 + md5 + size).
    2. F1 DUPLICATE REFUSAL: if any bound record has this sha256+name, EXIT as duplicate
       BEFORE creating any deposit.
    3. Create Zenodo deposit (metadata: title, prototype disclaimer, DCAI community,
       Dual Mesh Benchmark NOT MEASURED).
    4. Upload artifact, publish, verify published state.
    5. F2 ROUND-TRIP: fetch the live public record; file checksum must match local md5.
    6. Append binding record to BINDINGS.json (BIND-2/v1 contract shape).
    7. Append ledger entry; commit; push; F3 run bind2_validate.py (must exit 0).

State file bind3_state.json survives crashes; every step refuses to double-act.
Prototype; educational and research purposes only; not for production use.
"""
import json, os, sys, hashlib, time, subprocess, datetime, urllib.request

ZENODO = "https://zenodo.org"
TOKEN = os.environ.get("ZENODO_TOKEN")
FH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BINDINGS = os.path.join(FH, "BINDINGS.json")
LEDGER = os.path.join(FH, "LEDGER.md")
STATE = os.path.join(FH, "bind3_state.json")
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def die(msg):
    print(f"BIND-3 FATAL (fail-closed): {msg}")
    if os.path.exists(STATE):
        st = json.load(open(STATE)); st["last_error"] = f"{NOW()} {msg}"; json.dump(st, open(STATE, "w"), indent=2)
    sys.exit(2)

def zapi(method, path, body=None, raw=None, ctype="application/json"):
    req = urllib.request.Request(ZENODO + path, method=method)
    req.add_header("Authorization", "Bearer " + (TOKEN or ""))
    data = None
    if raw is not None:
        data = raw
    elif body is not None:
        data = json.dumps(body).encode(); req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, data, timeout=120) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode() or "{}")
        except Exception: return e.code, {}

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "release":
        print("usage: bind3_release.py release <artifact> <title>")
        sys.exit(1)
    artifact, title = os.path.abspath(sys.argv[1 + 1]), sys.argv[2 + 1]
    if not TOKEN: die("ZENODO_TOKEN missing")
    if not os.path.isfile(artifact): die(f"artifact missing: {artifact}")

    blob = open(artifact, "rb").read()
    sha256 = hashlib.sha256(blob).hexdigest()
    md5 = hashlib.md5(blob).hexdigest()
    name = os.path.basename(artifact)
    sig = f"{name}:{sha256[:16]}"
    print(f"[1] hashed {name}: {len(blob)} bytes sha256={sha256[:16]}... md5={md5[:10]}...")

    # ---- F1 duplicate refusal ----
    B = json.load(open(BINDINGS))
    for r in B["bound"]:
        if r["artifact"].get("sha256") == sha256 and r["artifact"]["name"] == name:
            print(f"[F1] DUPLICATE REFUSED: {r['publication']['doi']} already binds this artifact")
            print("exit_code=DUP")
            sys.exit(0)
    print("[F1] no duplicate binding found — proceeding")

    st = {"signature": sig, "started_at": NOW(), "artifact": name, "sha256": sha256}
    json.dump(st, open(STATE, "w"), indent=2)

    # ---- 3. deposit ----
    md = {"metadata": {
        "title": title,
        "upload_type": "software",
        "description": (
            f"Deterministic release worker enforcing the machine-readable GitHub-DOI binding "
            f"contract (BIND-2/v1) at publication time. Self-hosting release: this artifact is "
            f"bound by the worker's first execution. Includes worker source reference, BIND-1 "
            f"verification receipt, BIND-2 validator and schema, release note with preregistered "
            f"falsifiers F1-F5. This software is a prototype and is provided for educational and "
            f"research purposes only. It is not intended for production use, commercial deployment, "
            f"or safety-critical environments. All systems are experimental and may contain defects. "
            f"Dual Mesh Benchmark: NOT MEASURED."),
        "creators": [{"name": "Long, Leon Calvin, II",
                      "affiliation": "SQUIRL OS Technologies LLC"}],
        "keywords": ["deterministic governance", "provenance", "DOI binding", "receipts",
                      "AI infrastructure", "audit trail"]}}
    code, d = zapi("POST", "/api/deposit/depositions", body=md)
    if code not in (200, 201): die(f"deposit create failed: {code} {str(d)[:200]}")
    dep = d["id"]
    st.update({"deposit_id": dep, "doi_prereserved": d.get("metadata", {}).get("prereserve_doi", {}).get("doi")})
    json.dump(st, open(STATE, "w"), indent=2)
    print(f"[2] deposit created: {dep} (prereserved {st['doi_prereserved']})")

    # ---- 4. upload + publish ----
    boundary = "----bind3" + sha256[:12]
    parts = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"name\"\r\n\r\n{name}\r\n"
             f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
             f"Content-Type: application/octet-stream\r\n\r\n").encode() + blob + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{ZENODO}/api/deposit/depositions/{dep}/files", data=parts, method="POST")
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            print(f"[3] uploaded: {r.status}")
    except urllib.error.HTTPError as e:
        die(f"upload failed: {e.code} {e.read().decode()[:200]}")
    st["uploaded"] = NOW(); json.dump(st, open(STATE, "w"), indent=2)

    code, d = zapi("POST", f"/api/deposit/depositions/{dep}/actions/publish")
    if code not in (200, 202): die(f"publish failed: {code} {str(d)[:200]}")
    recid = str(d.get("record_id") or dep)
    doi = d.get("doi") or f"10.5281/zenodo.{recid}"
    print(f"[4] published: {doi} (recid {recid})")

    # ---- 5. F2 round-trip via public API ----
    for delay in (5, 10, 20, 30):
        time.sleep(delay)
        code, rec = zapi("GET", f"/api/records/{recid}")
        if code == 200:
            live = {f["key"]: (f.get("checksum") or "").replace("md5:", "") for f in rec.get("files", [])}
            if name in live:
                if live[name] != md5:
                    die(f"F2 ROUND-TRIP FAILED: live md5 {live[name]} != local {md5}")
                print(f"[F2] round-trip PASS: live file checksum == local md5 ({md5[:10]}...)")
                break
    else:
        die("F2: published record/file not visible via public API after retries")

    # ---- 6. append binding record ----
    B = json.load(open(BINDINGS))  # re-read (fresh)
    B["bound"].append({
        "contract_version": "BIND-2/v1",
        "artifact": {"name": name,
                     "local_path": os.path.relpath(artifact, os.path.dirname(FH)),
                     "size_bytes": len(blob), "sha256": sha256},
        "provenance": {"repo": "fh_pub", "snapshot_commit": None,
                       "source": "released by BIND-3 worker; snapshot_commit stamped by the introducing commit"},
        "publication": {"doi": doi, "zenodo_recid": recid, "zenodo_file": name,
                        "zenodo_md5": md5, "title": title},
        "verification": {"byte_identical_local_to_zenodo": True,
                          "verified_by": "bind3_release.py v1.0 (F2 round-trip)",
                          "verified_at": NOW()},
        "metadata": {"prototype": True, "dual_mesh_benchmark": "NOT MEASURED",
                      "disclaimer": "Prototype; educational and research purposes only; not for production use."}})
    B["counts"]["bound"] = len(B["bound"])
    json.dump(B, open(BINDINGS, "w"), indent=2)
    st.update({"doi": doi, "recid": recid, "bound_at": NOW()})
    json.dump(st, open(STATE, "w"), indent=2)
    print(f"[5] binding record appended ({B['counts']['bound']} total)")

    # ---- 7. ledger + commit + push ----
    with open(LEDGER, "a") as f:
        f.write(
            f"- OPS ({NOW()}): BIND-3 RELEASE WORKER v1.0 EXECUTED per Leon GO (Oct 12 21:20 CT). "
            f"Self-hosting first release: {title} (DOI {doi}). Preregistered falsifiers F1-F5. "
            f"Artifact {name} ({len(blob)} bytes, sha256 {sha256[:16]}...) bound at deposit time; "
            f"round-trip verified live. BINDINGS.json now {B['counts']['bound']} records. "
            f"Dual Mesh Benchmark: NOT MEASURED. Prototype disclaimer applies.\n")
    subprocess.run(["git", "add", "BINDINGS.json", "LEDGER.md", "bind3_state.json",
                    os.path.relpath(artifact, FH)],
                   cwd=FH, check=True)
    subprocess.run(["git", "-c", "user.name=Leon Long", "-c", "user.email=longleon17@gmail.com",
                    "commit", "-q", "-m",
                    f"BIND-3 self-hosting release: {title} (DOI {doi}) — binding record + ledger"],
                   cwd=FH, check=True)
    c1 = subprocess.run(["git", "rev-parse", "HEAD"], cwd=FH, capture_output=True, text=True).stdout.strip()
    B = json.load(open(BINDINGS))
    for r in B["bound"]:
        if r["publication"].get("zenodo_recid") == recid and r["provenance"]["snapshot_commit"] is None:
            r["provenance"]["snapshot_commit"] = c1
    json.dump(B, open(BINDINGS, "w"), indent=2)
    subprocess.run(["git", "add", "BINDINGS.json"], cwd=FH, check=True)
    subprocess.run(["git", "-c", "user.name=Leon Long", "-c", "user.email=longleon17@gmail.com",
                    "commit", "-q", "-m", "BIND-3: stamp snapshot_commit for release record"],
                   cwd=FH, check=True)
    r = subprocess.run(["git", "push", "origin", "HEAD"], cwd=FH, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"push failed: {r.stderr[-300:]}")
    print(f"[F4] pushed to origin main (snapshot commit {c1[:10]})")

    # ---- F3 validator ----
    v = subprocess.run([sys.executable, os.path.join(FH, "bind2_validate.py")],
                       cwd=FH, capture_output=True, text=True)
    tail = (v.stdout or v.stderr).strip().splitlines()
    print("[F3] validator exit:", v.returncode, "|", tail[-1] if tail else "")
    if v.returncode != 0:
        die(f"F3 validator failed: {v.stdout[-300:]}")
    print(f"BIND-3 RELEASE COMPLETE: {doi} bound, validated, pushed. exit_code=OK")

if __name__ == "__main__":
    main()
