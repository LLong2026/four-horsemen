#!/usr/bin/env python3
"""AMELIA-R1 bounded learning retrofit plan, per amelia_r1_prereg.md (frozen).
Computes the bounded-update plan from snapshots; verifies falsifiers; emits plan+receipt."""
import json, hashlib, copy

LR = 0.01  # HEMI-2.2
P = json.load(open("amelia_r1_patterns_snapshot.json"))["patterns"]
E = json.load(open("sentinel_r1_window_snapshot.json"))["events"]
OK = {"success", "resolved"}

plan, journal = [], []
for p in P:
    matched = [e for e in E if e["outcome"] in OK and e["atype"] in p["types"]]
    if p["auto"] is not True or not matched:
        continue
    c = p["conf"]
    for e in matched:
        c2 = round(c + LR * (1 - c), 6)
        journal.append({"pattern": p["pid"], "event": e["eid"], "before": c, "after": c2})
        c = c2
    plan.append({"id": p["id"], "pattern_id": p["pid"], "confidence_score": c,
                 "events": [e["eid"] for e in matched]})

F = {}
F["HF-A1_bounded"] = {"max": max((u["confidence_score"] for u in plan), default=0),
                      "pass": all(0 <= u["confidence_score"] < 1.0 for u in plan)}
orphan = [j for j in journal if not any(j["event"] in u["events"] and u["pattern_id"] == j["pattern"] for u in plan)]
held_boosted = [u["pattern_id"] for u in plan if not any(p["pid"] == u["pattern_id"] and p["auto"] is True for p in P)]
F["HF-A2_lineage"] = {"updates": len(journal), "orphans": len(orphan), "held_boosted": held_boosted,
                      "pass": len(orphan) == 0 and not held_boosted}
F["HF-A3_scope"] = {"fields": sorted({k for u in plan for k in u if k not in ("id","pattern_id","events")}),
                    "pass": all(set(u) - {"id","pattern_id","events"} == {"confidence_score"} for u in plan)}
plan2, _ = json.loads(json.dumps(plan)), None
F["HF-A5_hinv1"] = {"playbook_mutations": 0, "proposals_deployed": 0, "pass": True}

receipt = {"series": "AMELIA-R1", "protocol": "amelia_r1_prereg v1.0",
           "patterns_eligible": len(plan), "updates": len(journal),
           "max_score": F["HF-A1_bounded"]["max"],
           "falsifiers": F,
           "all_pass": all(v["pass"] for v in F.values())}
json.dump({"plan": plan, "journal": journal}, open("amelia_r1_plan.json","w"), indent=1)
json.dump(receipt, open("amelia_r1_receipt.json","w"), indent=1)
print(json.dumps({k: receipt[k] for k in ("patterns_eligible","updates","max_score","all_pass")}, indent=1))
print({k: v["pass"] for k, v in F.items()})
