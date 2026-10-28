"""Generiše statičke HTML stranice iz zajedničkih delova (zaglavlje, footer, sprite). Rezultat je čist HTML.
Pokretanje: python3 izvor/alati/build-pages.py"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IZ = f"{R}/izvor"; S = f"{R}/sajt"   # IZ = izvori, S = gotov sajt za upload
META = json.load(open(f"{IZ}/generisano/meta.json"))
SPRITE = open(f"{IZ}/alati/sprite.svg", encoding="utf8").read()
import hashlib
def _v(f): return hashlib.md5(open(f"{S}/{f}","rb").read()).hexdigest()[:8]  # promena sadržaja = novi URL = keš se osvežava
V_CSS, V_JS, V_BOOT = _v("css/site.min.css"), _v("js/site.min.js"), _v("js/boot.js")
SITE = "https://abrasevic.rs"  # TODO: potvrditi konačni domen

def ico(n, cls="ico"): return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{n}"/></svg>'
def seal(s=120, cls=""): return f'<svg class="seal {cls}" aria-hidden="true" focusable="false" width="{s}" height="{s}"><use href="#seal"/></svg>'

def pic(key, alt, sizes, eager=False, pos=None, cls=""):
    m = META[key]; w, h = m["w"], m["h"]
    ws = m["sizes"]; big = ws[-1]
    def ss(ext): return ", ".join(f"img/{key}-{x}.{ext} {x}w" for x in ws)
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="img/{key}-1200.jpg" srcset="{ss("jpg")}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load}></picture>')

CSP = "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self' mailto:; frame-src https://www.youtube-nocookie.com"
NAV = [("index.html", "Početna"), ("istorija.html", "Istorija"), ("sekcije.html", "Sekcije"), ("galerija.html", "Galerija"), ("kontakt.html", "Kontakt")]

def head(title, desc, page, og_title=None, extra=""):
    return f'''<!DOCTYPE html>
<html lang="sr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#07070f" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{SITE}/{'' if page == 'index.html' else page}">
<meta property="og:type" content="website"><meta property="og:locale" content="sr_RS">
<meta property="og:title" content="{og_title or title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{'' if page == 'index.html' else page}"><meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{og_title or title}">
<meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/img/og.jpg">
<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="img/icons/favicon-32.png">
<link rel="apple-touch-icon" href="img/icons/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/manrope-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.min.css?v={V_CSS}">
<script src="js/boot.js?v={V_BOOT}"></script>
{extra}</head>
'''

def header(page):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a></li>' for h, t in NAV)
    sheet_links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}{ico("arrow")}</a></li>' for h, t in NAV)
    return f'''<body>
{SPRITE}
<a class="skip" href="#main">Preskoči na sadržaj</a>
<div class="progress" aria-hidden="true"></div>
<div class="bg" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="nav">
  <div class="nav-bar">
    <a class="brand" href="index.html"><img class="on-light" src="img/mark-s.png" width="160" height="{MARK_H}" alt=""><img class="on-dark" src="img/mark-light-s.png" width="160" height="{MARK_H}" alt=""><span>Abrašević<small>Kraljevo · 1926–2026</small></span></a>
    <nav aria-label="Glavna navigacija"><ul class="nav-links">{links}</ul></nav>
    <a class="btn nav-cta" href="kontakt.html">Pridruži se</a>
    <button class="icon-btn" type="button" data-theme-toggle aria-label="Promeni temu (svetla/tamna)">{ico("sun","ico sun")}{ico("moon","ico moon")}</button>
    <button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="sheet" aria-label="Otvori meni">{ico("menu","ico open")}{ico("close","ico close")}</button>
  </div>
</header>
<div class="sheet" id="sheet"><nav class="sheet-panel glass" aria-label="Mobilna navigacija"><ul>{sheet_links}</ul></nav></div>
'''

def footer():
    fl = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    return f'''<footer class="footer">
  <div class="wrap">
    <div class="big-name" aria-hidden="true">Abrašević</div>
    <div class="foot glass">
      <div>
        <div class="foot-brand"><img class="on-light" src="img/logo-s.png" width="280" height="{LOGO_H}" alt="KUD Abrašević Kraljevo — 100 godina"><img class="on-dark" src="img/logo-light-s.png" width="280" height="{LOGO_H}" alt="" aria-hidden="true">{seal(96)}</div>
      </div>
      <div><h2>Stranice</h2><ul>{fl}</ul></div>
      <div><h2>Kontakt</h2><ul>
        <li><a href="https://www.google.com/maps/search/?api=1&amp;query=Vojvode+Stepe+8+Kraljevo" target="_blank" rel="noopener noreferrer">{ico("pin")}Vojvode Stepe 8, 36000 Kraljevo</a></li>
        <li><a href="tel:+38136331746">{ico("phone")}+381 36 331 746</a></li>
        <li><a href="tel:+38163333746">{ico("phone")}+381 63 333 746</a></li>
        <li><a href="mailto:abrasevic_kv@mts.rs">{ico("mail")}<span>abrasevic_kv@mts.rs</span></a></li>
      </ul></div>
      <div><h2>Zapratite nas</h2>
        <div class="social">
          <a href="https://sr-rs.facebook.com/kudabrasevic.kraljevo/" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{ico("fb")}</a>
          <a href="https://www.instagram.com/kud.abrasevic/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">{ico("ig")}</a>
          <a href="https://www.youtube.com/channel/UCG3QizGtlDCb6fDte9GqJrQ" target="_blank" rel="noopener noreferrer" aria-label="YouTube">{ico("yt")}</a>
        </div>
      </div>
    </div>
    <div class="legal"><span>© 1926–2026 KUD „Abrašević“ Kraljevo</span><span>Created by <a href="https://instagram.com/devbyvojin/" target="_blank" rel="noopener noreferrer">devbyvojin</a></span><!-- TODO: dodati autore fotografija (kredit) kada ih KUD potvrdi --></div>
  </div>
</footer>
<script src="js/site.min.js?v={V_JS}" defer></script>
</body>
</html>
'''

from PIL import Image
_m = Image.open(f"{S}/img/mark-s.png"); MARK_H = round(_m.height * 160 / _m.width)
_l = Image.open(f"{S}/img/logo-s.png"); LOGO_H = round(_l.height * 280 / _l.width)


JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"PerformingGroup","name":"KUD „Abrašević“ Kraljevo","alternateName":"Kulturno-umetničko društvo „Abrašević“","url":"%s/","logo":"%s/img/logo.png","image":"%s/img/og.jpg","foundingDate":"1926","description":"Kulturno-umetničko društvo iz Kraljeva osnovano 1926. Folklor, narodni orkestar, hor, drama, pevačke grupe, muzička radionica i moderni balet.","address":{"@type":"PostalAddress","streetAddress":"Vojvode Stepe 8","postalCode":"36000","addressLocality":"Kraljevo","addressCountry":"RS"},"telephone":"+38136331746","sameAs":["https://sr-rs.facebook.com/kudabrasevic.kraljevo/","https://www.instagram.com/kud.abrasevic/","https://www.youtube.com/channel/UCG3QizGtlDCb6fDte9GqJrQ"]}
</script>
""" % (SITE, SITE, SITE)

