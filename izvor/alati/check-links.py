"""Proverava da svaka putanja (href, src, srcset, url() u CSS-u) u sajt/ pokazuje na postojeći fajl i da svako #sidro postoji."""
import os, re, sys, glob
D = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sajt")
bad = 0; n = 0
ids = {}
def ids_of(path):
    if path not in ids: ids[path] = set(re.findall(r'\sid="([^"]+)"', open(path, encoding="utf8").read()))
    return ids[path]
def resolve(cur, ref):
    ref = ref.split("?")[0]
    if ref.startswith("/"): return os.path.join(D, ref.lstrip("/"))
    return os.path.normpath(os.path.join(os.path.dirname(cur), ref))
for f in glob.glob(D + "/*.html"):
    t = open(f, encoding="utf8").read()
    refs = re.findall(r'(?:href|src)="([^"]+)"', t)
    for s in re.findall(r'srcset="([^"]+)"', t): refs += [x.strip().split(" ")[0] for x in s.split(",")]
    refs += re.findall(r'(?:data-full|data-mid)="([^"]+)"', t)
    for r in refs:
        if r.startswith(("http:", "https:", "mailto:", "tel:", "data:")): continue
        n += 1
        if r.startswith("#"):
            if r != "#" and r[1:] not in ids_of(f) : print("SIDRO NE POSTOJI", os.path.basename(f), r); bad += 1
            continue
        p = resolve(f, r.split("#")[0]); frag = r.split("#")[1] if "#" in r else None
        if not os.path.isfile(p): print("FAJL NE POSTOJI", os.path.basename(f), r); bad += 1
        elif frag and p.endswith(".html") and frag not in ids_of(p): print("SIDRO NE POSTOJI", r); bad += 1
for f in glob.glob(D + "/css/*.css"):
    for u in re.findall(r"url\(['\"]?([^'\")]+)", open(f, encoding="utf8").read()):
        if u.startswith("data:"): continue
        n += 1
        if not os.path.isfile(os.path.normpath(os.path.join(os.path.dirname(f), u))): print("CSS URL NE POSTOJI", u); bad += 1
mani = open(D + "/site.webmanifest").read()
for u in re.findall(r'"src": "([^"]+)"', mani):
    n += 1
    if not os.path.isfile(D + u): print("MANIFEST", u); bad += 1
print(f"proverio {n} putanja, grešaka: {bad}"); sys.exit(1 if bad else 0)
