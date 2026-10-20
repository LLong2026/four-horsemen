#!/usr/bin/env python3
"""SQUIRREL RAILS v1 — frozen route kit (no repairs; see RAILS_FROZEN_v1.md).
Usage: python3 squirrel_rails.py carrier <TAG> <PAYLOAD_HEX>
Fires the fast pair (XLM transport + XRP anchor) with the frozen constructions
and times both legs end-to-end. Keys are gitignored key files; never log secrets."""
import json, time, sys, urllib.request, base64

TA = "/app/tmp_push/fh_push/tokenization-adoption"

def leg_xlm(tag, payload: bytes):
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    assert kp.public_key == keyf["public"], "XLM keyfile mismatch"
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct,
          network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE, base_fee=100)
          .append_manage_data_op(data_name=tag, data_value=payload)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    return {"hash": resp.get("hash"), "ledger": resp.get("ledger"),
            "ok": bool(resp.get("successful")), "seconds": round(time.time()-t0, 1),
            "readback": f"https://horizon.stellar.org/accounts/{kp.public_key}/data/{tag}"}

def leg_xrp(tag, payload_hex):
    import xrpl
    from xrpl.clients import JsonRpcClient
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    from xrpl.wallet import Wallet
    keyf = json.load(open(f"{TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    public_key, private_key = derive_keypair(keyf["seed"])
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"], "XRP keyfile mismatch"
    client = JsonRpcClient("https://xrplcluster.com")
    seq = client.request(AccountInfo(account=classic, ledger_index="validated")
           ).result["account_data"]["Sequence"]
    wallet = Wallet(public_key=public_key, private_key=private_key, seed=keyf["seed"])
    wallet.sequence = seq
    t0 = time.time()
    tx = AccountSet(account=wallet.classic_address, fee="10",
        memos=[Memo(memo_type=tag.encode().hex(), memo_data=payload_hex)])
    signed = sign(autofill(tx, client, wallet), wallet)
    r = submit(signed, client).result
    return {"txid": r["tx_json"]["hash"], "engine": r["engine_result"],
            "ok": r["engine_result"] == "tesSUCCESS",
            "seconds": round(time.time()-t0, 1)}

def main():
    tag, payload_hex = sys.argv[2], sys.argv[3]
    payload = bytes.fromhex(payload_hex)
    assert len(payload) == 37 and payload[:4] == b"SQDR", "37-byte SQDR envelope only"
    t_total = time.time()
    out = {"tag": tag, "payload_hex": payload_hex}
    out["xlm"] = leg_xlm(tag, payload)
    out["xrp"] = leg_xrp(tag, payload_hex)
    out["total_seconds"] = round(time.time()-t_total, 1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
