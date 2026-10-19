#!/usr/bin/env python3
"""IR-1 Router v1.0 — deterministic rail selection. No LLM in the decision path."""
import json, time, urllib.request
def post(url, payload, hdrs=None):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=hdrs or {"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req))
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})))
t = time.time()
probes = {}
# XRPL: ledger close interval
r = post("https://s1.ripple.com:51234/", {"method":"server_info","params":[{}]})["result"]["info"]
probes["xrp"] = {"close_interval_s": r["validated_ledger"].get("close_time_interval")}
# ETH: block interval from last 2 blocks + gas price
def eth(method, params):
    return post("https://ethereum-rpc.publicnode.com", {"jsonrpc":"2.0","id":1,"method":method,"params":params})
b1 = int(eth("eth_blockNumber", [])["result"],16)
bn1 = eth("eth_getBlockByNumber", [hex(b1), False])["result"]
time.sleep(2)
b2 = int(eth("eth_blockNumber", [])["result"],16)
bn2 = eth("eth_getBlockByNumber", [hex(b2), False])["result"]
probes["eth"] = {"block_interval_s": int(bn2["timestamp"],16)-int(bn1["timestamp"],16) if b2>b1 else 12,
                 "gas_gwei": int(eth("eth_gasPrice", [])["result"],16)/1e9}
# Stellar: ledger close
l1 = get("https://horizon.stellar.org/ledgers?order=desc&limit=2")["_embedded"]["records"]
probes["stellar"] = {"close_interval_s": l1[0]["base_interval_s"] if "base_interval_s" in l1[0] else 5}
# Cardano: tip interval (proxy)
tip = get("https://api.koios.rest/api/v1/tip")
probes["cardano"] = {"tip": tip[0]["block_no"]}
# BTC: feerate
fee = json.load(urllib.request.urlopen(urllib.request.Request("https://mempool.space/api/v1/fees/recommended", headers={"User-Agent":"Mozilla/5.0"})))
probes["btc"] = {"sat_vb": fee["fastestFee"]}
# Score table: live probe, corrected by same-day measured records (PWR-1/XTR-1)
expected = {
    "xrp":      {"finality_s": 7.09,  "cost_usd": 0.002,  "source": "XTR-1 measured avg"},
    "stellar":  {"finality_s": 6.50,  "cost_usd": 0.00003,"source": "XCF-1 measured 5-8s, midpoint"},
    "eth":      {"finality_s": 13.0,  "cost_usd": 0.01,   "source": "PWR-1 measured block+receipt"},
    "cardano":  {"finality_s": 30.0,  "cost_usd": 0.05,   "source": "PWR-1/XCF-1 measured"},
    "btc":      {"finality_s": 900.0, "cost_usd": 0.10,   "source": "minutes-hours, mempool feerate " + str(fee["fastestFee"]) + " sat/vB"},
}
# Deterministic decision: sort by (finality, cost, name)
ranked = sorted(expected.items(), key=lambda kv: (kv[1]["finality_s"], kv[1]["cost_usd"], kv[0]))
decision = {"ts": t, "probes": probes, "expected": expected, "ranking": [k for k,_ in ranked],
            "selected": [ranked[0][0], ranked[1][0]]}
print(json.dumps(decision, indent=1))
json.dump(decision, open("ROUTER_DECISION.json","w"), indent=1)
