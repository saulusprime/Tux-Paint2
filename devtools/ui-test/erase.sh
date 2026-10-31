#!/bin/bash
# usage: erase.sh OUTDIR BINARY [SCALE]
# Erase prompt of the Open dialog at 800x600 times SCALE (an integer,
# default 1): draw a dot, save, open, select the first picture, ask to
# erase it, answer "No". Then prints the saved thumbnail sizes and checks
# that nothing reached the trash.
# Uses a copy of ~/.cache/tuxpaint-test-canon as savedir and a test trash
# (XDG_DATA_HOME=~/.cache/tuxpaint-test-xdg), never the user's own.
# Run from the VS Code Flatpak sandbox, like regress.sh.
S=$(dirname "$(realpath "$0")")
out=$1; bin=$2; scale=${3:-1}
mkdir -p "$out" && rm -f "$out"/*.png
cd "$HOME" && flatpak-spawn --host bash -c 'rm -rf ~/.cache/tuxpaint-test ~/.cache/tuxpaint-test-xdg &&
  cp -a ~/.cache/tuxpaint-test-canon ~/.cache/tuxpaint-test && mkdir -p ~/.cache/tuxpaint-test-xdg'
flatpak-spawn --host --directory="$HOME" --env=TP_BIN="$bin" --env=TP_ARGS="--savedir=$HOME/.cache/tuxpaint-test" \
  --env=TP_WRAP="env XDG_DATA_HOME=$HOME/.cache/tuxpaint-test-xdg" \
  --env=TP_SCALE="$scale" --env=TP_BUTTON=$((48 * scale)) \
  python3 - $((800 * scale))x$((600 * scale)) move:48,16 wait:1 click:48,16 wait:1 \
  click:400,300 wait:1 tool:13 wait:2 \
  tool:12 wait:1 click:170,75 wait:1 shot:e0-open \
  click:632,448 wait:2 shot:e1-erase click:205,302 wait:1 shot:e2-no \
  < "$S/tp_session.py" | tar xf - -C "$out"
flatpak-spawn --host bash -c 'pgrep -a -x tuxpaint && echo "ATTENZIONE: processo rimasto" || true'
flatpak-spawn --host python3 -c '
import glob, os
from PIL import Image
d = os.path.expanduser("~/.cache/tuxpaint-test/saved")
print("disegni:", len(glob.glob(d + "/*.png")))
for f in sorted(glob.glob(d + "/.thumbs/*.png")):
    print("miniatura salvata:", os.path.basename(f), "%dx%d" % Image.open(f).size)
t = os.path.expanduser("~/.cache/tuxpaint-test-xdg")
n = sum(len(fs) for _, _, fs in os.walk(t))
print("file nel Cestino di prova:", n)'
ls "$out"
