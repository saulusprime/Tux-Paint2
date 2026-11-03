#!/usr/bin/env python3
"""Rebuild src/tuxpaint.desktop from src/tuxpaint.desktop.in and the .po files.

usage: devtools/po/update-desktop.py [PO_DIR [OUTPUT]]

Does what "intltool-merge -d" does in src/Makefile (intltool isn't
installed on Debian 13 by default): each "_Key=text" line becomes
"Key=text", followed by "Key[LANG]=translation" for every catalog that has
a translation of that text (not fuzzy), languages in byte order. Needs
msgcat (gettext). PO_DIR defaults to src/po, OUTPUT to src/tuxpaint.desktop
("-" for standard output).
"""
import glob
import os
import subprocess
import sys

SRC = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "src")
PO_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SRC, "po")
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(SRC, "tuxpaint.desktop")


def unquote(s):
    s = s.strip()[1:-1]
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(s[i + 1], s[i + 1]))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def translations(path):
    text = subprocess.run(["msgcat", "--no-wrap", path], capture_output=True,
                          text=True, check=True).stdout
    found = {}
    for block in text.split("\n\n"):
        fuzzy, msgid, msgstr = False, None, None
        for line in block.splitlines():
            if line.startswith("#,") and "fuzzy" in line:
                fuzzy = True
            elif line.startswith("msgid "):
                msgid = unquote(line[6:])
            elif line.startswith("msgstr "):
                msgstr = unquote(line[7:])
        if msgid and msgstr and not fuzzy:
            found[msgid] = msgstr
    return found


catalogs = {os.path.basename(p)[:-3]: translations(p)
            for p in glob.glob(os.path.join(PO_DIR, "*.po"))}

out = []
with open(os.path.join(SRC, "tuxpaint.desktop.in"), encoding="utf-8") as f:
    for line in f.read().splitlines():
        if line.startswith("_") and "=" in line:
            key, text = line[1:].split("=", 1)
            out.append(f"{key}={text}")
            for lang in sorted(catalogs):
                if text in catalogs[lang]:
                    out.append(f"{key}[{lang}]={catalogs[lang][text]}")
        else:
            out.append(line)

result = "\n".join(out) + "\n"
if OUTPUT == "-":
    sys.stdout.write(result)
else:
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(result)
