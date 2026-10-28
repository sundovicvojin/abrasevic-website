# Sajt KUD „Abrašević“ Kraljevo — 100 godina (1926–2026)

Statički sajt: čist HTML, CSS i vanilla JS. Nema servera, baze, frameworka ni eksternih zavisnosti (fontovi su self-hostovani, nema trekera).

## Šta se otprema na server

Samo sadržaj foldera **`dist/`** (144 fajla, ~9 MB). Sve ostalo u projektu su izvori i alati i ne ide na server.

1. Otvori `dist/` i otpremi **sve** (uključujući skrivene `.htaccess` i `_headers`) u koren sajta (FTP, cPanel, Netlify, Cloudflare Pages…).
2. Domen: u kodu je privremeno `https://abrasevic.rs` (canonical, Open Graph, `sitemap.xml`, `robots.txt`, JSON-LD). Ako je domen drugačiji, vidi „Promena domena“.
3. Sigurnosna zaglavlja:
   - **Apache** (većina hostinga): `.htaccess` radi sam (CSP, nosniff, Referrer-Policy, Permissions-Policy, X-Frame-Options, HSTS, keširanje, gzip/brotli, 404, preusmerenje na https).
   - **Netlify / Cloudflare Pages**: koristi `_headers` (`.htaccess` ignoriše).
   - **Nginx**: prepiši zaglavlja iz `_headers` u `add_header` direktive.
   - `frame-ancestors` ne radi preko `<meta>`, zato je CSP i u zaglavlju. Ako hosting ne prihvata ni jedan od fajlova, sajt i dalje radi (CSP iz `<meta>` ostaje), ali bez ostalih zaglavlja.
4. Sajt očekuje da je u korenu domena (`/`). Za podfolder bi trebalo izmeniti putanje u `404.html` i `site.webmanifest`.

## Struktura

```
index.html        početna: hero, početak 1926, vremenska linija, jubilej, sekcije, nastupi, galerija, poziv
istorija.html     istorija: imena, mesta, prekidi, ljudi
sekcije.html      sve sekcije u detalje
galerija.html     galerija + lightbox
kontakt.html      kontakt podaci + forma (otvara e-poštu)
404.html          stranica „ne postoji“
css/              izvori: main.css (dizajn sistem), fonts.css, photos.css  →  site.min.css (generisan)
js/               boot.js (tema, nivo uređaja), main.js (izvor)  →  site.min.js (generisan)
fonts/            Fraunces + Manrope (woff2, OFL licenca)
img/              generisane slike (AVIF/WebP/JPEG), logo, OG slika
assets/           ORIGINALI (logo, fotografije) – ne menjati, ne otpremati
tools/            skripte za generisanje (vidi dole)
dist/             gotov folder za otpremanje (generiše se)
```

## Kako se menja sadržaj

Stranice se **generišu** iz `tools/build-pages.py` (zajednički meni i footer, kartice, vremenska linija). To je lokalna alatka, na serveru se ništa ne izvršava. Izmene tekstova radi u tom fajlu, a zatim pokreni (potrebni su Python 3 i Pillow):

```
python3 tools/build-min.py && python3 tools/build-pages.py && python3 tools/make-dist.py
python3 tools/check-links.py       # proverava putanje i sidra u dist/
```

Ne menjaj ručno `index.html` itd. u korenu ako ćeš ponovo pokretati `build-pages.py` (ručne izmene se prepisuju). Ako ne želiš Python, možeš da menjaš HTML fajlove u `dist/` direktno; tekst je običan HTML.

| Šta menjaš | Gde |
|---|---|
| Tekst vremenske linije | `TL` u `tools/build-pages.py` |
| Sekcije (kartice i detalji) | `SECS` u `tools/build-pages.py` |
| **Događaji jubileja** | funkcija `jubilej()`: dodaj `<li class="event">…</li>` (datum ide u `<span class="d">`) |
| Festival „Leto kod Abraševića“ | funkcija `performances()` |
| Spisak zemalja | `COUNTRIES` |
| Rukovodioci na stranici Istorija | `people` u funkciji `istorija()` |
| Kontakt podaci | `footer()`, `join_cta()`, `kontakt()` |
| Boje i fontovi | promenljive na vrhu `css/main.css` (`:root`). Paleta: plava `#1f1f44`, zlatna `#c9922e` / `#e2b254`, bela i crna; bez crvene |
| Domen | `SITE` na vrhu `tools/build-pages.py` + `robots.txt`, `sitemap.xml` (JSON-LD i OG se prave iz `SITE`) |