def write(name, html): open(f"{S}/{name}", "w", encoding="utf8").write(html)

TL = [
 ("1926", "Rađa se Umetnička grupa „Abrašević“", None,
  ["Osnivač je <strong>Dragi Tešić</strong>, i sam član šabačkog Abraševića. Prvu upravu čine Dara Marković, Živko Biščić, Velimir Petrović i Pavle Pajić.",
   "Tri sekcije: <strong>hor, drama i tamburaški sastav</strong>, uz skromnu biblioteku.",
   "Rad u Sindikalnom domu u ulici Cara Lazara 72. Do kraja rata grupa je više puta prekidala rad: 1929, 1932, 1936, 1939. i 1941–1945."],
  "Najstarija kulturna institucija u Kraljevu."),
 ("1940-e", "Posle rata: novo ime, nova igra", None,
  ["Grupa dva puta menja ime, u „Polet“ i „Goč“, a od <strong>1947.</strong> nosi današnji naziv: KUD „Abrašević“ Kraljevo. Među rukovodiocima bio je i profesor Vesnić (1945–1947).",
   "<strong>1946.</strong> počinje rad folklorna sekcija, koja će postati sinonim za „Abrašević“.",
   "<strong>1949.</strong> drama prerasta u Gradsko narodno pozorište, današnje Kraljevačko pozorište."],
  "Iz „Abraševića“ nikla je prva profesionalna scena u gradu."),
 ("1960-e", "Prvi put preko granice", None,
  ["<strong>1964.</strong> prvi veliki festival: Zelena Gora u Poljskoj. Članstvo se umnožava i formiraju se još tri dečija ansambla.",
   "Sve sekcije se sele u novoizgrađeni Dom društvenih organizacija (1964).",
   "Krajem decenije putovanja u Austriju, Englesku, Holandiju i SR Nemačku, i veze sa dijasporom (Šramberg, Geteborg)."],
  "Počinje put koji traje do danas."),
 ("1970-e", "Orkestri, instrumenti, nova kuća", None,
  ["<strong>1971.</strong> formiraju se dva orkestra, narodni i zabavni, sa više solista.",
   "<strong>1973.</strong> nabavlja se veći broj instrumenata i potrebna oprema. Iz muzičke sekcije potekli su mnogi izvođači srpske narodne muzike.",
   "<strong>1979.</strong> društvo se seli u prostorije Dobrovoljnog vatrogasnog društva, gde je i danas (Vojvode Stepe 8)."],
  "Adresa koja traje već skoro pola veka."),
 ("1980-e", "Sve više nas", None,
  ["„Abrašević“ se omasovljava i postaje poznat u zemlji i inostranstvu. Na međunarodne turneje i gostovanja odlazi se skoro svake godine.",
   "<strong>1985.</strong> osniva se sekcija modernog baleta."],
  "Folklor je baza oko koje raste celo stvaralaštvo."),
 ("1990-e", "Svet u dometu ruke", None,
  ["<strong>1995.</strong> društvo, pod rukovodstvom koreografa Slavoljuba Panovića, postaje član međunarodne asocijacije CIOFF.",
   "Festivali u Brazilu (1996) i Sjedinjenim Američkim Državama (1997).",
   "<strong>1998.</strong> osniva se ansambl veterana, a prvi ansambl i narodni orkestar odlaze na turneju u Australiju. Osniva se i dečiji narodni orkestar."],
  "Prekookeanske turneje otvaraju vrata sve većem članstvu."),
 ("2000-e", "Od Kine do Evrope", None,
  ["<strong>2003.</strong> festival u Narodnoj Republici Kini.",
   "<strong>2007.</strong> ponovo Australija, pa evropska turneja: Engleska, Francuska, Italija i Švajcarska.",
   "<strong>2008.</strong> obnovljen je rad horske sekcije dečijim horom. <strong>2009.</strong> počinje rad dramska sekcija „PROZORIŠTE“."],
  "Nove sekcije vraćaju u kuću pesmu i pozornicu."),
 ("2010-e", "Devedeset godina i devet turneja", None,
  ["<strong>2010.</strong> Španija, Azurna obala i Venecija. <strong>2015.</strong> počinju muška i ženska pevačka grupa, a narodni orkestar daje koncert „Putovanje“.",
   "<strong>2016.</strong> povratak u CIOFF, svečana akademija i koncert u Hali sportova povodom 90 godina. <strong>2017.</strong> osniva se muzička radionica.",
   "<strong>2019.</strong> jedna od najuspešnijih godina: čak <strong>9 inostranih turneja</strong>."],
  "Devedeset godina, pa još deset."),
 ("2020-e", "Veliki jubilej na vidiku", ("cioff-09", "Nasmejani igrači u narodnoj nošnji na zalasku sunca, u prirodi", "(min-width:960px) 40vw, 90vw", "50% 30%"),
  ["Uprkos pandemiji, rad se nastavlja sa kratkim prekidima, a turneje u Turskoj, Severnoj Makedoniji i Crnoj Gori su održane.",
   "<strong>2021.</strong> jubilej od 95 godina obeležen je koncertima i trodnevnom manifestacijom „Puna kuća Abraševića“.",
   "Društvo je član srpske sekcije CIOFF-a i organizator šestodnevnog festivala <strong>„Leto kod Abraševića“</strong>.",
   "<strong>2026.</strong> sto godina igre, pesme i tradicije."],
  "Sto godina. I još mnogo pesama."),
]

