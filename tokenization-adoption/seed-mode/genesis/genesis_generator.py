#!/usr/bin/env python3
"""GENESIS GENERATOR v1.0 — real seed-mode reconstruction engine (architecture demo).
A 32-byte seed fully determines an original blueprint artwork (PNG). Same seed in,
same PNG out, byte-identical. This is NOT the TGC method (patent-adjacent, private);
it is a production-grade demonstration of the seed-mode receipt architecture."""
import hashlib, sys, os
from PIL import Image, ImageDraw, ImageFont

SEED_FILE = sys.argv[1] if len(sys.argv) > 1 else "seed.bin"
OUT_FILE  = sys.argv[2] if len(sys.argv) > 2 else "genesis_artifact.png"
seed = open(SEED_FILE, "rb").read()
assert len(seed) == 32, "seed must be exactly 32 bytes"

def rb(n):  # deterministic byte stream from seed (SHA-256 DRBG)
    out = b""
    i = 0
    while len(out) < n:
        out += hashlib.sha256(seed + i.to_bytes(4, "big")).digest(); i += 1
    return out[:n]

S = {  # every generative parameter derives from the seed
 "rose_k":   2 + rb(1)[0] % 7,
 "petal_d":  120 + rb(1)[0] % 90,
 "liss_fx":  1 + rb(1)[0] % 6,  "liss_fy": 1 + rb(1)[0] % 6,
 "liss_ph":  (rb(1)[0] % 180) / 57.2958,
 "branch_a": 12 + rb(1)[0] % 22,
 "branch_n": 4 + rb(1)[0] % 4,
 "hue":      140 + rb(1)[0] % 80,
 "ring_n":   2 + rb(1)[0] % 4,
}
W, H = 1200, 900
CX, CY = 470, 440
img = Image.new("RGB", (W, H), (9, 18, 34))
d = ImageDraw.Draw(img)
def glow_line(pts, base=(90, 220, 170), w=1):
    for i, (a, b) in enumerate(pts):
        d.line([a, b], fill=(30+i*0, 90+i*0, 60+i*0), width=w)  # dim under
    for a, b in pts:
        d.line([a, b], fill=base, width=w)
# blueprint grid
for x in range(0, W, 30): d.line([(x,0),(x,H)], fill=(16, 34, 60), width=1)
for y in range(0, H, 30): d.line([(0,y),(W,y)], fill=(16, 34, 60), width=1)
for x in range(0, W, 150): d.line([(x,0),(x,H)], fill=(24, 48, 82), width=1)
for y in range(0, H, 150): d.line([(0,y),(W,y)], fill=(24, 48, 82), width=1)
import math
# ring structure
for r in range(1, S["ring_n"]+1):
    rr = 90 + r*62 + rb(1)[0] % 18
    d.ellipse([CX-rr, CY-rr, CX+rr, CY+rr], outline=(45, 120, 110), width=1)
# rose curve (glow)
pts = []
for t in range(0, 31416, 6):
    th = t/10000.0
    r = S["petal_d"] * abs(math.sin(S["rose_k"]*th))
    pts.append([(CX + r*math.cos(th), CY + r*math.sin(th)),
                (CX + r*math.cos(th+0.0022), CY + r*math.sin(th+0.0022))])
glow_line(pts, (90, 220, 170), 2)
# lissajous interference overlay
pts2 = []
for t in range(0, 62832, 4):
    th = t/10000.0
    x = 250*math.sin(S["liss_fx"]*th + S["liss_ph"]) + CX
    y = 210*math.sin(S["liss_fy"]*th) + CY
    x2 = 250*math.sin(S["liss_fx"]*(th+0.0025) + S["liss_ph"]) + CX
    y2 = 210*math.sin(S["liss_fy"]*(th+0.0025)) + CY
    pts2.append([(x,y),(x2,y2)])
glow_line(pts2, (70, 170, 230), 1)
# fractal branches
def branch(x, y, ang, ln, depth):
    if depth == 0 or ln < 3: return
    nx, ny = x + ln*math.cos(ang), y + ln*math.sin(ang)
    c = (110 + depth*8, 220, 150)
    d.line([(x,y),(nx,ny)], fill=c, width=max(1, depth//2))
    branch(nx, ny, ang - math.radians(S["branch_a"] + rb(1)[0]%6), ln*0.72, depth-1)
    branch(nx, ny, ang + math.radians(S["branch_a"] + rb(1)[0]%6), ln*0.72, depth-1)
# NOTE: rb() inside branch makes it still deterministic (same seed => same bytes)
for b in range(S["branch_n"]):
    ba = (360/S["branch_n"])*b + rb(1)[0] % 20
    branch(CX, CY, math.radians(ba), 60 + rb(1)[0] % 40, 6)
# checksum tape (visual bit strip)
tape_y = H - 150
d.rectangle([40, tape_y, W-340, tape_y+44], outline=(60, 130, 120), width=1)
bits = rb(140)
for i, byte in enumerate(bits):
    for j in range(8):
        x = 44 + i*8 + j
        if (byte >> j) & 1: d.point((x, tape_y+8+ (j%4)*8), fill=(120, 230, 180))
# title block
try:
    f_t = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 20)
    f_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
except Exception:
    f_t = f_s = ImageFont.load_default()
tb = [W-460, H-190, W-40, H-40]
d.rectangle(tb, outline=(70, 150, 140), width=2)
seed_sha = hashlib.sha256(seed).hexdigest()
serial = hashlib.sha256(seed + b"SERIAL").hexdigest()[:12].upper()
d.text((tb[0]+14, tb[1]+12), "GENESIS ARTIFACT — SEED-MODE ORIGINAL", font=f_t, fill=(140, 235, 190))
d.text((tb[0]+14, tb[1]+44), f"SEED: 32 bytes  SHA-256 {seed_sha[:24]}...", font=f_s, fill=(120, 200, 170))
d.text((tb[0]+14, tb[1]+64), f"SERIAL {serial}   SAME SEED IN, SAME ART OUT", font=f_s, fill=(120, 200, 170))
d.text((tb[0]+14, tb[1]+84), "RECONSTRUCTED FROM THE CHAIN ALONE", font=f_s, fill=(120, 200, 170))
d.text((tb[0]+14, tb[1]+104), "SQUIRL OS // 2026-10-18  THE HASH IS THE ARTIFACT", font=f_s, fill=(140, 235, 190))
img.save(OUT_FILE, "PNG")
print("generated", OUT_FILE, os.path.getsize(OUT_FILE), "bytes")
