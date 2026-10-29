"""Run on the host: compare two sets of PNGs read from a tar on stdin.

usage: tar cf - DIR_A DIR_B | flatpak-spawn --host python3 -c "$(cat compare.py)" DIR_A DIR_B
Prints, for each image, the number of differing pixels and their bounding box.
"""
import io, sys, tarfile
from PIL import Image, ImageChops

a, b = sys.argv[1], sys.argv[2]
files = {}
with tarfile.open(fileobj=sys.stdin.buffer, mode="r|") as t:
    for m in t:
        if m.isfile() and m.name.endswith(".png"):
            files[m.name] = Image.open(io.BytesIO(t.extractfile(m).read())).convert("RGB")

for name in sorted(n for n in files if n.startswith(a + "/")):
    other = b + name[len(a):]
    if other not in files:
        print("%-16s missing in %s" % (name, b))
        continue
    ia, ib = files[name], files[other]
    if ia.size != ib.size:
        print("%-16s size %s vs %s" % (name[len(a) + 1:], ia.size, ib.size))
        continue
    diff = ImageChops.difference(ia, ib)
    bbox = diff.getbbox()
    n = sum(1 for p in diff.getdata() if p != (0, 0, 0))
    print("%-16s %s" % (name[len(a) + 1:], "identical" if bbox is None else "%d px differ, bbox %s" % (n, bbox)))
