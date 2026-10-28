// Učitava se u <head> pre iscrtavanja: tema, nivo uređaja (full/lite) i oznaka da JS radi.
(function () {
  var d = document.documentElement;
  d.classList.add('js');
  try { var t = localStorage.getItem('theme'); if (t === 'light' || t === 'dark') d.setAttribute('data-theme', t); } catch (e) {}
  var lite = false;
  try {
    var mem = navigator.deviceMemory, cores = navigator.hardwareConcurrency;
    if (cores && cores <= 4) lite = true;
    if (mem && mem <= 4) lite = true;
    if (window.matchMedia('(pointer: coarse)').matches && window.innerWidth < 900) lite = true;
    if (window.innerWidth < 560) lite = true;
    var c = navigator.connection; if (c && (c.saveData || /2g/.test(c.effectiveType || ''))) lite = true;
  } catch (e) {}
  d.setAttribute('data-tier', lite ? 'lite' : 'full');
})();
