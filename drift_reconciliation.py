#!/usr/bin/env python3
"""SIP-3 (approved Leon GO, Oct 13, 2026, 11:55 CT): cumulative drift reconciliation audit.
Stage-1 instrument-level deployment (battery/nightly runners). Exact identity proven in
SBR-5 (closure 0.00e+00); budget default 1e-4 (instrument choice; production value is Leon's)."""
import json

def reconcile(journal, final_weight, initial_weight, drift_budget=1e-4, corpus_prefixes=("BENCH-",)):
    """Fold journal crossings; attribute anomalous drift; flag above budget. Returns audit dict."""
    w = initial_weight
    legit = 0.0; foreign = 0.0
    for j in journal:
        delta = j["after"] - j["before"]
        if any(j["event_id"].startswith(p) for p in corpus_prefixes): legit += delta
        else: foreign += delta
        w = j["after"]
    closure = (final_weight - initial_weight) - legit - foreign
    anomalous = final_weight - (initial_weight + legit)
    return {"closure_gap": closure, "attributed_foreign_drift": foreign,
            "anomalous_drift": anomalous, "budget": drift_budget,
            "flagged": anomalous > drift_budget,
            "verdict": "FLAG" if anomalous > drift_budget else "WITHIN_BUDGET"}
