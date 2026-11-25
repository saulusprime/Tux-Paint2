#!/usr/bin/env python3
"""Check Tux Paint lessons and draw a sheet with their steps.

Usage: lesson_preview.py [--out DIR] [--size W] [--langs en,it] PATH...

PATH is a lesson's .txt file, or a folder searched for them (e.g. lessons/).
For each lesson it prints the problems found (see lessons/README.txt for the
rules) and, with --out, writes DIR/LEVEL-NAME.png: the finished picture, then
every step as the "Learn" tool shows it once the step's animation is over,
each with its instructions in the languages asked for.

The exit status is 1 if any lesson has errors (warnings don't count).

Needs Python 3 with Pillow, and librsvg (>= 2.46) and cairo, used
through ctypes as Tux Paint uses them (no PyGObject nor pycairo).
"""

import argparse
import ctypes
import ctypes.util
import os
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

SVG_NS = "{http://www.w3.org/2000/svg}"
KINDS = ("draw", "guide", "color", "erase")
LEVELS = {"easy": (3, 5), "medium": (5, 7), "hard": (7, 100)}
MAX_TEXT = 110

# As in src/lessons.c
HIGHLIGHT = (0xff / 255, 0x4d / 255, 0x2e / 255)
GUIDE_HIGHLIGHT = (0xff / 255, 0x9e / 255, 0x80 / 255)


def load_lib(name, soname):
    path = ctypes.util.find_library(name) or soname
    return ctypes.CDLL(path)


_cairo = load_lib("cairo", "libcairo.so.2")
_rsvg = load_lib("rsvg-2", "librsvg-2.so.2")
_gobject = load_lib("gobject-2.0", "libgobject-2.0.so.0")

_vp = ctypes.c_void_p
_cairo.cairo_image_surface_create.restype = _vp
_cairo.cairo_image_surface_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
_cairo.cairo_create.restype = _vp
_cairo.cairo_create.argtypes = [_vp]
_cairo.cairo_destroy.argtypes = [_vp]
_cairo.cairo_surface_destroy.argtypes = [_vp]
_cairo.cairo_surface_flush.argtypes = [_vp]
_cairo.cairo_image_surface_get_data.restype = ctypes.POINTER(ctypes.c_ubyte)
_cairo.cairo_image_surface_get_data.argtypes = [_vp]
_cairo.cairo_image_surface_get_stride.argtypes = [_vp]
_cairo.cairo_set_source_rgb.argtypes = [_vp, ctypes.c_double, ctypes.c_double, ctypes.c_double]
_cairo.cairo_paint.argtypes = [_vp]
_cairo.cairo_mask_surface.argtypes = [_vp, _vp, ctypes.c_double, ctypes.c_double]
_cairo.cairo_arc.argtypes = [_vp] + [ctypes.c_double] * 5
_cairo.cairo_fill_preserve.argtypes = [_vp]
_cairo.cairo_stroke.argtypes = [_vp]
_cairo.cairo_set_line_width.argtypes = [_vp, ctypes.c_double]
_rsvg.rsvg_handle_new_from_file.restype = _vp
_rsvg.rsvg_handle_new_from_file.argtypes = [ctypes.c_char_p, ctypes.POINTER(_vp)]
_rsvg.rsvg_handle_render_layer.argtypes = [_vp, _vp, ctypes.c_char_p, _vp, ctypes.POINTER(_vp)]
_rsvg.rsvg_handle_render_layer.restype = ctypes.c_int
_gobject.g_object_unref.argtypes = [_vp]

FORMAT_ARGB32 = 0


class RsvgRectangle(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double),
                ("width", ctypes.c_double), ("height", ctypes.c_double)]


class Svg:
    """An RsvgHandle"""

    def __init__(self, path):
        err = _vp()
        self.handle = _rsvg.rsvg_handle_new_from_file(path.encode(), ctypes.byref(err))
        if not self.handle:
            raise OSError(f"librsvg can't load {path}")

    def __del__(self):
        if getattr(self, "handle", None):
            _gobject.g_object_unref(self.handle)

    def render_layer(self, canvas, layer, w, h):
        vp = RsvgRectangle(0, 0, w, h)
        err = _vp()
        if not _rsvg.rsvg_handle_render_layer(self.handle, canvas.cr, ("#" + layer).encode(),
                                              ctypes.byref(vp), ctypes.byref(err)):
            raise KeyError(layer)


