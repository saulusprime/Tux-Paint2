#!/usr/bin/env python3
"""Draw the icon of the Cross Stitch Magic tool (magic/icons/crossstitch.png).

usage: devtools/content/crossstitch_icon.py [REPOSITORY_ROOT]

A heart of cross stitches, black on transparent like the other Magic icons
(40x30), drawn 8 times bigger and then reduced, for smooth edges.
"""
import os
import sys

from PIL import Image, ImageDraw

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")
W, H = 40, 30
K = 8              # drawing enlargement
CELL = 5           # a square of the fabric, in icon pixels
HEART = [
    ".XX.XX.",
    "XXXXXXX",
    "XXXXXXX",
    ".XXXXX.",
    "..XXX..",
    "...X...",
]

big = Image.new("RGBA", (W * K, H * K), (0, 0, 0, 0))
draw = ImageDraw.Draw(big)
left = (W - CELL * len(HEART[0])) / 2.0
top = (H - CELL * len(HEART)) / 2.0

for row, line in enumerate(HEART):
    for col, c in enumerate(line):
        x0 = (left + col * CELL) * K
        y0 = (top + row * CELL) * K
        x1 = x0 + CELL * K
        y1 = y0 + CELL * K
        if c != "X":
            continue
        inset = K * 0.6
        width = int(K * 1.3)
        draw.line((x0 + inset, y0 + inset, x1 - inset, y1 - inset),
                  fill=(0, 0, 0, 200), width=width)
        draw.line((x1 - inset, y0 + inset, x0 + inset, y1 - inset),
                  fill=(0, 0, 0, 255), width=width)

path = os.path.join(ROOT, "magic", "icons", "crossstitch.png")
big.resize((W, H), Image.LANCZOS).save(path, optimize=True)
print(os.path.normpath(path))
