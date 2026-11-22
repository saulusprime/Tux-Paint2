# Prova delle lezioni senza interfaccia

`lesson_frames.c` disegna, con il `src/lessons.c` di Tux Paint, quello che lo
strumento Impara mostra delle lezioni di una cartella, in file BMP: le
miniature del selettore, l'immagine finita prima del primo passo e dopo
l'ultimo, ogni passo ad animazione finita e al 10% dell'animazione, le
schede dei livelli e le cornici delle miniature. Niente finestre, niente
Tux Paint: serve per vedere il disegno in C (cairo e librsvg) e per farlo
girare sotto AddressSanitizer.

Per controllare i file di una lezione (le regole di `lessons/README.txt`) e
vederne i passi uno accanto all'altro c'è invece
`devtools/content/lesson_preview.py`, in Python.

## Compilazione ed esempio

```sh
# (senza i pacchetti -dev installati: le librerie di devtools/sysroot)
eval "$(devtools/sysroot/sysroot.sh env | head -1)"

cc -g -O1 -W -Wall -fsanitize=address -Isrc \
  $(pkg-config --cflags sdl librsvg-2.0 cairo) \
  -o ~/.cache/lesson_frames devtools/lesson-test/lesson_frames.c src/lessons.c \
  $(pkg-config --libs sdl librsvg-2.0 cairo) -lSDL_image -lm
mkdir -p ~/.cache/lesson-frames
~/.cache/lesson_frames lessons it ~/.cache/lesson-frames 608 424
```

Argomenti: la cartella delle lezioni (con `easy/`, `medium/`, `hard/`,
`custom/`), la lingua dei testi, la cartella di uscita e, facoltative,
larghezza e altezza dell'area del lettore (608×424 è quella a 800×600).
Stampa titoli e passi nella lingua scelta.
