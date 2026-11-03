#!/bin/bash
# Merge src/po/tuxpaint.pot into the translations, filling in what's missing
# from those of today's Tux Paint.
#
# Usage: devtools/po/fill-from-upstream.sh UPSTREAM_PO_DIR [LANG...]
#
# UPSTREAM_PO_DIR is the src/po folder of a checkout of today's Tux Paint
# (https://git.code.sf.net/p/tuxpaint/tuxpaint). Like
# devtools/po/update-po.sh, this merges the template into LANG.po (every
# language, if none is given), but with the translated messages of
# UPSTREAM_PO_DIR/LANG.po as a compendium: a message that has no
# translation here, and has one there for the same msgid, gets that one.
# Translations already here are kept.
#
# A few messages of this fork say "your entire picture" where today's Tux
# Paint says "the entire picture"; those are taken too.
#
# Run devtools/po/update-po.sh first, so that the template is current.

set -e

up="$(realpath "$1")"
shift

cd "$(dirname "$(realpath "$0")")/../../src/po"

if [ $# -eq 0 ]; then
  set -- $(ls *.po | sed 's/\.po$//')
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

for lang in "$@"; do
  echo -n "$lang: "
  if [ -f "$up/$lang.po" ]; then
    msgattrib --translated --no-fuzzy --no-obsolete --no-wrap \
      "$up/$lang.po" |
      sed -e 's/^msgid "Click to make the entire picture blocky\."$/msgid "Click to make your entire picture blocky."/' \
          -e 's/^msgid "Click to turn the entire picture into a chalk drawing\."$/msgid "Click to turn your entire picture into a chalk drawing."/' \
          -e 's/^msgid "Click to turn the entire picture into a cartoon\."$/msgid "Click to turn your entire picture into a cartoon."/' \
          -e 's/^msgid "Click to emboss the entire picture\."$/msgid "Click to emboss your entire picture."/' \
      > "$tmp/compendium.po"
    msgmerge --quiet --update --previous --backup=none \
      --compendium="$tmp/compendium.po" "$lang.po" tuxpaint.pot
  else
    echo -n "(not in $up) "
    msgmerge --quiet --update --previous --backup=none "$lang.po" tuxpaint.pot
  fi
  msgfmt --check --statistics -o /dev/null "$lang.po"
done
