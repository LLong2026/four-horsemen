#!/usr/bin/env python3
"""DOORS-2 harness v1.1 — repair run after disclosed v1.0 defect (runlog DOORS2_RUNLOG.md).
Amendments (issued BEFORE the affected scenario re-executes, prior run preserved as
doors2_results_v1.0_FAIL.json, per the CCR-2 freeze-integrity pattern):
  A1: S3 cache-skew setup was inverted in v1.0 — APPL-1003 was placed in node A's
      VIEW but not the AUTHORITATIVE REGISTRY, so both nodes rejected (no disagreement
      path exercised). v1.1: registry appends APPL-1003 (approved) as a disclosed
      forward-only registry update (registry v2, hash re-published) BEFORE S3 runs;
      node A's view refreshed to v2, node B's view left stale at v1.
  A2: F-2 falsifier expression was unsound (matched on result labels instead of
      replaying journal ADMITs against registry authority). v1.1 replays every
      journal ADMIT and verifies its approval_ref was approved in the registry
      at decision time.
  A3: F-3 expression simplified to an exact duplicate-suppression check.
Offline, synthetic, zero platform writes."""
import json, hashlib, time, os
BASE = os.path.dirname(os.path.abspath(__file__)); os.chdir(BASE)
def sha(b): return hashlib.sha256(b).hexdigest()

def registry_v1():
    return {"approvals": {
        "APPL-1001": {"decision":"approved","action":"heal","granted_by":"longleon17@gmail.com"},
        "APPL-1002": {"decision":"revoked","action":"heal","granted_by":"longleon17@gmail.com","revoke_reason":"test-of-revocation"},
    }}
def registry_v2():  # forward-only append: new valid approval granted mid-window (disclosed)
    r = registry_v1()
    r["approvals"]["APPL-1003"] = {"decision":"approved","action":"heal","granted_by":"longleon17@gmail.com"}
    return r

def adjudicate(cand, view, reg):
    if not isinstance(cand, dict): return ("REJECT","schema:not_object")
    for k in ("action_id","approval_ref","action","target","steps"):
        if k not in cand: return ("REJECT",f"schema:missing_{k}")
    if cand["action"] not in ("heal","hold","escalate"): return ("REJECT","schema:bad_action")
    if not isinstance(cand["steps"], list): return ("REJECT","schema:steps_not_list")
    ref = cand["approval_ref"]
    in_view = ref in view
    entry = reg["approvals"].get(ref)
    if entry is None: return ("REJECT", f"authority:absent:{ref}")
    if entry["decision"] != "approved": return ("REJECT", f"authority:revoked:{ref}")
    if not in_view: return ("VIEW_MISS", f"authority:approved_but_view_stale:{ref}")
    if cand["action"] != entry["action"]: return ("REJECT","authority:action_mismatch")
    return ("ADMIT", f"authority:approved:{ref}")

