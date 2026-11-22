#!/usr/bin/env python3
"""Write compositions/captions.html from timings.json.

Each spoken phrase is cut into caption groups of at most MAX_WORDS words;
a group's time inside its phrase is proportional to its characters. Phrases
already pasted on screen word for word (Lorca's verse) are not captioned.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_WORDS = 5
SKIP = ("densa miel", "limón nuestro")
# Spoken numbers read better as figures on screen.
SHOW = {
    "mil ochocientos ochenta y uno": "1881",
    "mil ochocientos ochenta y nueve": "1889",
}


NOBREAK = ("Edad de Oro", "Morón de la Frontera", "Antonio Chacón", "Silverio Franconetti", "calle Rosario")
STOP = {"de", "la", "el", "en", "un", "una", "y", "que", "las", "los", "del", "al", "por", "se", "su", "a", "no", "ya"}


def groups(text):
    """Split at punctuation first, then into balanced runs of at most MAX_WORDS;
    a run never ends on a function word (it moves to the next run)."""
    out = []
    for clause in [c.strip() for c in __import__("re").findall(r"[^,.:;…]+[,.:;…]*", text) if c.strip()]:
        words = clause.split(" ")
        n = max(1, -(-len(words) // MAX_WORDS))
        size = -(-len(words) // n)
        runs = [words[i:i + size] for i in range(0, len(words), size)]
        # A run longer than one caption line is halved.
        fixed = []
        for r in runs:
            if len(" ".join(r)) > 32 and len(r) >= 4:
                h = len(r) // 2
                fixed += [r[:h], r[h:]]
            else:
                fixed.append(r)
        runs = fixed
        for i in range(len(runs) - 1):
            while len(runs[i]) > 1 and runs[i][-1].lower().strip(",.") in STOP:
                runs[i + 1].insert(0, runs[i].pop())
        out += [r for r in runs if r]
    # Merge one-word or two-word scraps into their neighbour when it stays short.
    merged = []
    for r in out:
        if merged and not merged[-1][-1].endswith((".", "…")) and (len(r) <= 2 or len(merged[-1]) <= 2) and len(merged[-1]) + len(r) <= MAX_WORDS + 1 and len(" ".join(merged[-1] + r)) <= 30:
            merged[-1] += r
        else:
            merged.append(r)
    return [" ".join(r).replace("\u00a0", " ") for r in merged]


KEYWORDS = ["cafés cantantes", "Silverio Franconetti", "Antonio Chacón", "Edad de Oro", "calle Rosario", "Lorca", "1881", "1889", "escenario", "vacía", "Andalucía", "cante"]


def mark(text):
    """Put the first brand keyword of a caption group in red (one per group)."""
    low = text.lower()
    for k in KEYWORDS:
        i = low.find(k.lower())
        if i >= 0:
            return text[:i] + '<span class="kw">' + text[i:i + len(k)] + "</span>" + text[i + len(k):]
    return text


def main():
    t = json.loads((ROOT / "timings.json").read_text())
    dur = t["duration"]
    items = []
    for s in t["scenes"]:
        for p in s["phrases"]:
            if any(k in p["text"] for k in SKIP):
                continue
            text = p["text"]
            for a, b in SHOW.items():
                text = text.replace(a, b)
            for k in NOBREAK:
                text = text.replace(k, k.replace(" ", "\u00a0"))
            gs = groups(text)
            total = sum(len(g) for g in gs)
            t0, span = p["start"], p["end"] - p["start"]
            for g in gs:
                d = span * len(g) / total
                items.append((round(t0, 3), round(d + 0.12, 3), g.rstrip(",:;")))
                t0 += d
    # Never overlap the next group.
    for i in range(len(items) - 1):
        s, d, g = items[i]
        items[i] = (s, round(min(d, items[i + 1][0] - s), 3), g)

    rows = []
    for i, (s, d, g) in enumerate(items):
        rows.append(
            f'    <div id="cap-{i+1:02d}" class="cap clip" data-start="{s}" data-duration="{d}">'
            f'<span class="cap-t">{mark(html.escape(g))}</span></div>'
        )
    doc = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    /* Brand subtitle plate (brand book §18): noche at 55 %, radius 14, cal Bold, one keyword in red. */
    .cap {{ position: absolute; left: 64px; width: 952px; top: 1290px; height: 150px; display: flex; align-items: flex-end; justify-content: center; }}
    .cap-t {{ display: inline-block; padding: 12px 24px 12px; background: rgba(20, 17, 16, 0.55); border-radius: 14px; color: #f4eee6;
      font-family: "Instrument Sans"; font-weight: 700; font-size: 54px; letter-spacing: -0.02em; line-height: 1.12; text-align: center; }}
    .kw {{ color: #d8231a; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    window.__timelines["captions"] = gsap.timeline({{ paused: true }});
  </script>
</template>
"""
    (ROOT / "compositions/captions.html").write_text(doc)
    print(f"{len(items)} caption groups, film {dur}s")


if __name__ == "__main__":
    main()
