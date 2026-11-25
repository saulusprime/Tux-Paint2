#!/usr/bin/env python3
"""Icons of the "Learn" tool and of its dialog's buttons.

Usage: learn_icons.py [REPO_DIR]

Writes, as SVG and as the PNG at the design size that Tux Paint uses with
48x48 buttons (bigger buttons use the SVG, see loadimagerb()):

  data/images/tools/learn      the tool: a sheet with a drawing, a pencil
  data/images/ui/learn_prev    previous step (arrow)
  data/images/ui/learn_next    next step (arrow)
  data/images/ui/learn_voice   say it again / voice on (speaker, waves)
  data/images/ui/learn_mute    voice off (speaker, cross)
  data/images/ui/learn_add     add a picture of the user's (a picture, a plus)
  data/images/ui/learn_rename  rename a picture of the user's (a name, a pencil)

All 40x30, black with transparency like the other tool icons (Tux Paint
turns them grey when the button is off). Needs Pillow, and librsvg and
cairo (through ctypes).
"""

import ctypes
import ctypes.util
import os
import sys

from PIL import Image

W, H = 40, 30
LINE = 'stroke="#000000" stroke-linecap="round" stroke-linejoin="round"'
LIGHT = 'fill="#000000" fill-opacity="0.35"'

ICONS = {
    "tools/learn": f'''
  <rect x="3" y="3.5" width="22" height="23" rx="1.5" fill="#000000" fill-opacity="0.12" {LINE} stroke-width="1.6"/>
  <circle cx="13" cy="13" r="4.2" {LIGHT} {LINE} stroke-width="1.4"/>
  <path d="M13,5.6 V7 M13,19 V20.4 M5.6,13 H7 M19,13 H20.4 M7.8,7.8 L8.8,8.8 M17.2,17.2 L18.2,18.2 M18.2,7.8 L17.2,8.8 M8.8,17.2 L7.8,18.2" fill="none" {LINE} stroke-width="1.3"/>
  <path d="M7,23 H19" fill="none" {LINE} stroke-width="1.3" stroke-dasharray="2 2"/>
  <path d="M34.5,2.5 L38,5.5 L26.5,19 L23,16 Z" {LIGHT} {LINE} stroke-width="1.4"/>
  <path d="M23,16 L26.5,19 L21.5,22.5 Z" fill="#000000" {LINE} stroke-width="1.2"/>''',

    "ui/learn_prev": f'''
  <path d="M5,15 L18,4 V10 H34 V20 H18 V26 Z" {LIGHT} {LINE} stroke-width="2"/>''',

    "ui/learn_next": f'''
  <path d="M35,15 L22,4 V10 H6 V20 H22 V26 Z" {LIGHT} {LINE} stroke-width="2"/>''',

    "ui/learn_voice": f'''
  <path d="M5,11 H11 L18,5 V25 L11,19 H5 Z" {LIGHT} {LINE} stroke-width="1.8"/>
  <path d="M22.5,10.5 Q25.5,15 22.5,19.5 M26.5,7 Q31.5,15 26.5,23 M30.5,3.5 Q37.5,15 30.5,26.5" fill="none" {LINE} stroke-width="2"/>''',

    "ui/learn_mute": f'''
  <path d="M5,11 H11 L18,5 V25 L11,19 H5 Z" {LIGHT} {LINE} stroke-width="1.8"/>
  <path d="M24,9.5 L35,20.5 M35,9.5 L24,20.5" fill="none" {LINE} stroke-width="2.6"/>''',

    "ui/learn_add": f'''
  <rect x="1.5" y="6.5" width="20" height="18" rx="1.5" fill="#000000" fill-opacity="0.12" {LINE} stroke-width="1.6"/>
  <path d="M4.5,21.5 L9.5,14 L13,18.5 L15.5,16 L18.5,21.5 Z" {LIGHT} {LINE} stroke-width="1.3"/>
  <circle cx="16" cy="10.5" r="1.8" {LIGHT} {LINE} stroke-width="1.2"/>
  <path d="M31.5,8 V22 M24.5,15 H38.5" fill="none" {LINE} stroke-width="3.4"/>''',

    "ui/learn_rename": f'''
  <rect x="1.5" y="10.5" width="25" height="13" rx="2" fill="#000000" fill-opacity="0.12" {LINE} stroke-width="1.6"/>
  <path d="M5.5,17 H14" fill="none" {LINE} stroke-width="3"/>
  <path d="M18,13.5 V20.5 M16.5,13.5 H19.5 M16.5,20.5 H19.5" fill="none" {LINE} stroke-width="1.3"/>
  <path d="M35.5,1.5 L38.5,4.5 L29,15.5 L26,12.5 Z" {LIGHT} {LINE} stroke-width="1.4"/>
  <path d="M26,12.5 L29,15.5 L24,19 Z" fill="#000000" {LINE} stroke-width="1.2"/>''',
}