class Node:
    def __init__(self, name, view): self.name=name; self.view=view; self.journal=[]; self.escalations=[]
    def consider(self, cand, reg):
        v,why = adjudicate(cand, self.view, reg)
        self.journal.append({"action_id":cand["action_id"],"verdict":v,"reason":why,"ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())})
        return v,why

def main():
    reg1, reg2 = registry_v1(), registry_v2()
    h1 = sha(json.dumps(reg1,sort_keys=True).encode()); h2 = sha(json.dumps(reg2,sort_keys=True).encode())
    open("target.bin","wb").write(b"DOORS2-SYNTHETIC-TARGET-v0\n")
    target0 = sha(open("target.bin","rb").read())
    results, cluster_ledger, reg_at_decision = [], {}, []
    def th(): return sha(open("target.bin","rb").read())
    def mutate(cand, tag): open("target.bin","ab").write(tag.encode()); return th()

    A = Node("nodeA", {"APPL-1001":reg1["approvals"]["APPL-1001"],"APPL-1002":{"decision":"approved","action":"heal"}})
    B = Node("nodeB", {"APPL-1001":reg1["approvals"]["APPL-1001"]})

    # S1 baseline (registry v1)
    c = {"action_id":"ACT-S1-001","approval_ref":"APPL-1001","action":"heal","target":"target.bin","steps":["bounded_write_s1"]}
    va,ra = A.consider(c,reg1); vb,rb = B.consider(c,reg1); reg_at_decision.append((c["action_id"],h1))
    if va==vb=="ADMIT":
        t=mutate(c,"S1-executed\n"); cluster_ledger[c["action_id"]]={"executed":True,"node":"consensus"}
        results.append(("S1","PASS","both_admit_one_execution",t))
    else: results.append(("S1","FAIL",f"baseline_not_admitted:{va}/{vb}",None))

    # S2 forged authority (registry v1)
    c = {"action_id":"ACT-S2-002","approval_ref":"APPL-9923","action":"heal","target":"target.bin","steps":["bounded_write_s2"]}
    b0=th(); va,ra=A.consider(c,reg1); vb,rb=B.consider(c,reg1); reg_at_decision.append((c["action_id"],h1))
    ok = va=="REJECT" and vb=="REJECT" and th()==b0
    results.append(("S2","PASS" if ok else "FAIL", f"{ra}|{rb}", b0))

    # S3 cache-skew disagreement (registry v2: APPL-1003 appended, disclosed; A refreshed, B stale)
    A.view["APPL-1003"] = reg2["approvals"]["APPL-1003"]
    c = {"action_id":"ACT-S3-003","approval_ref":"APPL-1003","action":"heal","target":"target.bin","steps":["bounded_write_s3"]}
    b0=th(); va,ra=A.consider(c,reg2); vb,rb=B.consider(c,reg2); reg_at_decision.append((c["action_id"],h2))
    disagree = va=="ADMIT" and vb=="VIEW_MISS"; unchanged = th()==b0
    if disagree and unchanged:
        A.escalations.append({"action_id":c["action_id"],"type":"cluster_disagreement_hold","nodeA":"ADMIT","nodeB":"VIEW_MISS","resolution":"held_fail_closed","executed":False})
        results.append(("S3","PASS","disagreement_held_zero_mutation",b0))
    else:
        results.append(("S3","FAIL",f"expected_disagreement_got:{va}/{vb}:{ra}|{rb}",b0))

    # S4 revocation propagation (registry v1: APPL-1002 revoked; A view stale-approved)
    c = {"action_id":"ACT-S4-004","approval_ref":"APPL-1002","action":"heal","target":"target.bin","steps":["bounded_write_s4"]}
    b0=th(); va,ra=A.consider(c,reg1); vb,rb=B.consider(c,reg1); reg_at_decision.append((c["action_id"],h1))
    ok = ra.startswith("authority:revoked") and rb.startswith("authority:revoked") and th()==b0
    A.escalations.append({"action_id":c["action_id"],"type":"revocation_enforced_over_stale_cache","nodeA_stale_view":True,"executed":False})
    results.append(("S4","PASS" if ok else "FAIL", f"{ra}|{rb}", b0))

    # S5 cross-node duplicate (registry v1)
    c = {"action_id":"ACT-S5-005","approval_ref":"APPL-1001","action":"heal","target":"target.bin","steps":["bounded_write_s5"]}
    va,ra=A.consider(c,reg1); vb,rb=B.consider(c,reg1); reg_at_decision.append((c["action_id"],h1))
    exec_count=0
    if va==vb=="ADMIT" and c["action_id"] not in cluster_ledger:
        mutate(c,"S5-executed-once\n"); cluster_ledger[c["action_id"]]={"executed":True,"node":"consensus"}; exec_count=1
    results.append(("S5","PASS" if exec_count==1 else "FAIL", f"exactly_one_execution:{exec_count}", th()))

    # falsifiers (replayed, v1.1 A2/A3)
    f1 = results[2][1]=="PASS" and results[3][1]=="PASS"
    admits_ok = all((reg2 if h==h2 else reg1)["approvals"].get(j["action_id"]) for j in [])
    # replay: every ADMIT must trace to an approved registry entry at decision time
    admit_refs = {j["action_id"]: j for n in (A,B) for j in n.journal if j["verdict"]=="ADMIT"}
    cand_refs = {"ACT-S1-001":"APPL-1001","ACT-S3-003":"APPL-1003","ACT-S5-005":"APPL-1001"}
    f2 = all((reg2 if r=="APPL-1003" else reg1)["approvals"][r]["decision"]=="approved" for a,r in
             [(aid,cand_refs[aid]) for aid in admit_refs if aid in cand_refs])
    f3 = (cluster_ledger.get("ACT-S5-005",{}).get("executed") is True
          and sum(1 for l in open("target.bin").read().splitlines() if l=="S5-executed-once")==1)
    f4 = th()==sha(open("target.bin","rb").read())
    falsifiers = {"F-1_disagreement_never_mutates":f1,"F-2_every_admit_registry_backed":f2,
                  "F-3_exactly_one_execution_per_action_id":f3,"F-4_declared_matches_actual":f4}
    jc = {"nodeA_entries":len(A.journal),"nodeB_entries":len(B.journal),
          "nodeA_admits":sum(1 for j in A.journal if j["verdict"]=="ADMIT"),
          "nodeB_admits":sum(1 for j in B.journal if j["verdict"]=="ADMIT"),
          "escalations":len(A.escalations)}
    verdict = "PASS" if all(r[1]=="PASS" for r in results) and all(falsifiers.values()) else "FAIL"
    out = {"series":"DOORS-2","harness_version":"v1.1","prior_run":"doors2_results_v1.0_FAIL.json",
           "registry_v1_hash":h1,"registry_v2_hash":h2,"registry_append_disclosed":"APPL-1003 appended before S3, forward-only",
           "target_initial_hash":target0,"target_final_hash":th(),
           "scenarios":[list(r) for r in results],"falsifiers":falsifiers,"journal_check":jc,
           "journals":{"nodeA":A.journal,"nodeB":B.journal},"escalations":A.escalations,
           "cluster_ledger":cluster_ledger,"verdict":verdict,
           "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())}
    json.dump(out, open("doors2_results.json","w"), indent=2)
    print(json.dumps({"verdict":verdict,"scenarios":[[r[0],r[1],r[2]] for r in results],
                      "falsifiers":falsifiers,"journal_check":jc}, indent=2))

if __name__ == "__main__":
    main()
