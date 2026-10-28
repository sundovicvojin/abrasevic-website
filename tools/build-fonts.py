"""Umanjuje self-hostovani font Manrope: ograničava težine na 400–800 i ostavlja samo glifove koje sajt koristi
(latinica sa č, ć, š, ž, đ, interpunkcija). Izvori (originalni woff2 sa Google Fonts, OFL licenca) su u tools/fonts-src/.
Pokretanje: python3 tools/build-fonts.py   (potrebni fonttools i brotli)"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIC = list(range(0x20, 0x7F)) + list(range(0xA1, 0x100)) + [0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022, 0x2026, 0x20AC, 0x2190, 0x2192, 0x2212]
EXT = [0x106, 0x107, 0x10C, 0x10D, 0x110, 0x111, 0x160, 0x161, 0x17D, 0x17E]
def build(name, limits, unis):
    f = TTFont(f"{R}/tools/fonts-src/{name}.woff2")
    f = instancer.instantiateVariableFont(f, limits)
    import io; b = io.BytesIO(); f.save(b); b.seek(0); f = TTFont(b, lazy=False)  # ponovo učitaj da se glifovi razreše
    opt = subset.Options(); opt.flavor = "woff2"; opt.layout_features = ["kern", "liga", "locl", "calt", "ccmp", "mark", "mkmk"]; opt.notdef_outline = True
    s = subset.Subsetter(opt); s.populate(unicodes=unis); s.subset(f)
    f.flavor = "woff2"; f.save(f"{R}/fonts/{name}.woff2")
    print(name, os.path.getsize(f"{R}/fonts/{name}.woff2"))
for fam, lim in (("manrope", {"wght": (400, 800)}),):
    build(f"{fam}-latin", lim, BASIC); build(f"{fam}-latin-ext", lim, EXT)
L = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD"
E_ = "U+0100-0130,U+0132-0151,U+0154-024F"
css = ""
for fam, F in (("manrope", "Manrope"),):
    for sub, rng in (("latin-ext", E_), ("latin", L)):
        css += f"@font-face{{font-family:'{F}';font-style:normal;font-weight:400 800;font-display:swap;src:url('../fonts/{fam}-{sub}.woff2') format('woff2');unicode-range:{rng}}}\n"
open(f"{R}/css/fonts.css", "w").write(css)
