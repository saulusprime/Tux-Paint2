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
| `compare.py` | Confronta due cartelle di catture |
| `segv_backtrace.c` | Pila delle chiamate ai crash, da caricare con `LD_PRELOAD` |

## Esempi

Variabili usate negli esempi:

```sh
D=/home/paolo/Sviluppo/tuxpaint/devtools/ui-test
OUT=/tmp/…/scratchpad/prova                 # cartella nuova, nel sandbox
B=$HOME/.cache/tuxpaint-baseline/tuxpaint   # binario di riferimento
N=$HOME/.local/bin/tuxpaint                 # binario installato
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

Sessione libera:

```sh
cd $HOME && flatpak-spawn --host --directory=$HOME \
  --env=TP_BUTTON=96 --env=TP_SCALE=2 \
  python3 - 1600x1200 move:48,16 wait:1 click:48,16 tool:7 shot:magie \
  < $D/tp_session.py | tar xf - -C $OUT
```

## Azioni di `tp_session.py`

| Azione | Effetto |
|--------|---------|
| `click:X,Y` | clic sinistro (coordinate moltiplicate per `TP_SCALE`) |
| `tool:N` | clic sullo strumento N (dimensione da `TP_BUTTON`) |
| `move:X,Y` | sposta il puntatore |
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
finestra. In quel caso scrive "STOP" e si ferma.