def timeline():
    out = []
    for i, (yr, h, im, pts, tag) in enumerate(TL):
        now = ' now' if yr == "2020-e" else ''
        side = 'rv-l' if i % 2 == 0 else 'rv-r'
        lis = "".join(f"<li>{p}</li>" for p in pts)
        img = ""
        if im:
            k, alt, sz, pos = im
            img = f'<div class="ph drift ph-{k}">{pic(k, alt, sz, pos=pos)}</div>'
        else:
            img = f"<!-- TODO: arhivska fotografija ({yr}) -->"
        out.append(f'''<li class="tl-item{now}"><span class="tl-dot" aria-hidden="true"></span>
  <article class="tl-card glass tilt rv {side}"><div class="tl-year">{yr}</div><h3>{h}</h3><ul>{lis}</ul><p><strong>{tag}</strong></p>{img}</article></li>''')
    return "\n".join(out)

def index():
    hero = pic("cioff-210", "Igrači u belim nošnjama sa krznenim kapama i igračice u maramama u kolu na sceni", "(min-width:900px) 42vw, 92vw", eager=True)
    body = f'''<main id="main">
<section class="hero" aria-labelledby="h1">
  <div class="hero-num rv" aria-hidden="true">100</div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="years glass hero-in">KUD „Abrašević“ Kraljevo <b><span>1926</span> – <span data-count data-from="1926" data-to="2026">2026</span></b></p>
      <h1 id="h1" class="hero-in d1">Vek igre, pesme i tradicije</h1>
      <p class="lead hero-in d2">Sto godina od osnivanja Umetničke grupe „Abrašević“ do ansambala u kojima danas igraju, sviraju i pevaju stotine članova.</p>
      <div class="cta hero-in d3"><a class="btn" href="#pocetak">Krenite kroz vek{ico("arrow")}</a><a class="btn ghost" href="kontakt.html">Pridruži nam se</a></div>
    </div>
    <figure class="hero-fig glass hero-in d2">
      <div class="ph drift ph-cioff-210 par k6">{hero}</div>
      {seal(148)}
    </figure>
  </div>
</section>

<section class="sec" id="pocetak" aria-labelledby="h-pocetak">
  <div class="wrap">
    <div class="sec-head rv"><h2 id="h-pocetak">Sve je počelo 1926.</h2>
      <p class="intro">Jedan hor, jedna dramska družina i tamburaši u maloj prostoriji. Niko od njih nije mogao da zna da će se njihova pesma čuti širom sveta.</p></div>
    <div class="origin">
      <div class="origin-main glass rv"><p class="big">Najstarija kulturna institucija u Kraljevu</p>
        <p>Društvo je 1926. osnovano kao „Umetnička grupa Abrašević“, a ime nosi po pesniku Kosti Abraševiću. Prve sekcije bile su hor, drama i tamburaški sastav.</p>
        <p>Iz njegovih redova formirano je 1949. prvo profesionalno pozorište u Kraljevu. Danas „Abrašević“ okuplja ansamble svih uzrasta, a organizuje i tradicionalni međunarodni festival folklora „Leto kod Abraševića“.</p></div>
      <div class="origin-side">
        <div class="card glass rv d1"><b>1926</b><p>Osnivanje Umetničke grupe „Abrašević“.</p></div>
        <div class="card glass rv d2"><b>1949</b><p>Iz društva izrasta prvo profesionalno pozorište u Kraljevu.</p></div>
        <div class="card glass rv d3"><b>1947</b><p>Danas poznato ime: KUD „Abrašević“ Kraljevo.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="istorija" aria-labelledby="h-vek">
  <div class="wrap">
    <div class="sec-head rv"><h2 id="h-vek">Vek, decenija po decenija</h2>
      <p class="intro">Ko se osvrne unazad, vidi žute fotografije, imena i lica. Evo kako je jedna grupa mladih ljudi 1926. postala društvo koje se zna na svim meridijanima.</p></div>
    <ol class="timeline" aria-label="Vremenska linija 1926–2026">
{timeline()}
<li class="tl-track" aria-hidden="true"></li><li class="tl-bar" aria-hidden="true"></li>
    </ol>
  </div>
</section>
{jubilej()}
{today()}
{performances()}
{gallery_preview()}
{join_cta()}
{film()}
</main>
'''
    return head("KUD „Abrašević“ Kraljevo — 100 godina (1926–2026)",
                "KUD „Abrašević“ Kraljevo slavi 100 godina: vek igre, pesme i tradicije. Folklor, orkestar, hor, drama i festival „Leto kod Abraševića“.",
                "index.html", extra=JSONLD) + header("index.html") + body + lightbox() + footer()


