// KUD „Abrašević“ — interakcije. Vanilla JS, bez zavisnosti. Animira se samo transform i opacity.
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lite = root.getAttribute('data-tier') === 'lite';
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- tema ---- */
  var themeBtn = $('[data-theme-toggle]');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  /* ---- navigacija: staklena traka + mobilni sheet ---- */
  var nav = $('.nav'), sheet = $('.sheet'), menuBtn = $('.menu-btn');
  function onScrollNav() { if (nav) nav.classList.toggle('scrolled', window.scrollY > 24); }
  onScrollNav();
  if (menuBtn && sheet) {
    var setMenu = function (open) {
      sheet.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? 'Zatvori meni' : 'Otvori meni');
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) { var a = $('a', sheet); if (a) a.focus(); } else menuBtn.focus();
    };
    menuBtn.addEventListener('click', function () { setMenu(!sheet.classList.contains('open')); });
    sheet.addEventListener('click', function (e) { if (e.target === sheet || e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('open')) setMenu(false); });
    sheet.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = $$('a,button', sheet).concat([menuBtn]);
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* ---- reveal pri skrolu ---- */
  var rv = $$('.rv');
  if (!('IntersectionObserver' in window) || reduce) {
    rv.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  }
  // slike: blur-up → prikaz kad su učitane
  $$('.ph img').forEach(function (img) {
    var show = function () { img.classList.add('in'); };
    if (img.complete && img.naturalWidth) show(); else { img.addEventListener('load', show); img.addEventListener('error', show); }
  });

  /* ---- brojači ---- */
  function runCount(el) {
    var to = +el.getAttribute('data-to'), from = +(el.getAttribute('data-from') || 0);
    var dur = +(el.getAttribute('data-dur') || 2200), t0 = null;
    function step(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = from; requestAnimationFrame(step);
  }
  var counters = $$('[data-count]');
  if (!reduce && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---- scroll: parallax (hero), progres linije, progres stranice ---- */
  var nativeScroll = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');
  var hero = $('.hero'), par = !reduce && !lite && !nativeScroll && hero;
  var tl = $('.timeline'), bar = $('.tl-bar'), items = $$('.tl-item');
  var prog = $('.progress'), nativeProg = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');
  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY, vh = window.innerHeight;
    onScrollNav();
    if (par && y < vh * 1.5) hero.style.setProperty('--py', (-y).toFixed(1));
    if (prog && !nativeProg) {
      var h = document.documentElement.scrollHeight - vh;
      prog.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0).toFixed(4) + ')';
    }
    if (tl && bar) {
      var r = tl.getBoundingClientRect();
      var p = (vh * 0.55 - r.top) / r.height;
      bar.style.transform = 'scaleY(' + Math.max(0, Math.min(1, p)).toFixed(4) + ')';
      var line = vh * 0.55;
      items.forEach(function (it) { it.classList.toggle('is-active', it.getBoundingClientRect().top < line); });
    }
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req);
  frame();

  /* ---- osvetljenje/tilt na staklenim karticama (samo fine pointer) ---- */
  if (fine && !reduce && !lite) {
    var raf = 0;
    document.addEventListener('pointermove', function (e) {
      var c = e.target.closest && e.target.closest('.tilt');
      if (!c) return;
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        var b = c.getBoundingClientRect(), x = (e.clientX - b.left) / b.width, y = (e.clientY - b.top) / b.height;
        c.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        c.style.setProperty('--rx', ((0.5 - y) * 5).toFixed(2) + 'deg'); c.style.setProperty('--ry', ((x - 0.5) * 6).toFixed(2) + 'deg');
      });
    });
    document.addEventListener('pointerout', function (e) {
      var c = e.target.closest && e.target.closest('.tilt');
      if (c && !c.contains(e.relatedTarget)) { c.style.setProperty('--rx', '0deg'); c.style.setProperty('--ry', '0deg'); }
    });
  }
})();

/* ---- e-pošta se sklapa u JS-u (zaštita od botova) ---- */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('a[data-mail]'), function (el) {
    var addr = el.getAttribute('data-mail').replace(' [at] ', '@');
    el.setAttribute('href', 'mailto:' + addr);
    if (el.hasAttribute('data-show')) el.textContent = addr;
  });
})();

