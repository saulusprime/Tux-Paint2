#!/usr/bin/env python3
"""make_hard.py: builds the hard lessons drawn with lessonkit (hard_a.py,
hard_b.py: biplane, garden chair, gumball machine, gummy bears, cat with a
pumpkin, horse with a foal, knitting friends, chicks in a nest, two foxes,
vulture) and checks them.

  python3 devtools/content/lessonkit/make_hard.py [--out DIR] [--only NAME,...] [--sheet FILE.png]

  --out DIR        where NAME.svg and NAME.txt go (default: lessons/hard)
  --only NAME,...  only these lessons (the files' names, e.g. two-foxes)
  --sheet FILE     also draw all the finished pictures on one sheet

For each lesson it prints its steps and the color report: errors (a seed
in the background: a gap in the lines), warnings, big areas left white
(often meant: eyes, the sky) and what check_areas.py finds. Exits with 1
on errors or area problems. Then check the steps with
../lesson_preview.py, which also draws them."""

import argparse
import os
import sys

from PIL import Image, ImageDraw

import check_areas
import hard_a
import hard_b
from lessonkit import lp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))


def main():
    ap = argparse.ArgumentParser(description="Builds and checks the hard lessons drawn with lessonkit.")
    ap.add_argument("--out", default=os.path.join(REPO, "lessons", "hard"))
    ap.add_argument("--only", default="")
    ap.add_argument("--sheet")
    args = ap.parse_args()
    only = [n for n in args.only.split(",") if n]
    lessons = [fn() for fn in hard_a.LESSONS + hard_b.LESSONS]
    unknown = set(only) - {les.name for les in lessons}
    if unknown:
        sys.exit(f"no such lesson: {', '.join(sorted(unknown))}")
    os.makedirs(args.out, exist_ok=True)
    pics, bad = [], 0
    for les in lessons:
        if only and les.name not in only:
            continue
        report = les.build(args.out)
        txt = os.path.join(args.out, les.name + ".txt")
        problems, areas = check_areas.check(txt)
        print(f"== {les.name}: {len(les.steps)} steps, {areas} areas, {len(problems)} area problems")
        for line in report + problems:
            print("   ", line)
        bad += sum(1 for line in report if line.startswith("ERROR")) + len(problems)
        if args.sheet:
            lesson = lp.parse_lesson(txt)
            img = lp.compose(lp.Svg(lesson.svg_path), lesson, len(lesson.steps) - 1, 640, 480, final=True)
            pics.append((les.name, img.convert("RGB")))
    if pics:
        w, h = 640, 480
        cols = 2 if len(pics) > 1 else 1
        rows = (len(pics) + cols - 1) // cols
        sheet = Image.new("RGB", (w * cols, (h + 20) * rows), (220, 220, 220))
        d = ImageDraw.Draw(sheet)
        for k, (name, img) in enumerate(pics):
            x, y = (k % cols) * w, (k // cols) * (h + 20)
            sheet.paste(img, (x, y))
            d.text((x + 8, y + h + 4), name, fill=(0, 0, 0))
        sheet.save(args.sheet)
        print(f"sheet: {args.sheet}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
