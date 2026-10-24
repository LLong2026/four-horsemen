#!/usr/bin/env python3
"""Fractional satoshi ownership-transfer hop (UAS TransferJob worker harness).
Envelope: SQDR + 0x12 (ownership transport) + artifact sha256 = 42 bytes OP_RETURN.
Usage: fractal_hop_fire.py --dest <btc_addr> --fraction <pct 1-100> --digest <hex64>
Signing identical to the proven XFER-1 / FRACTAL-1 mainnet hops (BIP-143 P2WPKH, low-S).
"""
import argparse, hashlib, json, urllib.request
import bitcoin
bitcoin.SelectParams("mainnet")
from bitcoin.core import CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, lx, CTxInWitness
from bitcoin.core.script import CScript, OP_RETURN, CScriptWitness
from bitcoin.wallet import CBitcoinSecret, P2WPKHBitcoinAddress

WRITER = "bc1qf4zs0fwvmdptq86xdg6rrfc5unqgmhdwharzw6"  # UAS BTC writer (sole funded program source)
FEE_CEIL_SAT_VB = 30
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def der_parse(sig):
    assert sig[0] == 0x30
    i = 2
    assert sig[i] == 0x02; l = sig[i+1]; r = int.from_bytes(sig[i+2:i+2+l], "big"); i += 2 + l
    assert sig[i] == 0x02; l = sig[i+1]; s = int.from_bytes(sig[i+2:i+2+l], "big")
    return r, s

def der_encode(r, s):
    def enc(i):
        b = i.to_bytes((i.bit_length() + 7) // 8 or 1, "big")
        if b[0] & 0x80: b = b"\x00" + b
        return bytes([0x02, len(b)]) + b
    body = enc(r) + enc(s)
    return bytes([0x30, len(body)]) + body

def low_s(sig):
    r, s = der_parse(sig)
    if s > N // 2: s = N - s
    return der_encode(r, s)

def bip143_sighash(tx, idx, amount, h160):
    h = lambda b: hashlib.sha256(b).digest()
    prevouts = b"".join(i.prevout.serialize() for i in tx.vin)
    seqs = b"".join(i.nSequence.to_bytes(4, "little") for i in tx.vin)
    outs = b"".join(o.serialize() for o in tx.vout)
    script_code = b"\x19\x76\xa9\x14" + h160 + b"\x88\xac"
    pre = (tx.nVersion.to_bytes(4, "little") + h(h(prevouts)) + h(h(seqs))
           + tx.vin[idx].prevout.serialize() + script_code
           + amount.to_bytes(8, "little") + tx.vin[idx].nSequence.to_bytes(4, "little")
           + h(h(outs)) + tx.nLockTime.to_bytes(4, "little") + (1).to_bytes(4, "little"))
    return h(h(pre))

def api(path, data=None):
    req = urllib.request.Request("https://mempool.space/api" + path,
        data=(data.encode() if isinstance(data, str) else data),
        headers={"Content-Type": "text/plain"})
    return urllib.request.urlopen(req, timeout=60).read().decode()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dest", required=True)
    p.add_argument("--fraction", type=float, required=True)
    p.add_argument("--digest", required=True)
    p.add_argument("--wif-file", default="/app/tmp_push/fh_push/tokenization-adoption/seed-mode/dropbox/dropbox_writer_key_mainnet.json")
    a = p.parse_args()
    assert 1 <= a.fraction <= 100, "fraction out of range"
    assert len(a.digest) == 64 and int(a.digest, 16) >= 0, "digest must be 64-hex"
    secret = CBitcoinSecret(json.load(open(a.wif_file))["wif"])
    h160 = hashlib.new("ripemd160", hashlib.sha256(bytes(secret.pub)).digest()).digest()
    from_addr = P2WPKHBitcoinAddress.from_scriptPubKey(CScript([0x00, h160]))
    assert str(from_addr) == WRITER, f"source mismatch {from_addr}"
    to_addr = P2WPKHBitcoinAddress(a.dest)
    assert str(to_addr) == a.dest, "dest not P2WPKH"
    env_hex = "5351445212" + a.digest

    fees = json.loads(api("/v1/fees/recommended"))
    fee_rate = min(max(1, fees.get("minimumFee", fees["fastestFee"])), FEE_CEIL_SAT_VB)  # economy doctrine
    est_vb = 190
    fee = max(300, int(fee_rate * est_vb))

    utxos = json.loads(api(f"/address/{from_addr}/utxo"))
    conf = sorted([u for u in utxos if u["status"]["confirmed"]], key=lambda u: -u["value"])
    assert conf, "no confirmed UTXOs"
    total = sum(u["value"] for u in conf)
    send = int(total * a.fraction / 100)
    assert send >= 546, f"dust: send {send}"
    assert total - send >= fee, "insufficient for fee"

    picked, acc = [], 0
    for u in conf:
        picked.append(u); acc += u["value"]
        if acc >= send + fee: break
    assert acc >= send + fee, "insufficient balance"
    change = acc - send - fee

    tx = CMutableTransaction(
        vin=[CMutableTxIn(COutPoint(lx(u["txid"]), u["vout"]), nSequence=0xFFFFFFFF) for u in picked],
        vout=[
            CMutableTxOut(send, to_addr.to_scriptPubKey()),
            CMutableTxOut(0, CScript([OP_RETURN, bytes.fromhex(env_hex)])),
            CMutableTxOut(change, from_addr.to_scriptPubKey()),
        ], nVersion=1, nLockTime=0)
    for i, u in enumerate(picked):
        sig_hash = bip143_sighash(tx, i, u["value"], h160)
        sig = low_s(secret.sign(sig_hash)) + b"\x01"
        tx.wit.vtxinwit.append(CTxInWitness(CScriptWitness([sig, bytes(secret.pub)])))
    raw = tx.serialize().hex()
    assert env_hex in raw, "envelope missing"
    try:
        txid = api("/tx", raw)
    except urllib.error.HTTPError as e:
        print("BROADCAST ERROR BODY:", e.read().decode()[:400]); raise
    print(json.dumps({"txid": txid, "sats_sent": send, "fee_sats": fee,
                      "change_sats": change, "source_balance_sats": total}))

if __name__ == "__main__":
    main()
