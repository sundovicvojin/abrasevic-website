"""Generiše optimizovane slike, logo varijante, favicon i OG sliku iz izvor/originali/ (originali ostaju netaknuti).
Pokretanje: python3 izvor/alati/build-assets.py  (potreban Pillow sa WebP/AVIF podrškom)"""
import os, json, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IZ = f"{R}/izvor"; S = f"{R}/sajt"   # IZ = izvori, S = gotov sajt za upload
SRC = f"{IZ}/originali/gallery-img"; OUT = f"{S}/img"; ICONS = f"{S}/img/icons"; GEN = f"{IZ}/generisano"
os.makedirs(OUT, exist_ok=True); os.makedirs(ICONS, exist_ok=True); os.makedirs(GEN, exist_ok=True)
WIDTHS = [480, 800, 1200, 1800]
meta = json.load(open(f"{GEN}/meta.json")) if os.path.exists(f"{GEN}/meta.json") else {}   # zadrži i unose iz build-poster.py

for fn in sorted(os.listdir(SRC)):
    if not fn.lower().endswith(".jpg"): continue
    key = os.path.splitext(fn)[0]
    im = Image.open(f"{SRC}/{fn}").convert("RGB")
    w0, h0 = im.size
    tiny = im.resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    ph = im.resize((24, round(24 * h0 / w0)), Image.LANCZOS)
    ph.save(f"{OUT}/{key}-ph.png", optimize=True)
    sizes = []
    for w in WIDTHS:
        h = round(h0 * w / w0)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(f"{OUT}/{key}-{w}.jpg", quality=78, optimize=True, progressive=True)
        r.save(f"{OUT}/{key}-{w}.webp", quality=76, method=6)
        r.save(f"{OUT}/{key}-{w}.avif", quality=52, speed=6)
        sizes.append(w)
    meta[key] = {"w": w0, "h": h0, "avg": "#%02x%02x%02x" % tiny, "sizes": sizes}
json.dump(meta, open(f"{GEN}/meta.json", "w"), indent=1)

# ---- logo ----
big = Image.open(os.environ.get("LOGO_PNG", f"{IZ}/alati/logo-big.png")).convert("RGBA")
bbox = big.getchannel("A").getbbox(); big = big.crop(bbox)
a = np.array(big)
navy = tuple(int(x) for x in a[a[..., 3] > 250][:, :3].mean(axis=0))
print("navy", "#%02x%02x%02x" % navy)
def tint(rgb):
    b = a.copy(); b[..., 0], b[..., 1], b[..., 2] = rgb; return Image.fromarray(b)
def save_logo(im, name, width):
    r = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    r.save(f"{OUT}/{name}.png", optimize=True); r.save(f"{OUT}/{name}.webp", quality=90, method=6)
    return r
save_logo(tint(navy), "logo", 1000); save_logo(tint((255, 255, 255)), "logo-light", 1000)
# samo "100" (iznad teksta): ~ gornjih 68% visine
mk = big.crop((0, 0, big.width, int(big.height * 0.70)))
mk = mk.crop(mk.getchannel("A").getbbox())
m = np.array(mk)
def mtint(rgb):
    b = m.copy(); b[..., 0], b[..., 1], b[..., 2] = rgb; return Image.fromarray(b)
save_logo(mtint(navy), "mark", 700); save_logo(mtint((255, 255, 255)), "mark-light", 700)
save_logo(mtint(navy), "mark-s", 160); save_logo(mtint((255, 255, 255)), "mark-light-s", 160)
save_logo(tint(navy), "logo-s", 280); save_logo(tint((255, 255, 255)), "logo-light-s", 280)

# ---- favicon ----
sq = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
mm = mk.copy(); mm.thumbnail((420, 420), Image.LANCZOS)
mm = Image.fromarray(np.where(np.array(mm)[..., 3:4] > 0, np.array(list(navy) + [0], dtype=np.uint8) + np.array([0, 0, 0, 0], dtype=np.uint8), 0).astype("uint8")) if False else mm
sq.alpha_composite(mm, ((512 - mm.width) // 2, (512 - mm.height) // 2))
sq.convert("RGB").resize((180, 180), Image.LANCZOS).save(f"{ICONS}/apple-touch-icon.png")
sq.resize((192, 192), Image.LANCZOS).save(f"{ICONS}/icon-192.png"); sq.save(f"{ICONS}/icon-512.png")
sq.resize((32, 32), Image.LANCZOS).save(f"{ICONS}/favicon-32.png")
sq.save(f"{S}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# ---- OG 1200x630 ----
og = Image.open(f"{SRC}/cioff-210.jpg").convert("RGB")
og = og.resize((1200, round(og.height * 1200 / og.width)), Image.LANCZOS)
og = og.crop((0, (og.height - 630) // 2, 1200, (og.height - 630) // 2 + 630))
ov = Image.new("RGBA", og.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
d.rectangle((0, 0, 1200, 630), fill=(20, 21, 48, 205))
og = Image.alpha_composite(og.convert("RGBA"), ov)
lg = Image.open(f"{OUT}/logo-light.png").copy(); lg.thumbnail((560, 520), Image.LANCZOS)
og.alpha_composite(lg, (70, (630 - lg.height) // 2))
d = ImageDraw.Draw(og)
def _manrope(w, size):  # OG slika koristi isti font kao sajt (Manrope), instanca date težine
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    import io
    f = instancer.instantiateVariableFont(TTFont(f"{IZ}/alati/fonts-src/manrope-latin.woff2"), {"wght": w}); f.flavor = None
    b = io.BytesIO(); f.save(b); b.seek(0); return ImageFont.truetype(b, size)
f1 = _manrope(800, 64); f2 = _manrope(600, 34)
d.text((690, 200), "100 godina", font=f1, fill=(255, 255, 255)); d.text((690, 285), "Vek igre, pesme\ni tradicije", font=f2, fill=(255, 255, 255), spacing=8)
d.text((690, 400), "KUD „Abrašević“ Kraljevo\n1926–2026", font=f2, fill=(226, 178, 84), spacing=8)
og.convert("RGB").save(f"{OUT}/og.jpg", quality=86, optimize=True)
print("ok")