SECS = [
 dict(id="folklor", title="Folklorna sekcija", icon="dance", short="Srce društva i sinonim za „Abrašević“: prvi ansambl, ansambl veterana, pet dečijih ansambala i dve rekreativne grupe.",
   facts=["Osnovana 1946.", "Oko 400 članova", "Preko 50 koreografija"],
   hist=["1946–1954. nastupa uglavnom u Kraljevu i okolini. Pravi uslovi za rad stižu tek preseljenjem u Dom društvenih organizacija.",
         "<strong>1964.</strong> Zelena Gora u Poljskoj donosi popularnost, članstvo se umnožava i formiraju se još tri dečija ansambla. Repertoar su tada pesme i igre iz cele SFRJ.",
         "Osamdesetih broj članova raste i sekcija postaje baza oko koje se formira celokupno umetničko stvaralaštvo.",
         "Do 1998. na čelu ansambla je koreograf Slavoljub Panović, potom Zvezdan Đurić, koga je nasledila Nataša Arsenijević.",
         "Koreografije: „Igre iz Studenice“, „Svadbeni običaji iz Grdelice“, „Igre iz Prizrena“, „Vranjsko polje“, „Bosilegradsko krajište“, „Igre iz okoline Beograda“, „Igre iz okoline Niša“ i mnoge druge.",
         "Nastupali su u Bugarskoj, Makedoniji, Švajcarskoj, Češkoj, Švedskoj, Australiji, Grčkoj, Kini, Brazilu, SAD, Španiji, Turskoj, Engleskoj i drugde."],
   lead=["Umetnički rukovodilac prvog ansambla od 2019: <strong>Dejan Prvanović</strong>", "Ansambl veterana (osnovan 1998): <strong>Nataša Arsenijević</strong>"],
   img=("abr1-011", "Mladi igrači u šubarama i prslucima sa šarenim pojasevima podižu ruke u igri na tamnoj sceni", "50% 35%")),
 dict(id="orkestar", title="Narodni orkestar", icon="note", short="Prati sve folklorne grupe i vokalne solisti, a po potrebi hor i pevačke grupe. Preko 30 članova.",
   facts=["Preko 30 članova", "Muzička sekcija postoji od 1926.", "Koncert „Putovanje“ 2015."],
   hist=["Muzička sekcija se može, uz dramsku, smatrati osnivačem društva: 1926. su uz hor postojali i tamburaši.",
         "<strong>1971.</strong> formiraju se dva orkestra, narodni i zabavni, a <strong>1973.</strong> nabavlja se veći broj instrumenata.",
         "Iz sekcije su potekli mnogi izvođači srpske narodne muzike, među njima Vesna Zmijanac, Dejana Đekić, Milan Simić i harmonikaš Miroljub Vrndić.",
         "Od 2001. na čelu je Rade Kuburović, koji je uveo najviše novina, među njima dečiji orkestar od učenika Muzičke škole „Stevan Mokranjac“. Većina njih danas svira u narodnom orkestru.",
         "<strong>2015.</strong> narodni orkestar održao je svoj celovečernji koncert „Putovanje“."],
   lead=["Na čelu orkestra: <strong>Veljko Miljković</strong>", "Korepetitor i prva harmonika (od 1993): <strong>Dejan Vuković</strong>"], img=None),
 dict(id="radionica", title="Muzička radionica", icon="guitar", short="Za one koji žele da nauče da sviraju: sa polaznicima rade članovi narodnog orkestra.",
   facts=["Osnovana krajem 2017.", "Devet instrumenata", "Praktično i teorijsko znanje"],
   hist=["Polaznici uče harmoniku, gitaru, kontrabas, trubu, frulu, klarinet, saksofon, violinu i kaval.",
         "Sa polaznicima rade članovi narodnog orkestra „Abraševića“.",
         "Članovi radionice imaju i samostalne nastupe, a neki su postali članovi narodnog orkestra."],
   lead=["Prijave i termini časova: <strong>obratite se društvu</strong>"], img=None),
 dict(id="hor", title="Horska sekcija", icon="notes", short="Dečiji hor sa oko sedamdeset numera i stariji mešoviti hor koji je svoj prvi nastup imao na „Letu kod Abraševića“.",
   facts=["Dečiji hor od 2008.", "Oko 70 numera (dečiji hor)", "Mešoviti hor od 2016."],
   hist=["Horska sekcija datira iz predratnog perioda, a veći uspesi beleže se od 1946. do 1970. na akademijama i takmičenjima širom SFRJ.",
         "Sekcija prekida rad od 1970. do 1974. Kasnije se više puta formiraju pevačke grupe, uglavnom od igrača sa pevačkim darom.",
         "<strong>2008.</strong> rad se obnavlja formiranjem dečijeg hora, koji brzo postaje popularan.",
         "<strong>2016.</strong> ponovo se formira stariji mešoviti hor, sa dvadesetak numera i inostranim gostovanjima."],
   lead=["Dečiji hor vodi: <strong>Dejana Živković Kuburović</strong>"], img=None),
 dict(id="drama", title="Dramska sekcija „PROZORIŠTE“", icon="masks", short="Jedna od sekcija koje su osnovale Umetničku grupu 1926. Obnovljena 2009, danas okuplja oko 30 članova u tri grupe.",
   facts=["Osnovana 1926.", "Obnovljena 2009.", "Oko 30 članova u tri grupe"],
   hist=["U početku radi u prostorijama hotela „Pariz“, gde se izvode i predstave, i uspešno gostuje u okolnim gradovima.",
         "<strong>1949.</strong> se osamostaljuje i formira se Narodno pozorište „Kraljevački oktobar“, koje i danas postoji.",
         "<strong>Septembra 2009.</strong> sekcija ponovo počinje rad pod imenom „PROZORIŠTE“, uz nagrade na pozorišnim festivalima u zemlji i inostranstvu.",
         "<strong>2017.</strong> izvedena je prva predstava za mlade u novijoj istoriji „Abraševića“. Dečija drama je na festivalu u Bugarskoj osvojila nagradu za najbolje izvedenu predstavu."],
   lead=["Rukovodilac od 2020: <strong>Ana Jerotijević</strong>", "Ranije su sekciju vodili Biljana Konstantinović, Dragan Pešić i Stefan Milikić"], img=None),
 dict(id="pevacke", title="Pevačke grupe", icon="mic", short="Muška i ženska pevačka grupa i etno grupa sa velikim brojem pesama na repertoaru.",
   facts=["Od 2015.", "Tri grupe", "Koncert u Kolarčevoj zadužbini"],
   hist=["Na inicijativu Borisava Miljkovića 2015. počinju sa radom muška i ženska pevačka grupa, a danas radi i etno grupa (mlađa ženska pevačka grupa).",
         "Grupe su imale zapažene nastupe širom Srbije na tradicionalnim saborima narodnog stvaralaštva i nekoliko celovečernjih koncerata, među njima i u Kolarčevoj zadužbini.",
         "Sa takmičenja su se uvek vraćale sa vrednim nagradama."],
   lead=["Rukovodioci, etnomuzikolozi: <strong>Borisav Miljković, Sofija Gračanac i Milica Gračanac</strong>"], img=None),
 dict(id="balet", title="Moderni balet", icon="ballet", short="Sekcija osnovana 1985. čija je plesna grupa gostovala i na festivalu u Rumuniji.",
   facts=["Osnovana 1985."],
   hist=["Sekcija modernog baleta osnovana je 1985. i u kasnijem periodu beležila je značajne rezultate.",
         "Plesna grupa gostovala je na festivalu u Klužu u Rumuniji.",
         "<!-- TODO: rukovodilac, uzrast i termin proba modernog baleta -->Podatke o rukovodiocu i probama potvrđujemo."],
   lead=[], img=("abr_balet-5", "Plesačice modernog baleta u crveno-smeđim kostimima u skoku na crnoj sceni", "50% 40%")),
]
SECS[0]["short"]=SECS[0]["short"]; SECS[1]["short"]=SECS[1]["short"].replace("solističe","solističe".replace("е","e"))

