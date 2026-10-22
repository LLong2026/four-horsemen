#!/usr/bin/env python3
"""UAS FIRE — process one NotarizationJob from the app queue on the TRIAD.
v1.0, 2026-10-22. Envelope: SQDR + 0x11 (UAS class) + sha256(file) = 37 bytes.
Usage: python3 uas_fire.py <digest_hex>
"""
import json, time, hashlib, sys, os, urllib.request, importlib.util

sys.path.insert(0, "/app/conversations/69b57685ca3719553a34597c/mcr3")
import mcr3_crossfire as cf

DIGEST_HEX = sys.argv[1]
OUTDIR = "/app/conversations/69b57685ca3719553a34597c/route-speed-sim"
JOBFILE = f"{OUTDIR}/UAS_JOB_{DIGEST_HEX[:12]}.json"

cf.DIGEST = bytes.fromhex(DIGEST_HEX)
cf.PAYLOAD = b"SQDR" + bytes([0x11]) + cf.DIGEST   # 0x11 = UAS notarization class
ENV = cf.PAYLOAD.hex()
UA = {"Content-Type": "application/json", "User-Agent": "uas/1.0"}
FEE_CEIL = 30
SAT_DEADLINE_S = 1800

def save(data):
    json.dump(data, open(JOBFILE, "w"), indent=1)

def log(line):
    with open(JOBFILE, "a") as f: pass
    print(line, flush=True)

# ---- XLM ----
def leg_xlm():
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{cf.TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct, network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee=100).append_manage_data_op(data_name="SQDR-UAS", data_value=cf.PAYLOAD)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    return {"xlm_tx_hash": resp.get("hash"), "xlm_ledger": resp.get("ledger"),
            "seconds": round(time.time()-t0, 1)}

# ---- XRP ----
def leg_xrp():
    from xrpl.clients import JsonRpcClient
    from xrpl.wallet import Wallet
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import Tx, AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    keyf = json.load(open(f"{cf.TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    seed = keyf["seed"]
    pk, priv = derive_keypair(seed)
    classic = derive_classic_address(pk)
    for ep in ("https://xrplcluster.com", "https://s1.ripple.com"):
        try:
            client = JsonRpcClient(ep)
            seq = client.request(AccountInfo(account=classic, ledger_index="validated")).result["account_data"]["Sequence"]
            wallet = Wallet(public_key=pk, private_key=priv, seed=seed)
            wallet.sequence = seq
            t0 = time.time()
            tx = AccountSet(account=wallet.classic_address, fee="10",
                memos=[Memo(memo_type="535144522d554153", memo_data=cf.PAYLOAD.hex())])
            signed = sign(autofill(tx, client, wallet), wallet)
            resp = submit(signed, client)
            er = resp.result.get("engine_result")
            if er not in ("tesSUCCESS", "terQUEUED", "tesPENDING"): raise RuntimeError(er)
            h = resp.result.get("tx_json", {}).get("hash") or signed.get_hash()
            for _ in range(20):
                r = client.request(Tx(transaction=h)).result
                if r.get("validated"): break
                time.sleep(2)
            return {"xrp_txid": h, "seconds": round(time.time()-t0, 1), "via": ep}
        except Exception as e:
            print(f"XRP {ep} failed: {str(e)[:90]}", flush=True)
    raise RuntimeError("XRP both endpoints failed")

# ---- SAT ----
def leg_sat():
    fees = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://mempool.space/api/v1/fees/recommended", headers=UA), timeout=15).read())
    if fees["fastestFee"] > FEE_CEIL:
        raise RuntimeError(f"fee ceiling: {fees['fastestFee']} sat/vB > {FEE_CEIL}")
    sw_path = f"{cf.TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec); spec.loader.exec_module(sw)
    sw.VERSION = 0x11
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{cf.TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    utxos = json.loads(sw.api("mainnet", f"/address/{addr}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO")
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, cf.DIGEST)
    try:
        txid = sw.api("mainnet", "/tx", raw); via = "mempool.space"
    except Exception as e1:
        print(f"SAT mempool push failed ({str(e1)[:80]}) — blockstream failover", flush=True)
        r = urllib.request.urlopen(urllib.request.Request(
            "https://blockstream.info/api/tx", data=raw.hex().encode(), headers=UA), timeout=20)
        txid = r.read().decode(); via = "blockstream.info"
    return {"btc_txid": txid, "fee_sats": info["fee"], "broadcast_via": via, "seconds": round(time.time()-t0, 1)}

def sat_confirm(txid):
    t0 = time.time()
    while time.time() - t0 < SAT_DEADLINE_S:
        try:
            st = json.loads(urllib.request.urlopen(urllib.request.Request(
                f"https://mempool.space/api/tx/{txid}/status", headers=UA), timeout=10).read())
            if st.get("confirmed"):
                return round(time.time()-t0, 1), st.get("block_height")
        except Exception:
            pass
        time.sleep(60)
    return None, None

# ---- readback (dual endpoints, byte-exact) ----
def readback(legs):
    import base64
    rb = {}
    h = legs["btc_txid"]
    t1 = json.dumps(json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://mempool.space/api/tx/{h}", headers=UA), timeout=15).read())).lower()
    t2 = json.dumps(json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://blockstream.info/api/tx/{h}", headers=UA), timeout=15).read())).lower()
    rb["sat"] = ENV.lower() in t1 and ENV.lower() in t2
    ops = json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://horizon.stellar.org/transactions/{legs['xlm_tx_hash']}/operations", headers=UA), timeout=15).read())
    op = [o for o in ops["_embedded"]["records"] if o["type"] == "manage_data"][0]
    rb["xlm"] = base64.b64decode(op["value"]).hex() == ENV and op.get("name") == "SQDR-UAS"
    rr = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://xrplcluster.com", data=json.dumps({"method": "tx", "params": [
            {"transaction": legs["xrp_txid"]}]}).encode(), headers=UA), timeout=15).read())
    md = rr["result"]["Memos"][0]["Memo"]
    rb["xrp"] = md["MemoData"].lower() == ENV and md["MemoType"].lower() == "535144522d554153"
    return rb

if __name__ == "__main__":
    out = {"digest": DIGEST_HEX, "envelope_hex": ENV, "rails": {}}
    save(out)
    out["rails"]["xlm"] = leg_xlm(); log(f"XLM: {out['rails']['xlm']}")
    save(out)
    out["rails"]["xrp"] = leg_xrp(); log(f"XRP: {out['rails']['xrp']}")
    save(out)
    out["rails"]["sat"] = leg_sat(); log(f"SAT broadcast: {out['rails']['sat']}")
    save(out)
    inc, bh = sat_confirm(out["rails"]["sat"]["btc_txid"])
    out["rails"]["sat"]["inclusion_seconds"] = inc
    out["rails"]["sat"]["block_height"] = bh
    out["rails"]["sat"]["confirmed"] = inc is not None
    log(f"SAT confirm: {inc}s block {bh}")
    save(out)
    rb = readback({**out["rails"]["xlm"], **out["rails"]["xrp"], **out["rails"]["sat"]})
    out["readback"] = rb
    out["all_pass"] = all(rb.values())
    save(out)
    print("UAS TRIAD:", "3/3 PASS" if out["all_pass"] else "FAIL", json.dumps(rb), flush=True)
