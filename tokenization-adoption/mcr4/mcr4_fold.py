#!/usr/bin/env python3
"""MCR-4 fold tool — corrected covenant spec (forward-only fix of the mcr3_builder.py
leaf-wrapper defect disclosed in the MCR-4 runlog). leaf = SHA-256(0x00 || sha256(file));
parent = SHA-256(0x01||L||R); peaks bagged right-to-left;
root = SHA-256(0x03 || bag || leaf_count u64 LE).
Gates: reproduces MCR-1 2d1a3214..., MCR-2 1929707e..., MCR-3 418fc5a8... byte-identical.
"""
import subprocess, hashlib, json, sys

REPO = "/app/tmp_push/fh_push"
def leaf_digests(commit):
    paths = subprocess.run(["git","-C",REPO,"ls-tree","-r","--name-only",commit],
                           capture_output=True,text=True,check=True).stdout.splitlines()
    paths = sorted(paths, key=lambda p: p.encode())
    ls = subprocess.run(["git","-C",REPO,"ls-tree","-r",commit],
                        capture_output=True,text=True,check=True).stdout.splitlines()
    oid_of={}
    for line in ls:
        meta,p=line.split("\t",1); oid_of[p]=meta.split()[2]
    proc=subprocess.Popen(["git","-C",REPO,"cat-file","--batch"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    leaves=[]
    for p in paths:
        proc.stdin.write((oid_of[p]+"\n").encode()); proc.stdin.flush()
        hdr=proc.stdout.readline().decode().strip(); n=int(hdr.rsplit(" ",1)[1])
        blob=proc.stdout.read(n); proc.stdout.read(1)
        leaves.append(hashlib.sha256(b"\x00"+hashlib.sha256(blob).digest()).digest())
    proc.stdin.close(); proc.wait()
    return leaves
def fold(leaves):
    stack=[]
    for leaf in leaves:
        stack.append([0,leaf])
        while len(stack)>=2 and stack[-1][0]==stack[-2][0]:
            r=stack.pop(); l=stack.pop()
            stack.append([l[0]+1,hashlib.sha256(b"\x01"+l[1]+r[1]).digest()])
    peaks=list(stack); bag=peaks[-1][1]
    for h,hh in reversed(peaks[:-1]): bag=hashlib.sha256(b"\x01"+hh+bag).digest()
    return hashlib.sha256(b"\x03"+bag+len(leaves).to_bytes(8,"little")).digest(), peaks
if __name__=="__main__":
    for commit,exp in [("7c492528c9f9624bb43846b745df9a480f4d1600","2d1a32145cf89a6b7909d3059abe560e6f3d908e7d510525f4457e096f2cc23a"),
                       ("bf13210","1929707efa24de4ff12f619af2c58c8c924d8bdbc7c45684608ef6e0fdcccb60"),
                       ("4c13ac3f9d21ef19e2db53a3a81a934f2519a458","418fc5a809a087ca9ae5d8d600e7d82abff6a92903b1b459e7481d3ef8eb8d06")]:
        r,_=fold(leaf_digests(commit)); assert r.hex()==exp, commit
        print("GATE", commit[:7], "PASS")
    target = sys.argv[1] if len(sys.argv)>1 else "029b32b"
    r,peaks=fold(leaf_digests(target))
    print(json.dumps({"commit":target,"root":r.hex(),"peaks":[[h,x.hex()] for h,x in peaks]}, indent=1))