def jubilej():
    return f"""<section class="sec" id="jubilej" aria-labelledby="h-jubilej"><div class="wrap">
  <div class="jubilee glass rv">
    <div><h2 id="h-jubilej">Sto godina slavimo zajedno</h2>
      <p class="intro" style="">Jubilej nije samo broj. To su generacije koje su ovde igrale, pevale i prijateljevale, i svi koji dolaze.</p>
      <p>Program jubileja, događaji i najave biće objavljeni na ovom mestu.</p>
      <div class="cta"><a class="btn" href="kontakt.html">Javite nam se{ico("arrow")}</a>{seal(88)}</div></div>
    <ul class="events">
      <!-- TODO: potvrditi tačne datume i mesta događaja jubileja; ovde dodavati nove <li class="event"> stavke -->
      <li class="event rv d1"><span class="d">2026</span><div><h3>Svečana akademija</h3><p>Datum i mesto biće objavljeni.</p></div></li>
      <li class="event rv d2"><span class="d">2026</span><div><h3>Jubilarni koncert</h3><p>Datum i mesto biće objavljeni.</p></div></li>
      <li class="event rv d3"><span class="d">2026</span><div><h3>Festival „Leto kod Abraševića“</h3><p>Termin jubilarnog izdanja biće objavljen.</p></div></li>
    </ul>
  </div></div></section>""".replace(' style=""','')

def today():
    cards = "".join(f"""<article class="card glass tilt rv d{(i%3)+1}"><span class="ico-wrap">{ico(s['icon'])}</span><h3>{s['title']}</h3><p>{s['short']}</p>
  <ul class="facts">{''.join(f'<li>{f}</li>' for f in s['facts'])}</ul>
  <!-- TODO: uzrast i termin proba za {s['title']} -->
  <a class="more" href="sekcije.html#{s['id']}">Saznaj više{ico("arrow")}</a></article>""" for i, s in enumerate(SECS))
    return f"""<section class="sec" id="danas" aria-labelledby="h-danas"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-danas">Ko smo danas</h2>
    <p class="intro">Pod istim krovom sviraju, pevaju, igraju i glume generacije. Izaberite svoju sekciju.</p></div>
  <div class="cards c3">{cards}</div>
  <p class="todo-note" style="">Uzrast i termine proba potvrđuje društvo; za informacije pozovite ili pišite.</p>
</div></section>""".replace(' style=""',' ').replace('<p class="todo-note"  >','<p class="todo-note">')

COUNTRIES = ["Poljska","Austrija","Engleska","Holandija","Nemačka","Brazil","SAD","Kina","Australija","Španija","Francuska","Italija","Švajcarska","Rumunija","Grčka","Turska","Češka","Bugarska","Makedonija","Švedska","Hrvatska","Bosna i Hercegovina","Mađarska","Ukrajina","Crna Gora","Slovenija"]
def performances():
    chips = "".join(f"<li>{c}</li>" for c in COUNTRIES)
    return f"""<section class="sec" id="nastupi" aria-labelledby="h-nastupi"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-nastupi">Nastupi na svim meridijanima</h2>
    <p class="intro">Od Zelene Gore 1964. do devet inostranih turneja u jednoj godini: pesma iz Kraljeva čula se na četiri kontinenta.</p></div>
  <div class="stats">
    <div class="stat glass rv d1"><b><span data-count data-from="0" data-to="100">100</span></b><span>godina rada</span></div>
    <div class="stat glass rv d2"><b><small>oko</small><span data-count data-from="0" data-to="400">400</span></b><span>članova folklorne sekcije</span></div>
    <div class="stat glass rv d3"><b><span data-count data-from="0" data-to="50">50</span>+</b><span>koreografija na repertoaru</span></div>
    <div class="stat glass rv d4"><b><span data-count data-from="0" data-to="9">9</span></b><span>inostranih turneja u 2019.</span></div>
  </div>
  <div class="world">
    <div class="glass rv"><h3>Gde smo sve nastupali</h3>
      <p>Evropa, Amerika, Azija i Australija: festivali i gostovanja CIOFF-a, prijateljstva sa društvima iz dijaspore i bratimljenja gradova.</p>
      <ul class="chips">{chips}</ul>
      <!-- TODO: proveriti i dopuniti spisak zemalja gostovanja -->
    </div>
    <div class="glass festival rv d2"><h3>Leto kod Abraševića</h3>
      <p>Tradicionalni međunarodni festival folklora koji društvo organizuje kao član srpske sekcije CIOFF-a. Šest dana igre, pesme i druženja u Kraljevu.</p>
      <!-- TODO: termin, mesto i program festivala za 2026. -->
      <p><strong>Termin i program biće objavljeni.</strong></p>
      <ul class="facts"><li>Šestodnevni festival</li><li>Član srpske sekcije CIOFF-a</li><li>CIOFF od 1995. (i ponovo od 2016.)</li></ul></div>
  </div></div></section>"""

def film():
    YT = "yJAS7HLsbC0"
    poster = pic("film-poster", "Naslovna slika filma o KUD „Abrašević“", "(min-width:1240px) 1176px, calc(100vw - 32px)")
    return f"""<section class="sec" id="film" aria-labelledby="h-film"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-film">Film o Abraševiću</h2>
    <p class="intro">Sto godina igre, pesme i tradicije u jednom filmu. Pustite ga i pogledajte kako je počelo i do kuda je stiglo.</p></div>
  <div class="film glass rv d1">
    <div class="film-frame" data-yt="{YT}">{poster}
      <button class="film-play" type="button" aria-label="Pusti film">{ico("play")}</button>
      <noscript><a class="film-nojs" href="https://youtu.be/{YT}" target="_blank" rel="noopener noreferrer">Pogledajte film na YouTube-u</a></noscript></div>
    <p class="film-note">Ako se video ne učita, <a href="https://youtu.be/{YT}" target="_blank" rel="noopener noreferrer">pogledajte ga na YouTube-u</a>.</p>
  </div>
</div></section>"""

