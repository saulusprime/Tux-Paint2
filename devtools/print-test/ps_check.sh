#!/bin/bash
# usage: ps_check.sh [OUTDIR]
# Checks that PostScript printing (src/postscript_print.c) centers the
# picture on the page, rotated or not, on A4 and Letter, and that an unknown
# paper size falls back to the default instead of crashing; then prints
# through commands that succeed and fail, which must be reported as such.
# OBJ=DIR uses the objects of another tree (e.g. the baseline). Needs a built
# tree (obj/postscript_print.o, obj/pixels.o), ghostscript and python3 with
# PIL. Runs on the host (from the VS Code sandbox it re-runs itself there).
if [ -e /.flatpak-info ]; then
  exec flatpak-spawn --host --directory="$HOME" ${OBJ:+--env=OBJ="$OBJ"} bash "$(realpath "$0")" "$@"
fi
T=$(realpath "$(dirname "$0")/../..")
out=${1:-$(mktemp -d)}
mkdir -p "$out"
gcc -o "$out/ps_check" "$T/devtools/print-test/ps_check.c" -I"$T/src" \
  $(sdl-config --cflags) "${OBJ:-$T/obj}/postscript_print.o" "${OBJ:-$T/obj}/pixels.o" \
  $(sdl-config --libs) -lpaper -lm || exit 1
status=0
for c in "1216 992 a4" "992 1216 a4" "800 600 letter" "1600 400 a4" "608 472 foo"; do
  set -- $c
  name="$1x$2-$3"
  "$out/ps_check" "$1" "$2" "$out/$name.ps" "$3" 2> "$out/$name.err" || { echo "$name: failed"; status=1; continue; }
  gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=png16m -r72 -sOutputFile="$out/$name.png" "$out/$name.ps"
  python3 - "$out/$name.png" "$name" "$(cat "$out/$name.err")" <<'PY' || status=1
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
w, h = im.size
red = Image.eval(im, lambda v: 255 if v > 128 else 0).split()
mask = Image.eval(Image.merge("RGB", red).convert("L"), lambda v: 255 if v == 76 else 0)
l, t, r, b = mask.getbbox()
margins = (l, w - r, t, h - b)
ok = abs(margins[0] - margins[1]) <= 1 and abs(margins[2] - margins[3]) <= 1
print("%-18s page %dx%d pt, margins left %d right %d top %d bottom %d: %s %s"
      % (sys.argv[2], w, h, *margins, "centered" if ok else "NOT CENTERED", sys.argv[3]))
sys.exit(0 if ok else 1)
PY
done
for c in "cat>/dev/null:0" "gzip>/dev/null:0" "false:1" "head -c 10 >/dev/null; exit 1:1"; do
  cmd=${c%:*}; want=${c##*:}
  "$out/ps_check" 608 472 "|$cmd" a4; got=$?
  [ "$got" = "$want" ] && r=ok || { r="WRONG"; status=1; }
  printf "%-36s reported %s, expected %s: %s\n" "print to \"$cmd\"" \
    "$([ $got = 0 ] && echo success || echo failure)" "$([ $want = 0 ] && echo success || echo failure)" "$r"
done
exit $status
