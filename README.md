# Sajt KUD „Abrašević“ Kraljevo — 100 godina (1926–2026)

Statički sajt: čist HTML, CSS i vanilla JS. Nema servera, baze, frameworka ni eksternih zavisnosti (fontovi su self-hostovani, nema trekera).

## Šta se otprema na server

Samo sadržaj foldera **`sajt/`** (142 fajla, ~9 MB). Sve ostalo u projektu su izvori, alati i dokumentacija i ne ide na server.

1. Otvori `sajt/` i otpremi **sve** (uključujući skrivene `.htaccess` i `_headers`) u koren sajta (FTP, cPanel, Netlify, Cloudflare Pages…).
2. Domen: u kodu je privremeno `https://abrasevic.rs` (canonical, Open Graph, `sitemap.xml`, `robots.txt`, JSON-LD). Ako je domen drugačiji, vidi „Promena domena“.
3. Sigurnosna zaglavlja:
   - **Apache** (većina hostinga): `.htaccess` radi sam (CSP, nosniff, Referrer-Policy, Permissions-Policy, X-Frame-Options, HSTS, keširanje, gzip/brotli, 404, preusmerenje na https).
   - **Netlify / Cloudflare Pages**: koristi `_headers` (`.htaccess` ignoriše).
   - **Nginx**: prepiši zaglavlja iz `_headers` u `add_header` direktive.
   - `frame-ancestors` ne radi preko `<meta>`, zato je CSP i u zaglavlju. Ako hosting ne prihvata ni jedan od fajlova, sajt i dalje radi (CSP iz `<meta>` ostaje), ali bez ostalih zaglavlja.
4. Sajt očekuje da je u korenu domena (`/`). Za podfolder bi trebalo izmeniti putanje u `404.html` i `site.webmanifest`.

## Struktura

```
sajt/                        ← OVO SE OTPREMA NA SERVER (gotov sajt)
  index.html                 početna: hero, početak 1926, vremenska linija, jubilej, sekcije, nastupi, galerija, poziv
  istorija.html              istorija: imena, mesta, prekidi, ljudi
  sekcije.html               sve sekcije u detalje
  galerija.html              galerija + lightbox
  kontakt.html               kontakt podaci + forma (otvara e-poštu)
  404.html                   stranica „ne postoji“
  css/  js/  fonts/          site.min.css, boot.js + site.min.js, Manrope (woff2, OFL licenca)
  img/                       slike (AVIF/WebP/JPEG), logo, OG slika; img/icons/ = ikonice
  favicon.ico  robots.txt  sitemap.xml  site.webmanifest  .htaccess  _headers

izvor/                       izvori (ne otpremaju se)
  originali/                 ORIGINALI (logo PDF/PSD, fotografije): ne menjati
  css/  js/                  main.css (dizajn sistem), fonts.css, photos.css; boot.js, main.js
  alati/                     Python skripte za generisanje (vidi dole), sprite.svg, izvorni fontovi
  generisano/                meta.json (dimenzije slika, interno)

dokumentacija/               prompt i SKILL.md (radni materijal)
README.md
```

## Kako se menja sadržaj

Stranice se **generišu** iz `izvor/alati/build-pages.py` (zajednički meni i footer, kartice, vremenska linija). To je lokalna alatka, na serveru se ništa ne izvršava. Izmene tekstova radi u tom fajlu, a zatim pokreni (potrebni su Python 3 i Pillow):

```
python3 izvor/alati/build-min.py && python3 izvor/alati/build-pages.py
python3 izvor/alati/check-links.py       # proverava putanje i sidra u sajt/
```

Ne menjaj ručno `sajt/*.html` ako ćeš ponovo pokretati `build-pages.py` (ručne izmene se prepisuju). Ako ne želiš Python, možeš da menjaš HTML fajlove u `sajt/` direktno; tekst je običan HTML.

| Šta menjaš | Gde |
|---|---|
| Tekst vremenske linije | `TL` u `izvor/alati/build-pages.py` |
| Sekcije (kartice i detalji) | `SECS` u `izvor/alati/build-pages.py` |
| **Događaji jubileja** | funkcija `jubilej()`: dodaj `<li class="event">…</li>` (datum ide u `<span class="d">`) |
| Festival „Leto kod Abraševića“ | funkcija `performances()` |
| Spisak zemalja | `COUNTRIES` |
| Rukovodioci na stranici Istorija | `people` u funkciji `istorija()` |
| Kontakt podaci | `footer()`, `join_cta()`, `kontakt()` |
| Boje i fontovi | promenljive na vrhu `izvor/css/main.css` (`:root`). Paleta: plava `#1f1f44`, zlatna `#c9922e` / `#e2b254`, bela i crna; bez crvene |
| Domen | `SITE` na vrhu `izvor/alati/build-pages.py` + `sajt/robots.txt`, `sajt/sitemap.xml` (JSON-LD i OG se prave iz `SITE`) |

### Nove fotografije u galeriji

1. Ubaci JPEG u `izvor/originali/gallery-img/`.
2. `python3 izvor/alati/build-assets.py` pravi AVIF/WebP/JPEG u više veličina, blur-up placeholder i `izvor/generisano/meta.json`.
3. Dodaj red u listu `GAL` u `izvor/alati/build-pages.py` (ključ je ime fajla bez `.jpg`, zatim opis (alt), kratak natpis i oblik: `wide`, `tall`, `full` ili prazno).
4. Pokreni komande iz prethodnog odeljka. Za novu fotografiju se pojavljuje novo ime fajla pa nema problema sa kešom.

### Arhivske fotografije u vremenskoj liniji

U `TL` svaki čvor ima polje za sliku (trenutno samo „2020-e“). Dodaj ključ slike, opis i kadar po uzoru na tu stavku.

## Bezbednost (ukratko)

- CSP: `default-src 'self'` i ništa spolja, bez inline skripti i stilova (zato se sve animira preko CSS klasa i `style.setProperty`).
- Kontakt forma ne šalje ništa preko sajta: proveri polja, ima honeypot i otvara `mailto:` sa ispunjenom porukom. Adrese e-pošte su obični `mailto:` linkovi.
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
| `izvor/alati/build-assets.py` | slike, logo, favicon i OG slika iz `izvor/originali/` |
| `izvor/alati/build-fonts.py` | smanjuje fontove (izvori u `izvor/alati/fonts-src/`) |
| `izvor/alati/build-min.py` | spaja i minifikuje CSS/JS |
| `izvor/alati/build-pages.py` | generiše HTML stranice |
| | `izvor/alati/check-links.py` | proverava putanje i sidra |

Font: Manrope, SIL Open Font License 1.1.