def join_cta():
    return f"""<section class="sec" id="pridruzi-se" aria-labelledby="h-join"><div class="wrap">
  <div class="join glass rv">
    <div><h2 id="h-join">Pridruži nam se</h2>
      <p class="intro" style="font-family:var(--serif)">Vrata su otvorena za svakoga ko voli da igra, peva, svira ili glumi.</p>
      <div class="cta"><a class="btn" href="kontakt.html">Kontakt i prijave{ico("arrow")}</a><a class="btn ghost" href="sekcije.html">Pogledaj sekcije</a></div></div>
    <ul class="contact-list">
      <li>{ico("pin")}<div><a href="https://www.google.com/maps/search/?api=1&amp;query=Vojvode+Stepe+8+Kraljevo" target="_blank" rel="noopener noreferrer">Vojvode Stepe 8, 36000 Kraljevo</a><small>Sedište društva</small></div></li>
      <li>{ico("phone")}<div><a href="tel:+38136331746">+381 36 331 746</a><small>Telefon društva</small></div></li>
      <li>{ico("mail")}<div><a href="mailto:abrasevic_kv@mts.rs">abrasevic_kv@mts.rs</a></div></li>
    </ul>
  </div></div></section>""".replace(' style="font-family:var(--serif)"','')

def page_hero(h1, lead):
    return f"""<section class="page-hero"><div class="wrap"><h1 class="hero-in">{h1}</h1><p class="lead hero-in d1">{lead}</p></div></section>"""

def istorija():
    people = [("Dragi Tešić","osnivač, 1926."),("Slavoljub Panović","koreograf prvog ansambla do 1998."),("Zvezdan Đurić","koreograf od 1998."),("Nataša Arsenijević","koreograf, ansambl veterana"),("Dejan Prvanović","umetnički rukovodilac prvog ansambla od 2019."),("Rade Kuburović","na čelu narodnog orkestra od 2001."),("Dejan Vuković","orkestar i korepeticija od 1993."),("Dejana Živković Kuburović","dečiji hor od 2008."),("Biljana Konstantinović","dramska sekcija od 2009."),("Ana Jerotijević","dramska sekcija od 2020.")]
    pl = "".join(f"<li><b>{n}</b><span>{r}</span></li>" for n, r in people)
    places = ["Sindikalni dom, Cara Lazara 72 (1926)","Hotel „Evropa“ (današnji hotel „Turist“)","Hotel „Nacional“, ugao Miloša Velikog i Hajduk Veljkove","Prostorije stare Pošte, ugao Hajduk Veljkove i Cara Lazara","Stara škola Četvrtog kraljevačkog bataljona, danas Trg Jovana Sarića","Dom društvenih organizacija (1964)","Prostorije Dobrovoljnog vatrogasnog društva, Vojvode Stepe 8 (od 1979)"]
    pls = "".join(f"<li>{x}</li>" for x in places)
    body = f"""<main id="main">
{page_hero("Istorija jednog veka","Od Umetničke grupe iz 1926. do društva koje je nastupalo na četiri kontinenta. Ovde je priča ispričana imenima, mestima i godinama.")}
<section class="sec" aria-labelledby="h-reci" style=""><div class="wrap">
  <div class="sec-head rv"><h2 id="h-reci">Reč o „Abraševiću“</h2></div>
  <div class="prose glass rv">
    <blockquote>Statistika će nam otkriti da je početak rada „Abraševića“ bio 1926. godine. Ali uspomene beleži duša, ona je osnivač i kičma „Abraševića“.</blockquote>
    <p>Tako piše Mile Nedeljković u tekstu kojim se društvo predstavlja. Za njega je istorija „neizbrisiva, kvalitetna i trajna inspiracija za nove generacije“, a posao koji društvo radi „posledica je lutanja srca“ koje se zasniva na otkrivanju, upoznavanju i usvajanju vrednosti.</p>
    <p>Putovanja i susreti sa drugačijim kulturama i gradovima ostavljaju u statistici pređene kilometre, a u ljudima ono što ostaje: <strong>„Abrašević – zdravi da ste svi.“</strong></p>
  </div></div></section>
<section class="sec" aria-labelledby="h-imena"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-imena">Imena, mesta i prekidi</h2><p class="intro">Društvo je nosilo više imena i menjalo adrese, ali nikada nije prestalo da traje.</p></div>
  <div class="cols">
    <div class="card glass rv"><h3>Kako se društvo zvalo</h3><p><strong>1926.</strong> Umetnička grupa „Abrašević“, zatim „Polet“ i „Goč“, a od <strong>1947.</strong> današnje KUD „Abrašević“ Kraljevo. Od tada društvo ima četiri sekcije: dramsku, horsku, muzičku i folklornu.</p></div>
    <div class="card glass rv d1"><h3>Kad je rad prekidan</h3><p>Do kraja Drugog svetskog rata grupa je više puta prekidala rad: <strong>1929, 1932, 1936, 1939</strong> i za vreme rata, od <strong>1941. do 1945.</strong> Sa kratkim prekidima radilo se i tokom pandemije, a turneje su ipak održane.</p></div>
    <div class="card glass rv"><h3>Gde smo radili</h3><ul class="chips" style="">{pls}</ul></div>
    <div class="card glass rv d1"><h3>Iz novijeg perioda</h3><p><strong>Decembar 2021.</strong> trodnevna manifestacija „Puna kuća Abraševića“ otvorena je koncertom horske muzike u Narodnom muzeju, nastavljena koncertom folklornih ansambala i završena koncertom prvog ansambla u Domu vojske. Reportažu sa koncerta „Prezivam se Abrašević“ prikazala je RTS.</p>
      <!-- TODO: dodati aktuelnosti iz 2022–2026; stari sajt ima vesti samo do februara 2022. -->
    </div>
  </div></div></section>
<section class="sec" aria-labelledby="h-ljudi"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-ljudi">Ljudi koji su gradili „Abrašević“</h2><p class="intro">Ime društva nose generacije igrača, muzičara, pevača i glumaca. Evo nekih od onih koji su ga vodili.</p></div>
  <div class="glass prose rv"><ul class="people">{pl}</ul>
    <p class="todo-note" style=""><!-- TODO: potvrditi i dopuniti spisak rukovodilaca (uključujući profesora Vesnića, 1945–1947) -->Spisak će KUD dopuniti.</p></div>
  <div class="cta rv" style=""><a class="btn" href="index.html#istorija">Nazad na vremensku liniju{ico("arrow")}</a><a class="btn ghost" href="sekcije.html">Pogledaj sekcije</a></div>
</div></section>
</main>
"""
    body = body.replace(' style=""','')
    return head("Istorija — KUD „Abrašević“ Kraljevo","Istorija KUD-a „Abrašević“ Kraljevo od 1926: imena, mesta, ljudi i prekidi rada u veku igre, pesme i tradicije.","istorija.html")+header("istorija.html")+body+footer()

