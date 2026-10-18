#!/usr/bin/env python3
"""SIP-042 DROPBOX reader — chain-pull recovery. THE BOX: read-only, keyless,
never signs, never broadcasts (D4 reader purity). Pull the tx, extract the
OP_RETURN, hand back the seed. Anyone can run this. Anyone."""
import argparse, json, sys, urllib.request, hashlib

MARKER, VERSION = b"SQDR", 0x01

def api(net, path):
    base = {"testnet": "https://blockstream.info/testnet/api",
            "testnet4": "https://mempool.space/testnet4/api",
            "mainnet": "https://blockstream.info/api"}[net]
    return json.loads(urllib.request.urlopen(base + path, timeout=60).read())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--network", default="testnet", choices=["testnet", "testnet4", "mainnet"])
    p.add_argument("--txid", required=True)
    a = p.parse_args()
    tx = api(a.network, f"/tx/{a.txid}")
    found = None
    for i, vout in enumerate(tx["vout"]):
        asm = vout.get("scriptpubkey_asm", "")
        if "OP_RETURN" in asm and vout.get("scriptpubkey_type") in ("op_return", "OP_RETURN"):
            payload = bytes.fromhex(vout["scriptpubkey"])
            # scriptpubkey hex = OP_RETURN(0x6a) + push(len) + data
            found = payload
    if not found:
        print("NO OP_RETURN OUTPUT — binary verdict: NOT DELIVERED (D2)")
        return 1
    # parse: 0x6a <len> <data>
    assert found[0] == 0x6a, "not OP_RETURN"
    ln = found[1]
    data = found[2:2+ln]
    if data[:4] != MARKER or data[4] != VERSION:
        print(f"UNRECOGNIZED MARKER: {data[:5].hex()} — not a DROPBOX payload")
        return 1
    seed = data[5:]
    print(f"DROPBOX PAYLOAD FOUND in tx {a.txid}")
    print(f"seed (hex): {seed.hex()}")
    print(f"seed sha256: {hashlib.sha256(seed).hexdigest()}")
    print(f"block height: {tx.get('status', {}).get('block_height')}")
    print("BINARY VERDICT: DELIVERED (D2)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
