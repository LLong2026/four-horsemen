#!/usr/bin/env python3
"""SIP-042 DROPBOX writer — segwit P2WPKH (tb1q) — TESTNET4 prototype.
Doctrine unchanged (frozen prereg sha 25a45075): D1 transfer-only, D2 binary,
D3 postage-only fee, D4 writer-side key only, D5 deterministic OP_RETURN payload.
BIP143 P2WPKH signing validated against the official BIP-143 Native P2WPKH
test vector (run --selftest).
Usage: dropbox_writer_sw.py --network testnet4 --seed-file seed.bin
"""
import argparse, hashlib, json, os, sys, urllib.request
import bitcoin
from bitcoin.core import CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, lx, CScript
from bitcoin.wallet import CBitcoinSecret, P2WPKHBitcoinAddress
from bitcoin.core.script import OP_RETURN, OP_0, SIGHASH_ALL, CScriptWitness
from bitcoin.core import CTxWitness, CTxInWitness

MARKER = b"SQDR"
VERSION = 0x01

def api(net, path, data=None):
    base = {"testnet4": "https://mempool.space/testnet4/api",
            "testnet": "https://blockstream.info/testnet/api",
            "mainnet": "https://blockstream.info/api"}[net]
    req = urllib.request.Request(base + path,
                                 data=(data.encode() if isinstance(data, str) else data),
                                 headers={"Content-Type": "text/plain"})
    return urllib.request.urlopen(req, timeout=60).read().decode()


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
    """Enforce SCRIPT_VERIFY_LOW_S standard policy: s = min(s, n-s)."""
    r, s = der_parse(sig)
    if s > N // 2: s = N - s
    return der_encode(r, s)

def wpkh_addr(secret):
    h160 = hashlib.new("ripemd160", sha(bytes(secret.pub))).digest()
    return P2WPKHBitcoinAddress.from_scriptPubKey(CScript([OP_0, h160]))

