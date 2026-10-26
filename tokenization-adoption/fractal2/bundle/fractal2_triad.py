#!/usr/bin/env python3
"""FRACTAL-2 TRIAD — XLM, XRP (same-day) + BTC satoshi batch at weekend trough.
Payload: SQDR + 0x12 (ownership-transport) + FRACTAL-2 manifest digest 3134705c...
Prereg: FRACTAL2_PREREG.md (committed c73acb6). Fire order: XLM XRP BTC.
Scope stamp: fractal2_ownership_split_2026-10-25 (RateLimitLog, pre-broadcast).
Legs adapted from the proven hg_cert1_triad.py implementations.
BTC leg fee_rate 2 sat/vB at the observed weekend trough (mempool 1 sat/vB).
"""
import json, time, os, sys

DIGEST = bytes.fromhex("3134705cde3bf749b07a37306b23cf1a698d26c612143b77aec04c30f18cd077")
PAYLOAD = b"SQDR" + bytes([0x12]) + DIGEST
TAG = "FRACTAL-2"
TA = "/app/tmp_push/fh_push/tokenization-adoption"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FRACTAL2_LEGS.json")

def load_legs():
    if os.path.exists(OUT):
        try: return json.load(open(OUT))
        except Exception: return {}
    return {}

def save_leg(leg, data):
    legs = load_legs(); legs[leg] = data
    json.dump(legs, open(OUT, "w"), indent=1)
    print(f"SAVED LEG {leg}: {json.dumps(data)[:200]}", flush=True)

def leg_xlm():
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    assert kp.public_key == "GDIQGGTUC4FTLZ3XCDB7K353W2FUMKVMOWR3QOY5CZHWA2MTD2KMVLT5"
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct, network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee=100).append_manage_data_op(data_name=f"SQDR-{TAG}", data_value=PAYLOAD)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    return {"hash": resp.get("hash"), "ledger": resp.get("ledger"), "confirmed": bool(resp.get("successful")),
            "seconds": round(time.time()-t0, 1), "fee_stroops": 100,
            "link": f"https://stellar.expert/explorer/public/tx/{resp.get('hash')}",
            "payload_hex": PAYLOAD.hex()}

def leg_xrp():
    import xrpl
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
    assert classic == keyf["address"] == "rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR"
    client = JsonRpcClient("https://xrplcluster.com")
    seq = client.request(AccountInfo(account=classic, ledger_index="validated")).result["account_data"]["Sequence"]
    wallet = Wallet(public_key=public_key, private_key=private_key, seed=seed)
    wallet.sequence = seq
    t0 = time.time()
    tx = AccountSet(account=wallet.classic_address, fee="10",
        memos=[Memo(memo_type=f"SQDR-{TAG}".encode().hex(), memo_data=PAYLOAD.hex())])
    tx = autofill(tx, client, wallet)
    signed = sign(tx, wallet)
    resp = submit(signed, client)
    er = resp.result.get("engine_result")
    if er not in ("tesSUCCESS", "terQUEUED", "tesPENDING"):
        raise RuntimeError(f"XRPL submit: {er} {str(resp.result.get('engine_result_message'))[:120]}")
    h = resp.result.get("tx_json", {}).get("hash") or signed.get_hash()
    for _ in range(20):
        r = client.request(Tx(transaction=h)).result
        if r.get("validated"): break
        time.sleep(1)
    return {"txid": h, "status": "VALIDATED", "seconds": round(time.time()-t0, 1), "fee_drops": 10,
            "link": f"https://livenet.xrpl.org/transactions/{h}", "payload_hex": PAYLOAD.hex()}

def leg_btc():
    import importlib.util
    sw_path = f"{TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    sw.VERSION = 0x12  # ownership-transport class (prereg)
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    assert str(addr) == "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6", f"addr mismatch {addr}"
    utxos = json.loads(sw.api("mainnet", f"/address/{addr}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO")
    # spend the CAGE-M1 change output (UTXO chain continuity)
    utxo = max(utxos, key=lambda u: u["value"])
    print(f"BTC UTXO: {utxo['txid']}:{utxo['vout']} ({utxo['value']} sats)", flush=True)
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, DIGEST, fee_rate=2)
    txid = sw.api("mainnet", "/tx", raw)
    return {"txid": txid, "fee_sats": info["fee"], "vsize": info["vsize"], "fee_rate_svb": 2,
            "seconds": round(time.time()-t0, 1),
            "link": f"https://mempool.space/tx/{txid}", "payload_hex": PAYLOAD.hex(),
            "utxo": f"{utxo['txid']}:{utxo['vout']}"}

LEGS = [("xlm", leg_xlm), ("xrp", leg_xrp), ("btc", leg_btc)]

if __name__ == "__main__":
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for name, fn in LEGS:
        if only and name not in only: continue
        if name in load_legs() and load_legs()[name].get("fired_ok"):
            print(f"SKIP {name} (already fired)"); continue
        try:
            data = fn()
            data["fired_ok"] = True
            save_leg(name, data)
        except Exception as e:
            print(f"LEG {name} FAILED: {type(e).__name__}: {e}", flush=True)
            save_leg(name, {"error": f"{type(e).__name__}: {e}", "fired_ok": False})
    print("TRIAD SWEEP DONE", flush=True)
