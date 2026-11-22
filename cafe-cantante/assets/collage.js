/* Shared collage helpers for every scene. Deterministic: no Math.random. */
(function () {
  var F = 1 / 30;

  function rng(s) {
    return function () {
      s = (s * 16807) % 2147483647;
      return (s - 1) / 2147483646;
    };
  }

  // Torn paper edge: a jagged polygon fixed by the element's data-torn seed.
  // data-amp is the tooth depth in % of the element (default 1.4).
  function tornPolygon(seed, amp) {
    var r = rng(seed * 7919 + 13), n = 22, p = [], i;
    for (i = 0; i <= n; i++) p.push((i / n) * 100 + "% " + r() * amp + "%");
    for (i = 1; i <= n; i++) p.push(100 - r() * amp * 0.7 + "% " + (i / n) * 100 + "%");
    for (i = n - 1; i >= 0; i--) p.push((i / n) * 100 + "% " + (100 - r() * amp) + "%");
    for (i = n - 1; i >= 1; i--) p.push(r() * amp * 0.7 + "% " + (i / n) * 100 + "%");
    return "polygon(" + p.join(",") + ")";
  }

  function torn(scope) {
    scope.querySelectorAll("[data-torn]").forEach(function (el) {
      el.style.clipPath = tornPolygon(+el.dataset.torn, +(el.dataset.amp || 1.4));
    });
  }

  // A vertical tear: left and right halves sharing one jagged seam (x in %).
  function tearHalves(leftEl, rightEl, seed, x) {
    var r = rng(seed * 104729 + 7), n = 30, seam = [], i;
    for (i = 0; i <= n; i++) seam.push([x + (r() - 0.5) * 7, (i / n) * 100]);
    var L = ["0% 0%"].concat(seam.map(function (q) { return q[0] + "% " + q[1] + "%"; }), ["0% 100%"]);
    var R = seam.map(function (q) { return q[0] + "% " + q[1] + "%"; }).concat(["100% 100%", "100% 0%"]);
    leftEl.style.clipPath = "polygon(" + L.join(",") + ")";
    rightEl.style.clipPath = "polygon(" + R.join(",") + ")";
  }

  // Paper slapped down: from 125% to 100% in 8 frames with a slight overshoot.
  function slap(tl, sel, t, rot, opts) {
    opts = opts || {};
    rot = rot || 0;
    tl.fromTo(
      sel,
      { opacity: 0, scale: opts.from || 1.25, rotation: rot + (opts.spin == null ? 6 : opts.spin) },
      { opacity: 1, scale: 1, rotation: rot, duration: (opts.frames || 8) * F, ease: "back.out(1.6)", stagger: opts.stagger || 0 },
      t
    );
    return tl;
  }

  // Paper peeled off and carried out of frame.
  function lift(tl, sel, t, opts) {
    opts = opts || {};
    tl.to(
      sel,
      { y: opts.y == null ? -160 : opts.y, x: opts.x || 0, rotation: "+=" + (opts.rot == null ? 8 : opts.rot), opacity: 0, duration: (opts.frames || 12) * F, ease: "power2.in", stagger: opts.stagger || 0 },
      t
    );
    return tl;
  }

  window.Collage = { F: F, rng: rng, torn: torn, tearHalves: tearHalves, slap: slap, lift: lift };
})();
