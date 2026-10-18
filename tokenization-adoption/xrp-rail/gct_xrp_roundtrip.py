#!/usr/bin/env python3
"""DGPNM-TOK-1 G2: XRPL mainnet custody round trip carrying the GCT method draft digest."""
import json, time
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import submit_and_wait
from xrpl.models.requests import AccountInfo, Tx
from xrpl.utils import xrp_to_drops

ASSET_HASH = "7fe0258684f8bee28069a8e53275fdd7ed33c71600055274dd5839c4de5b2c8b"
MARKER_TYPE = "SQDR-XRP-ANCHOR-1"
CARRY = xrp_to_drops(1)
client = JsonRpcClient("https://xrplcluster.com")
wA = Wallet.from_seed(json.load(open("xrp_writer_key_mainnet_a.json"))["seed"])
wB = Wallet.from_seed(json.load(open("xrp_writer_key_mainnet_b.json"))["seed"])
bal = int(client.request(AccountInfo(account=wA.classic_address,
             ledger_index="validated")).result["account_data"]["Balance"])
print("wallet A:", wA.classic_address, "balance %.6f XRP" % (bal / 1e6))

def hop(w_from, w_to, label):
    t0 = time.time()
    tx = Payment(account=w_from.classic_address, amount=CARRY,
                 destination=w_to.classic_address,
                 memos=[Memo(memo_type=MARKER_TYPE.encode().hex(),
                             memo_format="hex".encode().hex(),
                             memo_data=ASSET_HASH)])
    r = submit_and_wait(tx, client, wallet=w_from).result
    assert r["engine_result"] == "tesSUCCESS", r
    txh = r["tx_json"]["hash"]
    fee = r["tx_json"]["Fee"]
    print("[%s] tesSUCCESS %s... fee %s drops (%.1fs)" % (label, txh[:16], fee, time.time() - t0))
    return {"txid": txh, "fee_drops": int(fee), "ledger_index": r.get("ledger_index"),
            "from": w_from.classic_address, "to": w_to.classic_address}

h1 = hop(wA, wB, "HOP1-A-to-B")
h2 = hop(wB, wA, "HOP2-B-to-A")
for h in (h1, h2):
    m = client.request(Tx(transaction=h["txid"])).result["tx_json"]["Memos"][0]["Memo"]
    assert m["MemoData"].lower() == ASSET_HASH.lower()
    print("  G4 read-back %s... digest byte-identical" % h["txid"][:14])
json.dump({"asset": "GCT method draft", "asset_hash": ASSET_HASH, "hop1": h1, "hop2": h2,
           "g4": "PASS", "total_fee_drops": h1["fee_drops"] + h2["fee_drops"]},
          open("../gct-tokenization/XRP_GCT_RESULT.json", "w"), indent=1)
print("G2 VERDICT: XRPL custody round trip complete")