class Canvas:
    """A cairo image surface with its context"""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.surf = _cairo.cairo_image_surface_create(FORMAT_ARGB32, w, h)
        self.cr = _cairo.cairo_create(self.surf)

    def __del__(self):
        _cairo.cairo_destroy(self.cr)
        _cairo.cairo_surface_destroy(self.surf)

    def to_pil(self):
        _cairo.cairo_surface_flush(self.surf)
        stride = _cairo.cairo_image_surface_get_stride(self.surf)
        data = ctypes.string_at(_cairo.cairo_image_surface_get_data(self.surf), stride * self.h)
        # (Premultiplied, native-endian ARGB: BGRA bytes here)
        return Image.frombuffer("RGBA", (self.w, self.h), data, "raw", "BGRa", stride, 1).copy()


class Lesson:
    def __init__(self, txt_path):
        self.txt_path = txt_path
        self.svg_path = txt_path[:-4] + ".svg"
        self.name = os.path.basename(txt_path)[:-4]
        self.level = os.path.basename(os.path.dirname(os.path.abspath(txt_path)))
        self.title = {}
        self.steps = []  # (kind, layer id or None, {lang: text})
        self.errors = []
        self.warnings = []


def parse_texts(lines, lesson, where):
    """English on the first line, then LANG.utf8=… lines"""
    texts = {}
    for i, line in enumerate(lines):
        m = re.match(r"^([A-Za-z]{2,3}(?:_[A-Za-z]{2})?(?:@\w+)?)\.utf8=(.*)$", line)
        if i == 0:
            if m:
                lesson.errors.append(f"{where}: the first line must be the English text")
            texts["en"] = line.strip()
        elif m:
            if m.group(1) in texts:
                lesson.errors.append(f"{where}: '{m.group(1)}' given twice")
            texts[m.group(1)] = m.group(2).strip()
        else:
            lesson.errors.append(f"{where}: unexpected line '{line}'")
    return texts


def parse_lesson(txt_path):
    lesson = Lesson(txt_path)
    with open(txt_path, encoding="utf-8") as f:
        raw = f.read()

    blocks, block = [], []
    for line in raw.split("\n"):
        line = line.rstrip()
        if line.startswith("#"):
            continue
        if line.strip() == "":
            if block:
                blocks.append(block)
                block = []
        else:
            block.append(line)
    if block:
        blocks.append(block)

    if not blocks:
        lesson.errors.append("empty lesson")
        return lesson

    lesson.title = parse_texts(blocks[0], lesson, "title")

    for n, block in enumerate(blocks[1:], 1):
        head = block[0].split()
        where = f"step {n}"
        if not head or head[0] not in KINDS:
            lesson.errors.append(f"{where}: '{block[0]}' is not draw/guide/color/erase ID")
            continue
        kind = head[0]
        layer = None
        if kind == "erase":
            if len(head) != 1:
                lesson.errors.append(f"{where}: 'erase' takes no group")
        elif len(head) != 2:
            lesson.errors.append(f"{where}: '{kind}' needs one group id")
            continue
        else:
            layer = head[1]
        if len(block) < 2:
            lesson.errors.append(f"{where}: no instructions")
            continue
        lesson.steps.append((kind, layer, parse_texts(block[1:], lesson, where)))

    return lesson


