#!/usr/bin/env python3
"""PATENT GENESIS GENERATOR v1.0 — Series No. 1: U.S. Patent Application No. 19/693,343
(Progammable Satoshi Tokenization, public reference only). A 32-byte seed fully determines
this original blueprint artwork. Same seed in, same PNG out, byte-identical.
Celebratory artifact: cites the patent publicly; discloses NO method detail."""
import hashlib, sys, os, math
from PIL import Image, ImageDraw, ImageFont
seed = open(sys.argv[1], "rb").read(); OUT = sys.argv[2]
assert len(seed) == 32
def rb(n):
    out = b""; i = 0
    while len(out) < n: out += hashlib.sha256(seed + i.to_bytes(4, "big")).digest(); i += 1
    return out[:n]
S = {"coins": 3 + rb(1)[0] % 3, "tree_depth": 5 + rb(1)[0] % 2, "rails": 4 + rb(1)[0] % 4,
     "spokes": 12 + rb(1)[0] % 10, "hue": 170 + rb(1)[0] % 50}
W, H = 1200, 900; CX, CY = 600, 430
img = Image.new("RGB", (W, H), (8, 14, 26)); d = ImageDraw.Draw(img)
for x in range(0, W, 30): d.line([(x,0),(x,H)], fill=(14, 28, 50), width=1)
for y in range(0, H, 30): d.line([(0,y),(W,y)], fill=(14, 28, 50), width=1)
for x in range(0, W, 150): d.line([(x,0),(x,H)], fill=(22, 42, 72), width=1)
for y in range(0, H, 150): d.line([(0,y),(W,y)], fill=(22, 42, 72), width=1)
# radial rails (settlement rails as spokes)
for i in range(S["spokes"]):
    a = 2*math.pi*i/S["spokes"]
    d.line([(CX,CY),(CX+380*math.cos(a), CY+380*math.sin(a))], fill=(40+ (i%3)*10, 80, 120), width=1)
# central programmable satoshi
d.ellipse([CX-70, CY-70, CX+70, CY+70], outline=(240, 180, 60), width=3)
d.ellipse([CX-58, CY-58, CX+58, CY+58], outline=(200, 150, 50), width=1)
d.line([(CX-22,CY-30),(CX-22,CY+32)], fill=(240,190,70), width=6)
d.line([(CX-22,CY-4),(CX+14,CY-4)], fill=(240,190,70), width=6)
d.line([(CX-22,CY+16),(CX+14,CY+16)], fill=(240,190,70), width=6)
d.line([(CX+14,CY-30),(CX+14,CY-8)], fill=(240,190,70), width=6)
d.line([(CX+14,CY+8),(CX+14,CY+32)], fill=(240,190,70), width=6)
# taproot script-path tree rising from the coin
def node(x, y, depth, spread):
    if depth == 0: return
    x2l, y2 = x - spread, y - 46 - rb(1)[0] % 14
    x2r = x + spread
    d.line([(x,y),(x2l,y2)], fill=(90, 200, 160), width=max(1, depth))
    d.line([(x,y),(x2r,y2)], fill=(90, 200, 160), width=max(1, depth))
    for cx in (x2l, x2r):
        d.ellipse([cx-4, y2-4, cx+4, y2+4], outline=(120, 230, 180), width=1)
        node(cx, y2, depth-1, spread*0.62)
node(CX, CY-74, S["tree_depth"], 150)
# satellite coins along rails
for i in range(S["coins"]):
    a = 2*math.pi*(rb(1)[0] % 60)/60
    r = 200 + rb(1)[0] % 120
    x, y = CX + r*math.cos(a), CY + r*math.sin(a)
    d.ellipse([x-16, y-16, x+16, y+16], outline=(230, 175, 60), width=2)
    d.ellipse([x-9, y-9, x+9, y+9], outline=(180, 140, 45), width=1)
# OP_RETURN data tape
ty = H - 170
d.rectangle([40, ty, W-460, ty+40], outline=(60, 130, 120), width=1)
for i, byte in enumerate(rb(140)):
    for j in range(8):
        if (byte >> j) & 1: d.point((44 + i*8 + j, ty + 8 + (j%4)*8), fill=(120, 230, 180))
# title block
try:
    f_t = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 19)
    f_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
except Exception:
    f_t = f_s = ImageFont.load_default()
tb = [W-430, H-200, W-40, H-40]
d.rectangle(tb, outline=(70, 150, 140), width=2)
ss = hashlib.sha256(seed).hexdigest()
serial = hashlib.sha256(seed + b"PATENT-SERIAL").hexdigest()[:12].upper()
d.text((tb[0]+14, tb[1]+12), "PATENT GENESIS ARTIFACT — SERIES No. 1", font=f_t, fill=(240, 200, 90))
d.text((tb[0]+14, tb[1]+42), "U.S. Patent Application No. 19/693,343", font=f_s, fill=(200, 170, 90))
d.text((tb[0]+14, tb[1]+62), "Programmable Satoshi Tokenization (public citation)", font=f_s, fill=(160, 140, 90))
d.text((tb[0]+14, tb[1]+82), f"SEED 32B  SHA-256 {ss[:24]}...", font=f_s, fill=(120, 200, 170))
d.text((tb[0]+14, tb[1]+102), f"SERIAL {serial}   SAME SEED IN, SAME ART OUT", font=f_s, fill=(120, 200, 170))
d.text((tb[0]+14, tb[1]+122), "SQUIRL OS // 2026-10-18  THE HASH IS THE ARTIFACT", font=f_s, fill=(240, 200, 90))
img.save(OUT, "PNG"); print("generated", OUT, os.path.getsize(OUT), "bytes")
