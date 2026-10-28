# Zadatak: Novi sajt za KUD „Abrašević“ Kraljevo (100 godina, 1926–2026)

Ti si senior front-end dizajner i developer. Napravi potpuno novi, moderan, siguran i responzivan sajt za Kulturno-umetničko društvo „Abrašević“ iz Kraljeva. Sajt mora da PRIČA PRIČU jednog veka igre, pesme i tradicije.

## 0. Prvo uradi ovo (redom, pre pisanja koda)

1. **Pročitaj SKILL.md** koji se nalazi u projektu (potraži ga: `find . -name "SKILL.md"`). Njegova pravila o dizajnu imaju prednost nad tvojim podrazumevanim izborima. Ako postoji `frontend-design` ili `ui-ux-pro-max` skill, učitaj ih takođe.
2. **Pregledaj `assets/`**: `assets/logo*` i `assets/gallery-img/*`. Izlistaj fajlove, proveri dimenzije i veličine, pogledaj slike (Read) i na osnovu njih izvuci paletu boja iz logoa.
3. **Pročitaj stari sajt https://abrasevic.rs** i izvuci sav tekst, nazive sekcija, kontakt podatke, adresu, društvene mreže, imena rukovodilaca i ansambala. Probaj WebFetch ili `curl`. **Ako je pristup blokiran, NE zaobilazi blokadu**, već me zamoli da nalepim tekst sa stranica, pa nastavi.
4. Napravi kratak plan (struktura fajlova, sekcije, animacioni sistem) i pređi na izradu bez čekanja na odobrenje, osim ako ti nešto bitno nedostaje.

## 1. Tehnička ograničenja

- **Samo statički sajt: čist HTML, CSS i vanilla JS.** Nema Node servera, PHP-a, baze, build koraka koji server mora da izvršava. Bez frameworka. Ako koristiš alat za optimizaciju slika lokalno, rezultat mora biti gotov statički folder spreman za upload.
- Struktura (predlog): `index.html`, `css/`, `js/`, `assets/`. Višestranični ili jedna dugačka stranica sa sidrima: odluči šta bolje služi priči, ali meni i footer moraju raditi na obe varijante. Preferiram jednu snažnu početnu stranicu + `istorija.html`, `sekcije.html`, `galerija.html`, `kontakt.html` ako ima dovoljno sadržaja.
- Bez eksternih zavisnosti koje nisu neophodne. Fontove **self-hostuj** (woff2, `font-display: swap`). Nema Google Fonts linkova, jQuery-ja ni trekera.
- Nema `eval`, nema `innerHTML` sa nepouzdanim podacima, nema inline `onclick` atributa.

## 2. Sigurnost (obavezno)

