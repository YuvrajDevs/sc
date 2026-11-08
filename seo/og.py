#!/usr/bin/env python3
"""Makes a 1200x630 share image for every English page: assets/og/<page path>.png.
Run after adding pages: `python3 seo/og.py` (only creates missing images; `--all` redraws every one)."""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FT = os.path.join(ROOT, "seo/fonts/spline_sans_mono.ttf")
BG, BG2, INK, MUTED, ACCENT = (11, 26, 29), (18, 40, 44), (230, 245, 243), (143, 179, 184), (79, 209, 217)
W, H = 1200, 630
LANGS = {l["code"] for l in json.load(open(os.path.join(ROOT, "i18n/langs.json")))}
EYEBROW = {"guides": "GUIDE", "compare": "COMPARE", "scenarios": "REAL SITUATION", "features": "FEATURE", "tools": "FREE TOOL"}

def font(size, weight):
    f = ImageFont.truetype(FT, size)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

logo = Image.open(os.path.join(ROOT, "assets/img/logo-512.png")).convert("RGBA").resize((76, 76))
mask = Image.new("L", (76, 76), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 75, 75), 18, fill=255)

def make(rel, meta, out):
    title = meta.get("navTitle") if rel.startswith("tools/") else None
    title = title or meta.get("title", "Sealcloak")
    title = re.sub(r"\s*·\s*Sealcloak$", "", title)
    sec = rel.split("/")[0] if "/" in rel else ""
    eyebrow = EYEBROW.get(sec, "PRIVATE VAULT FOR ANDROID")
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    # streaming bars, like the site background
    import random; random.seed(rel)
    for y in range(0, H, 34):
        x = random.randint(-200, 200)
        while x < W:
            w = random.randint(40, 260)
            if random.random() < .35: d.rounded_rectangle((x, y + 6, x + w, y + 26), 6, fill=BG2)
            x += w + random.randint(20, 120)
    d.rectangle((0, 0, W, H), fill=None)
    ov = Image.new("RGBA", (W, H), (11, 26, 29, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle((48, 48, W - 48, H - 48), 36, fill=(11, 26, 29, 225), outline=(36, 65, 74, 255), width=2)
    im = Image.alpha_composite(im.convert("RGBA"), ov); d = ImageDraw.Draw(im)
    im.paste(logo, (96, 96), mask)
    d.text((190, 134), "Sealcloak", font=font(40, 700), fill=INK, anchor="lm")
    d.text((96, 228), eyebrow, font=font(26, 600), fill=ACCENT, anchor="lm")
    size = 64
    while True:
        f = font(size, 700); lines = wrap(d, title, f, W - 192)
        if len(lines) <= 3 or size <= 40: break
        size -= 4
    y = 270
    for ln in lines[:3]:
        d.text((96, y), ln, font=f, fill=INK); y += int(size * 1.22)
    d.text((96, H - 100), "Encrypted on your phone · No account · No internet", font=font(24, 400), fill=MUTED, anchor="lm")
    d.text((W - 96, H - 100), "sealcloak.com", font=font(24, 600), fill=ACCENT, anchor="rm")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.convert("RGB").save(out, "PNG", optimize=True)

n = 0
for dp, _, fs in os.walk(os.path.join(ROOT, "content")):
    for fn in fs:
        if not fn.endswith(".html"): continue
        rel = os.path.relpath(os.path.join(dp, fn), os.path.join(ROOT, "content"))
        if rel.split("/")[0] in LANGS or fn == "404.html": continue
        key = rel[:-5]
        out = os.path.join(ROOT, "assets/og", key + ".png")
        if os.path.exists(out) and "--all" not in sys.argv: continue
        raw = open(os.path.join(dp, fn)).read()
        m = re.match(r"<!--meta\s*([\s\S]*?)-->", raw)
        make(rel, json.loads(m.group(1)) if m else {}, out); n += 1
print(f"made {n} share images")
