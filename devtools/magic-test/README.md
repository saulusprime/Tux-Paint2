# Prova dei plugin Magia senza interfaccia

`magic_run.c` carica un plugin Magia (`magic/*.so`) fuori da Tux Paint, gli
dà come tela un'immagine e ne salva il risultato. Le funzioni dell'API
(`getpixel`, `putpixel`, `line`, `touched`, `rgbtohsv`, …) sono copie di
quelle di Tux Paint, con le stesse regole: `last` è il disegno com'era
prima del tratto, `touched` si azzera a ogni clic, `button_down` vale 1 tra
clic e rilascio. Niente audio. Serve per vedere che cosa fa uno strumento
senza aprire finestre, e per far girare i plugin sotto AddressSanitizer.

## Compilazione (sull'host)

Dopo una build normale, che genera `src/tp_magic_api.h`:

```sh
cc -g -O1 -Wall -W $(pkg-config --cflags sdl) -Isrc \
  devtools/magic-test/magic_run.c src/rgblinear.c -o ~/.cache/tp-magic/magic_run \
  $(pkg-config --libs sdl) -lSDL_image -Wl,--no-as-needed -lSDL_mixer \
  -Wl,--as-needed -ldl -lm
```

SDL_mixer va collegata anche se non si usa: i plugin ne chiamano le
funzioni (`Mix_LoadWAV`), che di solito trovano in Tux Paint. Con
`--as-needed`, che su Debian è attivo, il linker la toglierebbe.

## Uso

```sh
magic_run PLUGIN.so STRUMENTO paint|full ENTRATA.png USCITA.bmp \
  [color=R,G,B] [click=X,Y] [drag=X,Y,X,Y...] [seed=N]
```

- `STRUMENTO`: il numero dello strumento nel plugin (0 il primo).
- `full`: un clic nella modalità a tutta immagine (al primo `click=`, o al
  centro). `paint`: ogni `click=` è un clic e un rilascio, ogni `drag=` un
  clic nel primo punto, un trascinamento per gli altri e un rilascio.
- `color=`: il colore scelto, per gli strumenti che lo usano (di default
  nero).
- Immagini e suoni del plugin vengono da `$DATA` (di default
  `~/.local/share/tuxpaint/`, cioè quelli installati).
- Stampa nome e descrizione dello strumento nella modalità scelta.
- `rand()` parte sempre dallo stesso seme (1, o `seed=`), quindi il
  risultato si ripete.

Esempio, Punto croce a tutta immagine e un tratto di Schiuma rossa:

```sh
cd ~/.cache/tp-magic
./magic_run ~/Sviluppo/tuxpaint/magic/crossstitch.so 0 full pic.png out.bmp
./magic_run ~/Sviluppo/tuxpaint/magic/foam.so 0 paint pic.png out.bmp \
  color=255,40,40 drag=60,300,200,330,300,360
```

## Con AddressSanitizer

Compilare `magic_run` e i plugin da provare con
`-g -O1 -fsanitize=address -fno-omit-frame-pointer` (per un plugin:
`cc FLAGS -fno-common -W -Wall $(pkg-config --cflags sdl) -Isrc -shared
-fpic -o PLUGIN.so magic/src/PLUGIN.c -lm`). Un errore o un leak fanno
uscire con un rapporto su stderr. Conviene provare anche una tela con lati
"strani" (per esempio 1003×701) e clic negli angoli.