def sekcije():
    blocks = []
    for i, s in enumerate(SECS):
        facts = "".join(f"<li>{f}</li>" for f in s["facts"])
        hist = "".join(f"<li>{h}</li>" for h in s["hist"])
        lead = "".join(f'<li>{l}</li>' for l in s["lead"])
        im = ""
        if s["img"]:
            k, alt, pos = s["img"]
            im = f'<div class="ph drift ph-{k} sec-img">{pic(k, alt, "(min-width:960px) 40vw, 92vw")}</div>'
        blocks.append(f"""<section class="sec sec-s" id="{s['id']}" aria-labelledby="h-{s['id']}"><div class="wrap">
  <div class="glass sec-detail rv{' flip' if i % 2 else ''}">
    <div class="sd-main"><span class="ico-wrap">{ico(s['icon'])}</span><h2 id="h-{s['id']}">{s['title']}</h2><p class="intro">{s['short']}</p>
      <ul class="facts">{facts}</ul>{('<ul class="people">'+lead+'</ul>') if lead else ''}
      <!-- TODO: uzrast i termin proba: {s['title']} -->
      <p class="todo-note">Uzrast i termine proba potvrđuje društvo.</p>
      <a class="btn" href="kontakt.html">Prijavi se{ico("arrow")}</a></div>
    <div class="sd-side">{im}<h3>Iz istorije sekcije</h3><ul class="hist">{hist}</ul></div>
  </div></div></section>""")
    nav = "".join(f'<li><a class="btn ghost" href="#{s["id"]}">{ico(s["icon"])}{s["title"].split(" „")[0]}</a></li>' for s in SECS)
    body = f"""<main id="main">
{page_hero("Sekcije","Folklor, orkestar, hor, drama, pevačke grupe, muzička radionica i moderni balet. Svaka sekcija ima svoju priču i svoje ljude.")}
<div class="wrap"><ul class="chipnav rv">{nav}</ul></div>
{''.join(blocks)}
</main>
"""
    return head("Sekcije — KUD „Abrašević“ Kraljevo","Sekcije KUD-a „Abrašević“: folklorna, narodni orkestar, muzička radionica, hor, dramska sekcija, pevačke grupe i moderni balet.","sekcije.html")+header("sekcije.html")+body+footer()

def kontakt():
    body = f"""<main id="main">
{page_hero("Kontakt","Dođite u Vojvode Stepe 8, pozovite nas ili nam pišite. Rado ćemo vas upoznati sa sekcijama.")}
<section class="sec" aria-labelledby="h-kontakt"><div class="wrap">
  <h2 class="sr" id="h-kontakt">Kontakt podaci i poruka</h2>
  <div class="contact-grid two">
    <div class="glass card rv"><h3>Kontakt informacije</h3>
      <ul class="contact-list">
        <li>{ico("pin")}<div><a href="https://www.google.com/maps/search/?api=1&amp;query=Vojvode+Stepe+8+Kraljevo" target="_blank" rel="noopener noreferrer">Vojvode Stepe 8, 36000 Kraljevo</a><small>Otvara mapu u novom prozoru</small></div></li>
        <li>{ico("phone")}<div><a href="tel:+38136331746">+381 36 331 746</a></div></li>
        <li>{ico("phone")}<div><a href="tel:+38163333746">+381 63 333 746</a></div></li>
        <li>{ico("mail")}<div><a href="mailto:abrasevic_kv@mts.rs">abrasevic_kv@mts.rs</a></div></li>
        <li>{ico("mail")}<div><a href="mailto:abrasevickraljevo@gmail.com">abrasevickraljevo@gmail.com</a></div></li>
      </ul>
      <div class="social" style=""><a href="https://sr-rs.facebook.com/kudabrasevic.kraljevo/" target="_blank" rel="noopener noreferrer" aria-label="Facebook">{ico("fb")}</a><a href="https://www.instagram.com/kud.abrasevic/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">{ico("ig")}</a><a href="https://www.youtube.com/channel/UCG3QizGtlDCb6fDte9GqJrQ" target="_blank" rel="noopener noreferrer" aria-label="YouTube">{ico("yt")}</a></div>
    </div>
    <div class="glass card rv d1"><h3>Rukovodstvo</h3>
      <div class="person"><b>Uroš Baltić</b>v.d. upravnik<br><a href="tel:+38163333746">+381 63 333 746</a></div>
      <div class="person"><b>Borisav Miljković</b>predsednik Upravnog odbora<br><a href="tel:+381643341739">+381 64 334 1739</a></div>
      <!-- TODO: potvrditi da su kontakt osobe i brojevi i dalje aktuelni (stari sajt) -->
    </div>
  </div>
</div></section>
<section class="sec" aria-labelledby="h-poruka"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-poruka">Napišite nam</h2><p class="intro">Poruka se ne šalje preko sajta. Dugme otvara vaš program za e-poštu sa već ispunjenom porukom, a ona stiže tek kad je vi pošaljete.</p></div>
  <form class="form glass rv" id="contact-form" novalidate data-mail="abrasevic_kv@mts.rs" aria-describedby="form-note">
    <div class="field"><label for="f-name">Ime i prezime</label><input id="f-name" name="name" type="text" autocomplete="name" required maxlength="80" aria-describedby="e-name"><p class="err" id="e-name" role="alert"></p></div>
    <div class="field"><label for="f-mail">Vaša e-pošta</label><input id="f-mail" name="email" type="email" autocomplete="email" required maxlength="120" aria-describedby="e-mail"><p class="err" id="e-mail" role="alert"></p></div>
    <div class="field"><label for="f-msg">Poruka</label><textarea id="f-msg" name="message" required minlength="10" maxlength="1500" aria-describedby="e-msg"></textarea><p class="err" id="e-msg" role="alert"></p></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Ne popunjavajte ovo polje</label><input id="f-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
    <button class="btn" type="submit">Otvori e-poštu{ico("mail")}</button>
    <p class="status" id="f-status" role="status"></p>
    <p class="form-note" id="form-note">Ako se program za e-poštu ne otvori, pišite direktno na adresu iznad ili nas pozovite.</p>
  </form>
</div></section>
</main>
"""
    body = body.replace(' style=""','')
    return head("Kontakt — KUD „Abrašević“ Kraljevo","Kontakt KUD-a „Abrašević“ Kraljevo: adresa Vojvode Stepe 8, telefoni, e-pošta, rukovodstvo i poruka.","kontakt.html")+header("kontakt.html")+body+footer()


