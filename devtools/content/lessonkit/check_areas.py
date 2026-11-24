#!/usr/bin/env python3
"""check_areas.py LESSON.txt...: looks for coloring mistakes in lessons.

Renders a lesson's drawn lines and its colors, then looks at every closed
area between the lines: an area that is partly white, or that has two
colors with no line between them, is reported, with where its smaller part
is (sheet coordinates, 640x480). That is a white gap left inside a line, or
a color that goes past its line. Exits with 1 if anything is found.

Needs Python 3 with Pillow, and lesson_preview.py (one folder up)."""

import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import lesson_preview as lp  # noqa: E402

K = 1.5             # pixels per sheet unit
MIN_PART = 13       # pixels: smaller parts are only antialiasing


def check(txt_path):
    """Returns (problems, number of areas); problems are lines of text"""
    lesson = lp.parse_lesson(txt_path)
    handle = lp.Svg(lesson.svg_path)
    w, h = int(640 * K), int(480 * K)

    def alpha(layers):
        canvas = lp.Canvas(w, h)
        for layer in layers:
            handle.render_layer(canvas, layer, w, h)
        return canvas.to_pil().getchannel("A").tobytes()

    lines = alpha([lay for k, lay, _ in lesson.steps if k == "draw"])
    free = bytearray(1 if a < 128 else 0 for a in lines)
    colors = [lay for k, lay, _ in lesson.steps if k == "color"]
    owner = bytearray(w * h)        # the last color painted there (1-based), 0 = white
    for n, lay in enumerate(colors, 1):
        for i, a in enumerate(alpha([lay])):
            if a >= 128:
                owner[i] = n

    label = bytearray(w * h)
    problems, areas = [], 0
    for start in range(w * h):
        if not free[start] or label[start]:
            continue
        areas += 1
        label[start] = 1
        q = deque([start])
        count, sums = {}, {}
        while q:
            i = q.popleft()
            c = owner[i]
            x, y = i % w, i // w
            count[c] = count.get(c, 0) + 1
            sx, sy = sums.get(c, (0, 0))
            sums[c] = (sx + x, sy + y)
            for j in (i - 1 if x > 0 else -1, i + 1 if x < w - 1 else -1, i - w, i + w):
                if 0 <= j < w * h and free[j] and not label[j]:
                    label[j] = 1
                    q.append(j)
        big = {c: v for c, v in count.items() if v >= MIN_PART}
        if len(big) > 1:
            names = ", ".join(f"{'white' if c == 0 else colors[c - 1]} {v} px" for c, v in sorted(big.items()))
            minor = min(big, key=big.get)
            mx, my = sums[minor][0] / big[minor] / K, sums[minor][1] / big[minor] / K
            problems.append(f"area at ({(start % w) / K:.0f}, {(start // w) / K:.0f}): {names}; "
                            f"the smaller part is near ({mx:.0f}, {my:.0f})")
    return problems, areas


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    bad = 0
    for path in sys.argv[1:]:
        problems, areas = check(path)
        print(f"{path}: {areas} areas, {len(problems)} problems")
        for p in problems:
            print("   ", p)
        bad += len(problems)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
