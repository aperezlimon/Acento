#!/usr/bin/env python3
"""Turn a photo or engraving into ink halftone dots on a transparent ground.

The look of the film is printed paper: every image is dots of one ink
(#1B1712), so the kraft or newsprint paper behind it shows through.

Usage: halftone.py SRC OUT WIDTH HEIGHT [--pitch 8] [--crop x0,y0,x1,y1]
                   [--angle 45] [--contrast 1.25] [--gamma 1.0]
Crop is in source-pixel fractions (0..1). The image is cover-fitted to WIDTH x HEIGHT.
"""
import argparse
import math
from PIL import Image, ImageDraw, ImageOps, ImageEnhance

INK = (27, 23, 18)
SS = 3  # supersampling for clean dot edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("width", type=int); ap.add_argument("height", type=int)
    ap.add_argument("--pitch", type=float, default=8)
    ap.add_argument("--crop", default="0,0,1,1")
    ap.add_argument("--angle", type=float, default=45)
    ap.add_argument("--contrast", type=float, default=1.25)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--max-dot", type=float, default=0.72,
                    help="dot radius at full black, as a fraction of pitch")
    a = ap.parse_args()

    im = Image.open(a.src).convert("L")
    x0, y0, x1, y1 = (float(v) for v in a.crop.split(","))
    im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im = ImageOps.fit(im, (a.width, a.height), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(a.contrast)

    W, H = a.width * SS, a.height * SS
    p = a.pitch * SS
    big = im.resize((W, H), Image.BILINEAR)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    th = math.radians(a.angle)
    c, s = math.cos(th), math.sin(th)
    cx, cy = W / 2, H / 2
    R = math.hypot(W, H) / 2 + p
    n = int(R / p) + 1
    px = big.load()
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = i * p, j * p
            x = cx + u * c - v * s
            y = cy + u * s + v * c
            if not (-p <= x < W + p and -p <= y < H + p):
                continue
            sx, sy = min(W - 1, max(0, int(x))), min(H - 1, max(0, int(y)))
            dark = 1 - (px[sx, sy] / 255.0)
            dark = dark ** a.gamma
            r = a.max_dot * p * math.sqrt(dark)
            if r > 0.35 * SS:
                d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    mask = mask.resize((a.width, a.height), Image.LANCZOS)
    out = Image.new("RGBA", (a.width, a.height), INK + (0,))
    out.putalpha(mask)
    out.save(a.out, optimize=True)
    print("wrote", a.out, a.width, "x", a.height)


if __name__ == "__main__":
    main()
