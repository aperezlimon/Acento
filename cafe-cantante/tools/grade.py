#!/usr/bin/env python3
"""Archival grade for the v2 photos: a warm two-tone print, no halftone.

Maps luminance onto ink (#16130f) -> paper (#efe6d4), lifts contrast a little,
optionally upscales small originals (Lanczos + unsharp + fine grain, so the
softness reads as an old print rather than as digital blur).

Usage: grade.py SRC OUT [--crop x0,y0,x1,y1 in px] [--upscale 2.0] [--grain 6] [--color]
"""
import argparse
import random
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

INK = (22, 19, 15)
PAPER = (239, 230, 212)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--crop")
    ap.add_argument("--upscale", type=float, default=1.0)
    ap.add_argument("--grain", type=float, default=4.0)
    ap.add_argument("--contrast", type=float, default=1.12)
    ap.add_argument("--color", action="store_true", help="keep colour (maps), only warm it")
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGB")
    if a.crop:
        im = im.crop(tuple(int(v) for v in a.crop.split(",")))
    if a.upscale != 1.0:
        im = im.resize((round(im.width * a.upscale), round(im.height * a.upscale)), Image.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    if a.color:
        out = ImageEnhance.Color(im).enhance(0.55)
        out = Image.blend(out, Image.new("RGB", out.size, PAPER), 0.08)
    else:
        g = ImageOps.autocontrast(im.convert("L"), cutoff=0.5)
        g = ImageEnhance.Contrast(g).enhance(a.contrast)
        out = ImageOps.colorize(g, INK, PAPER)
    if a.grain:
        rnd = random.Random(17)
        px = out.load()
        for y in range(out.height):
            for x in range(out.width):
                n = int(rnd.gauss(0, a.grain))
                r, gg, b = px[x, y]
                px[x, y] = (max(0, min(255, r + n)), max(0, min(255, gg + n)), max(0, min(255, b + n)))
    out.save(a.out, quality=90, optimize=True)
    print("wrote", a.out, out.size)


if __name__ == "__main__":
    main()
