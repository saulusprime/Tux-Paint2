#!/usr/bin/env python3
"""Vectorize greyscale UI icons (black line art) into SVG, with potrace.

usage: trace_icons.py POTRACE_DIR ICON.png...    (writes ICON.svg next to it)

POTRACE_DIR holds potrace's mkbitmap and potrace programs (bin/) and
library (lib/), e.g. extracted from Debian's potrace and libpotrace0
packages. Each icon is traced in three layers: where it's visible (filled
with its typical light color, if it has light parts), where there's some
ink (half-transparent black: thin light lines, shading, soft edges; the
icons are mostly black with some transparency), and where it's dark
(black). The SVG keeps the PNG's size, which Tux Paint takes as the design
size.
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
    icon_to_svg(png)
