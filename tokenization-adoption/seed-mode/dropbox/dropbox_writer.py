#!/usr/bin/env python3
"""SIP-042 DROPBOX writer — TESTNET prototype.
Doctrine (frozen prereg sha 25a45075):
  D1 transfer-only (delivers, retains nothing)   D2 binary outcome (lands or not)
  D3 no monetary function (fee = postage only)   D4 keys live ONLY on the writer side
  D5 deterministic destination (marker||version||seed in OP_RETURN)
Payload: 4-byte marker + version byte + 32-byte seed = 37 bytes (OP_RETURN max 80).
Usage: dropbox_writer.py --network testnet --seed-file seed.bin
"""
import argparse, hashlib, json, os, sys, urllib.request
import bitcoin
from bitcoin.core import CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, CScript, lx
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.core.script import OP_RETURN, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

MARKER = b"SQDR"
VERSION = 0x01

def api(net, path, data=None):
    base = {"testnet": "https://blockstream.info/testnet/api",
            "testnet4": "https://mempool.space/testnet4/api",
            "mainnet": "https://blockstream.info/api"}[net]
    req = urllib.request.Request(base + path,
                                 data=(data.encode() if isinstance(data, str) else data),
                                 headers={"Content-Type": "text/plain"})
    return urllib.request.urlopen(req, timeout=60).read().decode()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--network", default="testnet", choices=["testnet", "testnet4", "mainnet"])
    p.add_argument("--keyfile", default="dropbox_writer_key.json")
    p.add_argument("--seed-file", required=True)
    args = p.parse_args()

    bitcoin.SelectParams("testnet" if args.network in ("testnet", "testnet4") else args.network)
    seed = open(args.seed_file, "rb").read()
    assert len(seed) == 32, "seed must be exactly 32 bytes (D5 determinism)"
    payload = MARKER + bytes([VERSION]) + seed

    # D4: writer-side key only
    if os.path.exists(args.keyfile):
        wif = json.load(open(args.keyfile))["wif"]
    else:
        wif = str(CBitcoinSecret.from_secret_bytes(os.urandom(32)))
        json.dump({"wif": wif, "network": args.network,
                   "note": "writer-side key only; fee postage only; never in reader"},
                  open(args.keyfile, "w"))
    secret = CBitcoinSecret(wif)
    addr = P2PKHBitcoinAddress.from_pubkey(secret.pub)
    print(f"writer address ({args.network}): {addr}")

    utxos = json.loads(api(args.network, f"/address/{addr}/utxo"))
    if not utxos:
        print(f"NO UTXO — faucet needed. Send {args.network} coins to: {addr}")
        return 2
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    print(f"spending utxo {utxo['txid']}:{utxo['vout']} ({utxo['value']} sats)")

    txin = CMutableTxIn(COutPoint(lx(utxo["txid"]), utxo["vout"]))
    # adaptive fee: never exceed the input, always leave a spendable change (>= dust 546)
    fee = max(150, min(1500, utxo["value"] - 546))
    if utxo["value"] - fee < 546:
        print(f"UTXO too small to fund a drop ({utxo['value']} sats) — binary verdict: NOT FUNDED (D2)")
        return 2
    print(f"fee: {fee} sats (adaptive)")
    txout_drop = CMutableTxOut(0, CScript([OP_RETURN, payload]))
    txout_change = CMutableTxOut(utxo["value"] - fee, addr.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout_drop, txout_change])

    sighash = SignatureHash(addr.to_scriptPubKey(), tx, 0, SIGHASH_ALL)
    sig = secret.sign(sighash) + b"\x01"
    txin.scriptSig = CScript([sig, secret.pub])
    VerifyScript(txin.scriptSig, addr.to_scriptPubKey(), tx, 0, (SCRIPT_VERIFY_P2SH,))

    raw = tx.serialize().hex()
    txid = api(args.network, "/tx", raw)
    print(f"BROADCAST OK — txid: {txid}")
    print(f"OP_RETURN payload: {payload.hex()}")
    print(f"seed sha256: {hashlib.sha256(seed).hexdigest()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
