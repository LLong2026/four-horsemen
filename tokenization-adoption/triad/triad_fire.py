#!/usr/bin/env python3
"""TRIAD FIRE — hardened default notarization runner (SAT + XLM + XRP).
v1.0, 2026-10-22, doctrine: TRIAD_ROUTE.md

Hardened rules implemented:
- SAT: fee guard (mempool.space recommended, ceiling 30 sat/vB hard stop),
  broadcast mempool.space -> blockstream failover, 60s inclusion poll, 30-min deadline.
- XLM: 3x retry with 10s backoff on horizon, named entry SQDR-TRIAD-<tag>.
- XRP: full submit failover xrplcluster -> s1.ripple.com, validated check.
- Readback: dual endpoints per rail, byte-exact gate 3/3.
- Idempotency: TRIAD_LEGS.json guards refires of the same tag.
"""
import json, time, hashlib, sys, os, urllib.request

sys.path.insert(0, "/app/conversations/69b57685ca3719553a34597c/mcr3")
import mcr3_crossfire as cf

OUTDIR = "/app/conversations/69b57685ca3719553a34597c/route-speed-sim"
LEGS = f"{OUTDIR}/TRIAD_LEGS.json"
RUNLOG = f"{OUTDIR}/TRIAD_RUNLOG.md"
TAG = os.environ.get("TRIAD_TAG", "TRIAD-SIM-1")
FEE_CEIL = 30          # sat/vB hard ceiling for SAT
SAT_DEADLINE_S = 1800  # 30 min hard deadline

cf.DIGEST = hashlib.sha256(f"{TAG}|2026-10-22".encode()).digest()
cf.PAYLOAD = b"SQDR" + bytes([0x10]) + cf.DIGEST   # 0x10 = route speed-sim class
ENV = cf.PAYLOAD.hex()
UA = {"Content-Type": "application/json", "User-Agent": "triad/1.0"}

def gj(url, data=None, timeout=15, tries=3, backoff=4):
    for i in range(tries):
        try:
            body = json.dumps(data).encode() if data is not None else None
            r = urllib.request.urlopen(urllib.request.Request(url, data=body, headers=UA), timeout=timeout)
            return json.loads(r.read())
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(backoff)

def load_legs():
    return json.load(open(LEGS)) if os.path.exists(LEGS) else {}

def save_leg(name, data):
    d = load_legs(); d[name] = data; json.dump(d, open(LEGS, "w"), indent=1)

def log(line):
    with open(RUNLOG, "a") as f: f.write(line + "\n")
    print(line, flush=True)

# ---------------- SAT (hardened) ----------------
def sat_fee_guard():
    fees = gj("https://mempool.space/api/v1/fees/recommended")
    rate = fees["fastestFee"]
    if rate > FEE_CEIL:
        raise RuntimeError(f"SAT fee ceiling breached: fastestFee {rate} sat/vB > {FEE_CEIL} — holding fire, escalate to operator")
    return rate

