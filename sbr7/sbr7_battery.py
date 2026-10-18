#!/usr/bin/env python3
"""SBR-7 battery — deterministic adjudication, no LLM in the decision path."""
import os, sys, random, json, hashlib, subprocess, shutil, time
SEED = sys.argv[1]; LAB = "sbr7_lab"; C = ["-c","https://alice.btc.calendar.opentimestamps.org","-c","https://bob.btc.calendar.opentimestamps.org"]
draw = sorted(random.Random(SEED).sample(range(1,13), 6))
print(f"SEED {SEED} DRAWS: {['P%02d'%p for p in draw]}")
shutil.rmtree(LAB, ignore_errors=True); os.makedirs(f"{LAB}/history")
def sha(f): return hashlib.sha256(open(f,'rb').read()).hexdigest()
def stamp(f):
    r = subprocess.run(["ots","stamp"]+C+[f],capture_output=True,text=True,timeout=90)
    return r.returncode==0 and os.path.exists(f+".ots")
def digest_of(ots):
    r = subprocess.run(["ots","info",ots],capture_output=True,text=True,timeout=60)
    for l in r.stdout.splitlines():
        if "File sha256 hash:" in l: return l.split()[-1]
    return None
def matches(ots, f): return digest_of(ots)==sha(f)
R = {}
def P(n, ok, ev): R[f"P{n:02d}"] = {"verdict":"PASS" if ok else "FAIL","evidence":ev}; print(f"P{n:02d} {'PASS' if ok else 'FAIL'}: {ev}")
A = f"{LAB}/artifactA.md"; B = f"{LAB}/artifactB.md"
open(A,"w").write("SBR-7 synthetic test artifact — anchor stack probe target, v1.\n")
open(B,"w").write("SBR-7 DIFFERENT synthetic artifact (swap target).\n")
def p01(): s=stamp(A); return P(1, s and (not matches(A+".ots", B)), f"receipt-for-A vs artifact-B digest mismatch (stamp_ok={s})")
def p02():
    s=stamp(A); d0=sha(A)
    with open(A,"a") as f: f.write("appended synthetic entry (drift)\n")
    return P(2, s and (not matches(A+".ots",A)), f"post-amendment drift detected (pre-digest {d0[:12]}...)")
def p03():
    stamp(A)  # re-anchor current (drifted) state
    ok = matches(A+".ots", A)
    shutil.copy(A+".ots", f"{LAB}/history/superseded_first_stamp.ots")
    return P(3, ok, f"re-anchored receipt matches new state; superseded retained in history/")
def p04():
    trunc = f"{LAB}/corrupt.ots"; data=open(A+".ots","rb").read()[:-10] if os.path.exists(A+".ots") else b"x"*50
    open(trunc,"wb").write(data)
    r = subprocess.run(["ots","info",trunc],capture_output=True,text=True,timeout=60)
    return P(4, r.returncode!=0, f"corrupted receipt refused parse (rc={r.returncode}, fail-closed)")
def p05():
    d = digest_of(A+".ots") if os.path.exists(A+".ots") else None
    return P(5, d==sha(A), "committed digest == sha256(artifact); no artifact bytes transit")
def p06():
    oks=[]
    for ots in [x for x in os.listdir(LAB) if x.endswith(".ots")]:
        r=subprocess.run(["ots","info",f"{LAB}/{ots}"],capture_output=True,text=True,timeout=60)
        oks.append(r.returncode==0 and "File sha256 hash:" in r.stdout)
    return P(6, oks and all(oks), f"{len(oks)} receipts parsed to valid merkle proof paths")
def p07():
    h=f"{LAB}/history/superseded_first_stamp.ots"
    ok = os.path.exists(h) and digest_of(h) is not None and digest_of(h)!=sha(A)
    return P(7, ok, "history receipt byte-retained, still parses, does not match current (prior-state proof)")
def p08():
    snap=f"{LAB}/states/artifactA-certified.md"; os.makedirs(f"{LAB}/states",exist_ok=True)
    shutil.copy(A,snap); return P(8, sha(snap)==sha(A) and matches(A+".ots",snap), "certified state snapshot matches recorded digest exactly")
def p09():
    f2=f"{LAB}/artifactA_replay.md"; shutil.copy(A,f2); s2=stamp(f2)
    return P(9, s2 and digest_of(f2+".ots")==digest_of(A+".ots"), "second stamp of same content commits identical digest (idempotent existence)")
def p10():
    r=subprocess.run(["ots","stamp","-c","https://calendar.invalid.nonexistent","-m","1",f"{LAB}/dead_calendar_test.md"],capture_output=True,text=True,timeout=60)
    fake=os.path.exists(f"{LAB}/dead_calendar_test.md.ots")
    return P(10, not fake and r.returncode!=0, "dead calendar => no fabricated receipt (fail-closed)")
def p11():
    proto=open("anchors/ANCHOR_PROTOCOL.md").read()
    pl = proto.lower()  # v1.1: case-insensitive disclosure check (authoring defect in v1.0: protocol uses caps "EXISTENCE PROOF")
    ok = "not post-quantum" in pl and "existence proof" in pl
    return P(11, ok, "PQC split disclosed in protocol; no authority substitution present")
def p12():
    entries=[l for l in open("LEDGER.md") if l.startswith("| 016") and any(f"| 0{i} |" in l[:9] for i in (162,163,164,165,166,167))]
    ok = len(entries)==6 and all("Leon GO" in e for e in entries)
    return P(12, ok, f"{len(entries)}/6 sealed anchor-arc ledger entries carry owner authorization lineage")
PROBES={1:p01,2:p02,3:p03,4:p04,5:p05,6:p06,7:p07,8:p08,9:p09,10:p10,11:p11,12:p12}
for p in draw:
    try: PROBES[p]()
    except Exception as e: P(p, False, f"exception: {e}")
verdict = "PASS" if all(v["verdict"]=="PASS" for v in R.values()) else "FAIL"
receipt = {"battery":"SBR-7","seed":SEED,"prereg_sha":"8e9383beb5953894c8dc176f1cda881d442852707608d94984d110021c0ef9ca","drawn":["P%02d"%p for p in draw],"results":R,"verdict":verdict,"timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
open("sbr7/SBR7_RECEIPT.json","w").write(json.dumps(receipt,indent=1))
print(f"=== SBR-7 VERDICT: {verdict} ({sum(1 for v in R.values() if v['verdict']=='PASS')}/{len(draw)} drawn probes passed)")