def check_lesson(lesson, langs, handle):
    if lesson.level == "custom":
        pass  # (the user's own: any number of steps)
    elif lesson.level not in LEVELS:
        lesson.warnings.append(f"folder '{lesson.level}' is not easy/medium/hard/custom")
    else:
        lo, hi = LEVELS[lesson.level]
        if not lo <= len(lesson.steps) <= hi:
            lesson.warnings.append(
                f"{len(lesson.steps)} steps, {lesson.level} lessons have {lo} to {hi}")

    for lang in langs:
        if lang not in lesson.title:
            lesson.errors.append(f"title: no '{lang}' text")

    # SVG structure
    try:
        root = ET.parse(lesson.svg_path).getroot()
    except (ET.ParseError, OSError) as e:
        lesson.errors.append(f"SVG: {e}")
        return
    if root.get("viewBox", "").split() != ["0", "0", "640", "480"]:
        lesson.errors.append("SVG: viewBox must be '0 0 640 480'")
    if root.get("width") != "640" or root.get("height") != "480":
        lesson.errors.append("SVG: width and height must be 640 and 480")

    groups = []
    for child in root:
        tag = child.tag.replace(SVG_NS, "")
        if tag in ("title", "desc", "defs", "metadata"):
            continue
        if tag != "g" or not child.get("id"):
            lesson.errors.append(f"SVG: top-level <{tag}> outside a step group")
            continue
        if not re.match(r"^[a-z0-9-]+$", child.get("id")):
            lesson.errors.append(f"SVG: bad group id '{child.get('id')}'")
        groups.append(child.get("id"))

    used = {}
    has_guides = False
    for n, (kind, layer, texts) in enumerate(lesson.steps, 1):
        where = f"step {n}"
        for lang in langs:
            if lang not in texts:
                lesson.errors.append(f"{where}: no '{lang}' text")
        for lang, text in texts.items():
            if len(text) > MAX_TEXT:
                lesson.warnings.append(f"{where} ({lang}): {len(text)} characters, keep it under {MAX_TEXT}")
        if kind == "guide":
            has_guides = True
        if kind == "erase" and not has_guides:
            lesson.errors.append(f"{where}: 'erase' with no guide before it")
        if layer is None:
            continue
        if layer in used:
            lesson.errors.append(f"{where}: group '{layer}' already used by step {used[layer]}")
        used[layer] = n
        if layer not in groups:
            lesson.errors.append(f"{where}: no top-level group '{layer}' in the SVG")

    for g in groups:
        if g not in used:
            lesson.errors.append(f"SVG: group '{g}' is not used by any step")

    if has_guides and not any(k == "erase" for k, _, _ in lesson.steps):
        lesson.warnings.append("guide shapes are never erased")

    # Colors: one per color group; lines dark
    for n, (kind, layer, texts) in enumerate(lesson.steps, 1):
        if layer is None or layer not in groups:
            continue
        img = layer_image(handle, layer, 320, 240)
        if kind == "color":
            share, color = dominant_color(img)
            if color is None:
                lesson.errors.append(f"step {n}: color group '{layer}' is empty")
            elif share < 0.9:
                lesson.warnings.append(
                    f"step {n}: color group '{layer}' has more than one color "
                    f"(#{color[0]:02x}{color[1]:02x}{color[2]:02x} is {share:.0%})")
        elif kind == "draw":
            share, color = dominant_color(img)
            if color is None:
                lesson.errors.append(f"step {n}: draw group '{layer}' is empty")
            elif sum(color) > 3 * 0x60:
                lesson.warnings.append(f"step {n}: draw group '{layer}' is not dark lines")


def layer_image(handle, layer, w, h):
    """The group alone, as a PIL RGBA image of the whole picture"""
    canvas = Canvas(w, h)
    handle.render_layer(canvas, layer, w, h)
    return canvas.to_pil()


def dominant_color(img):
    """The most common color of the opaque pixels, and its share"""
    counts = {}
    total = 0
    data = img.tobytes()
    for i in range(0, len(data), 4):
        r, g, b, a = data[i:i + 4]
        if a < 200:
            continue
        key = (r & 0xf8, g & 0xf8, b & 0xf8)
        counts[key] = counts.get(key, 0) + 1
        total += 1
    if not total:
        return 0, None
    key = max(counts, key=counts.get)
    return counts[key] / total, key


def compose(handle, lesson, upto, w, h, final=False):
    """Step `upto` (0-based) as shown once its animation is over; with
    final, the finished picture (all colors and lines, no guides)"""
    canvas = Canvas(w, h)
    cr = canvas.cr
    _cairo.cairo_set_source_rgb(cr, 1, 1, 1)
    _cairo.cairo_paint(cr)

    steps = lesson.steps
    last = len(steps) - 1 if final else upto

    def erased_after(i):
        return any(steps[j][0] == "erase" for j in range(i + 1, last + 1))

    def paint(layer, tint):
        if tint is None:
            handle.render_layer(canvas, layer, w, h)
        else:
            tmp = Canvas(w, h)
            handle.render_layer(tmp, layer, w, h)
            _cairo.cairo_set_source_rgb(cr, *tint)
            _cairo.cairo_mask_surface(cr, tmp.surf, 0, 0)

    for want in ("color", "guide", "draw"):
        for i in range(last + 1):
            kind, layer, _ = steps[i]
            if kind != want:
                continue
            if kind == "guide" and (final or erased_after(i)):
                continue
            new = (i == upto and not final)
            if kind == "draw":
                paint(layer, HIGHLIGHT if new else None)
            elif kind == "guide":
                paint(layer, GUIDE_HIGHLIGHT if new else None)
            else:
                paint(layer, None)

    # The crayon of a coloring step (a plain dot here)
    if not final and steps[upto][0] == "color":
        img = layer_image(handle, steps[upto][1], w, h)
        _, color = dominant_color(img)
        if color:
            r = h / 12
            _cairo.cairo_arc(cr, w - r * 1.6, r * 1.6, r, 0, 6.2832)
            _cairo.cairo_set_source_rgb(cr, *(c / 255 for c in color))
            _cairo.cairo_fill_preserve(cr)
            _cairo.cairo_set_source_rgb(cr, 0.17, 0.17, 0.17)
            _cairo.cairo_set_line_width(cr, 2)
            _cairo.cairo_stroke(cr)

    return canvas.to_pil()


