#!/bin/bash
# usage: regress.sh OUTDIR BINARY WINDOWSIZE BUTTONSIZE
# Standard main-screen capture sequence: one shot per tool.
# Run from the VS Code Flatpak sandbox: Tux Paint is driven on the host
# (X11/XWayland, needs xwininfo, xwd, ffmpeg and libXtst there).
S=$(dirname "$(realpath "$0")")
out=$1; bin=$2; size=$3; button=$4
mkdir -p "$out" && rm -f "$out"/*.png
# TP_ARGS (extra Tux Paint options) and TP_SOUND are passed on if set
cd "$HOME" && flatpak-spawn --host --directory="$HOME" --env=TP_BIN="$bin" --env=TP_BUTTON="$button" \
  --env=TP_ARGS="$TP_ARGS" --env=TP_SOUND="$TP_SOUND" \
  python3 - "$size" move:$((button)),$((button / 3)) wait:1 click:$((button)),$((button / 3)) wait:1 shot:00-brush \
  tool:1 shot:01-stamp tool:2 shot:02-lines tool:3 shot:03-shapes \
  tool:4 wait:15 shot:04-text tool:5 wait:1 shot:05-label tool:7 shot:07-magic tool:10 shot:10-eraser \
  < "$S/tp_session.py" | tar xf - -C "$out"
flatpak-spawn --host bash -c 'pgrep -a -x tuxpaint && echo "ATTENZIONE: processo rimasto" || true'
ls "$out"
