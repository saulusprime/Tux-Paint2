# Prove automatiche dell'interfaccia

Script per pilotare Tux Paint, catturarne la finestra e confrontare le
catture pixel per pixel. Si lanciano dalla shell di VS Code (sandbox
Flatpak): Tux Paint gira sull'host, sotto XWayland.

Contesto, regole e insidie: `HANDOFF.md` §5bis.

**Prima di lanciarli**, chiedere all'utente di non usare mouse, rotella e
tastiera: le finestre di prova compaiono sul suo schermo.

## Requisiti sull'host

`xwininfo`, `xprop`, `xwd`, `ffmpeg`, `python3` con PIL, `libXtst.so.6`,
`libXfixes.so.3`.

## File

| File | Cosa fa |
|------|---------|
| `tp_session.py` | Il motore: avvia Tux Paint, esegue le azioni, scrive su stdout un tar di PNG |
| `regress.sh` | Una cattura per strumento della schermata principale |
| `dialogs.sh` | Tutti i dialoghi (uscita, Apri, presentazione, Nuovo, selettore colore) |
| `erase.sh` | Richiesta "Cancella" di Apri, con Cestino e cartella di salvataggio di prova |
| `compare.py` | Confronta due cartelle di catture |
| `segv_backtrace.c` | Pila delle chiamate ai crash, da caricare con `LD_PRELOAD` |
| `nodlclose.c` | Rende nullo `dlclose()`, da caricare con `LD_PRELOAD`: separa nei rapporti di AddressSanitizer la memoria dei plugin |

## Esempi

Variabili usate negli esempi:

```sh
D=/home/paolo/Sviluppo/tuxpaint/devtools/ui-test
OUT=/tmp/…/scratchpad/prova                 # cartella nuova, nel sandbox
B=$HOME/.cache/tuxpaint-baseline/tuxpaint   # binario di riferimento
N=$HOME/.local/bin/tuxpaint                 # binario installato
```

Il binario di riferimento usa i suoi plugin, in
`~/.cache/tuxpaint-baseline/plugins-0922`: quelli installati hanno
l'API del fork (0x00010003), che lui rifiuta. Per ricompilarlo:

```sh
flatpak-spawn --host bash -c 'cd ~/.cache/tuxpaint-baseline &&
  make PREFIX=$HOME/.local MAGIC_PREFIX=$HOME/.cache/tuxpaint-baseline/plugins-0922 \
    tuxpaint magic-plugins && cp magic/*.so plugins-0922/'
```

Invariante a 800×600, schermata principale e dialoghi:

```sh
$D/regress.sh $OUT/base800 $B 800x600 48
$D/regress.sh $OUT/new800  $N 800x600 48
$D/dialogs.sh $OUT/dlg-base800 $B
$D/dialogs.sh $OUT/dlg-new800  $N
cd $OUT && tar cf - base800 new800 | (cd $HOME && flatpak-spawn --host \
  --directory=$HOME python3 -c "$(cat $D/compare.py)" base800 new800)
```

A scala 2 (finestra 1600×1200, pulsanti da 96 px); per i dialoghi la scala
va come terzo argomento:

```sh
$D/regress.sh $OUT/new1600 $N 1600x1200 96
$D/dialogs.sh $OUT/dlg-new1600 $N 2
```

Richiesta "Cancella": disegna un punto, salva, apre, chiede di cancellare
il primo disegno e risponde "No". Poi stampa le dimensioni delle miniature
salvate e controlla che il Cestino di prova sia vuoto:

```sh
$D/erase.sh $OUT/erase800 $N
$D/erase.sh $OUT/erase1600 $N 2
```

Schermo intero: con dimensione `-` lo script non passa `--windowed` né
`--windowsize`, e le opzioni vengono da `TP_ARGS`. A schermo intero la
finestra copre tutto lo schermo:

```sh
cd $HOME && flatpak-spawn --host --directory=$HOME \
  --env=TP_BUTTON=128 --env=TP_START_WAIT=7 --env=TP_ARGS=--fullscreen=native \
  python3 - - info:avvio shot:pieno key:Alt_L+Return wait:2 info:dopo \
  < $D/tp_session.py | tar xf - -C $OUT
```

Sessione libera:

```sh
cd $HOME && flatpak-spawn --host --directory=$HOME \
  --env=TP_BUTTON=96 --env=TP_SCALE=2 \
  python3 - 1600x1200 move:48,16 wait:1 click:48,16 tool:7 shot:magie \
  < $D/tp_session.py | tar xf - -C $OUT
```