# (id, alt, kratak natpis, pozicija kadra, oblik)
GAL = [
 ("abr1-019", "Igrač i igračica okićeni cvećem u svečanoj igri na tamnoj sceni", "Igra i cveće na sceni", "wide"),
 ("abr1-038", "Žene u belim maramama i narodnim nošnjama sede na sceni uz pletene korpe, scena iz koreografije", "Scena iz koreografije", "tall"),
 ("cioff-210", "Igrači u belim nošnjama sa krznenim kapama i igračice u maramama u kolu", "U kolu", ""),
 ("cioff-09", "Nasmejani igrači u narodnoj nošnji na zalasku sunca u prirodi", "Zalazak sunca", ""),
 ("abr1-011", "Mladi igrači u šubarama i prslucima sa šarenim pojasevima podižu ruke u igri na tamnoj sceni", "Igra u šubarama", ""),
 ("abr_balet-5", "Plesačice modernog baleta u crveno-smeđim kostimima u skoku na crnoj sceni", "Moderni balet", ""),
 ("ciof-116", "Plesačice iz gostujućeg ansambla u raskošnim vezenim nošnjama i sa crvenim maramama na festivalu", "Gosti na festivalu", ""),
 ("ciof-061", "Igrači u narodnoj nošnji podižu ruke na otvorenoj sceni, u pozadini muzičari", "Na otvorenoj sceni", "full"),
]
def tile(k, alt, cap, shape, i):
    sz = "(min-width:860px) 66vw, 100vw" if shape in ("wide", "full") else "(min-width:860px) 33vw, 50vw"
    if shape == "tall": sz = "(min-width:860px) 33vw, 50vw"
    return (f'<a class="tile {shape} rv d{(i%3)+1}" href="img/{k}-1800.jpg" data-lb data-cap="{cap}" data-full="img/{k}-1800.webp" data-mid="img/{k}-1200.webp">'
            f'<div class="ph ph-{k}">{pic(k, alt, sz)}</div><span class="cap">{cap}</span></a>')

def bento(items):
    return '<div class="bento">' + "".join(tile(k, a, c, s, i) for i, (k, a, c, s) in enumerate(items)) + '</div>'

def lightbox():
    return f"""<dialog class="lb" id="lb" aria-label="Pregled fotografije" aria-modal="true">
  <p class="lb-count" aria-live="polite"></p>
  <button class="lb-btn lb-close" type="button" aria-label="Zatvori">{ico("close")}</button>
  <button class="lb-btn lb-prev" type="button" aria-label="Prethodna fotografija">{ico("left")}</button>
  <button class="lb-btn lb-next" type="button" aria-label="Sledeća fotografija">{ico("right")}</button>
  <div class="lb-stage"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="" width="1800" height="1200"></div>
  <p class="lb-cap"></p>
</dialog>
"""

def gallery_preview():
    return f"""<section class="sec" id="galerija" aria-labelledby="h-gal"><div class="wrap">
  <div class="sec-head rv"><h2 id="h-gal">Trenuci sa scene</h2>
    <p class="intro">Nošnje, osmesi i kolo koje se ne prekida. Kliknite na fotografiju da je vidite u punoj veličini.</p></div>
  {bento(GAL[:6] if False else [GAL[0], GAL[1], GAL[2], GAL[3], GAL[6], GAL[5]])}
  <div class="cta rv"><a class="btn" href="galerija.html">Cela galerija{ico("arrow")}</a></div>
</div></section>"""

def galerija():
    body = f"""<main id="main">
{page_hero("Galerija","Osam fotografija iz scena, sa festivala i sa putovanja. Kliknite na fotografiju za prikaz preko celog ekrana; strelice na tastaturi ili prevlačenje prstom listaju dalje.")}
<section class="sec" style="" aria-labelledby="h-gal2"><div class="wrap">
  <h2 class="sr" id="h-gal2">Fotografije</h2>
  {bento(GAL)}
  <!-- TODO: dodati nove fotografije (izvor/originali/gallery-img → python3 izvor/alati/build-assets.py) i u GAL listu u tools/build-pages.py; uz njih godinu i događaj -->
  <p class="todo-note rv">Godina i događaj uz fotografije biće dodati kada ih društvo potvrdi.</p>
</div></section>
</main>
""".replace(' style=""','').replace('<section class="sec" style="" ','<section class="sec" ')
    return head("Galerija — KUD „Abrašević“ Kraljevo","Galerija KUD-a „Abrašević“ Kraljevo: fotografije igrača, orkestra i baleta sa scena i festivala.","galerija.html")+header("galerija.html")+body+lightbox()+footer()

write("index.html", index())
write("istorija.html", istorija())
write("sekcije.html", sekcije())
write("kontakt.html", kontakt())
write("galerija.html", galerija())

def nf():
    body = f"""<main id="main"><div class="notfound"><div class="glass">
  <div class="big" aria-hidden="true">404</div>
  <h1>Ova stranica ne postoji</h1>
  <p class="lead">Možda je adresa pogrešno ukucana ili je stranica premeštena. Vratite se na početnu ili pogledajte sekcije.</p>
  <div class="cta" style="justify-content:center"><a class="btn" href="/index.html">Na početnu{ico("arrow")}</a><a class="btn ghost" href="/sekcije.html">Sekcije</a></div>
</div></div></main>
""".replace(' style="justify-content:center"', '')
    html = head("Stranica nije pronađena — KUD „Abrašević“ Kraljevo", "Tražena stranica ne postoji.", "404.html") + header("404.html") + body + footer()
    html = html.replace('<meta name="robots"', '<meta name="robots"').replace("<title>", '<meta name="robots" content="noindex"><title>', 1)
    import re
    # 404 se služi sa bilo koje putanje: sve interne putanje moraju biti apsolutne
    html = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)([^"]+)"', r'\1="/\2"', html)
    html = html.replace('srcset="img/', 'srcset="/img/')
    write("404.html", html)
nf()
print("pages ok")
