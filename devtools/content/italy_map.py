#!/usr/bin/env python3
"""Generate the starter with the map of Italy and its regions (SVG, 608x472).

usage: devtools/content/italy_map.py REGIONS.shp COUNTRIES.shp [REPOSITORY_ROOT]

REGIONS.shp: Istat, "Confini delle unità amministrative a fini statistici",
generalized version, regions (Reg01012026_g_WGS84.shp in
https://www.istat.it/storage/cartografia/confini_amministrativi/generalizzati/2026/Limiti01012026_g.zip,
UTM zone 32N). Licence CC BY 4.0: the starter credits it.
COUNTRIES.shp: Natural Earth 1:10m Admin 0 - Countries
(https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip,
public domain), for the neighbouring countries, in grey.

Writes starters/worldmap_italy.svg (the lines, which stay on top of the
drawing) and starters/worldmap_italy-back.svg (sea, neighbouring countries,
the regions in white, and the same lines). The borders between regions are
simplified once for both sides, so that they meet exactly and the fill
tool can't leak from a region into the next. Islands smaller than
MIN_ISLAND are left out. Needs only Python.
"""
import math
import os
import struct
import sys

W, H = 608, 472
MARGIN = 8
TOLERANCE = 0.25        # px, Douglas-Peucker
MIN_ISLAND = 2.0        # px^2
COAST_WIDTH = 2.0       # Italy's outline: coast and land borders
BORDER_WIDTH = 1.2      # between regions
SEA = "#bfe0f5"
NEIGHBOURS = "#d9d9d9"
NOT_NEIGHBOURS = {"ITA", "VAT"}  # (San Marino is drawn as a neighbour)
SMALL_ISLAND = 12.0     # px^2: below this, an island has the thin line
SAN_MARINO = (12.38, 43.88, 12.54, 44.00)  # lon/lat box: thin line around it

ROOT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")


# --- Shapefiles -------------------------------------------------------------

def read_shp(path):
    """List of shapes, each a list of rings, each a list of (x, y)."""
    with open(path, "rb") as f:
        data = f.read()
    shapes = []
    pos = 100
    while pos < len(data):
        _, length = struct.unpack(">ii", data[pos:pos + 8])
        content = data[pos + 8:pos + 8 + 2 * length]
        pos += 8 + 2 * length
        shape_type = struct.unpack("<i", content[:4])[0]
        if shape_type == 0:
            shapes.append([])
            continue
        if shape_type not in (5, 15, 25):
            raise ValueError(f"{path}: shape type {shape_type} isn't a polygon")
        nparts, npoints = struct.unpack("<ii", content[36:44])
        parts = list(struct.unpack(f"<{nparts}i", content[44:44 + 4 * nparts]))
        off = 44 + 4 * nparts
        coords = struct.unpack(f"<{2 * npoints}d", content[off:off + 16 * npoints])
        points = list(zip(coords[0::2], coords[1::2]))
        parts.append(npoints)
        shapes.append([points[parts[i]:parts[i + 1]] for i in range(nparts)])
    return shapes


def read_dbf(path):
    with open(path, "rb") as f:
        data = f.read()
    nrec, header_len, rec_len = struct.unpack("<IHH", data[4:12])
    fields = []
    pos = 32
    while data[pos] != 0x0D:
        fields.append((data[pos:pos + 11].split(b"\0")[0].decode("ascii"),
                       data[pos + 16]))
        pos += 32
    records = []
    for i in range(nrec):
        rec = data[header_len + i * rec_len:header_len + (i + 1) * rec_len]
        off = 1
        values = {}
        for name, size in fields:
            values[name] = rec[off:off + size].decode("utf-8", "replace").strip()
            off += size
        records.append(values)
    return records


# --- Geometry ---------------------------------------------------------------

def utm32(lon, lat):
    """WGS84 longitude/latitude to UTM zone 32N, as in the Istat files."""
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    k0 = 0.9996
    phi = math.radians(lat)
    n = a / math.sqrt(1 - e2 * math.sin(phi) ** 2)
    t = math.tan(phi) ** 2
    c = ep2 * math.cos(phi) ** 2
    aa = math.cos(phi) * math.radians(lon - 9.0)
    m = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * phi
             - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * phi)
             + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * phi)
             - (35 * e2 ** 3 / 3072) * math.sin(6 * phi))
    x = k0 * n * (aa + (1 - t + c) * aa ** 3 / 6
                  + (5 - 18 * t + t * t + 72 * c - 58 * ep2) * aa ** 5 / 120) + 500000
    y = k0 * (m + n * math.tan(phi) * (aa * aa / 2 + (5 - t + 9 * c + 4 * c * c) * aa ** 4 / 24
                                        + (61 - 58 * t + t * t + 600 * c - 330 * ep2) * aa ** 6 / 720))
    return x, y


def area(ring):
    """Signed area; negative for a clockwise ring (y up), as shapefiles
    have their outer rings."""
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        s += x1 * y2 - x2 * y1
    return s / 2


