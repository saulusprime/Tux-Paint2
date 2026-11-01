#!/usr/bin/env python3
"""Make the traced SVG versions of PNG icons: of the tools
(data/images/tools/), of some interface images (data/images/ui/) and of
the Magic tools (magic/icons/).

usage: devtools/content/svg_icons.py POTRACE_DIR [REPOSITORY_ROOT]

Runs trace_icons.py (see there for POTRACE_DIR) on the icons that trace
well, each in the way that suits it. Tux Paint draws the SVG instead of
the PNG when the buttons are bigger than 48x48 (loadimagerb(), and the
Magic API's load_icon() for plugins). The choice was made looking at each
icon at 2.67 times its size, PNG (enlarged with Lanczos) next to the two
kinds of tracing:

- LINES: black line art, traced in the default two layers;
- TONES: flat greys, traced with --tones, one layer for each grey;
- the others stay PNG: gradients, shading, light parts inside dark ones,
  photos. Tools: sfx, speak. Interface: the gel buttons (yes, no, back,
  erase, open, play, scroll arrows), trash, printer, mouse, mirror,
  paintcan, popup_arrow, select_digits, the on-screen keyboard's keys, and
  magic_paint with magic_fullscreen (the second doesn't trace well, and
  they're side by side). Magic: alien, blind, blur, cartoon, chalk, edges,
  emboss, fade, fill, foam, fold, light, metalpaint, mirror, noise, puzzle,
  rain, rainbow, realrainbow, ripples, sharpen, smudge, snowball, the three
  string_art, tint, toothpaste, wetpaint, xor.
"""
import os
import subprocess
import sys

TOOLS = """brush eraser label label_select lines magic new open print quit
redo save shapes stamp text undo""".split()

UI = """bold dead40x40 flip grow italic next prev save_over shrink
slideshow""".split()

LINES = """calligraphy crossstitch distortion drip fisheye flip fretwork glasstile
halftone kal_pattern kal_tiles kalidescope largebrick mosaic mosaic_shaped_hex
mosaic_shaped_irregular mosaic_shaped_square negative perspective picasso
realrainbow-roygbiv rosette shift silhouette smallbrick snowflake
symmetric_leftright symmetric_updown tornado tv wavelet waves zoom""".split()

TONES = "blocks colornwhite confetti darken flower grass".split()

potrace = sys.argv[1]
root = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")
trace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "trace_icons.py")

for folder, names, options in (
        (("data", "images", "tools"), TOOLS, []),
        (("data", "images", "ui"), UI, []),
        (("magic", "icons"), LINES, []),
        (("magic", "icons"), TONES, ["--tones"])):
    subprocess.run([sys.executable, trace, potrace] + options +
                   [os.path.join(root, *folder, n + ".png") for n in names], check=True)