### Nove fotografije u galeriji

1. Ubaci JPEG u `assets/gallery-img/`.
2. `python3 tools/build-assets.py` pravi AVIF/WebP/JPEG u više veličina, blur-up placeholder i `img/meta.json`.
3. Dodaj red u listu `GAL` u `tools/build-pages.py` (ključ je ime fajla bez `.jpg`, zatim opis (alt), kratak natpis i oblik: `wide`, `tall`, `full` ili prazno).
4. Pokreni komande iz prethodnog odeljka. Za novu fotografiju se pojavljuje novo ime fajla pa nema problema sa kešom.

### Arhivske fotografije u vremenskoj liniji

U `TL` svaki čvor ima polje za sliku (trenutno samo „2020-e“). Dodaj ključ slike, opis i kadar po uzoru na tu stavku.

## Bezbednost (ukratko)

- CSP: `default-src 'self'` i ništa spolja, bez inline skripti i stilova (zato se sve animira preko CSS klasa i `style.setProperty`).
- Kontakt forma ne šalje ništa preko sajta: proveri polja, ima honeypot i otvara `mailto:` sa ispunjenom porukom. Adresa e-pošte se sklapa u JS-u (zaštita od botova); bez JS-a link e-pošte ne radi, vidi se „[at]“ oblik.
- Spoljni linkovi (mape i društvene mreže) imaju `rel="noopener noreferrer"`.
- Na sajtu nema imena maloletnika uz fotografije.

## Pristupačnost i performanse

- Lighthouse (mobilni, simulirano): Performance 99–100, Accessibility 100, SEO 100 (merenja iz razvoja).
- Poštuje se `prefers-reduced-motion`; na slabijim uređajima (`≤4` jezgra, malo memorije, telefoni sa dodirom) isključeni su teški efekti (blur, parallax, pokretni oblici).
- Tamna tema: sistemska + ručni prekidač u meniju.

## TODO: podaci koje treba da dobijem od KUD-a

- [ ] **Konačan domen** sajta.
- [ ] **Program jubileja 2026**: datum i mesto svečane akademije, jubilarnog koncerta, termin festivala „Leto kod Abraševića“.
- [ ] **Termini proba i uzrast** za svaku sekciju (folklor, orkestar, radionica, hor, drama, pevačke grupe, balet); rukovodilac i probe modernog baleta.
- [ ] **Arhivske fotografije** za decenije 1926–2010-e (vremenska linija).
- [ ] **Autori fotografija** (kredit) i godina/događaj uz svaku fotografiju u galeriji; potvrda opisa na fotografijama (`ciof-116`: gostujući ansambl).
- [ ] **Saglasnost** za objavljivanje fotografija na kojima su maloletnici (moderni balet, dečiji ansambli).
- [ ] **Aktuelnosti 2022–2026** (stari sajt je imao vesti samo do februara 2022).
- [ ] Potvrda da su **Uroš Baltić (v.d. upravnik)** i **Borisav Miljković (predsednik UO)** i dalje kontakt osobe i da su brojevi tačni.
- [ ] Potvrda **spiska zemalja** gostovanja i činjenica koje su uzete iz teksta starog sajta (osnivač Dragi Tešić, članovi prve uprave, lokacije, imena rukovodilaca sekcija).
- [ ] Potvrda tvrdnji iz zadatka koje nisu na starom sajtu: ime po pesniku Kosti Abraševiću; rukovodilac profesor Vesnić (1945–1947); „prvo profesionalno pozorište u Kraljevu“ (1949).
- [ ] Prekidač latinica/ćirilica nije napravljen (font za naslove nema ćirilicu); stari sajt je bio ćirilični. Reci ako je potreban.

## Alati (samo za razvoj, ne za server)

| Skripta | Šta radi |
|---|---|
| `tools/build-assets.py` | slike, logo, favicon i OG slika iz `assets/` |
| `tools/build-fonts.py` | smanjuje fontove (izvori u `tools/fonts-src/`) |
| `tools/build-min.py` | spaja i minifikuje CSS/JS |
| `tools/build-pages.py` | generiše HTML stranice |
| `tools/make-dist.py` | pravi `dist/` |
| `tools/check-links.py` | proverava putanje i sidra |

Fontovi: Fraunces i Manrope, SIL Open Font License 1.1.
