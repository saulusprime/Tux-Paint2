"""lessonkit: write Tux Paint lessons (see lessons/README.txt) as Python, in
the sheet's own coordinates (640x480, y down).

Lines are chains of cubic and straight segments (Ch), made with the shape
helpers below (circle, arc, curve, leaf, ...). A Lesson collects the steps:
guide and draw groups of lines, erase, and color areas. Parts behind others
are hidden with clip paths (Lesson.behind).

Color areas are not drawn by hand: Lesson.build() renders the lesson's own
lines, fills the areas around the seed points given for each color, grows
them a little under the lines and traces them back to paths, so that every
color fits its lines, with no white gap.

Needs Python 3 with Pillow, and lesson_preview.py (one folder up) for
librsvg and cairo."""

import math
import os
import sys
import tempfile
from collections import deque

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import lesson_preview as lp  # noqa: E402

DARK = "#2b2b2b"
LINE = (f'fill="none" stroke="{DARK}" stroke-width="6" stroke-linecap="round" '
        'stroke-linejoin="round"')
GUIDE = ('fill="none" stroke="#8a9bb0" stroke-width="3" stroke-dasharray="10 8" '
         'stroke-linecap="round"')

# --------------------------------------------------------------- geometry


def f(v):
    """A number for the SVG: one decimal, none if it is .0"""
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def pt(p):
    return f"{f(p[0])},{f(p[1])}"


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def C(c1, c2, p):
    """A cubic segment to p"""
    return ("C", c1, c2, p)


def L(p):
    """A straight segment to p"""
    return ("L", p)


class Ch:
    """A chain of cubic and straight segments"""

    def __init__(self, start, *segs):
        self.start = start
        self.segs = list(segs)

    @property
    def end(self):
        return self.segs[-1][-1]

    def at(self, i, t):
        frm = self.start if i == 0 else self.segs[i - 1][-1]
        s = self.segs[i]
        if s[0] == "C":
            return bez(frm, s[1], s[2], s[3], t)
        return (frm[0] + (s[1][0] - frm[0]) * t, frm[1] + (s[1][1] - frm[1]) * t)

    def body(self):
        out = []
        for s in self.segs:
            if s[0] == "C":
                out.append(f"C {pt(s[1])} {pt(s[2])} {pt(s[3])}")
            else:
                out.append(f"L {pt(s[1])}")
        return " ".join(out)

    def d(self, close=False):
        return f"M {pt(self.start)} {self.body()}" + (" Z" if close else "")

    def rev(self):
        items, cur = [], self.start
        for s in self.segs:
            items.append((cur, s))
            cur = s[-1]
        segs = []
        for frm, s in reversed(items):
            segs.append(C(s[2], s[1], frm) if s[0] == "C" else L(frm))
        return Ch(cur, *segs)

    def map(self, fn):
        segs = [C(fn(s[1]), fn(s[2]), fn(s[3])) if s[0] == "C" else L(fn(s[1]))
                for s in self.segs]
        return Ch(fn(self.start), *segs)

    def points(self, n=12):
        """Points along the chain, n per segment"""
        out = [self.start]
        for i in range(len(self.segs)):
            for k in range(1, n + 1):
                out.append(self.at(i, k / n))
        return out


def ellipse(cx, cy, rx, ry, rot=0.0):
    k = 0.5523
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def r(x, y):
        return (cx + x * c - y * s, cy + x * s + y * c)
    return Ch(r(rx, 0),
              C(r(rx, k * ry), r(k * rx, ry), r(0, ry)),
              C(r(-k * rx, ry), r(-rx, k * ry), r(-rx, 0)),
              C(r(-rx, -k * ry), r(-k * rx, -ry), r(0, -ry)),
              C(r(k * rx, -ry), r(rx, -k * ry), r(rx, 0)))


def poly(*pts, close=False):
    """Straight segments through points"""
    segs = [L(p) for p in pts[1:]] + ([L(pts[0])] if close else [])
    return Ch(pts[0], *segs)


