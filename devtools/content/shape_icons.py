#!/usr/bin/env python3
"""Generate SVG versions of the Shapes tool's icons (data/images/shapes/).

usage: devtools/content/shape_icons.py [REPOSITORY_ROOT]

Sizes, places and line widths are measured from the PNG icons (40x30), so
the SVGs draw the same shapes, sharp at any size. Tux Paint uses them when
the buttons are bigger than 48x48 (see loadimagerb()).
"""
import math
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")
W, H = 40, 30


def write(name, body):
    path = os.path.join(ROOT, "data", "images", "shapes", name + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                'viewBox="0 0 %d %d">\n'
                '<!-- Drawn after %s.png (devtools/content/shape_icons.py) -->\n'
                '%s\n</svg>\n' % (W, H, W, H, name, body))
    print(os.path.normpath(path))


def polygon(points):
    return " ".join("%.2f,%.2f" % p for p in points)


def regular(cx, cy, r, n, start):
    """Corners of a regular n-gon, the first one at angle start (degrees,
    0 = up, clockwise)."""
    return [(cx + r * math.sin(math.radians(start + 360.0 * i / n)),
             cy - r * math.cos(math.radians(start + 360.0 * i / n))) for i in range(n)]


def both(name, outline, filled):
    write(name, outline)
    write(name + "_f", filled)


# Square: x 10-30, y 5-25, 1-pixel line
both("square",
     '<rect x="10.5" y="5.5" width="20" height="20" fill="none" stroke="#000" stroke-width="1"/>',
     '<rect x="10" y="5" width="21" height="21" fill="#000"/>')

# Rectangle: x 4-34, y 7-18
both("rectangle",
     '<rect x="4.5" y="7.5" width="30" height="11" fill="none" stroke="#000" stroke-width="1"/>',
     '<rect x="4" y="7" width="31" height="12" fill="#000"/>')

# Circle: 25 pixels across, centered at 20.5, 15.5
both("circle",
     '<circle cx="20.5" cy="15.5" r="12" fill="none" stroke="#000" stroke-width="1"/>',
     '<circle cx="20.5" cy="15.5" r="12.5" fill="#000"/>')

# Oval: x 3-36, y 12-22
both("oval",
     '<ellipse cx="20" cy="17.5" rx="16.5" ry="5" fill="none" stroke="#000" stroke-width="1"/>',
     '<ellipse cx="20" cy="17.5" rx="17" ry="5.5" fill="#000"/>')

# Octagon: 30 pixels across, flat sides up and down, 2-pixel line
both("octagon",
     '<polygon points="%s" fill="none" stroke="#000" stroke-width="2.1" '
     'stroke-linejoin="miter"/>' % polygon(regular(20, 15, (15 - 1.05) / math.cos(math.pi / 8), 8, 22.5)),
     '<polygon points="%s" fill="#000"/>' % polygon(regular(20, 15, 15 / math.cos(math.pi / 8), 8, 22.5)))

# Pentagon: 20 pixels across, a point up at y 5
r = 20 / (2 * math.sin(math.radians(72)))
both("pentagon",
     '<polygon points="%s" fill="none" stroke="#000" stroke-width="1.3" '
     'stroke-linejoin="miter"/>' % polygon(regular(20, 5 + r, r - 0.9, 5, 0)),
     '<polygon points="%s" fill="#000"/>' % polygon(regular(20, 5 + r, r, 5, 0)))

# Diamond: about 27 x 26, 1.9-pixel line (the filled one is a pixel more
# to the left)
both("diamond",
     '<polygon points="21.5,4.3 34,16 21.5,27.7 9,16" fill="none" stroke="#000" '
     'stroke-width="1.9" stroke-linejoin="miter"/>',
     '<polygon points="20.5,3 34,16 20.5,29 7,16" fill="#000"/>')

# Triangle: apex at 20.5, 5, base at y 22, x 9-32
both("triangle",
     '<polygon points="20.5,6.2 31,21.5 10,21.5" fill="none" stroke="#000" '
     'stroke-width="1" stroke-linejoin="miter"/>',
     '<polygon points="20.5,5 32,22 9,22" fill="#000"/>')
