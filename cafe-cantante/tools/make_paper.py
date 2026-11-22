#!/usr/bin/env python3
"""Seamless paper tiles: kraft fibre (ground) and newsprint (clippings).

Deterministic (fixed seed). Fibres are short dark and light strokes plus a
fine grain, so the paper reads as paper in compression without a gradient.
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/paper"
S = 540


def tile(base, dark, light, n_fibres, grain, seed, name):
    rnd = random.Random(seed)
    im = Image.new("RGB", (S * 3, S * 3), base)
    d = ImageDraw.Draw(im)
    for _ in range(n_fibres):
        x, y = rnd.uniform(S, 2 * S), rnd.uniform(S, 2 * S)
        L = rnd.uniform(6, 34)
        dx, dy = rnd.uniform(-1, 1) * L, rnd.uniform(-0.35, 0.35) * L
        col = dark if rnd.random() < 0.6 else light
        a = rnd.uniform(0.15, 0.5)
        c = tuple(int(b + (cc - b) * a) for b, cc in zip(base, col))
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d.line((x + ox, y + oy, x + dx + ox, y + dy + oy), fill=c, width=1)
    im = im.crop((S, S, 2 * S, 2 * S)).filter(ImageFilter.GaussianBlur(0.45))
    px = im.load()
    for y in range(S):
        for x in range(S):
            g = int(rnd.gauss(0, grain))
            r, gg, b = px[x, y]
            px[x, y] = (max(0, min(255, r + g)), max(0, min(255, gg + g)), max(0, min(255, b + g)))
    OUT.mkdir(parents=True, exist_ok=True)
    im.save(OUT / name, optimize=True)
    print("wrote", OUT / name)


tile((201, 167, 124), (120, 88, 55), (226, 200, 160), 2600, 5, 7, "kraft-fibre.png")
tile((230, 220, 195), (150, 140, 120), (245, 240, 228), 1400, 4, 11, "newsprint.png")