def smooth(*pts, close=False, corners=()):
    """A Catmull-Rom curve through the points (corners: indexes with no tangent)"""
    pts = list(pts)
    n = len(pts)
    if close:
        pts = pts + [pts[0]]

    def tangent(i):
        if (i % n) in corners:
            return (0.0, 0.0)
        if close:
            a, b = pts[(i - 1) % n], pts[(i + 1) % n]
            return ((b[0] - a[0]) / 2, (b[1] - a[1]) / 2)
        if i == 0:
            a, b = pts[0], pts[1]
        elif i == len(pts) - 1:
            a, b = pts[-2], pts[-1]
        else:
            a, b = pts[i - 1], pts[i + 1]
            return ((b[0] - a[0]) / 2, (b[1] - a[1]) / 2)
        return (b[0] - a[0], b[1] - a[1])

    segs = []
    for i in range(len(pts) - 1):
        p0, p1 = pts[i], pts[i + 1]
        t0, t1 = tangent(i), tangent(i + 1)
        segs.append(C((p0[0] + t0[0] / 3, p0[1] + t0[1] / 3),
                      (p1[0] - t1[0] / 3, p1[1] - t1[1] / 3), p1))
    return Ch(pts[0], *segs)


def join(*chains):
    """One chain from chains that follow each other"""
    out = Ch(chains[0].start, *chains[0].segs)
    for c in chains[1:]:
        if math.dist(out.end, c.start) > 0.01:
            out.segs.append(L(c.start))
        out.segs.extend(c.segs)
    return out


def rdp(pts, eps):
    """Ramer-Douglas-Peucker simplification of a polyline"""
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    best, bi = -1.0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        if ln < 1e-9:
            dd = math.dist(p, a)
        else:
            dd = abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / ln
        if dd > best:
            best, bi = dd, i
    if best <= eps:
        return [a, b]
    return rdp(pts[:bi + 1], eps)[:-1] + rdp(pts[bi:], eps)

# ----------------------------------------------------------------- shapes


def circle(cx, cy, r):
    return ellipse(cx, cy, r, r)


def ell(cx, cy, rx, ry, rot=0.0):
    return ellipse(cx, cy, rx, ry, rot)


def arc(cx, cy, rx, ry, a0, a1, rot=0.0):
    """An elliptic arc from angle a0 to a1 (degrees, y down: 90 is below)"""
    n = max(1, math.ceil(abs(a1 - a0) / 90))
    da = (a1 - a0) / n
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def pt_(a):
        x, y = rx * math.cos(math.radians(a)), ry * math.sin(math.radians(a))
        return (cx + x * c - y * s, cy + x * s + y * c)

    def tan(a):
        x, y = -rx * math.sin(math.radians(a)), ry * math.cos(math.radians(a))
        return (x * c - y * s, x * s + y * c)
    k = 4 / 3 * math.tan(math.radians(da) / 4)
    segs = []
    for i in range(n):
        b0, b1 = a0 + da * i, a0 + da * (i + 1)
        p0, p1 = pt_(b0), pt_(b1)
        t0, t1 = tan(b0), tan(b1)
        segs.append(C((p0[0] + k * t0[0], p0[1] + k * t0[1]), (p1[0] - k * t1[0], p1[1] - k * t1[1]), p1))
    return Ch(pt_(a0), *segs)


def curve(*pts, close=False, corners=()):
    return smooth(*pts, close=close, corners=corners)


def line(*pts, close=False):
    return poly(*pts, close=close)


def rrect(x0, y0, x1, y1, r):
    """A rectangle with round corners"""
    k = 0.5523 * r
    return Ch((x0 + r, y0), L((x1 - r, y0)), C((x1 - r + k, y0), (x1, y0 + r - k), (x1, y0 + r)),
              L((x1, y1 - r)), C((x1, y1 - r + k), (x1 - r + k, y1), (x1 - r, y1)),
              L((x0 + r, y1)), C((x0 + r - k, y1), (x0, y1 - r + k), (x0, y1 - r)),
              L((x0, y0 + r)), C((x0, y0 + r - k), (x0 + r - k, y0), (x0 + r, y0)))


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for k in range(2 * n):
        a = math.radians(rot + 180.0 / n * k)
        r = ro if k % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(*pts, close=True)


def moved(ch, dx=0.0, dy=0.0, s=1.0, ox=0.0, oy=0.0, flip=False):
    """Scaled by s around (ox, oy), mirrored left-right if flip, then moved"""
    def fn(p):
        x, y = ox + (p[0] - ox) * s, oy + (p[1] - oy) * s
        if flip:
            x = 2 * ox - x
        return (x + dx, y + dy)
    return ch.map(fn)


def leaf(base, tip, w, bend=0.0):
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    ln = math.hypot(dx, dy)
    nx, ny = dy / ln, -dx / ln

    def at(t, s):
        return (base[0] + dx * t + nx * s, base[1] + dy * t + ny * s)
    return Ch(base, C(at(0.25, w * 1.2 + bend), at(0.7, w * 1.0 + bend), tip),
              C(at(0.7, -w * 1.0 + bend), at(0.25, -w * 1.2 + bend), base))


