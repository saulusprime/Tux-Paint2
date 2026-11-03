#!/bin/bash
# Regenerate src/po/tuxpaint.pot and merge it into some translations.
#
# Usage: devtools/po/update-po.sh [LANG...]     (e.g. "it", "it de")
#
# Like src/po/update-po.sh, but needs only the gettext tools (no intltool,
# which Debian 13 doesn't install by default), and merges only the
# languages given instead of all of them. It doesn't rebuild
# src/tuxpaint.desktop, whose translations come from the .po files:
# devtools/po/update-desktop.py does.

set -e

cd "$(dirname "$(realpath "$0")")/../../src/po"

cp POTFILES.in.in POTFILES.in
ls ../../magic/src/*.c | cut -b 4- >> POTFILES.in

# As intltool does, a .desktop.in becomes a .h file with one N_() for each
# translatable "_Key=" line, so references read "../tuxpaint.desktop.in.h"
files=()
while read -r f; do
  case "$f" in
    \[*|"") ;;
    *.desktop.in)
      awk '/^_/ { sub(/^[^=]*=/, ""); gsub(/"/, "\\\"");
                  printf "char *s = N_(\"%s\");\n", $0 }' "../$f" > "../$f.h"
      files+=("../$f.h") ;;
    *) files+=("../$f") ;;
  esac
done < POTFILES.in

trap 'rm -f ../*.desktop.in.h tuxpaint.pot.tmp' EXIT
xgettext --from-code=UTF-8 --add-comments --keyword=_ --keyword=N_ \
  --language=C -o tuxpaint.pot.tmp "${files[@]}"
msguniq tuxpaint.pot.tmp > tuxpaint.pot

for lang in "$@"; do
  echo -n "$lang: "
  msgmerge --update --previous --backup=none "$lang.po" tuxpaint.pot
  msgfmt --check --statistics -o /dev/null "$lang.po"
done
