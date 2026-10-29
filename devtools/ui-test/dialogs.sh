#!/bin/bash
# usage: dialogs.sh OUTDIR BINARY [SCALE]
# Dialog capture sequence at 800x600 times SCALE (an integer, default 1;
# coordinates below are for 48x48 buttons and get multiplied by SCALE):
# quit prompt, Open, slideshow (select, play), New, color picker.
# Uses a copy of ~/.cache/tuxpaint-test-canon (two saved pictures) as savedir.
# Run from the VS Code Flatpak sandbox, like regress.sh.
S=$(dirname "$(realpath "$0")")
out=$1; bin=$2; scale=${3:-1}
mkdir -p "$out" && rm -f "$out"/*.png
cd "$HOME" && flatpak-spawn --host bash -c 'rm -rf ~/.cache/tuxpaint-test && cp -a ~/.cache/tuxpaint-test-canon ~/.cache/tuxpaint-test'
flatpak-spawn --host --directory="$HOME" --env=TP_BIN="$bin" --env=TP_ARGS="--savedir=$HOME/.cache/tuxpaint-test" \
  --env=TP_SCALE="$scale" --env=TP_BUTTON=$((48 * scale)) \
  python3 - $((800 * scale))x$((600 * scale)) click:48,16 wait:1 \
  tool:15 wait:1 shot:q1-quit click:205,302 wait:1 \
  tool:12 wait:1 shot:o1-open click:170,75 shot:o2-selected \
  click:168,448 wait:1 shot:s1-slides click:680,448 wait:1 shot:s2-back click:680,448 wait:1 \
  tool:11 wait:2 shot:n1-new click:680,448 wait:1 \
  click:772,496 wait:1 shot:c1-picker click:525,335 wait:1 \
  tool:12 wait:1 click:168,448 wait:1 click:170,75 click:320,75 shot:s3-selected \
  click:120,448 wait:2 shot:p1-play \
  < "$S/tp_session.py" | tar xf - -C "$out"
flatpak-spawn --host bash -c 'pgrep -a -x tuxpaint && echo "ATTENZIONE: processo rimasto" || true'
ls "$out"