def flower(cx, cy, r, n=5, rot=-90.0):
    def polar(rad, deg):
        a = math.radians(deg)
        return (cx + rad * math.cos(a), cy + rad * math.sin(a))
    step = 360.0 / n
    segs = []
    for k in range(n):
        a = rot + step * k
        segs.append(C(polar(1.45 * r, a - step * 0.42), polar(1.45 * r, a + step * 0.42),
                      polar(0.45 * r, a + step / 2)))
    return Ch(polar(0.45 * r, rot - step / 2), *segs)


def cloud(x0, y0, x1, y1):
    """A cloud: flat bottom from x0 to x1 at y1, bumps up to about y0"""
    w, h = x1 - x0, y1 - y0
    return curve((x0 + 0.12 * w, y1), (x0, y1 - 0.3 * h), (x0 + 0.12 * w, y1 - 0.62 * h),
                 (x0 + 0.3 * w, y1 - 0.6 * h), (x0 + 0.42 * w, y0), (x0 + 0.62 * w, y0 + 0.05 * h),
                 (x0 + 0.72 * w, y1 - 0.6 * h), (x0 + 0.9 * w, y1 - 0.55 * h), (x1, y1 - 0.25 * h),
                 (x0 + 0.88 * w, y1), close=True, corners=(0, 9, 3, 6))


def sun(cx, cy, r, rays=8, gap=8, length=18):
    out = [circle(cx, cy, r)]
    for k in range(rays):
        a = math.radians(360 / rays * k - 90)
        out.append(line((cx + (r + gap) * math.cos(a), cy + (r + gap) * math.sin(a)),
                        (cx + (r + gap + length) * math.cos(a), cy + (r + gap + length) * math.sin(a))))
    return out

# ------------------------------------------------------------ color areas


K = 2                       # pixels per sheet unit, for the fills
W, H = 640 * K, 480 * K


class Raster:
    """The lesson's lines, rendered: the free (not line) pixels, split into areas"""

    def __init__(self, svg_path, layers, frame):
        handle = lp.Svg(svg_path)
        canvas = lp.Canvas(W, H)
        for layer in layers:
            handle.render_layer(canvas, layer, W, H)
        alpha = canvas.to_pil().getchannel("A").tobytes()
        fx0, fy0, fx1, fy1 = (round(v * K) for v in frame)
        self.frame = (fx0, fy0, fx1, fy1)
        self.free = bytearray(W * H)
        for y in range(fy0, fy1):
            row = y * W
            for x in range(fx0, fx1):
                if alpha[row + x] < 128:
                    self.free[row + x] = 1
        self.label = [0] * (W * H)
        self.sizes = [0]

    def _fill(self, s):
        n = len(self.sizes)
        self.label[s] = n
        q = deque([s])
        size = 0
        while q:
            i = q.popleft()
            size += 1
            xx = i % W
            for j in (i - 1 if xx else -1, i + 1 if xx < W - 1 else -1, i - W, i + W):
                if 0 <= j < W * H and self.free[j] and not self.label[j]:
                    self.label[j] = n
                    q.append(j)
        self.sizes.append(size)
        return n

    def area(self, seed):
        """The label of the free area around a seed point"""
        x, y = seed
        s = round(y * K) * W + round(x * K)
        if not self.free[s]:
            # on a line: look around for the nearest free pixel
            best = None
            for dy in range(-6, 7):
                for dx in range(-6, 7):
                    j = s + dy * W + dx
                    if 0 <= j < W * H and self.free[j]:
                        dd = dx * dx + dy * dy
                        if best is None or dd < best[0]:
                            best = (dd, j)
            if best is None:
                raise ValueError(f"seed {seed} is on a line")
            s = best[1]
        if self.label[s]:
            return self.label[s]
        return self._fill(s)

    def all_areas(self):
        """Labels every free area not labeled yet"""
        for s in range(W * H):
            if self.free[s] and not self.label[s]:
                self._fill(s)

    def mask(self, labels, grow=4):
        """A 0/255 mask of these areas, grown by a few pixels under the lines"""
        labels = set(labels)
        m = bytearray(255 if lab in labels else 0 for lab in self.label)
        img = Image.frombytes("L", (W, H), bytes(m))
        if grow:
            img = img.filter(ImageFilter.MaxFilter(2 * grow + 1))
        # keep inside the frame
        fx0, fy0, fx1, fy1 = self.frame
        frame = Image.new("L", (W, H), 0)
        frame.paste(255, (fx0, fy0, fx1, fy1))
        return Image.frombytes("L", (W, H), bytes(a & b for a, b in zip(img.tobytes(), frame.tobytes())))