- `Content-Security-Policy` preko `<meta http-equiv>` (npr. `default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'none'; form-action 'self' mailto:; frame-ancestors` ne radi preko meta, pa ga navedi u fajlu iz tačke ispod). Bez inline skripti i stilova gde god je moguće.
- Priloži **`.htaccess` i `_headers`** (kao primere, jer ne znam koji je web server) sa: CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` (isključi kameru, mikrofon, geolokaciju), `X-Frame-Options: DENY`, HSTS, keširanje statike, gzip/brotli.
- Svi spoljni linkovi: `rel="noopener noreferrer"`. Društvene mreže samo kao obični linkovi.
- Kontakt forma (ako je ima): bez backend-a ne sme da „obećava“ slanje. Ili koristi `mailto:` sa jasnom porukom, ili samo prikaži kontakt podatke. Dodaj honeypot polje i validaciju na klijentu. Email adresu zaštiti od bot-prikupljanja (sastavi je u JS-u).
- Ne ostavljaj lične podatke maloletnika na sajtu (imena dece uz fotografije) osim ako ih ja izričito dam.

## 3. Dizajn: „Apple glass“ + narativ

**Estetika:** Apple-ov „liquid glass“ / glassmorphism, ali elegantno, ne kičasto.
- Poluprozirni paneli: `backdrop-filter: blur(20px) saturate(180%)`, tanke svetle ivice (1px, `rgba(255,255,255,.25)`), unutrašnji highlight, meke velike senke, veliki radijusi (20–28px).
- Slojevi: pozadina sa velikim, blago pokretnim gradijent-oblicima (iz boja logoa) ili fotografijom, preko nje staklene kartice. Navigacija je plutajuća staklena traka koja se menja pri skrolu.
- **Fallback**: `@supports not (backdrop-filter: blur(1px))` daje čvrstu poluprozirnu pozadinu. Proveri kontrast teksta na staklu (WCAG AA, min 4.5:1). Dodaj tamnu temu preko `prefers-color-scheme` i ručni prekidač.
- Tipografija: izražajan serif za naslove (osećaj tradicije, mora podržavati **ćirilicu i latinicu sa č, ć, š, ž, đ**) + čist sans za tekst. Veliki, hrabri naslovi, puno belog prostora.
- Boje izvuci iz logoa. Ako logo nema jasnu paletu, predloži toplu narodnu paletu (tamnocrvena, zlatna/okr, duboka tamna, krem), ali ostani dosledan.

**Naglasak na 100 godina (najvažnije):**
- Hero: ogromno „100“ kao vizuelni element (npr. brojač koji se animira 1926 → 2026), uz slogan, npr. „Vek igre, pesme i tradicije“ (možeš predložiti bolji). Logo i oznaka „1926–2026“ vidljivi od prvog ekrana.
- Jubilarna oznaka (pečat/značka „100 godina“) vraća se kroz sajt: u navigaciji, footeru, naslovima sekcija.
- Posebna sekcija „Jubilej“ (događaji, program, najave). Ostavi je lako izmenljivom jer nemam sve podatke.

**Priča (scrollytelling):** sajt se čita kao putovanje kroz vek:
1. Hero: 100 godina.
2. Početak: 1926, osnivanje, ime po pesniku Kosti Abraševiću.
3. **Vremenska linija 1926 → 2026** (vertikalna, pinovana ili sa progresom pri skrolu), čvorovi dekada sa kratkim tekstom i slikom.
4. Ko smo danas: sekcije i ansambli.
5. Nastupi, festival, gostovanja.
6. Galerija.
7. Pridruži nam se + kontakt.
Svaka sekcija ima kratak emotivan uvod pre „informacija“.

## 4. Animacije (ključne, ali performantne)

- Reveal pri skrolu preko `IntersectionObserver` (fade/slide/blur-in, stagger za kartice). Za moderne browsere koristi i `animation-timeline: scroll()/view()` uz fallback.
- Parallax slojevi u hero-u, magnetno/„tilt“ osvetljenje na staklenim karticama pratilo bi miš (samo na uređajima sa `pointer: fine`).
- Brojači (1926 → 2026, broj članova, nastupa), progres linija na timeline-u, plutajući gradijent-oblici u pozadini, smooth lightbox prelazi, hover stanja sa „sjajem“.
- **Animiraj samo `transform` i `opacity`**, koristi `will-change` štedljivo. Bez layout thrashinga.
- **Poštuj `prefers-reduced-motion`**: sve isključi ili svedi na jednostavan fade.
- **Dva nivoa (tiered):** detektuj slabije uređaje (`navigator.hardwareConcurrency <= 4`, `deviceMemory`, `matchMedia('(pointer: coarse)')`, mala širina) i na njima isključi teške efekte (veliki blur, parallax, čestice), a zadrži osnovne reveal-e. Nijedan telefon ne sme da laguje.
- Cilj: Lighthouse Performance ≥ 90 na mobilnom, bez CLS skokova.

## 5. Sadržaj

- **Prepiši i prerasporedi tekst sa starog sajta.** Tekst mi se ne sviđa kako je prikazan, ali ga iskoristi: razbij ga u **kartice** (npr. po sekciji/ansamblu: naziv, kratak opis, uzrast, termin proba ako ga ima, dugme), istakni ključne rečenice, skrati dugačke paragrafe, dodaj naslove i ikonice (inline SVG). Ne izmišljaj činjenice.
- Sve što ne znaš (datumi, rukovodioci, termini proba, brojevi) označi vidljivim `<!-- TODO: -->` komentarom i spiskom na kraju rada, a na stranici stavi neutralan tekst, ne lažne podatke.
- Provereno (koristi): KUD „Abrašević“ Kraljevo osnovan je **1926**. Iz njegovih redova formirano je 1949. prvo profesionalno pozorište u Kraljevu. Među rukovodiocima bio je i profesor Vesnić (1945–1947). Društvo ima tradicionalni međunarodni festival folklora **„Leto kod Abraševića“**. Ime nosi po pesniku Kosti Abraševiću. Sve ostalo proveri sa starog sajta ili me pitaj.
- Jezik: srpski (latinica), ispravni dijakritici. Predloži i opciju prekidača latinica/ćirilica samo ako ne komplikuje kod.

## 6. Galerija

- Koristi slike iz `assets/gallery-img/`. Napravi optimizovane verzije (WebP/AVIF + JPEG fallback, više veličina, `srcset`/`sizes`), sačuvaj originale netaknute. Blur-up/dominant-color placeholder.
- Masonry ili bento raspored u staklenim okvirima, `loading="lazy"`, `decoding="async"`, eksplicitne `width/height`.
- Lightbox bez biblioteke: tastatura (Esc, strelice), swipe na telefonu, fokus-trap, `aria-modal`, zatvaranje klikom van slike.
- Smisleni `alt` tekstovi (ako ne znaš šta je na slici, pogledaj je i opiši).

## 7. Responzivnost i pristupačnost

- Mobile-first, testiraj 360, 390, 768, 1024, 1440 px. Bez horizontalnog skrola. Meni na telefonu: staklena „sheet“ navigacija.
- Semantički HTML (`header/nav/main/section/footer`), jedan `h1`, skip-link, vidljiv fokus, tastaturna navigacija, ARIA samo gde treba, dovoljno velike ciljne površine (≥44px).

## 8. SEO i deljenje

- `<title>`, meta opis, canonical, Open Graph i Twitter kartice (napravi OG sliku 1200×630 sa logoom i „100 godina“), `lang="sr"`, favicon set iz logoa, `site.webmanifest`.
- JSON-LD (`PerformingGroup` ili `Organization`) sa podacima koje potvrdimo, `sitemap.xml`, `robots.txt`, 404 stranica u istom stilu.

## 9. Kontrola kvaliteta pre predaje

- Proveri sve linkove i putanje slika, validiraj HTML, pokreni Lighthouse ako je dostupan (ili ručno proceni), proveri kontrast i `prefers-reduced-motion`, testiraj na uskom ekranu.
- Napravi `README.md`: struktura fajlova, kako se menja tekst/slike/događaji, kako se postavlja na server (samo upload statičkih fajlova), lista TODO podataka koje treba da dobijem od KUD-a.

## 10. Način rada

Radi samostalno i u fazama: (1) pregled resursa i plan, (2) dizajn sistem (CSS promenljive, glass komponente, tipografija), (3) hero + timeline, (4) ostale sekcije i kartice, (5) galerija, (6) animacije i optimizacija, (7) sigurnosna zaglavlja, SEO, README. Posle svake faze kratko javi šta je urađeno. Na kraju daj sažetak i listu stvari koje moram da potvrdim.
