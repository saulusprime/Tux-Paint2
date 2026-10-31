#!/usr/bin/env python3
"""Generate the school-themed starters and templates (SVG, 608x472).

usage: devtools/content/school_svgs.py [REPOSITORY_ROOT]

608x472 is the canvas of an 800x600 window; Tux Paint renders SVGs at the
size of the canvas, so they stay sharp at any window size.
"""
import math
import os
import sys

W, H = 608, 472
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")


def svg(title, body, extra_defs=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<title>{title}</title>
<!-- Made for this fork of Tux Paint (devtools/content/school_svgs.py), 2026. GNU GPL v2 or later, like Tux Paint. -->
{extra_defs}{body}</svg>
'''


def write(rel, text):
    path = os.path.join(ROOT, rel)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(os.path.normpath(path), len(text))


# --- Template: squared notebook paper ("quaderno a quadretti") -------------
def notebook_squared():
    q = 16
    off_y = (H % q) / 2
    lines = []
    for x in range(0, W + 1, q):
        lines.append(f'M{x} 0V{H}')
    y = off_y
    while y <= H:
        lines.append(f'M0 {y:g}H{W}')
        y += q
    body = (f'<rect width="{W}" height="{H}" fill="#fdfdfa"/>\n'
            f'<path d="{" ".join(lines)}" stroke="#9fc3e6" stroke-width="0.8" fill="none"/>\n')
    write("templates/notebook_squared.svg",
          svg("Squared notebook paper", body))


# --- Template: lined notebook paper ("quaderno a righe") --------------------
def notebook_lined():
    step = 24
    lines = " ".join(f'M0 {y}H{W}' for y in range(56, H - 8, step))
    body = (f'<rect width="{W}" height="{H}" fill="#fdfdfa"/>\n'
            f'<path d="{lines}" stroke="#93b4dc" stroke-width="1" fill="none"/>\n'
            f'<path d="M64 0V{H}" stroke="#e07a7a" stroke-width="1.4" fill="none"/>\n')
    write("templates/notebook_lined.svg", svg("Lined notebook paper", body))


# --- Template: music manuscript paper ("quaderno pentagrammato") -----------
def music_staff():
    gap, staves, top, pitch = 8, 6, 40, 70
    x0, x1 = 32, W - 32
    lines, bars = [], []
    for s in range(staves):
        y0 = top + s * pitch
        for i in range(5):
            lines.append(f'M{x0} {y0 + i * gap}H{x1}')
        bars.append(f'M{x0} {y0}V{y0 + 4 * gap}M{x1} {y0}V{y0 + 4 * gap}')
    body = (f'<rect width="{W}" height="{H}" fill="#fdfdfa"/>\n'
            f'<path d="{" ".join(lines)}" stroke="#3a3a3a" stroke-width="1" fill="none"/>\n'
            f'<path d="{" ".join(bars)}" stroke="#3a3a3a" stroke-width="1.6" fill="none"/>\n')
    write("templates/music_staff.svg", svg("Music manuscript paper", body))


# --- Template: blackboard ("lavagna") ---------------------------------------
def blackboard():
    defs = '''<defs>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#a0682f"/><stop offset="1" stop-color="#7a4a1e"/>
</linearGradient>
<radialGradient id="board" cx="0.5" cy="0.45" r="0.75">
<stop offset="0" stop-color="#36584a"/><stop offset="1" stop-color="#22392f"/>
</radialGradient>
<filter id="dust" x="-0.5" y="-0.5" width="2" height="2">
<feGaussianBlur stdDeviation="14"/>
</filter>
</defs>
'''
    fx, ft, fb = 18, 18, 40          # frame: sides/top, bottom (with tray)
    bx, by, bw, bh = fx, ft, W - 2 * fx, H - ft - fb
    smudges = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" '
        f'opacity="{op}" filter="url(#dust)"/>\n'
        for cx, cy, rx, ry, op in [(170, 150, 110, 34, 0.07),
                                   (420, 300, 130, 30, 0.06),
                                   (300, 90, 90, 20, 0.05),
                                   (120, 340, 70, 22, 0.05)])
    tray_y = H - fb + 8
    chalks = "".join(
        f'<rect x="{x}" y="{tray_y + 4}" width="{w}" height="8" rx="3" fill="{c}" '
        f'stroke="#00000033" stroke-width="0.6"/>\n'
        for x, w, c in [(392, 40, "#f6f6f0"), (442, 30, "#f7e98a"),
                        (480, 24, "#f4a9c0")])
    eraser = (f'<rect x="96" y="{tray_y - 2}" width="70" height="14" rx="2" fill="#b7793c"/>\n'
              f'<rect x="96" y="{tray_y + 10}" width="70" height="6" rx="1" fill="#5b5f66"/>\n')
    body = (f'<rect width="{W}" height="{H}" fill="url(#wood)"/>\n'
            f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#board)" '
            f'stroke="#5e3814" stroke-width="2"/>\n'
            + smudges +
            f'<rect x="{fx - 6}" y="{tray_y}" width="{W - 2 * fx + 12}" height="16" rx="3" '
            f'fill="#8a5726" stroke="#5e3814" stroke-width="1.5"/>\n'
            + eraser + chalks)
    write("templates/blackboard.svg", svg("Blackboard", body, defs))


# --- Starter: clock face to learn the time ("orologio") ---------------------
def clock():
    cx, cy, r = W / 2, H / 2, 210
    ticks = []
    for i in range(60):
        a = math.radians(i * 6)
        r0 = r - 34 if i % 5 == 0 else r - 24
        w = 5 if i % 5 == 0 else 2
        x0, y0 = cx + r0 * math.sin(a), cy - r0 * math.cos(a)
        x1, y1 = cx + (r - 14) * math.sin(a), cy - (r - 14) * math.cos(a)
        ticks.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
                     f'stroke-width="{w}"/>')
    nums = []
    for h in range(1, 13):
        a = math.radians(h * 30)
        rn = r - 66
        x, y = cx + rn * math.sin(a), cy - rn * math.cos(a)
        nums.append(f'<text x="{x:.1f}" y="{y + 12:.1f}">{h}</text>')
    body = ('<g fill="none" stroke="#000000" stroke-linecap="round">\n'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke-width="7"/>\n'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 14}" stroke-width="2.5"/>\n'
            + "\n".join(ticks) + '\n</g>\n'
            '<g font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="36" '
            'text-anchor="middle" fill="#000000">\n' + "\n".join(nums) + '\n</g>\n'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="#000000"/>\n')
    write("starters/clock.svg", svg("Clock face", body))


# --- Starter: school building to colour ("scuola") ---------------------------
def school():
    s = 'fill="none" stroke="#000000" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
    parts = []
    gy = 430                                    # ground line
    # Main block and wings
    parts.append(f'<rect x="150" y="190" width="308" height="{gy - 190}"/>')
    parts.append(f'<rect x="40" y="250" width="110" height="{gy - 250}"/>')
    parts.append(f'<rect x="458" y="250" width="110" height="{gy - 250}"/>')
    # Roofs: pediment over the main block, flat cornices over the wings
    parts.append('<path d="M138 190 L304 100 L470 190 Z"/>')
    parts.append('<rect x="32" y="238" width="126" height="12"/>')
    parts.append('<rect x="450" y="238" width="126" height="12"/>')
    # Clock in the pediment
    parts.append('<circle cx="304" cy="152" r="26"/>')
    parts.append('<path d="M304 152 V134 M304 152 H318"/>')
    # Flag on the top of the pediment
    parts.append('<path d="M304 100 V40"/>')
    parts.append('<path d="M304 42 H352 V70 H304"/>')
    parts.append('<path d="M320 42 V70 M336 42 V70"/>')
    # Windows of the main block: two rows of four, minus the door spot
    for row, y in enumerate((214, 300)):
        for col, x in enumerate((172, 236, 332, 396)):
            if row == 1 and col in (1, 2):
                continue
            parts.append(f'<rect x="{x}" y="{y}" width="40" height="52"/>')
            parts.append(f'<path d="M{x + 20} {y} V{y + 52} M{x} {y + 22} H{x + 40}"/>')
    # Door with steps
    parts.append(f'<path d="M262 {gy - 16} V318 A42 42 0 0 1 346 318 V{gy - 16}"/>')
    parts.append(f'<path d="M304 {gy - 16} V276"/>')
    parts.append('<circle cx="294" cy="372" r="3"/><circle cx="314" cy="372" r="3"/>')
    parts.append(f'<rect x="248" y="{gy - 16}" width="112" height="8"/>')
    parts.append(f'<rect x="236" y="{gy - 8}" width="136" height="8"/>')
    # Windows of the wings
    for x in (62, 106, 480, 524):
        parts.append(f'<rect x="{x}" y="276" width="24" height="40"/>')
        parts.append(f'<rect x="{x}" y="346" width="24" height="40"/>')
    # Ground, sun and clouds
    parts.append(f'<path d="M0 {gy} H{W}"/>')
    parts.append('<circle cx="66" cy="70" r="30"/>')
    rays = " ".join(
        f'M{66 + 40 * math.cos(math.radians(a)):.1f} {70 + 40 * math.sin(math.radians(a)):.1f} '
        f'L{66 + 54 * math.cos(math.radians(a)):.1f} {70 + 54 * math.sin(math.radians(a)):.1f}'
        for a in range(0, 360, 45))
    parts.append(f'<path d="{rays}"/>')
    for x, y in ((420, 58), (494, 122)):
        parts.append(f'<path d="M{x} {y} a18 18 0 0 1 30 -14 a22 22 0 0 1 40 6 '
                     f'a16 16 0 0 1 6 30 H{x + 2} a12 12 0 0 1 -2 -22 Z"/>')
    body = f'<g {s}>\n' + "\n".join(parts) + '\n</g>\n'
    write("starters/school.svg", svg("School building", body))


notebook_squared()
notebook_lined()
music_staff()
blackboard()
clock()
school()
