"""Spaja i minifikuje izvore u jedan CSS i jedan JS fajl (manje zahteva, manji transfer).
Izvori: css/fonts.css + css/photos.css + css/main.css → css/site.min.css ; js/main.js → js/site.min.js
Pokretanje posle svake izmene izvora: python3 izvor/alati/build-min.py"""
import re, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IZ = f"{R}/izvor"; S = f"{R}/sajt"   # IZ = izvori, S = gotov sajt za upload
def rd(p): return open(f"{IZ}/{p}", encoding="utf8").read()

css = rd("css/fonts.css") + "\n" + rd("css/photos.css") + "\n" + rd("css/main.css")
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = re.sub(r"\s+", " ", css)
css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
css = re.sub(r":\s+", ":", css)
css = css.replace(";}", "}")
os.makedirs(f"{S}/css", exist_ok=True); os.makedirs(f"{S}/js", exist_ok=True); import shutil; shutil.copy(f"{IZ}/js/boot.js", f"{S}/js/boot.js")
open(f"{S}/css/site.min.css", "w", encoding="utf8").write(css.strip())

out = []
for line in rd("js/main.js").split("\n"):
    s = line.strip()
    if not s or s.startswith("//") or (s.startswith("/*") and s.endswith("*/")): continue
    out.append(s)
js = "\n".join(out)
open(f"{S}/js/site.min.js", "w", encoding="utf8").write(js + "\n")
print("css", len(css), "js", len(js))
