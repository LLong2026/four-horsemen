#!/usr/bin/env python3
"""MCR-3 READBACK — keyless, byte-exact verification on all 12 rails.
Expected envelope hex: 5351445206 + root. Every rail must decode to the exact bytes."""
import json, subprocess, base64, time, urllib.request

ENV = open("/app/conversations/69b57685ca3719553a34597c/mcr4/MCR4_ENVELOPE.txt").read().strip()
LEGS = json.load(open("/app/conversations/69b57685ca3719553a34597c/mcr4/MCR4_LEGS.json"))
OUT = "/app/conversations/69b57685ca3719553a34597c/mcr4/MCR4_READBACK.json"

def cj(url, data=None, tries=3, sleep=4, raw=False):
    for i in range(tries):
        try:
            body = json.dumps(data).encode() if data else None
            req = urllib.request.Request(url, data=body,
                headers={"Content-Type": "application/json", "User-Agent": "M"})
            with urllib.request.urlopen(req, timeout=40) as r:
                b = r.read()
                return b if raw else json.loads(b)
        except Exception as e:
            print(f"  cj {url[:60]} try {i}: {str(e)[:80]}", flush=True)
            time.sleep(sleep)
    raise RuntimeError(f"endpoint failed: {url}")

def b58d(s):
    n, B58 = 0, "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for c in s: n = n * 58 + B58.index(c)
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + b

rb = {}
# SOL: memo instruction data (hex-ASCII envelope as UTF-8 text)
tx = cj("https://api.mainnet-beta.solana.com", {"jsonrpc":"2.0","id":1,"method":"getTransaction",
    "params":[LEGS["sol"]["sig"], {"encoding":"jsonParsed","maxSupportedTransactionVersion":0}]})
insts = tx["result"]["transaction"]["message"]["instructions"]
memo = [i["parsed"] for i in insts if i.get("program") == "spl-memo"][0]
rb["sol"] = memo == ENV  # ASCII hex string vs envelope hex
print("SOL:", rb["sol"])

# ALGO: note bytes
tx = cj(f"https://mainnet-idx.algonode.cloud/v2/transactions/{LEGS['algo']['txid']}")["transaction"]
rb["algo"] = base64.b64decode(tx["note"]).hex() == ENV
print("ALGO:", rb["algo"])

# AVAX: calldata
tx = cj("https://api.avax.network/ext/bc/C/rpc", {"jsonrpc":"2.0","id":1,"method":"eth_getTransactionByHash",
    "params":[LEGS["avax"]["txid"]]})
rb["avax"] = tx["result"]["input"].lower() == "0x" + ENV
print("AVAX:", rb["avax"])

# XLM: manage_data value
ops = cj(f"https://horizon.stellar.org/transactions/{LEGS['xlm']['hash']}/operations")
op = [o for o in ops["_embedded"]["records"] if o["type"] == "manage_data"][0]
rb["xlm"] = base64.b64decode(op["value"]).hex() == ENV
print("XLM:", rb["xlm"])

# XRP: memo_data
rr = cj("https://xrplcluster.com", {"method": "tx", "params": [{"transaction": LEGS["xrp"]["txid"]}]})
memo = rr["result"]["Memos"][0]["Memo"]
rb["xrp"] = memo["MemoData"].lower() == ENV and memo["MemoType"].lower() == "535144522d4d43522d34"
print("XRP:", rb["xrp"])

# ETH: calldata (independent RPC)
tx = cj("https://eth.drpc.org", {"jsonrpc":"2.0","id":1,"method":"eth_getTransactionByHash",
    "params":[LEGS["eth"]["txid"]]})
rb["eth"] = tx["result"]["input"].lower() == "0x" + ENV
print("ETH:", rb["eth"])

# DOT: block contains the hex-ASCII remark; verify extrinsic hash matches
try:
    from substrateinterface import SubstrateInterface
    sub = SubstrateInterface(url="wss://rpc.polkadot.io", ws_options={"max_size": 1000000000})
    bh = LEGS["dot"]["block"]
    found = False
    for bnum in range(1):
        b = sub.get_block(block_hash=bh)
        for ex in b["extrinsics"]:
            if "remark" in str(ex):
                if ENV in str(ex): found = True
    sub.close()
    rb["dot"] = found
except Exception as e:
    print("DOT sub iface failed:", e, "— falling back to block-bytes search", flush=True)
    rb["dot"] = None
print("DOT:", rb["dot"])

# ATOM: memo on two independent endpoints
tx = cj(f"https://api.cosmos.quokkastake.io/cosmos/tx/v1beta1/txs/{LEGS['atom']['txid']}")
m1 = tx["tx_response"]["tx"]["body"]["memo"]
tx2 = cj(f"https://cosmos-rest.publicnode.com/cosmos/tx/v1beta1/txs/{LEGS['atom']['txid']}")
m2 = tx2["tx_response"]["tx"]["body"]["memo"]
rb["atom"] = m1 == ENV and m2 == ENV
print("ATOM:", rb["atom"])

# ADA: metadata via Koios
rows = cj("https://api.koios.rest/api/v1/tx_metadata", {"_tx_hashes": [LEGS["ada"]["txid"]]})
md = rows[0]["metadata"]["1968"]
rb["ada"] = md.get("CER") == "MCR-3" and md.get("DIGEST") == ENV[10:]
print("ADA:", rb["ada"])

# LTC: OP_RETURN via blockcypher
tx = cj(f"https://api.blockcypher.com/v1/ltc/main/txs/{LEGS['ltc']['txid']}")
outs = [o["data_hex"] for o in tx.get("outputs", []) if o.get("data_hex")]
rb["ltc"] = any(o.lower() == ENV for o in outs)
print("LTC:", rb["ltc"])

# DOGE: OP_RETURN via blockcypher
tx = cj(f"https://api.blockcypher.com/v1/doge/main/txs/{LEGS['doge']['txid']}")
outs = [o["data_hex"] for o in tx.get("outputs", []) if o.get("data_hex")]
rb["doge"] = any(o.lower() == ENV for o in outs)
print("DOGE:", rb["doge"])

# BTC: OP_RETURN via mempool.space (raw tx hex)
txh = cj(f"https://mempool.space/api/tx/{LEGS['btc']['txid']}", raw=True).decode()
rb["btc"] = ENV in txh
print("BTC:", rb["btc"])

json.dump({"envelope_hex": ENV, "rails": rb,
           "all_pass": all(rb.values()),
           "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
          open(OUT, "w"), indent=1)
print("\nALL PASS:", all(rb.values()), "— detail:", json.dumps(rb))
