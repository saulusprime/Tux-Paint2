#!/usr/bin/env python3
"""Vectorize greyscale UI icons (black line art) into SVG, with potrace.

usage: trace_icons.py POTRACE_DIR [--tones] ICON.png...
       (writes ICON.svg next to each)

POTRACE_DIR holds potrace's mkbitmap and potrace programs (bin/) and
library (lib/), e.g. extracted from Debian's potrace and libpotrace0
packages. The icons are mostly black with some transparency. Each one is
traced in layers: where it's visible (filled with its typical light
color, if it has light parts), then the ink on top:

- by default, two layers: where there's some ink (half-transparent black:
  thin light lines, shading, soft edges) and where it's dark (black);
- with --tones, a layer for each flat tone of the icon, found in the
  histogram of its darkness away from edges, with the opacity that gives
  that tone once stacked. A black-only icon is one layer, cut at half
  darkness, so its lines keep their weight; flat greys stay grey.
  Gradients get only their flat parts: such icons look better as PNGs.

The SVG keeps the PNG's size, which Tux Paint takes as the design size.
"""
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

SCALE = 8          # mkbitmap's enlargement before tracing

tools = sys.argv[1]
env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(tools, "lib"))
tones = "--tones" in sys.argv[2:]


def trace(mask, tmp, name, coverage):
    """Trace where a greyscale coverage mask (255 = full) is at least
    coverage (0 to 1); SVG path data and potrace's transform, in
    SCALE-times enlarged coordinates."""
    pgm = os.path.join(tmp, name + ".pgm")
    pbm = os.path.join(tmp, name + ".pbm")
    svg = os.path.join(tmp, name + ".svg")
    # mkbitmap and potrace want dark = inside: what's darker than the
    # threshold
    Image.eval(mask, lambda v: 255 - v).save(pgm)
    subprocess.run([os.path.join(tools, "bin", "mkbitmap"), "-n", "-s", str(SCALE),
                    "-3", "-t", str(1 - coverage), "-o", pbm, pgm], check=True, env=env)
    subprocess.run([os.path.join(tools, "bin", "potrace"), "-s", "-t", "4",
                    "-O", "0.4", "-a", "1.0", "--flat", "-o", svg, pbm], check=True, env=env)
    text = open(svg).read()
    transform = re.search(r'<g transform="([^"]*)"', text)
    paths = re.findall(r'<path d="([^"]*)"', text)
    return (transform.group(1) if transform else ""), " ".join(paths)


def tone_levels(dark, w, h):
    """The flat tones of darkness (1-255) in an icon: peaks of the
    histogram of pixels whose 3x3 neighbourhood is even."""
    px = dark.load()
    hist = [0] * 16
    values = []
    for y in range(h):
        for x in range(w):
            v = px[x, y]
            if v <= 20:
                continue
            near = [px[i, j] for i in range(max(0, x - 1), min(w, x + 2))
                    for j in range(max(0, y - 1), min(h, y + 2))]
            if max(near) - min(near) > 24:
                continue
            hist[v // 16] += 1
            values.append(v)
    if not values:
        return [255]
    levels = []
    for b in range(16):
        if hist[b] < 0.04 * len(values):
            continue
        if (b > 0 and hist[b - 1] > hist[b]) or (b < 15 and hist[b + 1] >= hist[b]):
            continue
        near = [v for v in values if abs(v - (b * 16 + 8)) <= 20]
        level = sum(near) // len(near)
        if levels and level - levels[-1] < 40:
            continue
        levels.append(level)
    return levels or [255]


def icon_to_svg(png):
    im = Image.open(png).convert("RGBA")
    w, h = im.size
    alpha = im.getchannel("A")
    lum = im.convert("L")

    visible = alpha
    dark = Image.new("L", (w, h))
    greys = []
    for y in range(h):
        for x in range(w):
            a = alpha.getpixel((x, y))
            l = lum.getpixel((x, y))
            dark.putpixel((x, y), a * (255 - l) // 255)
            if a >= 128 and l > 64:
                greys.append(l)

    layers = []
    with tempfile.TemporaryDirectory() as tmp:
        if len(greys) >= 4:
            greys.sort()
            grey = greys[len(greys) // 2]
            layers.append(('fill="#%02x%02x%02x"' % (grey, grey, grey),) +
                          trace(visible, tmp, "visible", 0.5))
        if tones:
            # Stacked layers of black: after layer i the darkness is
            # levels[i], so its opacity is what's left to get there
            below = 0
            for i, level in enumerate(tone_levels(dark, w, h)):
                opacity = (level - below) / (255.0 - below)
                cut = (below + level) / 2.0 / 255
                fill = 'fill="#000000"' + (' fill-opacity="%.3f"' % opacity if opacity < 0.995 else '')
                layers.append((fill,) + trace(dark, tmp, "tone%d" % i, cut))
                below = level
        else:
            layers.append(('fill="#000000" fill-opacity="0.4"',) + trace(dark, tmp, "ink", 0.2))
            layers.append(('fill="#000000"',) + trace(dark, tmp, "dark", 0.5))

    body = ""
    for fill, transform, paths in layers:
        if paths:
            body += '<g transform="scale(%g) %s" %s>\n<path d="%s"/>\n</g>\n' % (
                1.0 / SCALE, transform, fill, paths)

    svg = png[:-4] + ".svg"
    with open(svg, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                'viewBox="0 0 %d %d">\n'
                '<!-- Traced from %s with potrace (devtools/content/trace_icons.py) -->\n'
                '%s</svg>\n' % (w, h, w, h, os.path.basename(png), body))
    print(svg)


for png in sys.argv[2:]:
    if png != "--tones":
        icon_to_svg(png)
