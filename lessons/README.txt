Tux Paint lessons ("Learn" tool)
================================

The "Learn" tool teaches children to draw a picture on paper, step by step:
for each step it shows what to draw (the new lines are highlighted), reads
the instruction aloud and lets the child go back and forth. Coloring steps
show the area to color and the color to use. At the end the finished picture
is shown, to compare with the one on paper.

Lessons live in three folders, one per difficulty level:

  easy/     3 to 5 steps, only basic shapes (circle, oval, line, triangle)
  medium/   5 to 7 steps
  hard/     7 to 100 steps; may use light guide shapes, erased at the end

Tux Paint looks for them in its data folder (e.g. /usr/share/tuxpaint/lessons)
and in the user's own folder (~/.tuxpaint/lessons/easy, …). Within a level,
lessons are listed by number of steps, then by title.

A fourth folder, custom/, is for the user's own pictures and lessons (usually
~/.tuxpaint/lessons/custom). Tux Paint doesn't ship or install anything
there, and its "Mine" tab only shows when it isn't empty. Besides lessons, it
takes plain pictures, SVG, PNG, JPEG or WebP, with no steps of their own: each
becomes a lesson that copies it with a 3 by 3 grid (look; draw a light grid;
copy box by box; erase the grid; color). For two files with the same name,
SVG wins over PNG, PNG over JPEG and WebP. The title is the file's name ("my_red-car"
becomes "My red car"), or the first block of NAME.txt if there is one with
just the title (and its translations); "#" comment lines there are a good
place for credits. EPS files aren't read: convert them to SVG first.
The Learn dialog's "Add" button copies a picture there, with the NAME.txt
next to it, from the user's Downloads, Pictures or Desktop folder, after
checking that it can be shown (and under another name if its name is taken).


A lesson is two files with the same name
----------------------------------------

  NAME.svg   the finished, colored drawing, split into one group per step
  NAME.txt   the title and the steps, with their instructions


NAME.svg
--------

- Size: width="640" height="480" viewBox="0 0 640 480". No background: the
  paper is white. Keep everything at least 20 units from the edges.
- Every step is a top-level group with an id: <g id="body">…</g>. Ids use
  lowercase letters, digits and hyphens. Each group belongs to exactly one
  step; there is nothing outside the groups (except <title>, <desc>,
  <defs>).
- "draw" groups (lines to draw with a pencil or a marker): stroke="#2b2b2b",
  stroke-width="6", stroke-linecap="round", stroke-linejoin="round",
  fill="none". Small solid details a child fills in with the pencil (pupils,
  a nose) may be filled with #2b2b2b.
- "guide" groups (light helper shapes, drawn softly and erased later):
  stroke="#8a9bb0", stroke-width="3", stroke-dasharray="10 8", fill="none".
- "color" groups: flat fill with ONE color, no stroke. The fill goes under
  the lines: reuse the outline's own geometry, so that no white gap is left.
  Colors are always drawn below the lines, whatever their order in the file.
  Use crayon-like colors, for example:

    yellow #ffd93b    orange #ff9f1c    red #e63946      pink #ff8fab
    purple #9b5de5    blue #3a86ff      light blue #8ecae6
    green #43aa8b     light green #90d26d                brown #9c6644
    gray #a0a4a8      black #2b2b2b

Simple shapes a child can copy work best: round caps, smooth curves, no
tiny details, no shading, no gradients, no text.


NAME.txt
--------

UTF-8 text. Lines starting with "#" are comments. Blocks are separated by
an empty line.

The first block is the title: the English title on the first line, then
one line per translation, "LANG.utf8=Title" (LANG as in Tux Paint's locale
names, e.g. "it", "pt_BR"), as in the stamps' description files.

Every other block is a step. Its first line says what kind of step it is
and which group of the SVG it shows:

  draw ID     draw the lines of group ID
  guide ID    draw the light helper shape of group ID
  color ID    color the area of group ID (one color)
  erase       erase all the guide shapes drawn so far (no group)

Then the instruction in English, on one line, and its translations, one per
line, "LANG.utf8=Instruction". Keep instructions short (one or two simple
sentences, at most about 110 characters): they are shown next to Tux and
read aloud. Talk to the child ("Draw…", "Color…"), name simple shapes
("a circle", "an oval", "a line like a smile", "a letter U") and places ("in
the middle", "on top", "on the left").

Example (easy/sun.txt):

  # Tux Paint lesson: steps for sun.svg
  Sun
  it.utf8=Sole

  draw circle
  Draw a big circle in the middle of the paper.
  it.utf8=Disegna un grande cerchio in mezzo al foglio.

  color sun-yellow
  Color the sun yellow.
  it.utf8=Colora il sole di giallo.


How the steps are shown
-----------------------

At step N, Tux Paint shows the groups of steps 1 to N: colors first, then
guide shapes (unless an "erase" step came after them), then lines. The
group of step N is the new one: lines and guides are shown in the highlight
color and blink for a moment; a color area blinks, and a crayon of its color
is shown next to the picture. An "erase" step shows the guide shapes
fading away.

Before the first step the finished picture is shown, with the title; after
the last one, the finished picture again.


Checking a lesson
-----------------

devtools/content/lesson_preview.py (Python 3 with Pillow; it uses librsvg
and cairo directly, as Tux Paint does) checks a lesson's files against these
rules and draws a sheet with every step as Tux Paint shows it:

  python3 devtools/content/lesson_preview.py --out /tmp/preview lessons/easy/sun.txt

devtools/content/lessonkit/check_areas.py checks the colors: it reports any
area between the lines that is partly white, or that has two colors with no
line between them:

  python3 devtools/content/lessonkit/check_areas.py lessons/hard/owl.txt

The hard lessons biplane, garden-chair, gumball-machine, gummy-bears,
halloween-cat, horse-foal, knitting-friends, nest-chicks, two-foxes and
vulture are written in Python with devtools/content/lessonkit/, which also
fills their colors from the lines. To change them, change hard_a.py or
hard_b.py there and run make_hard.py, rather than editing their SVG.
