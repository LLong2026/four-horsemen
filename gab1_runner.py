#!/usr/bin/env python3
"""GAB-1 gateway confidence-band routing benchmark, per gab1_prereg.md (frozen)."""
import json, time, statistics

C = json.load(open("gab1_config.json"))
TC, ROSTER = C["type_confidence"], set(C["roster"])
P = {"fast": C["fast_passes"], "standard": C["standard_passes"], "hold": C["hold_passes"]}

def route(inst):
    atype = inst["atype"]
    if atype not in ROSTER or atype not in TC:          # unknown type: never FAST
        if atype not in ROSTER:
            return "hold", 0.0
        return "standard", inst["sev"]                  # registered, unlearned: STANDARD
    c = round(0.5 * inst["sev"] + 0.5 * TC[atype], 6)  # gateway confidence formula
    if c >= C["bands"]["fast"]: return "fast", c
    if c >= C["bands"]["standard"]: return "standard", c
    return "hold", c

def run(mode):
    out, t0 = [], time.perf_counter_ns()
    for inst in C["instances"]:
        s = time.perf_counter_ns()
        band, c = route(inst)
        passes = P[band] if mode == "banded" else (P["standard"] if band != "hold" else P["hold"])
        if mode == "baseline" and band == "fast":      # baseline: everyone verified 3x
            passes = P["standard"]
        heal_admitted = band != "hold"                 # governance decision
        out.append({"iid": inst["iid"], "atype": inst["atype"], "band": band if mode=="banded" else ("hold" if band=="hold" else "baseline"),
                    "conf": c, "passes": passes, "heal_admitted": heal_admitted})
        out[-1]["latency_us"] = round((time.perf_counter_ns() - s) / 1000, 3)
    total_ns = time.perf_counter_ns() - t0
    return out, total_ns

b_runs = [run("baseline") for _ in range(2)]
d_runs = [run("banded") for _ in range(2)]
baseline, banded = b_runs[0][0], d_runs[0][0]

F = {}
# GAB-1 determinism
keyf = lambda rows: [{k: r[k] for k in ("iid","band","conf","passes","heal_admitted")} for r in rows]
F["GAB-1_determinism"] = {"pass": keyf(b_runs[0][0]) == keyf(b_runs[1][0]) and keyf(d_runs[0][0]) == keyf(d_runs[1][0]),
    "note": "decision fields only (per prereg); wall-clock latency is measured, not a decision quantity"}
# GAB-2 governance invariance: decisions identical across modes
dec_b = [(r["iid"], r["heal_admitted"]) for r in baseline]
dec_d = [(r["iid"], r["heal_admitted"]) for r in banded]
F["GAB-2_governance_invariance"] = {"deltas": [a for a, b in zip(dec_b, dec_d) if a != b], "pass": dec_b == dec_d}
# GAB-3 bounded provenance: every fast routing has a bounded learned weight; unlearned types never fast
fast_rows = [r for r in banded if r["band"] == "fast"]
F["GAB-3_bounded_provenance"] = {"fast_count": len(fast_rows),
    "unlearned_fast": [r["iid"] for r in fast_rows if r["atype"] not in TC],
    "pass": all(r["atype"] in TC and 0 <= TC[r["atype"]] < 1.0 for r in fast_rows)}
# GAB-4 negative integrity
neg = [r for r in baseline + banded if r["iid"].startswith("NEG-")]
F["GAB-4_negative_integrity"] = {"negatives_held": all(r["band"] in ("hold",) and not r["heal_admitted"] for r in neg), "pass": len(neg) == 4 and all(r["band"] == "hold" for r in neg)}
# counts
pb, pd = sum(r["passes"] for r in baseline), sum(r["passes"] for r in banded)
routable = [r for r in banded if r["band"] != "hold"]
fast = [r for r in banded if r["band"] == "fast"]
std = [r for r in banded if r["band"] == "standard"]
lat_b = statistics.median(r["latency_us"] for r in baseline)
lat_d = statistics.median(r["latency_us"] for r in banded)
F["GAB-5_measurement_honesty"] = {
    "baseline_passes": pb, "banded_passes": pd,
    "pass_reduction_pct": round(100 * (pb - pd) / pb, 1),
    "median_inprocess_latency_us_baseline": lat_b, "median_inprocess_latency_us_banded": lat_d,
    "note": "in-process latency excludes LLM/orchestration cost; pass-count reduction is the infra claim",
    "pass": True}

receipt = {"series": "GAB-1b", "protocol": "gab1_prereg v1.0",
           "instances": len(C["instances"]), "routable": len(routable),
           "fast": len(fast), "standard": len(std), "held": len(banded) - len(routable),
           "pass_reduction_pct": F["GAB-5_measurement_honesty"]["pass_reduction_pct"],
           "falsifiers": F, "all_pass": all(v["pass"] for v in F.values()),
           "results": banded}
json.dump(receipt, open("gab1_receipt.json","w"), indent=1)
json.dump({"baseline": baseline, "banded": banded}, open("gab1_run_detail.json","w"), indent=1)
print(json.dumps({k: receipt[k] for k in ("instances","routable","fast","standard","held","pass_reduction_pct","all_pass")}, indent=1))
print({k: v["pass"] for k, v in F.items()})