/* ---- kontakt forma: validacija + mailto (bez backend-a) ---- */
(function () {
  var f = document.getElementById('contact-form');
  if (!f) return;
  var st = document.getElementById('f-status');
  function err(id, msg) { var e = document.getElementById(id); if (e) e.textContent = msg; return !msg; }
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    st.textContent = '';
    if (f.elements.website && f.elements.website.value) return; // honeypot: botovi ga popune
    var name = f.elements.name.value.trim(), mail = f.elements.email.value.trim(), msg = f.elements.message.value.trim();
    var ok = true;
    ok = err('e-name', name.length < 2 ? 'Upišite ime i prezime.' : '') && ok;
    ok = err('e-mail', /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail) ? '' : 'Upišite ispravnu adresu e-pošte.') && ok;
    ok = err('e-msg', msg.length < 10 ? 'Poruka je prekratka (najmanje 10 znakova).' : '') && ok;
    if (!ok) { var bad = f.querySelector('.err:not(:empty)'); if (bad) bad.previousElementSibling.focus(); return; }
    var to = f.getAttribute('data-mail').replace(' [at] ', '@');
    var subject = 'Poruka sa sajta KUD Abrašević — ' + name;
    var body = msg + '\n\n—\n' + name + '\n' + mail;
    window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    st.textContent = 'Otvaramo vaš program za e-poštu. Poruka je poslata tek kada u njemu pritisnete „Pošalji“.';
  });
})();

/* ---- lightbox bez biblioteke: <dialog>, tastatura, swipe, klik van slike ---- */
(function () {
  var dlg = document.getElementById('lb');
  var links = Array.prototype.slice.call(document.querySelectorAll('a[data-lb]'));
  if (!dlg || !links.length || typeof dlg.showModal !== 'function') return; // bez podrške: linkovi otvaraju sliku direktno
  var img = dlg.querySelector('.lb-stage img'), cap = dlg.querySelector('.lb-cap'), cnt = dlg.querySelector('.lb-count');
  var prev = dlg.querySelector('.lb-prev'), next = dlg.querySelector('.lb-next'), close = dlg.querySelector('.lb-close');
  var cur = 0, reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function altOf(a) { var i = a.querySelector('img'); return i ? i.getAttribute('alt') : ''; }
  function show(i, instant) {
    cur = (i + links.length) % links.length;
    var a = links[cur];
    var apply = function () {
      img.src = a.getAttribute('data-mid');
      img.srcset = a.getAttribute('data-mid') + ' 1200w, ' + a.getAttribute('data-full') + ' 1800w';
      img.sizes = '100vw';
      img.alt = altOf(a);
      cap.textContent = a.getAttribute('data-cap');
      cnt.textContent = (cur + 1) + ' / ' + links.length;
      img.classList.remove('swap');
    };
    if (instant || reduce) apply(); else { img.classList.add('swap'); setTimeout(apply, 140); }
    [cur - 1, cur + 1].forEach(function (n) { var p = new Image(); p.src = links[(n + links.length) % links.length].getAttribute('data-mid'); });
  }
  function open(i) {
    show(i, true);
    dlg.showModal();
    document.documentElement.style.overflow = 'hidden';
    close.focus();
  }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) { if (e.metaKey || e.ctrlKey || e.shiftKey) return; e.preventDefault(); open(i); });
  });
  prev.addEventListener('click', function () { show(cur - 1); });
  next.addEventListener('click', function () { show(cur + 1); });
  close.addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('close', function () { document.documentElement.style.overflow = ''; });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
  });
  // klik van slike (na pozadinu / praznu površinu) zatvara
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target.classList.contains('lb-stage') || e.target === cap) dlg.close();
  });
  // swipe
  var x0 = null, y0 = 0;
  dlg.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch') { x0 = e.clientX; y0 = e.clientY; } });
  dlg.addEventListener('pointerup', function (e) {
    if (x0 === null) return;
    var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(dx < 0 ? cur + 1 : cur - 1);
  });
  dlg.addEventListener('pointercancel', function () { x0 = null; });
})();