def simplify(points, tol):
    """Douglas-Peucker, keeping both ends."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        i, j = stack.pop()
        (x1, y1), (x2, y2) = points[i], points[j]
        dx, dy = x2 - x1, y2 - y1
        norm = math.hypot(dx, dy)
        best, best_k = -1.0, -1
        for k in range(i + 1, j):
            x, y = points[k]
            if norm == 0:
                d = math.hypot(x - x1, y - y1)
            else:
                d = abs(dy * (x - x1) - dx * (y - y1)) / norm
            if d > best:
                best, best_k = d, k
        if best > tol:
            keep[best_k] = True
            stack += [(i, best_k), (best_k, j)]
    return [p for p, k in zip(points, keep) if k]


def clip(ring, x0, y0, x1, y1):
    """Sutherland-Hodgman: the part of a polygon inside a rectangle."""
    for inside, cross in (
            (lambda p: p[0] >= x0, lambda p, q: (x0, p[1] + (q[1] - p[1]) * (x0 - p[0]) / (q[0] - p[0]))),
            (lambda p: p[0] <= x1, lambda p, q: (x1, p[1] + (q[1] - p[1]) * (x1 - p[0]) / (q[0] - p[0]))),
            (lambda p: p[1] >= y0, lambda p, q: (p[0] + (q[0] - p[0]) * (y0 - p[1]) / (q[1] - p[1]), y0)),
            (lambda p: p[1] <= y1, lambda p, q: (p[0] + (q[0] - p[0]) * (y1 - p[1]) / (q[1] - p[1]), y1))):
        out = []
        for p, q in zip(ring, ring[1:] + ring[:1]):
            if inside(q):
                if not inside(p):
                    out.append(cross(p, q))
                out.append(q)
            elif inside(p):
                out.append(cross(p, q))
        ring = out
        if not ring:
            break
    return ring


def simplify_closed(points, tol):
    """A closed ring (first point not repeated) cut in two at the point
    farthest from the first one."""
    far = max(range(len(points)), key=lambda k: math.dist(points[0], points[k]))
    a = simplify(points[:far + 1], tol)
    b = simplify(points[far:] + points[:1], tol)
    return a[:-1] + b[:-1]


# --- The regions, as arcs between the points where three borders meet ------

def build_arcs(rings):
    """rings: list of lists of integer points (not repeating the first).
    Returns arcs (lists of points) and, for each ring, a list of
    (arc index, reversed)."""
    neighbours = {}
    for ring in rings:
        n = len(ring)
        for i, p in enumerate(ring):
            s = neighbours.setdefault(p, set())
            s.add(ring[i - 1])
            s.add(ring[(i + 1) % n])
    junction = {p for p, s in neighbours.items() if len(s) != 2}

    arcs, index, ring_arcs = [], {}, []
    for ring in rings:
        starts = [i for i, p in enumerate(ring) if p in junction]
        pieces = []
        if not starts:
            # A ring that touches no other: one closed arc, the same
            # whichever point it starts from
            k = ring.index(min(ring))
            rot = ring[k:] + ring[:k]
            rev = [rot[0]] + rot[:0:-1]
            pieces.append((rot, rev, True))
        else:
            n = len(ring)
            for a, b in zip(starts, starts[1:] + [starts[0] + n]):
                piece = [ring[i % n] for i in range(a, b + 1)]
                pieces.append((piece, piece[::-1], False))
        refs = []
        for piece, rev, closed in pieces:
            key, rkey = tuple(piece), tuple(rev)
            if key in index:
                refs.append((index[key], False))
            elif rkey in index:
                refs.append((index[rkey], True))
            else:
                index[key] = len(arcs)
                arcs.append({"points": piece, "closed": closed, "uses": 0})
                refs.append((index[key], False))
            arcs[refs[-1][0]]["uses"] += 1
        ring_arcs.append(refs)
    return arcs, ring_arcs


def ring_points(refs, arcs):
    out = []
    for i, rev in refs:
        pts = arcs[i]["simple"]
        if arcs[i]["closed"]:
            return pts[::-1] if rev else pts
        pts = pts[::-1] if rev else pts
        out += pts[:-1]
    return out


def path(rings):
    return " ".join("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in ring) + "Z"
                    for ring in rings)


def open_path(lines):
    return " ".join("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in line)
                    for line in lines)


def main():
    regions = read_shp(sys.argv[1])
    region_rings, region_of = [], []
    for r, shape in enumerate(regions):
        for ring in shape:
            pts = [(round(x * 100), round(y * 100)) for x, y in ring]
            clean = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
            if clean[0] == clean[-1]:
                clean.pop()
            region_rings.append(clean)
            region_of.append(r)

    arcs, ring_arcs = build_arcs(region_rings)

    # Fit the outer rings of the mainland and of the islands kept into the
    # canvas, the same scale both ways
    def big_enough(k, scale):
        return abs(area(region_rings[k])) * (scale / 100) ** 2 >= MIN_ISLAND

    scale = 1e-3        # (a first guess, for the islands' size)
    for _ in range(3):
        outer = [k for k in range(len(region_rings))
                 if area(region_rings[k]) < 0 and big_enough(k, scale)]
        xs = [p[0] / 100 for k in outer for p in region_rings[k]]
        ys = [p[1] / 100 for k in outer for p in region_rings[k]]
        scale = min((W - 2 * MARGIN) / (max(xs) - min(xs)),
                    (H - 2 * MARGIN) / (max(ys) - min(ys)))
    off_x = (W - (max(xs) - min(xs)) * scale) / 2 - min(xs) * scale
    off_y = (H - (max(ys) - min(ys)) * scale) / 2 + max(ys) * scale

    def to_px(x, y):
        return (x * scale + off_x, off_y - y * scale)

    kept = [k for k in range(len(region_rings)) if big_enough(k, scale)]
    for arc in arcs:
        pts = [to_px(x / 100, y / 100) for x, y in arc["points"]]
        arc["simple"] = (simplify_closed(pts, TOLERANCE) if arc["closed"]
                         else simplify(pts, TOLERANCE))

    used = {}
    for k in kept:
        for i, _ in ring_arcs[k]:
            used[i] = used.get(i, 0) + 1

    # Italy's outline has the thick line, except around San Marino (a
    # hole between two regions) and around the small islands
    sm = [to_px(*utm32(lon, lat)) for lon, lat in
          ((SAN_MARINO[0], SAN_MARINO[1]), (SAN_MARINO[2], SAN_MARINO[3]))]

    def thin(arc):
        if all(sm[0][0] <= x <= sm[1][0] and sm[1][1] <= y <= sm[0][1]
               for x, y in arc["simple"]):
            return True
        return arc["closed"] and abs(area(arc["simple"])) < SMALL_ISLAND

    def line(arc):
        return arc["simple"] + (arc["simple"][:1] if arc["closed"] else [])

    coast = [line(arcs[i]) for i, n in used.items() if n == 1 and not thin(arcs[i])]
    borders = [line(arcs[i]) for i, n in used.items() if n > 1 or thin(arcs[i])]

    by_region = {}
    for k in kept:
        by_region.setdefault(region_of[k], []).append(ring_points(ring_arcs[k], arcs))

    # Neighbouring countries, cut to what's near the canvas
    names = read_dbf(sys.argv[2][:-4] + ".dbf")
    neighbours = []
    for rec, shape in zip(names, read_shp(sys.argv[2])):
        if rec.get("ADM0_A3") in NOT_NEIGHBOURS:
            continue
        for ring in shape:
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < 0 or min(lons) > 25 or max(lats) < 30 or min(lats) > 52:
                continue
            pts = clip([to_px(*utm32(lon, lat)) for lon, lat in ring[:-1]],
                       -4, -4, W + 4, H + 4)
            if len(pts) < 3:
                continue
            pts = simplify_closed(pts, TOLERANCE)
            if len(pts) >= 3 and abs(area(pts)) >= MIN_ISLAND:
                neighbours.append(pts)

    lines = (f'<path d="{open_path(borders)}" fill="none" stroke="#000" '
             f'stroke-width="{BORDER_WIDTH}" stroke-linejoin="round" stroke-linecap="round"/>\n'
             f'<path d="{open_path(coast)}" fill="none" stroke="#000" '
             f'stroke-width="{COAST_WIDTH}" stroke-linejoin="round" stroke-linecap="round"/>\n')
    land = "".join(f'<path d="{path(rings)}" fill="#fff" fill-rule="evenodd"/>\n'
                   for _, rings in sorted(by_region.items()))
    back = (f'<rect width="{W}" height="{H}" fill="{SEA}"/>\n'
            f'<path d="{path(neighbours)}" fill="{NEIGHBOURS}" stroke="{NEIGHBOURS}" '
            f'stroke-width="0.8" stroke-linejoin="round"/>\n' + land + lines)

    credit = ("Map of Italy and its regions, made for this fork of Tux Paint "
              "(devtools/content/italy_map.py), 2026. Region boundaries: Istat, "
              "Confini delle unita' amministrative a fini statistici al 1 gennaio "
              "2026 (versione generalizzata), CC BY 4.0, simplified and redrawn. "
              "Neighbouring countries: Natural Earth (public domain).")
    for name, title, body in (("worldmap_italy", "Italy, regions", lines),
                              ("worldmap_italy-back", "Italy, regions (background)", back)):
        text = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}">\n<title>{title}</title>\n<!-- {credit} -->\n'
                f'{body}</svg>\n')
        out = os.path.join(ROOT, "starters", name + ".svg")
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(os.path.normpath(out), len(text))
    print(f"regions: {len(by_region)}, rings kept: {len(kept)} of {len(region_rings)}, "
          f"arcs: {len(used)} ({len(coast)} outline, {len(borders)} between regions), "
          f"neighbour rings: {len(neighbours)}, scale: {scale * 1000:.4f} px/km")


main()
