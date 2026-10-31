"""Run on the host: drive Tux Paint and capture screenshots.

usage: flatpak-spawn --host [--env=TP_BIN=path] [--env=TP_BUTTON=px] [--env=TP_ARGS="opts"] [--env=TP_SCALE=n] \
         [--env=TP_START_WAIT=sec] [--env=TP_LOG=host-file-for-tuxpaint-output] [--env=TP_WRAP=cmd] \
         [--env=TP_SOUND=1 (sound on, through SDL's silent "dummy" audio driver)] \
         python3 - WINDOWSIZE ACTION... < tp_session.py > shots.tar

WINDOWSIZE is e.g. 800x600 (run windowed at that size), or "-" to pass no
--windowed/--windowsize (e.g. to test TP_ARGS="--fullscreen").

ACTION is one of:
  click:X,Y   left click at window coordinates (X,Y)
  tool:N      left click on tool button N (button size from TP_BUTTON, default 48)
  drag:X1,Y1,X2,Y2  press at (X1,Y1), move to (X2,Y2), release
  move:X,Y    move the pointer without clicking
  key:K1+K2[:SEC]  press X keysyms in order (e.g. Alt_L+Return), hold SEC
              seconds (default 0.1), release in reverse order
  cursor:NAME save the current mouse cursor (via XFixes) to NAME.png
  wait:SEC    sleep
  shot:NAME   capture the window to NAME.png
  info:NAME   print the window's position, size and map state to stderr
Writes a tar archive of the PNGs to stdout.

Safety: only the window of the Tux Paint process started here is used (by
_NET_WM_PID; other Tux Paint windows, e.g. the user's, are ignored). It is
activated first, and before every pointer action the script checks that it
is the topmost window under the pointer; if not (e.g. it opened behind
another window), it stops without clicking. Likewise it never presses keys
unless the keyboard focus is in that window.
"""
import ctypes, io, os, subprocess, sys, tarfile, tempfile, time

size, actions = sys.argv[1], sys.argv[2:]
binary = os.environ.get("TP_BIN", os.path.expanduser("~/.local/bin/tuxpaint"))
button = int(os.environ.get("TP_BUTTON", "48"))
title_h = int(40 * button / 48 + 0.5)
start_wait = float(os.environ.get("TP_START_WAIT", "5"))
extra_args = os.environ.get("TP_ARGS", "").split()
scale = float(os.environ.get("TP_SCALE", "1"))  # multiplies click/drag coordinates

x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")
xfixes = ctypes.CDLL("libXfixes.so.3")
x11.XOpenDisplay.restype = ctypes.c_void_p


class XFixesCursorImage(ctypes.Structure):
    _fields_ = [("x", ctypes.c_short), ("y", ctypes.c_short),
                ("width", ctypes.c_ushort), ("height", ctypes.c_ushort),
                ("xhot", ctypes.c_ushort), ("yhot", ctypes.c_ushort),
                ("cursor_serial", ctypes.c_ulong),
                ("pixels", ctypes.POINTER(ctypes.c_ulong)),
                ("atom", ctypes.c_ulong), ("name", ctypes.c_char_p)]


class XClientMessageEvent(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int), ("serial", ctypes.c_ulong),
                ("send_event", ctypes.c_int), ("display", ctypes.c_void_p),
                ("window", ctypes.c_ulong), ("message_type", ctypes.c_ulong),
                ("format", ctypes.c_int), ("data", ctypes.c_long * 5),
                ("pad", ctypes.c_long * 16)]  # XEvent is 24 longs


xfixes.XFixesGetCursorImage.restype = ctypes.POINTER(XFixesCursorImage)
x11.XDefaultRootWindow.restype = ctypes.c_ulong
x11.XInternAtom.restype = ctypes.c_ulong
x11.XStringToKeysym.argtypes = [ctypes.c_char_p]
x11.XStringToKeysym.restype = ctypes.c_ulong
x11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
x11.XKeysymToKeycode.restype = ctypes.c_ubyte
dpy = ctypes.c_void_p(x11.XOpenDisplay(None))
root = x11.XDefaultRootWindow(dpy)


def toplevel(w):
    """The child of the root window that contains window w (its frame)."""
    r, parent, children, n = ctypes.c_ulong(), ctypes.c_ulong(), ctypes.POINTER(ctypes.c_ulong)(), ctypes.c_uint()
    while True:
        x11.XQueryTree(dpy, ctypes.c_ulong(w), ctypes.byref(r), ctypes.byref(parent),
                       ctypes.byref(children), ctypes.byref(n))
        if children:
            x11.XFree(children)
        if parent.value in (0, root):
            return w
        w = parent.value


