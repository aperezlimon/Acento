/* Editorial helpers for the v2 scenes. Deterministic: no Math.random. */
(function () {
  var F = 1 / 30;

  // A headline is printed left to right (a wipe), never faded or slid up.
  function wipe(tl, sel, t, dur) {
    tl.fromTo(sel, { clipPath: "inset(-10% 100% -10% 0%)" }, { clipPath: "inset(-10% 0% -10% 0%)", duration: dur || 12 * F, ease: "power2.out" }, t);
  }

  // Marker highlight behind a word: the albero bar is drawn, the word turns ink.
  function mark(tl, sel, t) {
    var bars = sel + " .mk-bar", words = sel + " .mk-t";
    tl.fromTo(bars, { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 9 * F, ease: "power2.inOut" }, t);
    tl.fromTo(words, { color: "var(--color-paper)" }, { color: "var(--color-ink)", duration: 3 * F, ease: "none" }, t + 9 * F);
  }

  // A label tag lands: a short scale settle, no fade-up.
  function tag(tl, sel, t) {
    tl.fromTo(sel, { opacity: 0, scale: 1.18 }, { opacity: 1, scale: 1, duration: 6 * F, ease: "back.out(1.7)" }, t);
  }

  // Draw an SVG stroke (ring, leader line).
  function draw(tl, el, t, dur) {
    var L = el.getTotalLength();
    tl.fromTo(el, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur || 14 * F, ease: "power2.inOut" }, t);
  }

  // Slow camera on a photograph.
  function drift(tl, sel, from, to, t, dur) {
    tl.fromTo(sel, from, Object.assign({ duration: dur, ease: "sine.inOut" }, to), t);
  }

  // Leave: a hard cut is the default between scenes; this is for elements that clear mid-scene.
  function clear(tl, sel, t) {
    tl.to(sel, { clipPath: "inset(-10% 0% -10% 100%)", duration: 8 * F, ease: "power2.in" }, t);
  }

  window.Ed = { F: F, wipe: wipe, mark: mark, tag: tag, draw: draw, drift: drift, clear: clear };
})();
