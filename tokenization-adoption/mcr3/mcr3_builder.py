#!/usr/bin/env python3
"""MCR-3 MMR builder — byte-exact MCR-1 covenant spec (validated against MCR-1 and MCR-2 frozen roots).
leaf:  SHA-256(0x00 || sha256(file)); parent: SHA-256(0x01||L||R); bag right-to-left;
root:  SHA-256(0x03 || bag || leaf_count u64 LE). Fast blob read via git cat-file --batch.
"""
import subprocess, hashlib, json, sys

REPO = "/app/tmp_push/fh_push"

def blob_bytes(commit):
    paths = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "--name-only", commit],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    paths = sorted(paths, key=lambda p: p.encode())
    # get blob SHAs in one call
    ls = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", commit],
                        capture_output=True, text=True, check=True).stdout.splitlines()
    oid_of = {}
    for line in ls:
        meta, p = line.split("\t", 1)
        oid_of[p] = meta.split()[2]
    proc = subprocess.Popen(["git", "-C", REPO, "cat-file", "--batch"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    blobs = {}
    for p in paths:
        proc.stdin.write((oid_of[p] + "\n").encode()); proc.stdin.flush()
        hdr = proc.stdout.readline().decode().strip()
        n = int(hdr.rsplit(" ", 1)[1])
        blobs[p] = proc.stdout.read(n); proc.stdout.read(1)
    proc.stdin.close(); proc.wait()
    return paths, [hashlib.sha256(blobs[p]).digest() for p in paths]

def fold(leaves):
    stack = []
    for leaf in leaves:
        stack.append([0, leaf])
        while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
            right = stack.pop(); left = stack.pop()
            stack.append([left[0] + 1, hashlib.sha256(b"\x01" + left[1] + right[1]).digest()])
    peaks = list(stack)
    bag = peaks[-1][1]
    for h, hh in reversed(peaks[:-1]):
        bag = hashlib.sha256(b"\x01" + hh + bag).digest()
    root = hashlib.sha256(b"\x03" + bag + len(leaves).to_bytes(8, "little")).digest()
    return root, peaks

if __name__ == "__main__":
    # GATE 1: MCR-1 commit 7c492528 -> root 2d1a3214...
    paths, leaves = blob_bytes("7c492528c9f9624bb43846b745df9a480f4d1600")
    r, _ = fold(leaves)
    ok1 = r.hex() == "2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a"
    print(f"GATE1 MCR-1 refold ({len(leaves)} leaves): {r.hex()} -> {'PASS' if ok1 else 'FAIL'}")
    assert ok1
    # GATE 2: MCR-2 commit bf13210 -> root 1929707e...
    paths, leaves = blob_bytes("bf13210")
    r, peaks = fold(leaves)
    ok2 = r.hex() == "1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60"
    print(f"GATE2 MCR-2 refold ({len(leaves)} leaves): {r.hex()} -> {'PASS' if ok2 else 'FAIL'}")
    assert ok2
    # MCR-3: current HEAD
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    paths, leaves = blob_bytes(head)
    r, peaks = fold(leaves)
    out = {"commit": head, "leaf_count": len(leaves), "root": r.hex(),
           "peaks": [[h, hh.hex()] for h, hh in peaks]}
    json.dump(out, open("MCR3_FOLD.json", "w"), indent=2)
    with open("MCR3_LEAF_INDEX.json", "w") as f:
        json.dump({"commit": head, "leaf_count": len(leaves),
                   "leaves": [l.hex() for l in leaves]}, f)
    print(f"MCR-3 FOLD @ {head[:12]}: {len(leaves)} leaves, peaks {'/'.join(str(h) for h,_ in peaks)}")
    print(f"MCR-3 ROOT: {r.hex()}")
    envelope = "5351445206" + r.hex()
    print(f"ENVELOPE hex: {envelope}")
    open("MCR3_ENVELOPE.txt", "w").write(envelope)