def trace_mask(img, eps=0.8):
    """Closed outlines (sheet coordinates) of a 0/255 mask"""
    w, h = img.size
    px = img.tobytes()

    def on(x, y):
        return 0 <= x < w and 0 <= y < h and px[y * w + x] > 127
    edges = {}
    for y in range(h):
        row = y * w
        for x in range(w):
            if px[row + x] > 127:
                if not on(x, y - 1):
                    edges.setdefault((x, y), []).append((x + 1, y))
                if not on(x + 1, y):
                    edges.setdefault((x + 1, y), []).append((x + 1, y + 1))
                if not on(x, y + 1):
                    edges.setdefault((x + 1, y + 1), []).append((x, y + 1))
                if not on(x - 1, y):
                    edges.setdefault((x, y + 1), []).append((x, y))
    loops = []
    while edges:
        start = next(iter(edges))
        loop = [start]
        cur = start
        prev_dir = None
        while True:
            nxt = edges[cur]
            if len(nxt) == 1:
                nb = nxt.pop()
            else:
                # turn right first (keeps touching corners apart)
                def turn(p):
                    d = (p[0] - cur[0], p[1] - cur[1])
                    if prev_dir is None:
                        return 0
                    cross = prev_dir[0] * d[1] - prev_dir[1] * d[0]
                    return -cross
                nxt.sort(key=turn)
                nb = nxt.pop(0)
            if not nxt:
                del edges[cur]
            prev_dir = (nb[0] - cur[0], nb[1] - cur[1])
            cur = nb
            if cur == start:
                break
            loop.append(cur)
        if len(loop) < 8:
            continue
        # edge midpoints, then simplified
        mids = [((loop[i][0] + loop[(i + 1) % len(loop)][0]) / 2,
                 (loop[i][1] + loop[(i + 1) % len(loop)][1]) / 2) for i in range(len(loop))]
        far = max(range(len(mids)), key=lambda i: math.dist(mids[0], mids[i]))
        a = rdp(mids[:far + 1], eps)
        b = rdp(mids[far:] + [mids[0]], eps)
        pts = a[:-1] + b[:-1]
        if len(pts) >= 3:
            loops.append([(x / K, y / K) for x, y in pts])
    return loops


def path_d(loops):
    return " ".join("M " + " L ".join(f"{f(x)},{f(y)}" for x, y in loop) + " Z" for loop in loops)

# ----------------------------------------------------------------- lesson


