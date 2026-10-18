#!/usr/bin/env python3
"""PREREG-XRP-RAIL-1 MAINNET execution — fires when wallet A is funded.
Usage: python3 xrp_mainnet_roundtrip.py   (exit 3 = awaiting funding)"""
import hashlib, json, time
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import submit_and_wait
from xrpl.models.requests import AccountInfo, Tx
from xrpl.utils import xrp_to_drops

ASSET_HASH = "81d4a5cb97fa972e89a3b65f51076384b64d4b630291a9986bd7b067adc3456c"
MARKER_TYPE = "SQDR-XRP-ANCHOR-1"
CARRY = xrp_to_drops(1)
NEED = xrp_to_drops(5)
client = JsonRpcClient("https://xrplcluster.com")

wA = Wallet(seed=json.load(open("xrp_writer_key_mainnet_a.json"))["seed"])
wB = Wallet(seed=json.load(open("xrp_writer_key_mainnet_b.json"))["seed"])
bal = int(client.request(AccountInfo(account=wA.classic_address,
             ledger_index="validated")).result["account_data"]["Balance"])
print(f"wallet A balance: {bal/1e6:.6f} XRP")
if bal < NEED:
    print(f"AWAITING FUNDING — send >= 5 XRP to: {wA.classic_address}")
    print(f"(receiver B staged at: {wB.classic_address})")
    raise SystemExit(3)

def hop(w_from, w_to, label):
    t0 = time.time()
    tx = Payment(account=w_from.classic_address, amount=CARRY,
                 destination=w_to.classic_address,
                 memos=[Memo(memo_type=MARKER_TYPE.encode().hex(),
                             memo_format="hex".encode().hex(),
                             memo_data=ASSET_HASH)])
    r = submit_and_wait(tx, client, wallet=w_from).result
    assert r["engine_result"] == "tesSUCCESS", r
    dt = time.time() - t0
    print(f"[{label}] tesSUCCESS hash {r['tx_json']['hash']} validated {dt:.1f}s fee {r['tx_json']['Fee']} drops")
    return {"txid": r["tx_json"]["hash"], "seconds": round(dt,1), "fee_drops": int(r["tx_json"]["Fee"]),
            "from": w_from.classic_address, "to": w_to.classic_address}

h1 = hop(wA, wB, "HOP1-A-to-B")
h2 = hop(wB, wA, "HOP2-B-to-A")
for hopd in (h1, h2):  # G4 round-trip read-back
    m = client.request(Tx(transaction=hopd["txid"])).result["tx_json"]["Memos"][0]["Memo"]
    assert m["MemoData"].lower() == ASSET_HASH.lower()
    print(f"  G4: {hopd['txid'][:14]}... digest byte-identical")
json.dump({"hop1": h1, "hop2": h2, "g4": "PASS",
           "total_fee_drops": h1["fee_drops"]+h2["fee_drops"]},
          open("XRP_MAINNET_RESULT.json","w"), indent=1)
print("VERDICT: ROUND TRIP COMPLETE — rail-agnostic custody demonstrated (XRPL mainnet)")