def find_font(size):
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def sheet(handle, lesson, langs, size):
    w, h = size, size * 3 // 4
    font = find_font(max(11, size // 26))
    bold = find_font(max(13, size // 20))
    cap_h = (font.size + 3) * 3 * len(langs) + bold.size + 12
    frames = [("0", " / ".join(lesson.title.get(l, "?") for l in langs),
               compose(handle, lesson, 0, w, h, final=True), {})]
    for i, (kind, layer, texts) in enumerate(lesson.steps):
        frames.append((str(i + 1), f"{kind} {layer or ''}",
                       compose(handle, lesson, i, w, h), texts))

    cols = 4
    rows = (len(frames) + cols - 1) // cols
    pad = 10
    out = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + cap_h + pad) + pad), (225, 228, 232))
    draw = ImageDraw.Draw(out)
    for n, (num, head, img, texts) in enumerate(frames):
        x = pad + (n % cols) * (w + pad)
        y = pad + (n // cols) * (h + cap_h + pad)
        out.paste(img.convert("RGB"), (x, y))
        draw.rectangle([x, y + h, x + w - 1, y + h + cap_h - 1], fill=(255, 255, 255))
        draw.text((x + 4, y + h + 4), f"{num}. {head}", font=bold, fill=(40, 40, 40))
        ty = y + h + bold.size + 8
        for lang in langs:
            if lang not in texts:
                continue
            for line in wrap(draw, f"[{lang}] {texts[lang]}", font, w - 8)[:3]:
                draw.text((x + 4, ty), line, font=font, fill=(60, 60, 90))
                ty += font.size + 3
    return out


def find_lessons(paths):
    found = []
    for path in paths:
        if os.path.isdir(path):
            for dirpath, _, files in sorted(os.walk(path)):
                for f in sorted(files):
                    if f.endswith(".txt") and f != "README.txt" and \
                            os.path.exists(os.path.join(dirpath, f[:-4] + ".svg")):
                        found.append(os.path.join(dirpath, f))
        else:
            found.append(path)
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", help="folder for the step sheets")
    ap.add_argument("--size", type=int, default=320, help="width of each step (default 320)")
    ap.add_argument("--langs", default="en,it", help="languages that must be there (default en,it)")
    args = ap.parse_args()
    langs = args.langs.split(",")

    failed = False
    for txt in find_lessons(args.paths):
        lesson = parse_lesson(txt)
        if lesson.level == "custom" and not lesson.steps and not lesson.errors:
            # (Just a title: Tux Paint copies the picture with a grid)
            print(f"custom/{lesson.name}: a picture with its title, nothing to check")
            continue
        try:
            handle = Svg(lesson.svg_path)
        except OSError as e:
            lesson.errors.append(f"SVG: {e}")
            handle = None
        if handle is not None:
            check_lesson(lesson, langs, handle)

        status = "ERRORS" if lesson.errors else ("warnings" if lesson.warnings else "ok")
        print(f"{lesson.level}/{lesson.name}: {len(lesson.steps)} steps, {status}")
        for e in lesson.errors:
            print(f"  error: {e}")
        for w in lesson.warnings:
            print(f"  warning: {w}")
        failed |= bool(lesson.errors)

        if args.out and handle is not None and not lesson.errors:
            os.makedirs(args.out, exist_ok=True)
            out = os.path.join(args.out, f"{lesson.level}-{lesson.name}.png")
            sheet(handle, lesson, langs, args.size).save(out)
            print(f"  sheet: {out}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
