#!/usr/bin/env python3
"""WEEKLY BTC LEDGET CHECKPOINT — batched deep-tier anchor (Twelfth patent native architecture).
v1.0, 2026-10-24, doctrine: BATCHED_BTC_CHECKPOINT_SPEC.md (cadence: WEEKLY, Leon GO 2026-10-24).

Anchors sha256(LEDGER.md) — the receipt-chain head commitment — to Bitcoin once per week.
Envelope: SQDR + 0x13 (ledger-head checkpoint class) + sha256(ledger file at fire time).
- Pays the ECONOMY market rate (max(1, mempool minimumFee), 30 sat/vB hard ceiling).
- Spends the writer's single UTXO: chain continuity inherited from prior anchors.
- Patience window: 6h confirm deadline (fast rails carry instant proof per artifact).
- Readback: byte-exact from mempool.space + blockstream.info.
- DRY RUN: CHECKPOINT_DRYRUN=1 builds against a synthetic UTXO and never broadcasts.
"""
import json, time, hashlib, sys, os, urllib.request

RUNDIR = "/app/conversations/69b57685ca3719553a34597c/fh_pub/tokenization-adoption/checkpoint"
os.makedirs(RUNDIR, exist_ok=True)
LEGS = f"{RUNDIR}/CKPT_LEGS.json"
RUNLOG = f"{RUNDIR}/CKPT_RUNLOG.md"
LEDGER = "/app/conversations/69b57685ca3719553a34597c/fh_pub/LEDGER.md"
SW = "/app/tmp_push/fh_push/tokenization-adoption/seed-mode/dropbox/dropbox_writer_sw.py"
KEY = "/app/tmp_push/fh_push/tokenization-adoption/seed-mode/dropbox/dropbox_writer_key_mainnet.json"
ADDR = "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6"
FEE_CEIL = 30
DEADLINE_S = 21600
UA = {"Content-Type": "application/json", "User-Agent": "btc-ckpt/1.0"}

def gj(url, data=None, timeout=15, tries=3, backoff=4):
    for i in range(tries):
        try:
            body = json.dumps(data).encode() if data is not None else None
            r = urllib.request.urlopen(urllib.request.Request(url, data=body, headers=UA), timeout=timeout)
            return json.loads(r.read())
        except Exception:
            if i == tries - 1: raise
            time.sleep(backoff)

def log(line):
    with open(RUNLOG, "a") as f: f.write(line + "\n")
    print(line, flush=True)

def fee_guard():
    fees = gj("https://mempool.space/api/v1/fees/recommended")
    rate = max(1, fees.get("minimumFee", fees["fastestFee"]))
    if rate > FEE_CEIL:
        raise RuntimeError(f"fee ceiling: economy rate {rate} sat/vB > {FEE_CEIL} — holding, defer to next window")
    return rate

def main():
    dry = os.environ.get("CHECKPOINT_DRYRUN") == "1"
    rate = fee_guard()
    log(f"fee guard OK: economy rate {rate} sat/vB")
    digest = hashlib.sha256(open(LEDGER, "rb").read()).digest()
    payload = b"SQDR" + bytes([0x13]) + digest
    env = payload.hex()
    log(f"ledger head digest: {digest.hex()}")
    log(f"envelope: {env}")

    import importlib.util
    spec = importlib.util.spec_from_file_location("sw", SW)
    sw = importlib.util.module_from_spec(spec); spec.loader.exec_module(sw)
    sw.VERSION = 0x13
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(KEY))["wif"]
    secret = sw.CBitcoinSecret(wif)
    assert str(sw.wpkh_addr(secret)) == ADDR
    utxos = json.loads(sw.api("mainnet", f"/address/{ADDR}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO — rail unfunded, escalate")
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    log(f"UTXO: {utxo['txid']}:{utxo['vout']} ({utxo['value']} sats)")

    if dry:
        test_utxo = {"txid": "00"*32, "vout": 0, "value": utxo["value"]}
        raw, info = sw.build_signed_tx("mainnet", wif, test_utxo, digest, fee_rate=rate)
        log(f"DRY RUN: built {info['vsize']} vB tx, fee {info['fee']} sats (${info['fee']/1e8*80669:.3f}) — NOT broadcast")
        return

    raw, info = sw.build_signed_tx("mainnet", wif, utxo, digest, fee_rate=rate)
    t0 = time.time()
    txid = None; via = None
    try:
        txid = sw.api("mainnet", "/tx", raw); via = "mempool.space"
    except Exception as e1:
        log(f"mempool.space push failed ({str(e1)[:80]}) — failing over to blockstream")
        r = urllib.request.urlopen(urllib.request.Request(
            "https://blockstream.info/api/tx", data=raw.hex().encode(), headers=UA), timeout=20)
        txid = r.read().decode(); via = "blockstream.info"
    log(f"broadcast OK: {txid} via {via}, fee {info['fee']} sats")
    json.dump({"envelope_hex": env, "ledger_sha256": digest.hex(), "txid": txid,
               "fee_sats": info["fee"], "fee_rate": rate, "broadcast_via": via,
               "utxo_spent": f"{utxo['txid']}:{utxo['vout']}",
               "broadcast_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "confirmed": False},
              open(LEGS, "w"), indent=1)

    inc = bh = None
    while time.time() - t0 < DEADLINE_S:
        try:
            st = gj(f"https://mempool.space/api/tx/{txid}/status", tries=2, timeout=10)
            if st.get("confirmed"):
                inc, bh = round(time.time()-t0, 1), st.get("block_height")
                break
        except Exception:
            pass
        time.sleep(60)
    if inc is None:
        log(f"NOT CONFIRMED within {DEADLINE_S}s — leaving mempool-pending state in legs, check later")
        return

    tx1 = gj(f"https://mempool.space/api/tx/{txid}")
    tx2 = gj(f"https://blockstream.info/api/tx/{txid}")
    envl = env.lower()
    rb = (envl in json.dumps(tx1).lower()) and (envl in json.dumps(tx2).lower())
    d = json.load(open(LEGS))
    d.update({"confirmed": True, "block_height": bh, "confirm_seconds": inc,
              "readback_ok": rb,
              "confirmed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    json.dump(d, open(LEGS, "w"), indent=1)
    log(f"CONFIRMED at block {bh} in {inc}s — readback byte-exact: {rb}")
    if not rb: raise RuntimeError("READBACK FAILED — envelope not byte-exact, escalate")

if __name__ == "__main__":
    main()
