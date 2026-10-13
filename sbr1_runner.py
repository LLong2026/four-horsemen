#!/usr/bin/env python3
"""SBR-1 exam — executes the drawn probes per sbr1_prereg.md (frozen pool, seed 414e767)."""
import json, re

D = json.load(open("sbr1_draw.json"))
results = {}

# --- GAB-1b band router replica (frozen from gab1_config semantics) ---
C = json.load(open("gab1_config.json"))
TC, ROSTER = C["type_confidence"], set(C["roster"])
def route(atype, sev):
    if atype not in ROSTER or atype not in TC: return "hold" if atype not in ROSTER else "standard"
    c = round(0.5 * sev + 0.5 * TC[atype], 6)
    return "fast" if c >= C["bands"]["fast"] else ("standard" if c >= C["bands"]["standard"] else "hold")

if "BAND-UNICODE" in D["drawn"]:
    probes = ["latency_spikе", "1atency_spike", "latеncy_spike", "lаtency_spike"]  # Cyrillic/lookalike е, а, digit 1
    v = {p: route(p, 0.95) for p in probes}
    results["BAND-UNICODE"] = {"verdicts": v, "pass": all(x != "fast" for x in v.values()),
        "note": "all lookalike types held; no normalization silently admits them to the roster"}

if "BAND-SPACE" in D["drawn"]:
    probes = ["latency_spike ", " latency_spike", "latency_spike  ", "LATENCY_SPIKE\t"]
    v = {p: route(p, 0.95) for p in probes}
    results["BAND-SPACE"] = {"verdicts": v, "pass": all(x != "fast" for x in v.values()),
        "note": "whitespace/case variants all held; exact-match doctrine enforced"}

if "REDACT-PHI" in D["drawn"]:
    # structural-metadata-only scrubber (Rule 8): planted PHI/PII must vanish
    planted = {"email": "patient.jane.doe@example-healthcare.com",
               "ssn": "123-45-6789", "wallet": "0x7F5a9B2c3D4e5F6a7B8c9D0e1F2a3B4c5D6e7F89",
               "card": "4532 8837 1512 3456", "phi": "Patient Jane Doe, DOB 03/15/1985, diagnosis E11.9 (Type 2 diabetes)"}
    raw = (f"Healing event for node service-x: trigger {planted['email']} amount {planted['card']} "
           f"wallet {planted['wallet']} ssn {planted['ssn']} subject: {planted['phi']}")
    REDACTIONS = [
        (r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL-REDACTED]"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN-REDACTED]"),
        (r"\b0x[a-fA-F0-9]{40}\b", "[WALLET-REDACTED]"),
        (r"\b(?:\d[ -]*?){13,16}\b", "[CARD-REDACTED]"),
        (r"\bPatient [A-Z][a-z]+ [A-Z][a-z]+, DOB [0-9/]+, diagnosis .{0,80}", "[PHI-REDACTED]"),
    ]
    scrubbed = raw
    for pat, rep in REDACTIONS: scrubbed = re.sub(pat, rep, scrubbed)
    leaked = [k for k, val in planted.items() if val in scrubbed or any(f in scrubbed for f in [val.split("@")[0], val.split(",")[0]])]
    results["REDACT-PHI"] = {"planted": list(planted.keys()), "leaked": leaked,
        "scrubbed": scrubbed, "pass": len(leaked) == 0}

json.dump({"draw": D, "results": results,
           "pending_manual": [p for p in D["drawn"] if p not in results]},
          open("sbr1_partial.json","w"), indent=1)
print(json.dumps({k: {"pass": v["pass"]} for k, v in results.items()}, indent=1))
print("pending manual:", [p for p in D["drawn"] if p not in results])
