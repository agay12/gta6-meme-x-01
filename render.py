#!/usr/bin/env python3
"""Render the gta6-meme-x-01 meme PNG (Vice sunset scene + make.fun ghost)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math, os

W, H = 1600, 1000
F = "/usr/share/fonts/truetype/dejavu/"
bold = lambda s: ImageFont.truetype(F + "DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- Vice sunset sky ---
stops = [(0, (24, 8, 48)), (0.45, (120, 20, 110)), (0.72, (215, 40, 120)), (1.0, (255, 140, 60))]
HORIZON = 640
for y in range(HORIZON):
    t = y / HORIZON
    for i in range(len(stops) - 1):
        a, b = stops[i], stops[i + 1]
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0])
            c = tuple(int(a[1][k] + (b[1][k] - a[1][k]) * u) for k in range(3))
            break
    d.line([(0, y), (W, y)], fill=c)

# retro striped sun
sun_cx, sun_cy, sun_r = W // 2, 560, 190
sun = Image.new("RGB", (W, HORIZON), (0, 0, 0))
sd = ImageDraw.Draw(sun)
sd.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], fill=(255, 210, 90))
for i, y0 in enumerate(range(sun_cy, sun_cy + sun_r, 26)):
    sd.rectangle([sun_cx - sun_r, y0, sun_cx + sun_r, y0 + 6 + i * 3], fill=(0, 0, 0))
mask = Image.new("L", (W, HORIZON), 0)
ImageDraw.Draw(mask).ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], fill=255)
img.paste(sun, (0, 0), mask)

# --- ocean ---
for y in range(HORIZON, H):
    t = (y - HORIZON) / (H - HORIZON)
    c = (int(60 - 30 * t), int(10 + 20 * t), int(90 + 40 * t))
    d.line([(0, y), (W, y)], fill=c)
# sun glitter on water
import random
random.seed(7)
for _ in range(500):
    y = HORIZON + random.randint(2, H - HORIZON - 2)
    spread = int((y - HORIZON) / (H - HORIZON) * 220) + 6
    x = sun_cx + random.randint(-spread, spread)
    d.line([(x, y), (x + random.randint(10, 60), y)], fill=(255, 170, 90))

# --- beach strip ---
d.rectangle([0, H - 90, W, H], fill=(30, 14, 50))

# --- neon make.fun sign on a pole, right side ---
def neon(text, x, y, size, glow_color, core_color=(255, 240, 250)):
    fnt = bold(size)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text((x, y), text, font=fnt, fill=glow_color)
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img.paste(glow, (0, 0), glow.convert("L"))
    d.text((x, y), text, font=fnt, fill=core_color)
neon("make.fun", 1075, 205, 62, (255, 40, 160))
# tube outline of the sign
d.rounded_rectangle([1060, 195, 1420, 285], radius=18, outline=(255, 80, 190), width=5)
d.line([(1240, 285), (1240, H - 90)], fill=(20, 10, 40), width=12)

# --- palms (curved trunk + drooping fronds) ---
def palm(cx, base_y, h, flip=1):
    trunk = [(cx + flip * (i / 14.0) ** 2 * 26, base_y - h * i / 14.0) for i in range(15)]
    d.line(trunk, fill=(15, 6, 35), width=22, joint="curve")
    top = trunk[-1]
    for a in range(-150, 40, 24):
        r = math.radians(a)
        dx, dy = math.cos(r) * flip * 1.0, math.sin(r) * 0.55
        L = h * 0.5
        pts = []
        for i in range(9):
            u = i / 8.0
            droop = 26 * u * u
            pts.append((top[0] + dx * L * u, top[1] + dy * L * u + droop))
        d.line(pts, fill=(15, 6, 35), width=11, joint="curve")
palm(170, H - 150, 430)
palm(1430, H - 150, 500, flip=-1)

# --- ghost mascot, worked into the scene (walking the beach at sunset) ---
ROOT = os.path.dirname(os.path.abspath(__file__))
mark = Image.open(os.path.join(ROOT, "assets", "mark-1024.png")).convert("RGBA")
g = mark.resize((560, 560), Image.LANCZOS)
img.paste(g, (520, 330), g)

# small shadow under the ghost
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).ellipse([560, 860, 1040, 920], fill=(0, 0, 0, 160))
sh = sh.filter(ImageFilter.GaussianBlur(12))
img.paste(Image.new("RGB", (W, H)), (0, 0), sh) if False else img.paste(Image.composite(sh.convert("RGB"), img, sh.split()[3]), (0, 0))

# --- caption, meme-bar style ---
def bar(y, h, color):
    d.rectangle([0, y, W, y + h], fill=color)
bar(0, 130, (12, 6, 28))
bar(H - 130, 130, (12, 6, 28))
t1 = "WAITED 13 YEARS FOR GTA 6..."
f1 = bold(66)
tw = d.textlength(t1, font=f1)
d.text(((W - tw) / 2, 32), t1, font=f1, fill=(255, 255, 255))
t2 = "MY AGENT EARNED $500 ON MAKE.FUN WHILE I WAITED"
f2 = bold(56)
tw = d.textlength(t2, font=f2)
if tw > W - 60:
    f2 = bold(int(56 * (W - 60) / tw))
    tw = d.textlength(t2, font=f2)
d.text(((W - tw) / 2, H - 100), t2, font=f2, fill=(255, 215, 240))

img.save(os.path.join(ROOT, "assets", "meme.png"), optimize=True)
print("rendered", img.size, os.path.getsize(os.path.join(ROOT, "assets", "meme.png")), "bytes")