def svg_text(body):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
            f'<!-- Made by devtools/content/learn_icons.py -->{body}\n</svg>\n')


def render(svg_path, w, h):
    """The SVG at w x h, as a PIL image (librsvg and cairo via ctypes)"""
    vp = ctypes.c_void_p
    cairo = ctypes.CDLL(ctypes.util.find_library("cairo") or "libcairo.so.2")
    rsvg = ctypes.CDLL(ctypes.util.find_library("rsvg-2") or "librsvg-2.so.2")
    gobject = ctypes.CDLL(ctypes.util.find_library("gobject-2.0") or "libgobject-2.0.so.0")
    cairo.cairo_image_surface_create.restype = vp
    cairo.cairo_create.restype = vp
    cairo.cairo_create.argtypes = [vp]
    cairo.cairo_image_surface_get_data.restype = ctypes.POINTER(ctypes.c_ubyte)
    cairo.cairo_image_surface_get_data.argtypes = [vp]
    cairo.cairo_image_surface_get_stride.argtypes = [vp]
    cairo.cairo_surface_flush.argtypes = [vp]
    cairo.cairo_destroy.argtypes = [vp]
    cairo.cairo_surface_destroy.argtypes = [vp]
    rsvg.rsvg_handle_new_from_file.restype = vp
    rsvg.rsvg_handle_new_from_file.argtypes = [ctypes.c_char_p, ctypes.POINTER(vp)]
    rsvg.rsvg_handle_render_document.argtypes = [vp, vp, vp, ctypes.POINTER(vp)]
    gobject.g_object_unref.argtypes = [vp]

    class Rect(ctypes.Structure):
        _fields_ = [(n, ctypes.c_double) for n in ("x", "y", "width", "height")]

    err = vp()
    handle = rsvg.rsvg_handle_new_from_file(svg_path.encode(), ctypes.byref(err))
    surf = cairo.cairo_image_surface_create(0, w, h)
    cr = cairo.cairo_create(surf)
    rect = Rect(0, 0, w, h)
    rsvg.rsvg_handle_render_document(handle, cr, ctypes.byref(rect), ctypes.byref(err))
    cairo.cairo_surface_flush(surf)
    stride = cairo.cairo_image_surface_get_stride(surf)
    data = ctypes.string_at(cairo.cairo_image_surface_get_data(surf), stride * h)
    img = Image.frombuffer("RGBA", (w, h), data, "raw", "BGRa", stride, 1).copy()
    cairo.cairo_destroy(cr)
    cairo.cairo_surface_destroy(surf)
    gobject.g_object_unref(handle)
    return img


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
    for name, body in ICONS.items():
        base = os.path.join(repo, "data", "images", name)
        with open(base + ".svg", "w") as f:
            f.write(svg_text(body))
        render(base + ".svg", W, H).convert("LA").save(base + ".png")
        print(base + ".{svg,png}")


if __name__ == "__main__":
    main()
