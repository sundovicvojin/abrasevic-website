"""Pravi folder dist/ sa tačno onim što se otprema na server (bez izvora, alata, originala i PSD fajlova).
Pokretanje (redom): python3 tools/build-min.py && python3 tools/build-pages.py && python3 tools/make-dist.py"""
import os, shutil, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f"{R}/dist"
if os.path.isdir(D): shutil.rmtree(D)
os.makedirs(D)
def cp(src, dst=None):
    dst = f"{D}/{dst or src}"; os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(f"{R}/{src}", dst)
for f in glob.glob(f"{R}/*.html"): cp(os.path.basename(f))
for f in ["site.webmanifest", "robots.txt", "sitemap.xml", ".htaccess", "_headers", "favicon.ico", "favicon-32.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png", "css/site.min.css", "js/boot.js", "js/site.min.js"]: cp(f)
for f in glob.glob(f"{R}/fonts/*.woff2"): cp(f"fonts/{os.path.basename(f)}")
for f in glob.glob(f"{R}/img/*"):
    n = os.path.basename(f)
    if n == "meta.json" or n.endswith("-ph.png"): continue   # -ph.png je već ugrađen u CSS kao placeholder → ostaje
    cp(f"img/{n}")
for f in glob.glob(f"{R}/img/*-ph.png"): cp(f"img/{os.path.basename(f)}")
tot = sum(os.path.getsize(os.path.join(a, b)) for a, _, fs in os.walk(D) for b in fs)
print("dist/ spreman:", sum(len(fs) for _, _, fs in os.walk(D)), "fajlova,", round(tot / 1e6, 1), "MB")