class Lesson:
    def __init__(self, name, en, it, comment=None):
        """name: the files' name; en, it: the title"""
        self.name, self.en, self.it = name, en, it
        self.comment = comment or f"Tux Paint lesson: steps for {name}.svg (see ../README.txt)"
        self.defs, self.groups, self.steps, self.colors = [], [], [], []
        self.inside, self.whites = {}, []
        self.nclip = 0

    # --- items of a group
    def p(self, ch, close=False, fill=None):
        extra = f' fill="{fill}" stroke="none"' if fill else ""
        return f'<path d="{ch.d(close)}"{extra}/>'

    def lines(self, *chs, close=False):
        return [self.p(c, close) for c in chs]

    def shapes(self, *chs):
        return [self.p(c, True) for c in chs]

    def dot(self, x, y, r, fill=DARK):
        return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="none"/>'

    def behind(self, items, *shapes):
        """Items hidden where the shapes (closed chains) are"""
        inner = "\n  ".join(items)
        for sh in shapes:
            self.nclip += 1
            cid = f"{self.name[:3]}{self.nclip}"
            self.defs.append(f'<clipPath id="{cid}"><path clip-rule="evenodd" d="M 0,0 H 640 V 480 H 0 Z '
                             f'{sh.d(True)}"/></clipPath>')
            inner = f'<g clip-path="url(#{cid})">{inner}</g>'
        return [inner]

    # --- steps
    def guide(self, gid, items, en, it):
        self.groups.append((gid, "guide", f'<g id="{gid}" {GUIDE}>\n  ' + "\n  ".join(items) + "\n</g>"))
        self.steps.append((f"guide {gid}", en, it))

    def draw(self, gid, items, en, it):
        self.groups.append((gid, "draw", f'<g id="{gid}" {LINE}>\n  ' + "\n  ".join(items) + "\n</g>"))
        self.steps.append((f"draw {gid}", en, it))

    def erase(self, en="Now erase the light lines with the eraser.",
              it="Adesso cancella con la gomma le linee leggere."):
        self.steps.append(("erase", en, it))

    def color(self, gid, hexcolor, seeds, en, it, inside=()):
        """seeds: points in the areas to color; inside: closed shapes whose
        areas (those mostly inside them, not claimed by another color's
        seeds) get this color too"""
        self.colors.append((gid, hexcolor, seeds))
        self.inside[gid] = list(inside)
        self.steps.append((f"color {gid}", en, it))

    def white(self, *points):
        """Areas that stay white, whatever shapes they are in"""
        self.whites += list(points)

    # --- output
    def svg(self, color_items=None):
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="480" viewBox="0 0 640 480">',
               f"<title>{self.en}</title>"]
        if self.defs:
            out.append("<defs>\n" + "\n".join(self.defs) + "\n</defs>")
        out += [g for _, _, g in self.groups]
        for gid, hexcolor, _ in self.colors:
            body = color_items[gid] if color_items else ""
            out.append(f'<g id="{gid}" fill="{hexcolor}" stroke="none">\n  {body}\n</g>')
        out.append("</svg>")
        return "\n".join(out) + "\n"

    def build(self, outdir):
        """Writes NAME.svg and NAME.txt in outdir, with the color areas
        filled from the lines; returns a report (lines of text)"""
        with tempfile.TemporaryDirectory() as tmp:
            lines_svg = os.path.join(tmp, f"{self.name}-lines.svg")
            with open(lines_svg, "w", encoding="utf-8") as fp:
                fp.write(self.svg({gid: "" for gid, _, _ in self.colors}))
            r = Raster(lines_svg, [g for g, k, _ in self.groups if k == "draw"], (0, 0, 640, 480))
        background = r.area((2, 2))
        report, used, items = [], set(), {}
        color_labels = {}
        for gid, hexcolor, seeds in self.colors:
            labels = set()
            for s in seeds:
                lab = r.area(tuple(s))
                if lab == background:
                    report.append(f"ERROR {gid}: seed {s} is in the background (a gap in the lines?)")
                    continue
                if lab in used and lab not in labels:
                    report.append(f"warning {gid}: seed {s} is in an area already colored")
                labels.add(lab)
            used |= labels
            color_labels[gid] = labels
        for s in self.whites:
            used.add(r.area(tuple(s)))
        first = len(r.sizes)
        r.all_areas()
        if any(self.inside.values()):
            tot = {}
            for lab in r.label:
                tot[lab] = tot.get(lab, 0) + 1
            for gid, _, _ in self.colors:
                if not self.inside.get(gid):
                    continue
                m = Image.new("L", (W, H), 0)
                d = ImageDraw.Draw(m)
                for sh in self.inside[gid]:
                    d.polygon([(x * K, y * K) for x, y in sh.points(16)], fill=255)
                mp = m.tobytes()
                inn = {}
                for i, lab in enumerate(r.label):
                    if mp[i]:
                        inn[lab] = inn.get(lab, 0) + 1
                for lab, n in inn.items():
                    if lab and lab != background and lab not in used and n >= 0.6 * tot[lab]:
                        color_labels[gid].add(lab)
                        used.add(lab)
        for gid, _, _ in self.colors:
            items[gid] = f'<path fill-rule="evenodd" d="{path_d(trace_mask(r.mask(color_labels[gid])))}"/>'

        # big areas left white: often meant (eyes, the sky), but worth a look
        firstpix = {}
        for i, lab in enumerate(r.label):
            if lab >= first and lab not in firstpix and lab not in used:
                firstpix[lab] = i
        for lab in sorted(firstpix, key=lambda lb: -r.sizes[lb]):
            if r.sizes[lab] >= 150:
                s = firstpix[lab]
                report.append(f"white: {r.sizes[lab]} px at "
                              f"({(s % W) / K + 1:.0f}, {(s // W) / K + 1:.0f})")
        with open(os.path.join(outdir, self.name + ".svg"), "w", encoding="utf-8") as fp:
            fp.write(self.svg(items))
        txt = [f"# {self.comment}", self.en, f"it.utf8={self.it}", ""]
        for head, en, it in self.steps:
            txt += [head, en, f"it.utf8={it}", ""]
        with open(os.path.join(outdir, self.name + ".txt"), "w", encoding="utf-8") as fp:
            fp.write("\n".join(txt).rstrip("\n") + "\n")
        return report
