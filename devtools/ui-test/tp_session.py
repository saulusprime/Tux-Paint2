"""Run on the host: drive Tux Paint and capture screenshots.

usage: flatpak-spawn --host [--env=TP_BIN=path] python3 - WINDOWSIZE ACTION... < tp_session.py > shots.tar

ACTION is one of:
  click:X,Y   left click at window coordinates (X,Y)
  tool:N      left click on tool button N (button size from TP_BUTTON, default 48)
  drag:X1,Y1,X2,Y2  press at (X1,Y1), move to (X2,Y2), release
  wait:SEC    sleep
  shot:NAME   capture the window to NAME.png
Writes a tar archive of the PNGs to stdout.
"""
import ctypes, io, os, subprocess, sys, tarfile, tempfile, time

size, actions = sys.argv[1], sys.argv[2:]
binary = os.environ.get("TP_BIN", os.path.expanduser("~/.local/bin/tuxpaint"))
button = int(os.environ.get("TP_BUTTON", "48"))
title_h = int(40 * button / 48 + 0.5)

x11 = ctypes.CDLL("libX11.so.6")
xtst = ctypes.CDLL("libXtst.so.6")
x11.XOpenDisplay.restype = ctypes.c_void_p
dpy = ctypes.c_void_p(x11.XOpenDisplay(None))

proc = subprocess.Popen(
    [binary, "--nolockfile", "--nosound",
     "--windowed", "--windowsize=" + size],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def window():
    tree = subprocess.run(["xwininfo", "-root", "-tree"], capture_output=True, text=True).stdout
    for line in tree.splitlines():
        if '"TuxPaint.TuxPaint"' in line:
            wid = line.split()[0]
            info = subprocess.run(["xwininfo", "-id", wid], capture_output=True, text=True).stdout
            pos = {}
            for l in info.splitlines():
                l = l.strip()
                if l.startswith("Absolute upper-left X:"):
                    pos["x"] = int(l.split(":")[1])
                if l.startswith("Absolute upper-left Y:"):
                    pos["y"] = int(l.split(":")[1])
            return wid, pos["x"], pos["y"]
    return None


out = tarfile.open(fileobj=sys.stdout.buffer, mode="w|")
try:
    time.sleep(5)
    win = window()
    if win is None:
        sys.exit("window not found")
    wid, wx, wy = win
    for act in actions:
        kind, _, arg = act.partition(":")
        if kind == "wait":
            time.sleep(float(arg))
        elif kind in ("click", "tool"):
            if kind == "tool":
                n = int(arg)
                x, y = (n % 2) * button + button // 2, title_h + (n // 2) * button + button // 2
            else:
                x, y = (int(v) for v in arg.split(","))
            xtst.XTestFakeMotionEvent(dpy, -1, wx + x, wy + y, 0)
            x11.XFlush(dpy)
            time.sleep(0.2)
            xtst.XTestFakeButtonEvent(dpy, 1, 1, 0)
            x11.XFlush(dpy)
            time.sleep(0.1)
            xtst.XTestFakeButtonEvent(dpy, 1, 0, 0)
            x11.XFlush(dpy)
            time.sleep(0.8)
        elif kind == "drag":
            x1, y1, x2, y2 = (int(v) for v in arg.split(","))
            xtst.XTestFakeMotionEvent(dpy, -1, wx + x1, wy + y1, 0)
            x11.XFlush(dpy)
            time.sleep(0.2)
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