def under_pointer():
    """The topmost top-level window under the pointer."""
    r, child = ctypes.c_ulong(), ctypes.c_ulong()
    i = ctypes.c_int()
    mask = ctypes.c_uint()
    x11.XQueryPointer(dpy, ctypes.c_ulong(root), ctypes.byref(r), ctypes.byref(child),
                      ctypes.byref(i), ctypes.byref(i), ctypes.byref(i), ctypes.byref(i),
                      ctypes.byref(mask))
    return child.value


def activate(w):
    """Ask the window manager to raise and focus w (as a pager would)."""
    ev = XClientMessageEvent()
    ev.type = 33  # ClientMessage
    ev.send_event = 1
    ev.window = w
    ev.message_type = x11.XInternAtom(dpy, b"_NET_ACTIVE_WINDOW", 0)
    ev.format = 32
    ev.data[0] = 2  # source: pager
    x11.XSendEvent(dpy, ctypes.c_ulong(root), 0, (1 << 19) | (1 << 20), ctypes.byref(ev))
    x11.XFlush(dpy)
    time.sleep(0.5)

def tuxpaint_windows():
    tree = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True).stdout
    return [l.split()[0] for l in tree.splitlines() if '"TuxPaint.TuxPaint"' in l]


def window_pid(wid):
    prop = subprocess.run(["xprop", "-id", wid, "_NET_WM_PID"], capture_output=True, text=True).stdout
    try:
        return int(prop.split("=")[1])
    except (IndexError, ValueError):
        return None


windows_before = set(tuxpaint_windows())
log = open(os.environ["TP_LOG"], "w") if "TP_LOG" in os.environ else subprocess.DEVNULL
wrapper = os.environ.get("TP_WRAP", "").split()  # e.g. "stdbuf -oL -eL"
sound = bool(os.environ.get("TP_SOUND"))
child_env = dict(os.environ, SDL_AUDIODRIVER="dummy") if sound else None
proc = subprocess.Popen(
    wrapper + [binary, "--nolockfile"] + ([] if sound else ["--nosound"]) +
    ([] if size == "-" else ["--windowed", "--windowsize=" + size]) + extra_args,
    stdout=log, stderr=subprocess.STDOUT, env=child_env)


def window():
    """Our Tux Paint window: new since launch, and owned by our process."""
    for wid in tuxpaint_windows():
        if wid in windows_before or window_pid(wid) != proc.pid:
            continue
        return wid
    return None


def origin(wid):
    """Where window wid is on the screen now (it moves when going fullscreen)."""
    info = subprocess.run(["xwininfo", "-id", wid], capture_output=True, text=True).stdout
    pos = {}
    for l in info.splitlines():
        l = l.strip()
        if l.startswith("Absolute upper-left X:"):
            pos["x"] = int(l.split(":")[1])
        if l.startswith("Absolute upper-left Y:"):
            pos["y"] = int(l.split(":")[1])
    return pos["x"], pos["y"]


