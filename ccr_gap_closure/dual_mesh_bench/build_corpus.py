#!/usr/bin/env python3
"""Dual Mesh Benchmark corpus builder. Deterministic (seed 20261011). Frozen roster ONLY (3 registered types)."""
import json,hashlib,random,sys
from pathlib import Path
SEED=20261011
ROSTER=[("latency_spike","PB-003: Latency Spike Resolver"),
        ("heartbeat_miss","PB-008: Heartbeat Re-igniter"),
        ("quantum_vulnerability_detected","PB-009: Quantum Vulnerability Migrator")]
def build(n=200):
    rng=random.Random(SEED); out=[]
    for i in range(n):
        at,pb=ROSTER[rng.randrange(len(ROSTER))]
        out.append({"instance_id":f"BENCH-{i:04d}","anomaly_type":at,"expected_playbook":pb,
                    "latency_ms":round(rng.uniform(5,4000),2),"cpu":round(rng.uniform(1,99),2),
                    "memory":round(rng.uniform(1,99),2),"error_count":rng.randrange(0,50)})
    return out
if __name__=="__main__":
    corpus=build(); text=json.dumps(corpus,indent=2,sort_keys=False)
    Path(sys.argv[1]).write_text(text)
    print("corpus sha256",hashlib.sha256(text.encode()).hexdigest(),"instances",len(corpus))