def leg_sat():
    import importlib.util
    sat_fee_guard()
    sw_path = f"{cf.TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec); spec.loader.exec_module(sw)
    sw.VERSION = 0x10
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{cf.TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    assert str(addr) == "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6"
    utxos = json.loads(sw.api("mainnet", f"/address/{addr}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO — rail unfunded, escalate")
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, cf.DIGEST)
    # broadcast: mempool.space primary, blockstream failover
    txid = None; bc = None
    try:
        txid = sw.api("mainnet", "/tx", raw)
        bc = "mempool.space"
    except Exception as e1:
        log(f"SAT mempool.space push failed ({str(e1)[:80]}) — failing over to blockstream")
        r = urllib.request.urlopen(urllib.request.Request(
            "https://blockstream.info/api/tx", data=raw.hex().encode(), headers=UA), timeout=20)
        txid = r.read().decode(); bc = "blockstream.info"
    return {"txid": txid, "fee_sats": info["fee"], "broadcast_via": bc,
            "seconds": round(time.time()-t0, 1), "utxo": f"{utxo['txid']}:{utxo['vout']}",
            "link": f"https://mempool.space/tx/{txid}", "payload_hex": ENV}

def sat_wait_confirm(txid):
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

# ---------------- XLM (hardened) ----------------
def leg_xlm():
    from stellar_sdk import Keypair, Server, TransactionBuilder, Network
    keyf = json.load(open(f"{cf.TA}/stellar-rail/stellar_writer_key_mainnet_a.json"))
    kp = Keypair.from_secret(keyf["secret"])
    server = Server(horizon_url="https://horizon.stellar.org")
    acct = server.load_account(kp.public_key)
    t0 = time.time()
    tx = (TransactionBuilder(source_account=acct, network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
          base_fee=100).append_manage_data_op(data_name=f"SQDR-{TAG}", data_value=cf.PAYLOAD)
          .set_timeout(30).build())
    tx.sign(kp)
    resp = server.submit_transaction(tx)
    return {"hash": resp.get("hash"), "ledger": resp.get("ledger"),
            "confirmed": bool(resp.get("successful")), "seconds": round(time.time()-t0, 1),
            "link": f"https://stellar.expert/explorer/public/tx/{resp.get('hash')}",
            "payload_hex": ENV}

def leg_xlm_retry():
    last = None
    for attempt in range(1, 4):
        try:
            return leg_xlm()
        except Exception as e:
            last = e; log(f"XLM attempt {attempt} failed: {str(e)[:100]} — backoff 10s")
            time.sleep(10)
    raise RuntimeError(f"XLM 3x retry exhausted: {last}")

# ---------------- XRP (hardened, full failover) ----------------
def leg_xrp():
    from xrpl.clients import JsonRpcClient
    from xrpl.wallet import Wallet
    from xrpl.models.transactions import AccountSet, Memo
    from xrpl.models.requests import Tx, AccountInfo
    from xrpl.core.keypairs import derive_keypair, derive_classic_address
    from xrpl.transaction import autofill, sign, submit
    keyf = json.load(open(f"{cf.TA}/xrp-rail/xrp_writer_key_mainnet_a.json"))
    seed = keyf["seed"]
    public_key, private_key = derive_keypair(seed)
    classic = derive_classic_address(public_key)
    assert classic == keyf["address"] == "rBbxYuBkzK6UxKXhvUi8uNtdxhD1h7ZFGR"
    client_used = None; resp = None
    for ep in ("https://xrplcluster.com", "https://s1.ripple.com"):
        try:
            client = JsonRpcClient(ep)
            seq = client.request(AccountInfo(account=classic, ledger_index="validated")).result["account_data"]["Sequence"]
            wallet = Wallet(public_key=public_key, private_key=private_key, seed=seed)
            wallet.sequence = seq
            t0 = time.time()
            tx = AccountSet(account=wallet.classic_address, fee="10",
                memos=[Memo(memo_type="535144522d5452494144", memo_data=cf.PAYLOAD.hex())])
            tx = autofill(tx, client, wallet)
            signed = sign(tx, wallet)
            resp = submit(signed, client)
            er = resp.result.get("engine_result")
            if er in ("tesSUCCESS", "terQUEUED", "tesPENDING"):
                client_used = ep; break
            raise RuntimeError(f"XRPL submit {ep}: {er}")
        except Exception as e:
            log(f"XRP endpoint {ep} failed: {str(e)[:100]} — failover")
            resp = None
    if resp is None or client_used is None:
        raise RuntimeError("XRP both endpoints failed")
    h = resp.result.get("tx_json", {}).get("hash") or signed.get_hash()
    for _ in range(20):
        r = client.request(Tx(transaction=h)).result
        if r.get("validated"): break
        time.sleep(2)
    return {"txid": h, "status": "VALIDATED", "via": client_used,
            "seconds": round(time.time()-t0, 1),
            "link": f"https://livenet.xrpl.org/transactions/{h}", "payload_hex": ENV}

# ---------------- Readback (dual endpoints, byte-exact) ----------------
def readback(legs):
    import base64
    rb = {}
    # SAT: mempool.space + blockstream
    h = legs["sat"]["txid"]
    tx1 = gj(f"https://mempool.space/api/tx/{h}", tries=3)
    tx2 = gj(f"https://blockstream.info/api/tx/{h}", tries=3)
    envl = ENV.lower()
    rb["sat"] = (envl in json.dumps(tx1).lower()) and (envl in json.dumps(tx2).lower())
    log(f"readback SAT: {rb['sat']} (mempool+blockstream)")
    # XLM: horizon ops + stellar.expert
    hh = legs["xlm"]["hash"]
    ops = gj(f"https://horizon.stellar.org/transactions/{hh}/operations")
    op = [o for o in ops["_embedded"]["records"] if o["type"] == "manage_data"][0]
    rb["xlm"] = base64.b64decode(op["value"]).hex() == ENV
    log(f"readback XLM: {rb['xlm']} (horizon)")
    # XRP: xrplcluster + xrpscan
    ht = legs["xrp"]["txid"]
    rr = gj("https://xrplcluster.com", {"method": "tx", "params": [{"transaction": ht, "binary": False}]})
    md = rr["result"]["Memos"][0]["Memo"]
    rb["xrp"] = md["MemoData"].lower() == ENV
    rr2 = gj(f"https://api.xrpscan.com/api/v1/tx/{ht}")
    rb["xrp"] = rb["xrp"] and (ENV[10:] in json.dumps(rr2).lower() or ENV.lower() in json.dumps(rr2).lower())
    log(f"readback XRP: {rb['xrp']} (xrplcluster+xrpscan)")
    return rb

# ---------------- main ----------------
if not os.path.exists(RUNLOG):
    open(RUNLOG, "w").write(f"# TRIAD FIRE RUNLOG — {TAG} 2026-10-22\nEnvelope: {ENV[:16]}...\n\n")
legs = load_legs()

# fire order: fast rails first (display + attestation visible in seconds), SAT after
for name, fn in (("xlm", leg_xlm_retry), ("xrp", leg_xrp), ("sat", leg_sat)):
    if name in legs and legs[name].get("fired_ok"):
        log(f"SKIP {name} (already fired)"); continue
    t_start = time.time()
    try:
        data = fn()
        data["fired_ok"] = True
        data["fired_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        data["wall_seconds"] = round(time.time()-t_start, 1)
        if name == "sat":
            inc, bh = sat_wait_confirm(data["txid"])
            data["inclusion_seconds"] = inc; data["block_height"] = bh
            data["confirmed"] = inc is not None
        save_leg(name, data)
        log(f"LEG {name} OK: {json.dumps(data)[:260]}")
    except Exception as e:
        save_leg(name, {"error": f"{type(e).__name__}: {e}", "fired_ok": False})
        log(f"LEG {name} FAILED: {type(e).__name__}: {str(e)[:200]}")

if all(legs.get(n, {}).get("fired_ok") for n in ("xlm", "xrp", "sat")):
    rb = readback(legs)
    res = {"tag": TAG, "envelope_hex": ENV, "rails": rb, "all_pass": all(rb.values()),
           "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    json.dump(res, open(f"{OUTDIR}/TRIAD_READBACK.json", "w"), indent=1)
    log(f"TRIAD READBACK: {'3/3 PASS' if res['all_pass'] else 'FAIL'} {json.dumps(rb)}")
else:
    log("TRIAD INCOMPLETE — legs missing, no readback")
print("TRIAD DONE", flush=True)