out = tarfile.open(fileobj=sys.stdout.buffer, mode="w|")
try:
    time.sleep(start_wait)
    wid = window()
    if wid is None:
        sys.exit("window of our Tux Paint (pid %d) not found" % proc.pid)
    activate(int(wid, 16))
    wx, wy = origin(wid)

    def pointer_to(x, y):
        """Move the pointer; False if Tux Paint isn't the window under it."""
        global wx, wy
        wx, wy = origin(wid)
        frame = toplevel(int(wid, 16))
        xtst.XTestFakeMotionEvent(dpy, -1, wx + x, wy + y, 0)
        x11.XFlush(dpy)
        time.sleep(0.2)
        top = under_pointer()
        if top != frame:
            sys.stderr.write("STOP: at %d,%d the topmost window is 0x%x, not Tux Paint (0x%x); "
                             "not clicking\n" % (x, y, top, frame))
            return False
        return True

    for act in actions:
        kind, _, arg = act.partition(":")
        if kind == "wait":
            time.sleep(float(arg))
        elif kind in ("click", "tool"):
            if kind == "tool":
                n = int(arg)
                x, y = (n % 2) * button + button // 2, title_h + (n // 2) * button + button // 2
            else:
                x, y = (int(int(v) * scale) for v in arg.split(","))
            if not pointer_to(x, y):
                break
            xtst.XTestFakeButtonEvent(dpy, 1, 1, 0)
            x11.XFlush(dpy)
            time.sleep(0.1)
            xtst.XTestFakeButtonEvent(dpy, 1, 0, 0)
            x11.XFlush(dpy)
            time.sleep(0.8)
        elif kind == "drag":
            x1, y1, x2, y2 = (int(int(v) * scale) for v in arg.split(","))
            if not pointer_to(x1, y1) or not pointer_to(x2, y2) or not pointer_to(x1, y1):
                break
            xtst.XTestFakeButtonEvent(dpy, 1, 1, 0)
            x11.XFlush(dpy)
            for i in range(1, 21):
                time.sleep(0.03)
                xtst.XTestFakeMotionEvent(dpy, -1, wx + x1 + (x2 - x1) * i // 20, wy + y1 + (y2 - y1) * i // 20, 0)
                x11.XFlush(dpy)
            time.sleep(0.1)
            xtst.XTestFakeButtonEvent(dpy, 1, 0, 0)
            x11.XFlush(dpy)
            time.sleep(0.8)
        elif kind == "key":
            names, _, hold = arg.partition(":")
            focus, revert = ctypes.c_ulong(), ctypes.c_int()
            x11.XGetInputFocus(dpy, ctypes.byref(focus), ctypes.byref(revert))
            if focus.value in (0, 1) or toplevel(focus.value) != toplevel(int(wid, 16)):
                sys.stderr.write("STOP: the keyboard focus (0x%x) is not in Tux Paint; "
                                 "not pressing keys\n" % focus.value)
                break
            codes = [x11.XKeysymToKeycode(dpy, x11.XStringToKeysym(n.encode())) for n in names.split("+")]
            if 0 in codes:
                sys.stderr.write("STOP: unknown key in %r\n" % names)
                break
            for c in codes:
                xtst.XTestFakeKeyEvent(dpy, c, 1, 0)
                x11.XFlush(dpy)
                time.sleep(0.05)
            time.sleep(float(hold or 0.1))
            for c in reversed(codes):
                xtst.XTestFakeKeyEvent(dpy, c, 0, 0)
                x11.XFlush(dpy)
                time.sleep(0.05)
            time.sleep(0.8)
        elif kind == "move":
            x, y = (int(int(v) * scale) for v in arg.split(","))
            if not pointer_to(x, y):
                break
            time.sleep(0.3)
        elif kind == "cursor":
            from PIL import Image
            ci = xfixes.XFixesGetCursorImage(dpy).contents
            argb = [ci.pixels[i] & 0xffffffff for i in range(ci.width * ci.height)]
            rgba = bytes(b for p in argb for b in ((p >> 16) & 255, (p >> 8) & 255, p & 255, p >> 24))
            buf = io.BytesIO()
            Image.frombytes("RGBA", (ci.width, ci.height), rgba).save(buf, "PNG")
            sys.stderr.write("%s: cursor %dx%d, hotspot %d,%d\n" % (arg, ci.width, ci.height, ci.xhot, ci.yhot))
            ti = tarfile.TarInfo(arg + ".png")
            ti.size = len(buf.getvalue())
            out.addfile(ti, io.BytesIO(buf.getvalue()))
        elif kind == "info":
            info = subprocess.run(["xwininfo", "-id", wid], capture_output=True, text=True).stdout
            got = {}
            for l in info.splitlines():
                k, _, v = l.strip().partition(":")
                got[k] = v.strip()
            sys.stderr.write("%s: %sx%s at %s,%s, %s\n" % (
                arg, got.get("Width"), got.get("Height"), got.get("Absolute upper-left X"),
                got.get("Absolute upper-left Y"), got.get("Map State")))
        elif kind == "shot":
            xwd = subprocess.run(["xwd", "-silent", "-id", wid], capture_output=True).stdout
            png = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "xwd_pipe", "-i", "-",
                                  "-f", "image2pipe", "-vcodec", "png", "-"],
                                 input=xwd, capture_output=True).stdout
            ti = tarfile.TarInfo(arg + ".png")
            ti.size = len(png)
            out.addfile(ti, io.BytesIO(png))
finally:
    out.close()
    proc.kill()
    proc.wait()
