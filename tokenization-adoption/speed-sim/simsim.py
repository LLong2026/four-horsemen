#!/usr/bin/env python3
"""ROUTE SPEED SIM 2026-10-22 — Phase 2: TRANSFER SCENARIOS on all 12 certified rails.
Payload: SPEED-SIM-1 envelope SQDR + 0x10 (route speed-sim, first use) + sha256 tag digest.
Micro self-transfers only (value stays in program wallets; fees are the only cost).
Timing: build+sign+broadcast+confirm per leg; PoW rails polled to inclusion.
Disclosed as speed sim / training-class leg: no DOI, no ledger entry unless Leon GO.
"""
import json, time, hashlib, sys, os, urllib.request

sys.path.insert(0, "/app/conversations/69b57685ca3719553a34597c/mcr3")
import mcr3_crossfire as cf

SIMDIR = "/app/conversations/69b57685ca3719553a34597c/route-speed-sim"
cf.DIGEST = hashlib.sha256(b"SPEED-SIM-1|route-hardening|2026-10-22").digest()
cf.PAYLOAD = b"SQDR" + bytes([0x10]) + cf.DIGEST
cf.OUT = f"{SIMDIR}/SPEED_SIM_LEGS.json"
cf.RUNLOG = f"{SIMDIR}/SPEED_SIM_RUNLOG.md"
ENV = cf.PAYLOAD.hex()

# BTC leg with envelope version 0x10 (function-local sw.VERSION=0x06 is MCR-3's)
def leg_btc_ss():
    import importlib.util
    sw_path = f"{cf.TA}/seed-mode/dropbox/dropbox_writer_sw.py"
    spec = importlib.util.spec_from_file_location("sw", sw_path)
    sw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sw)
    sw.VERSION = 0x10
    sw.bitcoin.SelectParams("mainnet")
    wif = json.load(open(f"{cf.TA}/seed-mode/dropbox/dropbox_writer_key_mainnet.json"))["wif"]
    secret = sw.CBitcoinSecret(wif)
    addr = sw.wpkh_addr(secret)
    assert str(addr) == "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6"
    utxos = json.loads(sw.api("mainnet", f"/address/{addr}/utxo"))
    if not utxos: raise RuntimeError("no BTC UTXO")
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    t0 = time.time()
    raw, info = sw.build_signed_tx("mainnet", wif, utxo, cf.DIGEST)
    txid = sw.api("mainnet", "/tx", raw)
    return {"txid": txid, "fee_sats": info["fee"], "seconds": round(time.time()-t0, 1),
            "link": f"https://mempool.space/tx/{txid}", "payload_hex": ENV,
            "utxo": f"{utxo['txid']}:{utxo['vout']}"}

LEGS = dict(cf.LEGS)  # name -> fn
LEGS["btc"] = leg_btc_ss
ORDER = ["xlm", "xrp", "sol", "algo", "avax", "eth", "dot", "atom", "ada", "ltc", "doge", "btc"]

def poll_pow(name, txid, deadline_s=600):
    """Poll block inclusion for PoW rails, return seconds to inclusion or None."""
    t0 = time.time()
    urls = {
        "ltc": f"https://litecoinspace.org/api/tx/{txid}/status",
        "doge": f"https://dogeblock.com/api/tx/{txid}",  # fallback handled by loop
        "btc": f"https://blockstream.info/api/tx/{txid}/status",
    }
    import json as j
    while time.time() - t0 < deadline_s:
        try:
            if name == "doge":
                r = urllib.request.urlopen(urllib.request.Request(
                    f"https://api.blockchair.com/dogecoin/dashboards/transaction/{txid}",
                    headers={"User-Agent": "speedsim"}), timeout=25)
                d = j.loads(r.read())["data"]
                if txid in d and d[txid].get("transaction", {}).get("block_id", 0) > 0:
                    return round(time.time() - t0, 1)
            else:
                r = urllib.request.urlopen(urllib.request.Request(urls[name],
                    headers={"User-Agent": "speedsim"}), timeout=25)
                d = j.loads(r.read())
                if d.get("confirmed"):
                    return round(time.time() - t0, 1)
        except Exception:
            pass
        time.sleep(12)
    return None

with open(cf.RUNLOG, "w") as f:
    f.write(f"# ROUTE SPEED SIM — transfer scenarios 2026-10-22\n\nEnvelope: `{ENV[:16]}...`\nPayload: SQDR + 0x10 (route speed-sim) + sha256(SPEED-SIM-1|route-hardening|2026-10-22)\n\n")

for name in ORDER:
    if name in cf.load_legs() and cf.load_legs()[name].get("fired_ok"):
        print(f"SKIP {name}"); continue
    t_start = time.time()
    try:
        data = LEGS[name]()
        data["fired_ok"] = True
        data["wall_seconds"] = round(time.time() - t_start, 1)
        data["fired_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if name in ("ltc", "doge", "btc"):
            data["broadcast_seconds"] = data.get("seconds")
            inc = poll_pow(name, data["txid"])
            data["inclusion_seconds"] = inc
            data["confirmed"] = inc is not None
        cf.save_leg(name, data)
        with open(cf.RUNLOG, "a") as f:
            f.write(f"- {name}: {json.dumps(data)[:300]}\n")
        print(f"== {name} OK: {json.dumps(data)[:220]}", flush=True)
    except Exception as e:
        cf.save_leg(name, {"error": f"{type(e).__name__}: {e}", "fired_ok": False})
        with open(cf.RUNLOG, "a") as f:
            f.write(f"- {name} FAILED: {type(e).__name__}: {str(e)[:200]}\n")
        print(f"== {name} FAILED: {type(e).__name__}: {e}", flush=True)

open(f"{SIMDIR}/SPEED_SIM_ENVELOPE.txt", "w").write(ENV)
print("TRANSFER SCENARIOS DONE", flush=True)