def sha(b): return hashlib.sha256(b).digest()
def dsha(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def bip143_sighash_p2wpkh(tx, idx, amount, h160, hashtype=SIGHASH_ALL):
    """BIP143 digest for native P2WPKH input. scriptCode is the 25-byte
    P2PKH script of the pubkey hash, varint-prefixed (0x19)."""
    script_code = b"\x19\x76\xa9\x14" + h160 + b"\x88\xac"
    prevouts = b"".join(txin.prevout.serialize() for txin in tx.vin)
    seqs = b"".join(txin.nSequence.to_bytes(4, "little") for txin in tx.vin)
    outs = b"".join(txout.serialize() for txout in tx.vout)
    preimage = (
        tx.nVersion.to_bytes(4, "little") +
        dsha(prevouts) +
        dsha(seqs) +
        tx.vin[idx].prevout.serialize() +
        script_code +
        amount.to_bytes(8, "little") +
        tx.vin[idx].nSequence.to_bytes(4, "little") +
        dsha(outs) +
        tx.nLockTime.to_bytes(4, "little") +
        hashtype.to_bytes(4, "little")
    )
    return dsha(preimage)

def build_signed_tx(net, wif, utxo, seed):
    bitcoin.SelectParams("testnet" if net != "mainnet" else "mainnet")
    secret = CBitcoinSecret(wif)
    addr = wpkh_addr(secret)
    h160 = hashlib.new("ripemd160", sha(bytes(secret.pub))).digest()
    payload = MARKER + bytes([VERSION]) + seed
    value = utxo["value"]
    if value - 546 < 150:
        print(f"UTXO too small to fund a drop ({value} sats) — binary verdict: NOT FUNDED (D2)")
        return None, None

    txin = CMutableTxIn(COutPoint(lx(utxo["txid"]), utxo["vout"]))
    txin.scriptSig = CScript()
    txout_drop = CMutableTxOut(0, CScript([OP_RETURN, payload]))
    txout_change = CMutableTxOut(value - 300, addr.to_scriptPubKey())
    tx = CMutableTransaction([txin], [txout_drop, txout_change])
    pub = bytes(secret.pub)

    def assemble(fee):
        txout_change.nValue = value - fee
        sighash = bip143_sighash_p2wpkh(tx, 0, value, h160)
        sig = low_s(secret.sign(sighash)) + b"\x01"
        tx.wit = CTxWitness([CTxInWitness(CScriptWitness([sig, pub]))])
        return tx.serialize()

    # two-pass fee: measure vsize with a provisional fee, then finalize
    provisional = assemble(300)
    tx.wit = CTxWitness()
    base_size = len(tx.serialize())
    vsize = (3 * base_size + len(provisional) + 3) // 4
    fee = max(150, min(1500, 5 * vsize, value - 546))
    raw = assemble(fee)
    return raw.hex(), {"address": str(addr), "fee": fee, "vsize": vsize,
                       "payload": payload.hex()}

def selftest():
    """Reproduce the official BIP-143 Native P2WPKH vector."""
    from bitcoin.core import x, lx, CTransaction
    utx = ("0100000002fff7f7881a8099afa6940d42d1e7f6362bec38171ea3edf433541db4e4ad969f"
           "00000000494830450221008b9d1dc26ba6a9cb62127b02742fa9d754cd3bebf337f7a55d114"
           "c8e5cdd30be022040529b194ba3f9281a99f2b1c0a19c0489bc22ede944ccf4ecbab4cc618"
           "ef3ed01eeffffffef51e1b804cc89d182d279655c3aa89e815b1b309fe287d9b2b55d57b90"
           "ec68a0100000000ffffffff02202cb206000000001976a9148280b37df378db99f66f85c95a"
           "783a76ac7a6d5988ac9093510d000000001976a9143bde42dbee7e4dbe6a21b2d50ce2f01"
           "67faa815988ac11000000")
    bitcoin.SelectParams("testnet")
    tx = CMutableTransaction.from_tx(CTransaction.deserialize(x(utx)))
    priv = "619c335025c7f4012e556c2a58b2506e30b8511b53ade95ea316fd8c3286feb9"
    secret = CBitcoinSecret.from_secret_bytes(x(priv))
    amount = 600000000
    h = bip143_sighash_p2wpkh(tx, 1, amount, x("1d0f172a0ecb48aee1be1f2687d2963ae33f71a1"))
    exp_hash = "c37af31116d1b27caf68aae9e3ac82f1477929014d5b917657d0eb49478cb670"
    assert h.hex() == exp_hash, f"sighash mismatch: {h.hex()}"
    # our signing is non-deterministic (OpenSSL k), so the vector's exact
    # signature bytes are not reproducible; instead we PROVE the digest
    # byte-exactly and prove our own signature is EC-valid for the pubkey.
    sig = low_s(secret.sign(h))
    from bitcoin.core.key import CPubKey
    pub = CPubKey(x("025476c2e83188368da1ff3e292e7acafcdb3566bb0ad253f62fc70f07aeee6357"))
    assert pub.verify(h, sig), "own signature failed EC verification"
    print("BIP143 SELFTEST: sigHash byte-exact MATCH to official vector + EC-valid low-S signature — PASS")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--network", default="testnet4", choices=["testnet", "testnet4", "mainnet"])
    p.add_argument("--keyfile", default="dropbox_writer_key.json")
    p.add_argument("--seed-file")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest:
        selftest(); return 0

    if not args.seed_file:
        print("--seed-file required (32 bytes, D5)"); return 2
    bitcoin.SelectParams("testnet" if args.network != "mainnet" else args.network)
    seed = open(args.seed_file, "rb").read()
    assert len(seed) == 32, "seed must be exactly 32 bytes (D5 determinism)"

    if os.path.exists(args.keyfile):
        wif = json.load(open(args.keyfile))["wif"]
    else:
        wif = str(CBitcoinSecret.from_secret_bytes(os.urandom(32)))
        json.dump({"wif": wif, "note": "writer-side key only; fee postage only; never in reader"},
                  open(args.keyfile, "w"))
    secret = CBitcoinSecret(wif)
    addr = wpkh_addr(secret)
    print(f"writer address (segwit, {args.network}): {addr}")

    utxos = json.loads(api(args.network, f"/address/{addr}/utxo"))
    if not utxos:
        print(f"NO UTXO — faucet needed. Send {args.network} coins to: {addr}")
        return 2
    utxo = sorted(utxos, key=lambda u: u["value"])[-1]
    print(f"spending utxo {utxo['txid']}:{utxo['vout']} ({utxo['value']} sats)")
    raw, info = build_signed_tx(args.network, wif, utxo, seed)
    if raw is None:
        return 2
    txid = api(args.network, "/tx", raw)
    print(f"BROADCAST OK — txid: {txid}")
    print(f"fee: {info['fee']} sats (adaptive)")
    print(f"OP_RETURN payload: {info['payload']}")
    print(f"seed sha256: {hashlib.sha256(seed).hexdigest()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
