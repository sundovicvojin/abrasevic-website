"""Pravi poster za sekciju „Film“ iz izvor/originali/film-poster.jpg (AVIF/WebP/JPEG, 480/800/1200) i upisuje ga u meta.json.
Original je jednom preuzet sa YouTube-a (maxresdefault.jpg); sajt u runtime-u ne učitava ništa sa ytimg.com.
Pokretanje: python3 izvor/alati/build-poster.py  (potreban Pillow sa WebP/AVIF podrškom)"""
import os, json
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IZ = f"{R}/izvor"; OUT = f"{R}/sajt/img"; META = f"{IZ}/generisano/meta.json"
key = "film-poster"
im = Image.open(f"{IZ}/originali/{key}.jpg").convert("RGB"); w0, h0 = im.size
sizes = [w for w in (480, 800, 1200) if w <= w0]
for w in sizes:
    r = im.resize((w, round(h0 * w / w0)), Image.LANCZOS)
    r.save(f"{OUT}/{key}-{w}.jpg", quality=78, optimize=True, progressive=True)
    r.save(f"{OUT}/{key}-{w}.webp", quality=76, method=6)
    r.save(f"{OUT}/{key}-{w}.avif", quality=52, speed=6)
meta = json.load(open(META))
meta[key] = {"w": w0, "h": h0, "avg": "#%02x%02x%02x" % im.resize((1, 1), Image.LANCZOS).getpixel((0, 0)), "sizes": sizes}
json.dump(meta, open(META, "w"), indent=1)
print("ok", sizes)
