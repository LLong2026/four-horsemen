#!/usr/bin/env python3
"""SIP-042 CUSTODY TRANSFER — ownership demonstration (transfer-only, D1/D3 doctrine).
The tokenized asset NEVER moves: the hash is stationary on chain, pullable by any viewer.
Ownership = control of the custody satoshis. Each transfer re-anchors the artifact hash.
BIP143 signing identical to the proven mainnet writer (dropbox_writer_sw.py).
"""
import argparse, hashlib, json, sys, urllib.request
import bitcoin
bitcoin.SelectParams("mainnet")
from bitcoin.core import CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, lx
from bitcoin.core.script import CScript, OP_RETURN
from bitcoin.wallet import CBitcoinSecret, P2WPKHBitcoinAddress
from bitcoin.core import CTxInWitness
from bitcoin.core.script import CScriptWitness

MARKER = b"SQDR"
VERSION_CUSTODY = 0x02
FEE_SATS = 800

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

def pubkey_to_addr(pub):
    h160 = hashlib.new("ripemd160", hashlib.sha256(bytes(pub)).digest()).digest()
    return P2WPKHBitcoinAddress.from_scriptPubKey(CScript([0x00, h160]))

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
    p.add_argument("--from-keyfile", required=True)
    p.add_argument("--to-address", required=True)
    p.add_argument("--asset-hash", required=True)
    p.add_argument("--label", default="CUSTODY")
    a = p.parse_args()

    wif = json.load(open(a.from_keyfile))["wif"]
    secret = CBitcoinSecret(wif)
    from_addr = pubkey_to_addr(secret.pub)
    to_addr = P2WPKHBitcoinAddress(a.to_address)
    assert str(to_addr).startswith("bc1q")

    utxos = json.loads(api(f"/address/{from_addr}/utxo"))
    if not utxos: print("NO UTXO in holder wallet"); return 2
    total_in = sum(u["value"] for u in utxos)
    print(f"holder: {from_addr} | utxos: {len(utxos)} | total: {total_in} sats")

    payload = MARKER + bytes([VERSION_CUSTODY]) + bytes.fromhex(a.asset_hash)
    txins = [CMutableTxIn(COutPoint(lx(u["txid"]), u["vout"])) for u in utxos]
    value_out = total_in - FEE_SATS
    tx = CMutableTransaction(txins, [
        CMutableTxOut(0, CScript([OP_RETURN, payload])),
        CMutableTxOut(value_out, to_addr.to_scriptPubKey())])

    pub = bytes(secret.pub)
    h160 = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
    for n, u in enumerate(utxos):
        sighash = bip143_sighash(tx, n, u["value"], h160)
        sig = low_s(secret.sign(sighash)) + b"\x01"
        tx.wit.vtxinwit[n] = CTxInWitness(CScriptWitness([sig, pub]))

    raw = tx.serialize().hex()
    txid = api("/tx", raw)
    print(f"CUSTODY TRANSFER [{a.label}] BROADCAST OK")
    print(f"txid: {txid}")
    print(f"from: {from_addr}")
    print(f"to:   {to_addr}")
    print(f"sats: {value_out} (fee {FEE_SATS})")
    print(f"re-anchored asset hash: {a.asset_hash}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
