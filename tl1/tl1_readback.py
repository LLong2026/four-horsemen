import json, base64, subprocess

TL_DIGEST = "6650efc9e393e9b1824fd7caba28ae67f88210727a03132c798fac5cadaafc9c"
EXPECT = "535144520e" + TL_DIGEST
legs = json.load(open("TL1_LEGS.json"))
out = {}

def get(url):
    req = __import__("urllib.request", fromlist=["Request"]).Request(url, headers={"User-Agent": "sqdr-tl1-readback"})
    return json.loads(__import__("urllib.request", fromlist=["urlopen"]).urlopen(req, timeout=30).read())

acct = get("https://horizon.stellar.org/accounts/GDIQGGTUC4FTLZ3XCDB7K353W2FUMKVMOWR3QOY5CZHWA2MTD2KMVLT5")
got = base64.b64decode(acct["data"]["SQDR-TL-1"]).hex()
out["xlm"] = {"match": got == EXPECT, "ledger": acct.get("last_modified_ledger")}

txr = json.loads(subprocess.run(["curl", "-s", "https://xrplcluster.com", "-d",
    json.dumps({"method": "tx", "params": [{"transaction": legs["xrp"]["txid"]}]})],
    capture_output=True, text=True).stdout)
memo = txr["result"]["Memos"][0]["Memo"]["MemoData"].lower()
out["xrp"] = {"match": memo == EXPECT, "validated": txr["result"].get("validated")}

t = get("https://mempool.space/api/tx/" + legs["btc"]["txid"])
opcands = [o["scriptpubkey"][4:] for o in t["vout"] if o.get("scriptpubkey_type") == "op_return"]
out["btc"] = {"match": bool(opcands) and opcands[0] == EXPECT,
              "block": t.get("status", {}).get("block_height")}

print(json.dumps(out, indent=1))
print("TRUSTABLE LOCK:", "3/3 BYTE-EXACT" if all(v["match"] for v in out.values()) else "MISMATCH")
