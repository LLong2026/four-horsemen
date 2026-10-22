#!/usr/bin/env python3
"""PAT-1 THE PATENT LOCK — USPTO provisional filing receipt anchor.
XLM data entry + XRP memo + BTC OP_RETURN. One digest, three consensus domains.
Artifact: PAT1 evidence bundle (DOI'd). Envelope byte 0x0F."""
import json, hashlib, time, importlib.util

TA = "/app/tmp_push/fh_push/tokenization-adoption"
BUNDLE_SHA = "b4f167cb2916dd3e8513f7c737bcbabbee98e78caf4291bfc3a9521ad64b3dc8"
DOI = "doi:10.5281/zenodo.23554560"

pre = f"SQDR-PAT-1|{BUNDLE_SHA}|{DOI}|apps=64/181,667+64/181,746".encode()
PAT_DIGEST = hashlib.sha256(pre).hexdigest()
PAYLOAD = b"SQDR" + bytes([0x0F]) + bytes.fromhex(PAT_DIGEST)
assert len(PAYLOAD) == 37
print(f"PAT1_DIGEST {PAT_DIGEST}")
print(f"PAYLOAD hex {PAYLOAD.hex()}")

def save_leg(name, data):
    p = "/app/conversations/69b57685ca3719553a34597c/pat1/PAT1_LEGS.json"
    try: legs = json.load(open(p))
    except Exception: legs = {}
    legs[name] = data
    json.dump(legs, open(p, "w"), indent=1)
    print(f"SAVED LEG {name}: {str(data)[:200]}")

def leg_xlm():
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    assert kp.public_key == keyf["public"] == "GDIQGGTUC4FTLZ3XCDB7K353W2FUMKVMOWR3QOY5CZHWA2MTD2KMVLT5"
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct, network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee=100).append_manage_data_op(data_name="SQDR-PAT-1", data_value=PAYLOAD)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    return {"hash": resp.get("hash"), "ledger": resp.get("ledger"),
            "confirmed": bool(resp.get("successful")), "seconds": round(time.time()-t0,1),
            "link": f"https://stellar.expert/explorer/public/tx/{resp.get('hash')}",
            "payload_hex": PAYLOAD.hex()}

def leg_xrp():
    from xrpl.clients import JsonRpcClient
    from xrpl.wallet import Wallet
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import Tx, AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    keyf = json.load(open(f"{TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    seed = keyf["seed"]
    public_key, private_key = derive_keypair(seed)
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"] == "rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR", f"addr mismatch {classic}"
    client = JsonRpcClient("https://xrplcluster.com")
    seq = client.request(AccountInfo(account=classic, ledger_index="validated")).result["account_data"]["Sequence"]
    wallet = Wallet(public_key=public_key, private_key=private_key, seed=seed)
    wallet.sequence = seq
    t0 = time.time()
    tx = AccountSet(account=wallet.classic_address, fee="10",
        memos=[Memo(memo_type="535144522d5041542d31", memo_data=PAYLOAD.hex())])
    tx = autofill(tx, client, wallet)
    signed = sign(tx, wallet)
    resp = submit(signed, client)
    er = resp.result.get("engine_result")
    if er not in ("tesSUCCESS", "terQUEUED", "tesPENDING"):
        raise RuntimeError(f"XRPL submit: {er}")
    h = resp.result.get("tx_json", {}).get("hash") or signed.get_hash()
    status = "PENDING"
    for _ in range(20):
        r = client.request(Tx(transaction=h)).result
        if r.get("validated"): status = "VALIDATED"; break
        time.sleep(1)
    return {"txid": h, "status": status, "seconds": round(time.time()-t0,1),
            "link": f"https://livenet.xrpl.org/transactions/{h}", "payload_hex": PAYLOAD.hex()}

def leg_btc():
    import sys
    sys.path.insert(0, "/app/conversations/69b57685ca3719553a34597c/wrap1")
    sw_path = f"{TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    sw.VERSION = 0x0F  # PAT-1 patent filing lock envelope
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    assert str(addr) == "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6", f"addr mismatch {addr}"
    utxo = {"txid": "0d53063045bc4b72c22ddda3f1935fa3863e985f54354a0b5250ed5e3d2ad3c7",
            "vout": 1, "value": 58969}  # live from mempool.space, conf 972548
    print(f"BTC UTXO: {utxo['txid']}:{utxo['vout']} = {utxo['value']} sats")
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, bytes.fromhex(PAT_DIGEST))
    txid = sw.api("mainnet", "/tx", raw)
    return {"txid": txid, "fee_sats": info["fee"], "seconds": round(time.time()-t0,1),
            "link": f"https://mempool.space/tx/{txid}", "payload_hex": PAYLOAD.hex()}

if __name__ == "__main__":
    for name, fn in [("xlm", leg_xlm), ("xrp", leg_xrp), ("btc", leg_btc)]:
        print(f"=== FIRING {name.upper()} LEG ===", flush=True)
        try:
            save_leg(name, fn())
        except Exception as e:
            save_leg(name, {"failed": True, "error": str(e)[:300]})
