#!/usr/bin/env python3
"""CAGE-M1 fold tool — genesis fold of the dedicated LLM-caging mountain.
Covenant spec (frozen MCR-1 covenant, byte-identical to the corrected mcr4_fold.py):
  leaf   = SHA-256(0x00 || sha256(file))
  parent = SHA-256(0x01 || L || R)
  peaks bagged right-to-left: bag starts at rightmost peak; then for each peak
  leftward, bag = SHA-256(0x01 || peak || bag)
  root   = SHA-256(0x03 || bag || leaf_count u64 LE)
Corpus: tokenization-adoption/cage_m1_corpus/ — every file in the folder is a leaf,
sorted by UTF-8 byte order of path. No file-level selection, no exclusions.
Envelope: SQDR + 0x07 + root (new CAGE series version byte, distinct from the
MCR series 0x06 mountain-update covenant).
Determinism gate: this fold() is byte-identical to mcr4_fold.py's fold() on
identical leaf inputs (verified in __main__ against random leaves).
"""
import hashlib, json, os, random

CORPUS = "/app/tmp_push/fh_push/tokenization-adoption/cage_m1_corpus"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "CAGE_M1_FOLD.json")
IDX = os.path.join(HERE, "CAGE_M1_LEAF_INDEX.json")

def sha256(b): return hashlib.sha256(b).digest()

def fold(leaves):
    stack = []
    for leaf in leaves:
        stack.append([0, leaf])
        while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
            r = stack.pop(); l = stack.pop()
            stack.append([l[0] + 1, sha256(b"\x01" + l[1] + r[1])])
    peaks = list(stack)
    bag = peaks[-1][1]
    for h, hh in reversed(peaks[:-1]):
        bag = sha256(b"\x01" + hh + bag)
    return sha256(b"\x03" + bag + len(leaves).to_bytes(8, "little")), peaks

def mcr4_fold_ref(leaves):
    # verbatim from tokenization-adoption/mcr4/mcr4_fold.py (proven MCR-1/2/3 gates)
    stack = []
    for leaf in leaves:
        stack.append([0, leaf])
        while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
            r = stack.pop(); l = stack.pop()
            stack.append([l[0] + 1, hashlib.sha256(b"\x01" + l[1] + r[1]).digest()])
    peaks = list(stack); bag = peaks[-1][1]
    for h, hh in reversed(peaks[:-1]):
        bag = hashlib.sha256(b"\x01" + hh + bag).digest()
    return hashlib.sha256(b"\x03" + bag + len(leaves).to_bytes(8, "little")).digest(), peaks

def main():
    # DETERMINISM GATE: byte-identical to the proven MCR-4 tool on random inputs
    rng = random.Random(7)
    for n in (1, 2, 3, 4, 7, 12, 33):
        ls = [sha256(bytes([n]) + rng.randbytes(16)) for _ in range(n)]
        a = fold(ls)[0]; b = mcr4_fold_ref(ls)[0]
        assert a == b, f"fold divergence at n={n}"
    print("DETERMINISM GATE PASS (fold byte-identical to mcr4_fold.py, n=1,2,3,4,7,12,33)")

    names = sorted(os.listdir(CORPUS), key=lambda n: n.encode())
    leaves, index = [], []
    for n in names:
        p = os.path.join(CORPUS, n)
        assert os.path.isfile(p)
        with open(p, "rb") as f:
            blob = f.read()
        leaves.append(sha256(b"\x00" + sha256(blob)))
        index.append({"path": n, "file_sha256": sha256(blob).hex(),
                      "leaf": leaves[-1].hex()})
    root, peaks = fold(leaves)
    result = {
        "series": "CAGE-M1",
        "covenant": "leaf=SHA-256(0x00||sha256(file)); parent=SHA-256(0x01||L||R); bag=rightmost peak, then bag=SHA-256(0x01||peak||bag) leftward; root=SHA-256(0x03||bag||leaf_count u64 LE)",
        "corpus_dir": "tokenization-adoption/cage_m1_corpus/",
        "leaf_count": len(leaves),
        "root": root.hex(),
        "peaks": [[h, d.hex()] for h, d in peaks],
        "envelope_hex_ascii": "5351445207" + root.hex(),
    }
    json.dump(result, open(OUT, "w"), indent=1)
    json.dump(index, open(IDX, "w"), indent=1)
    print(json.dumps(result, indent=1))

if __name__ == "__main__":
    main()
