#!/usr/bin/env python3
"""PATENT GENESIS GENERATOR v1.1 — Series No. 1: U.S. Patent Application No. 19/693,343.
v1.0 defect (disclosed, ledger 0184): title-block text overflow and graphic collisions.
v1.1 fixes: reserved layout band, enlarged title block, padded text, graphics clipped
out of text zones. Same seed in, same art out — determinism unchanged."""
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
W, H = 1200, 900; CX, CY = 560, 400
TB = [W-470, H-250, W-30, H-30]      # title block: 440x220, generous
TAPE = [40, H-150, W-520, H-108]     # tape: clear of the title block
def in_reserved(x, y):               # keep graphics out of text zones
    if TB[0]-20 <= x <= TB[2]+20 and TB[1]-20 <= y <= TB[3]+20: return True
    if TAPE[0]-20 <= x <= TAPE[2]+20 and TAPE[1]-20 <= y <= TAPE[3]+20: return True
    return False
img = Image.new("RGB", (W, H), (8, 14, 26)); d = ImageDraw.Draw(img)
for x in range(0, W, 30): d.line([(x,0),(x,H)], fill=(14, 28, 50), width=1)
for y in range(0, H, 30): d.line([(0,y),(W,y)], fill=(14, 28, 50), width=1)
for x in range(0, W, 150): d.line([(x,0),(x,H)], fill=(22, 42, 72), width=1)
for y in range(0, H, 150): d.line([(0,y),(W,y)], fill=(22, 42, 72), width=1)
# radial rails — endpoints clipped out of reserved zones
for i in range(S["spokes"]):
    a = 2*math.pi*i/S["spokes"]
    ex, ey = CX + 380*math.cos(a), CY + 380*math.sin(a)
    if in_reserved(ex, ey):
        ex, ey = CX + 260*math.cos(a), CY + 260*math.sin(a)
    d.line([(CX, CY), (ex, ey)], fill=(40 + (i % 3)*10, 80, 120), width=1)
# central programmable satoshi
d.ellipse([CX-70, CY-70, CX+70, CY+70], outline=(240, 180, 60), width=3)
d.ellipse([CX-58, CY-58, CX+58, CY+58], outline=(200, 150, 50), width=1)
d.line([(CX-22,CY-30),(CX-22,CY+32)], fill=(240,190,70), width=6)
d.line([(CX-22,CY-4),(CX+14,CY-4)], fill=(240,190,70), width=6)
d.line([(CX-22,CY+16),(CX+14,CY+16)], fill=(240,190,70), width=6)
d.line([(CX+14,CY-30),(CX+14,CY-8)], fill=(240,190,70), width=6)
d.line([(CX+14,CY+8),(CX+14,CY+32)], fill=(240,190,70), width=6)
# taproot script-path tree (upward only — stays clear of the bottom band)
def node(x, y, depth, spread):
    if depth == 0 or y < 40: return
    y2 = y - 46 - rb(1)[0] % 14
    for x2 in (x - spread, x + spread):
        d.line([(x, y), (x2, y2)], fill=(90, 200, 160), width=max(1, depth))
        d.ellipse([x2-4, y2-4, x2+4, y2+4], outline=(120, 230, 180), width=1)
        node(x2, y2, depth-1, spread*0.62)
node(CX, CY-74, S["tree_depth"], 150)
# satellite coins — placed only outside reserved zones
placed = 0; tries = 0
while placed < S["coins"] and tries < 40:
    tries += 1
    a = 2*math.pi*(rb(1)[0] % 60)/60; r = 180 + rb(1)[0] % 130
    x, y = CX + r*math.cos(a), CY + r*math.sin(a)
    if in_reserved(x, y): continue
    placed += 1
    d.ellipse([x-16, y-16, x+16, y+16], outline=(230, 175, 60), width=2)
    d.ellipse([x-9, y-9, x+9, y+9], outline=(180, 140, 45), width=1)
# OP_RETURN tape
d.rectangle(TAPE, outline=(60, 130, 120), width=1)
for i, byte in enumerate(rb(136)):
    for j in range(8):
        if (byte >> j) & 1: d.point((44 + i*8 + j, TAPE[1] + 10 + (j % 4)*8), fill=(120, 230, 180))
# title block (padded, generous line spacing)
try:
    f_t = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 17)
    f_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)
except Exception:
    f_t = f_s = ImageFont.load_default()
d.rectangle(TB, outline=(70, 150, 140), width=2)
ss = hashlib.sha256(seed).hexdigest()
serial = hashlib.sha256(seed + b"PATENT-SERIAL").hexdigest()[:12].upper()
L = TB[0]+16; Y = TB[1]
d.text((L, Y+16),  "PATENT GENESIS ARTIFACT — SERIES No. 1", font=f_t, fill=(240, 200, 90))
d.text((L, Y+52),  "U.S. Patent Application No. 19/693,343", font=f_s, fill=(200, 170, 90))
d.text((L, Y+76),  "Programmable Satoshi Tokenization (public citation)", font=f_s, fill=(160, 140, 90))
d.text((L, Y+104), f"SEED 32B  SHA-256 {ss[:24]}...", font=f_s, fill=(120, 200, 170))
d.text((L, Y+128), f"SERIAL {serial}   SAME SEED IN, SAME ART OUT", font=f_s, fill=(120, 200, 170))
d.text((L, Y+160), "GENERATOR v1.1 (v1.0 layout defect disclosed)", font=f_s, fill=(140, 190, 170))
d.text((L, Y+184), "SQUIRL OS // 2026-10-18  THE HASH IS THE ARTIFACT", font=f_s, fill=(240, 200, 90))
img.save(OUT, "PNG"); print("generated", OUT, os.path.getsize(OUT), "bytes")
