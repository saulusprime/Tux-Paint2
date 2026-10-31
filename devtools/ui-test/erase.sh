#!/bin/bash
# usage: erase.sh OUTDIR BINARY [SCALE [ANSWER]]
# Erase prompt of the Open dialog at 800x600 times SCALE (an integer,
# default 1): draw a dot, save, open, select the first picture, ask to
# erase it, answer ANSWER ("no", the default, or "yes"). Then prints the
# saved thumbnail sizes and what reached the trash.
# Uses a copy of ~/.cache/tuxpaint-test-canon as savedir and a test trash,
# never the user's own: XDG_DATA_HOME=$TP_TEST_XDG (on the host; default
# ~/.cache/tuxpaint-test-xdg; e.g. /tmp/... to be on another filesystem
# than the savedir, so that moving to the trash has to copy).
# Run from the VS Code Flatpak sandbox, like regress.sh.
S=$(dirname "$(realpath "$0")")
out=$1; bin=$2; scale=${3:-1}; answer=${4:-no}
xdg=${TP_TEST_XDG:-$HOME/.cache/tuxpaint-test-xdg}
[ "$answer" = yes ] && reply=205,250 || reply=205,302
mkdir -p "$out" && rm -f "$out"/*.png
cd "$HOME" && flatpak-spawn --host --env=XDG="$xdg" bash -c 'rm -rf ~/.cache/tuxpaint-test "$XDG" &&
  cp -a ~/.cache/tuxpaint-test-canon ~/.cache/tuxpaint-test && mkdir -p "$XDG"'
flatpak-spawn --host --directory="$HOME" --env=TP_BIN="$bin" --env=TP_ARGS="--savedir=$HOME/.cache/tuxpaint-test" \
  --env=TP_WRAP="env XDG_DATA_HOME=$xdg" \
  --env=TP_SCALE="$scale" --env=TP_BUTTON=$((48 * scale)) \
  python3 - $((800 * scale))x$((600 * scale)) move:48,16 wait:1 click:48,16 wait:1 \
  click:400,300 wait:1 tool:13 wait:2 \
  tool:12 wait:1 click:170,75 wait:1 shot:e0-open \
  click:632,448 wait:2 shot:e1-erase click:$reply wait:2 shot:e2-$answer \
  < "$S/tp_session.py" | tar xf - -C "$out"
flatpak-spawn --host bash -c 'pgrep -a -x tuxpaint && echo "ATTENZIONE: processo rimasto" || true'
flatpak-spawn --host --env=XDG="$xdg" python3 -c '
import glob, os, stat
from PIL import Image
d = os.path.expanduser("~/.cache/tuxpaint-test/saved")
print("disegni:", len(glob.glob(d + "/*.png")))
for f in sorted(glob.glob(d + "/.thumbs/*.png")):
    print("miniatura salvata:", os.path.basename(f), "%dx%d" % Image.open(f).size)
t = os.environ["XDG"]
n = 0
for dp, dns, fs in os.walk(t):
    for dn in dns:
        print("cartella %s: %o" % (os.path.relpath(os.path.join(dp, dn), t), stat.S_IMODE(os.stat(os.path.join(dp, dn)).st_mode)))
    for f in fs:
        n += 1
        print("nel Cestino di prova: %s, %d byte" % (os.path.relpath(os.path.join(dp, f), t), os.path.getsize(os.path.join(dp, f))))
print("file nel Cestino di prova:", n)'
ls "$out"