Memoria, con AddressSanitizer: una build a parte in un worktree, poi una
sessione che chiude Tux Paint col pulsante Esci (con SIGKILL non c'è
rapporto). Sì della richiesta d'uscita a (205, 250) a 800×600:

```sh
flatpak-spawn --host bash -c 'cd ~/Sviluppo/tuxpaint &&
  git worktree add --detach ~/.cache/tuxpaint-asan HEAD; cd ~/.cache/tuxpaint-asan &&
  make -j4 PREFIX=$HOME/.local OPTFLAGS="-O1 -g -fsanitize=address -fno-omit-frame-pointer" tuxpaint'
cd $HOME && flatpak-spawn --host --directory=$HOME --env=TP_BIN=$HOME/.cache/tuxpaint-asan/tuxpaint \
  --env=TP_START_WAIT=15 --env=TP_ARGS=--savedir=$HOME/.cache/tuxpaint-test \
  --env=TP_WRAP="env ASAN_OPTIONS=detect_leaks=1:log_path=$HOME/.cache/tp-asan/run" \
  python3 - 800x600 move:48,16 wait:2 click:48,16 wait:2 tool:4 wait:8 \
  tool:15 wait:3 click:205,250 wait:15 < $D/tp_session.py > /dev/null
```

Con `LD_PRELOAD=$HOME/.cache/nodlclose.so` in `TP_WRAP` (compilata da
`nodlclose.c`) aggiungere anche `verify_asan_link_order=0` ad
`ASAN_OPTIONS`. Per pile complete anche nelle librerie senza frame
pointer: `fast_unwind_on_malloc=0:malloc_context_size=12`, molto più lento
(dare più tempo prima di Esci e dopo Sì).

Cestino: `erase.sh OUT BIN [SCALA [RISPOSTA]]` risponde "yes" se richiesto;
`TP_TEST_XDG=/tmp/prova-cestino` mette il Cestino di prova su un altro
filesystem, così lo spostamento deve copiare.

Senza finestra: con `SDL_VIDEODRIVER=dummy` Tux Paint parte senza aprire
nulla sullo schermo. Basta per controllare che l'avvio non vada in crash
(`timeout -s KILL 20 …`: codice 137 se era ancora vivo, 139 se è andato in
crash), non per cliccare.

## Azioni di `tp_session.py`

| Azione | Effetto |
|--------|---------|
| `click:X,Y` | clic sinistro (coordinate moltiplicate per `TP_SCALE`) |
| `tool:N` | clic sullo strumento N (dimensione da `TP_BUTTON`) |
| `move:X,Y` | sposta il puntatore |
| `key:K1+K2[:S]` | preme i tasti X indicati, in ordine (es. `Alt_L+Return`), li tiene premuti S secondi (default 0,1) e li rilascia al contrario |
| `info:NOME` | scrive su stderr posizione, dimensione e stato della finestra |
| `drag:X1,Y1,X2,Y2` | trascina (poco affidabile se l'utente usa il mouse) |
| `wait:S` | attende S secondi |
| `shot:NOME` | cattura la finestra in `NOME.png` |
| `cursor:NOME` | salva il cursore attuale in `NOME.png` |

## Variabili di `tp_session.py`

| Variabile | Effetto |
|-----------|---------|
| `TP_BIN` | binario da avviare (default `~/.local/bin/tuxpaint`) |
| `TP_BUTTON` | dimensione dei pulsanti, per `tool:N` (default 48) |
| `TP_SCALE` | moltiplica le coordinate di `click`, `move`, `drag` |
| `TP_ARGS` | opzioni aggiuntive per Tux Paint (es. `--savedir=…`) |
| `TP_START_WAIT` | attesa iniziale in secondi (default 5) |
| `TP_LOG` | file sull'host dove scrivere l'output di Tux Paint |
| `TP_WRAP` | comando con cui avviarlo (es. `stdbuf -oL -eL`, `env VAR=…`) |
| `TP_SOUND` | se impostata: audio attivo, col driver SDL `dummy` (muto) |

Sicurezza: lo script usa solo la finestra del processo che ha avviato, la
porta in primo piano e non clicca mai se sotto il puntatore c'è un'altra
finestra. Allo stesso modo non preme tasti se il focus della tastiera non è
in quella finestra. In entrambi i casi scrive "STOP" e si ferma.
