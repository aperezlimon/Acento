/* Acento motion helpers (brand book §19): 180 bpm grid, firm short springs, 23° cuts.
   Deterministic: no Math.random, no timers. */
(function () {
  var BEAT = 1 / 3; // 333 ms
  var F = 1 / 30;

  // Entrances land on the beat grid.
  function snap(t) { return Math.round(t / BEAT) * BEAT; }

  // A firm entrance: small scale settle, no slide, no bounce.
  function enter(tl, sel, t, opts) {
    opts = opts || {};
    tl.fromTo(sel, { opacity: 0, scale: opts.from || 0.94 }, { opacity: 1, scale: 1, duration: opts.dur || 8 * F, ease: "power3.out", stagger: opts.stagger || 0 }, snap(t));
  }

  // Words are written left to right (a clip wipe).
  function write(tl, sel, t, dur) {
    tl.fromTo(sel, { clipPath: "inset(-20% 100% -20% 0%)" }, { clipPath: "inset(-20% 0% -20% 0%)", duration: dur || 9 * F, ease: "power2.out" }, snap(t));
  }

  // A picture is revealed by a diagonal edge at the brand angle (23°), left to right.
  function reveal(tl, sel, t, dur) {
    tl.fromTo(sel,
      { clipPath: "polygon(-60% 0%, -60% 0%, -102% 100%, -102% 100%)" },
      { clipPath: "polygon(-60% 0%, 160% 0%, 118% 100%, -102% 100%)", duration: dur || 2 * BEAT, ease: "power2.inOut" }, snap(t));
  }

  // Clear an element along the same diagonal.
  function conceal(tl, sel, t, dur) {
    tl.to(sel, { clipPath: "polygon(160% 0%, 160% 0%, 118% 100%, 118% 100%)", duration: dur || 2 * BEAT, ease: "power2.in" }, snap(t));
  }

  // Red flash of the background on a sounding accent (10–15 %).
  function flash(tl, sel, t) {
    tl.fromTo(sel, { opacity: 0 }, { opacity: 0.14, duration: 2 * F, ease: "none" }, snap(t));
    tl.to(sel, { opacity: 0, duration: 8 * F, ease: "power2.out" }, snap(t) + 2 * F);
  }

  // Huella rítmica: light the 12 beats in order, accents grow, the 12 lands red.
  function huella(tl, scopeSel, t) {
    var items = document.querySelectorAll(scopeSel + " .hb");
    items.forEach(function (el, i) {
      tl.fromTo(el, { opacity: 0.18 }, { opacity: 1, duration: 2 * F, ease: "none" }, snap(t) + i * BEAT);
      if (el.classList.contains("acc")) {
        tl.fromTo(el.querySelector("svg"), { scale: 0.6, transformOrigin: "30% 90%" }, { scale: 1, duration: 5 * F, ease: "power3.out" }, snap(t) + i * BEAT);
      }
    });
  }

  window.Acento = { BEAT: BEAT, F: F, snap: snap, enter: enter, write: write, reveal: reveal, conceal: conceal, flash: flash, huella: huella };
})();
