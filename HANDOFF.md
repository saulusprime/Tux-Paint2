# HANDOFF — Tux Paint (fork Lliurex)

Documento di passaggio di consegne: chi riprende il lavoro (persona o agente)
parte da qui. Contiene lo stato attuale del progetto e il **diario completo**
delle attività, in ordine cronologico.

Workflow dei file di progetto:

| File         | Contenuto                                                        |
|--------------|------------------------------------------------------------------|
| `HANDOFF.md` | Stato attuale, contesto, diario di bordo (si aggiunge in fondo)  |
| `TODO.md`    | Idee, feature e attività da fare, con priorità                   |
| `ASIS.md`    | Attività completate, spostate da `TODO.md` quando chiuse         |

Regola: quando un'attività di `TODO.md` è conclusa, si **sposta** (non si copia)
in `ASIS.md` con data ed esito, e si aggiunge una voce al diario qui sotto.

---

## 0. Come riprendere

Per chi riparte, anche dopo una pausa o una compressione del contesto:

1. Leggere questo file fino alla §6. Il diario (§7) serve solo per i
   dettagli. Poi [TODO.md](TODO.md): l'utente di solito indica una sezione
   o una voce da fare.
2. Controllare il branch: `git branch -v`. Il lavoro nuovo si fa su un
   branch dedicato, **mai direttamente su `master`**. Si committa solo su
   richiesta, si fa push solo su richiesta, sul remote `github` (§1).
3. La shell di VS Code è un sandbox Flatpak: compilazione ed esecuzione
   avvengono **sull'host**. `./dev.sh build|install|run` passa da solo
   all'host (§4); per altri comandi usare
   `flatpak-spawn --host --directory=$HOME bash -c '…'`.
4. Prove dell'interfaccia: script in `devtools/ui-test/` (§5bis).
   **Prima di ogni prova automatica chiedere all'utente di non usare
   mouse, rotella e tastiera per qualche minuto**: le finestre di prova
   compaiono sul suo schermo e ogni interferenza sporca le catture. A
   800×600 tutto deve restare identico al pixel al binario di
   riferimento.
5. A fine attività: spostare la voce da TODO ad ASIS con data ed esito,
   aggiungere una voce di diario qui (§7) e aggiornare §1 e §6 se
   cambiano.
6. Lingua: l'utente scrive in italiano; i file di progetto sono in
   italiano. Codice, commenti e messaggi di commit sono in inglese, come il
   resto del sorgente.

## 1. Stato attuale (al 2026-11-03)

- **Progetto**: Tux Paint, programma di disegno per bambini (3+ anni), GPL v2.
- **Versione del codice**: 0.9.22 (upstream del 5 agosto 2014),
  `MAGIC_API_VERSION 0x00010003` dal 2026-11-01: la 0x00000003 della
  0.9.22 più `load_icon()` del fork, che accetta anche i plugin 0x00000003
  (vedi [Makefile](Makefile) e §5bis).
- **Origine del repository**: fork di LliureX, `origin` =
  `https://github.com/lliurex/tuxpaint.git`. Il commit iniziale
  (`5550718 Ported from Ubuntu`, jrpelegrina, 2018-10-16) importa il
  sorgente 0.9.22 così come pacchettizzato in Ubuntu.
- **Repository dell'utente**: remote `github` =
  `git@github.com:saulusprime/Tux-Paint2.git` (pubblico,
  `https://github.com/saulusprime/Tux-Paint2`), via SSH con la chiave
  dell'utente. Dal 2026-11-01 ci sono tutti i branch, ognuno collegato al
  suo (`git push` dal branch basta); `master` è il predefinito. `origin`
  resta LliureX, solo da leggere.
- **Decisioni prese** (2026-10-29):
  - **Strategia**: si resta sulla **0.9.22 con SDL 1.2** (tramite
    sdl12-compat) e la si corregge. Niente riallineamento all'upstream né
    porting a SDL2, per ora.
  - **Obiettivo**: **sperimentazione personale**. Target solo Linux;
    packaging, distribuzione e altre piattaforme non sono priorità.
- **Branch** (tutti pubblicati su `github`, niente su `origin`):

| Branch | Commit | Contenuto |
|--------|--------|-----------|
| `content/l10n-more` | ultimo commit | **branch attivo**: le tre voci rimaste di "Contenuti e localizzazione" (`79764ea`…`8783ffa`) e file di progetto. Parte da `master`. **Da unire in `master`**, dopo una prova a mano, con avanzamento rapido fino a qui |
| `master` | `ab1c9b8` | tutto fino a "UI scalabile con la finestra" e l'utente tra i contributori: avanzamento rapido del 2026-11-01 a `feature/tools`, a `feature/dialog-resize`, poi a `docs/authors` |
| `docs/authors` | come `master` | Paolo Pierno tra i contributori (`docs/AUTHORS.txt`, intestazione di `crossstitch.c`); già unito in `master` |
| `feature/dialog-resize` | `fc88915` | i dialoghi si rifanno alla nuova dimensione (`6bfe48f`, `41af788`) e file di progetto; già unito in `master` |
| `feature/more-svg-icons` | `922b762` | `load_icon()` nell'API dei plugin, la sua versione 0x00010003, icone SVG per 39 magie e 10 immagini dell'interfaccia (`c7414af`…`922b762`); già unito in `master` |
| `feature/tools`, `feature/svg-icons`, `feature/resizable`, `content/l10n`, `quality/warnings`, `quality/fixme`, `feature/fullscreen` | | già uniti in `master` |
| `fix/erase-prompt-thumbnail` | come `master` | già unito in `master` |
| `feature/sharper-icons` | `a3e6464` | già unito in `master` |
| `feature/ui-scaling` | `f0f9036` | già unito in `master` |
| `build/host-debian13` | `ec9ebe3` | già unito in `master` |

- **Identità git**: `Paolo <lymphalab@outlook.it>`, configurata solo nel
  repository (`.git/config`).
- **Build**: sull'host Debian 13.7 con GCC 14.2; 0 errori e, dal
  2026-10-31, **0 warning** (erano 96), anche con AddressSanitizer a
  `-O1`. Un warning nuovo è un segnale da guardare.
- **Installato in `~/.local`**: la build di `content/l10n-more`, tutto
  funzionante, compresi Testo ed Etichetta, con la raccolta completa dei
  timbri (`./dev.sh stamps`, 957 timbri). Lanciatore nel menu, con la
  voce "Schermo intero" nel menu dell'icona (clic destro); dati utente in
  `~/.tuxpaint/`.
- **Modifiche rispetto a 0.9.22**:

| Area | Commit | Cosa |
|------|--------|------|
| Build con GCC 14 | `b92a7d1` | loader con `const char *` (`load_kpx`, `load_svg`, `myIMG_Load*`); prototipi di `show_version`/`show_usage` in `src/parse.h`; `-lm` nel Makefile; `.gitignore` |
| Strumenti di sviluppo | `93fc7df`, poi altri | `dev.sh` (§4); `devtools/ui-test/` (§5bis) |
| UI scalabile | `d346e60`, `321db8b`, `0c7bcf9` | schermata principale, dialoghi, cursori, schermata iniziale, tastiera a schermo (§5bis) |
| Font di Testo/Etichetta | `b7021ac` | il processo figlio dei font esce con `_exit(0)`: prima andava in crash in `exit()`, nel gestore di Mesa ereditato, e il genitore scartava i font. Sostituisce il ripiego col thread `6d3f130` |
| Rifiniture UI | `c06ba8f` | opzione `buttonsize`; finestra iniziale più grande sugli schermi grandi; passo del mouse da tastiera proporzionale |
| Icone più nitide | `7cb40aa` | ingrandimento Lanczos-3 delle immagini dell'interfaccia |
| Richiesta "Cancella" | `4f95ada` | miniatura senza la barra nera sopra (difetto della 0.9.22); margine scalato della miniatura salvata |
| Schermo intero | `65874c7`, `3f43e1a` (su `feature/fullscreen`) | Alt+Invio in finestra e a schermo intero; `fullscreen` senza dimensione usa la risoluzione dello schermo; voce "Schermo intero" nel lanciatore; `--fullscreen` senza valore accettato (difetto della 0.9.22) (§5bis) |
| FIXME e difetti trovati | `3ff7788`…`4a09172` (su `quality/fixme`) | plugin Magia senza limite fisso e scaricati all'uscita; font liberati all'uscita; stampa PostScript (carta sconosciuta, esito del comando); `--lang help` dalla tabella; ordinamento senza maiuscole; finestra Nuovo: `frame_heart`, modelli personali; crash con un file senza punto tra i plugin (§5ter, ASIS) |
| Warning e leak | `b80ff08`…`7c3066f` (su `quality/warnings`) | build senza warning; disegni salvati: recupero dello sfondo incorporato e doppio `free`; Cestino (permessi, copia troncata, percorsi); leak a ogni uso (selettore colore, Apri, i tre dialoghi, SVG, Erba, Piega); librsvg senza API deprecate; formato in Mosaic Shaped; joystick e metodi di input (§5ter, ASIS) |
| Contenuti e localizzazione | `0aca7bd`…`bb2b180` (su `content/l10n`) | `./dev.sh stamps` (raccolta completa dei timbri); ultima riga dei `.dat`/`.txt` dei timbri; `it.po` rivisto e modello rigenerato senza intltool; campione di punteggiatura dei font; azione "Schermo intero" nel modello del `.desktop`; sei Starter e modelli SVG per la scuola; manuale ed EXTENDING in italiano (§5quater, ASIS) |
| Ridisegno alla nuova dimensione | `54b36d4`…`7672e81` (su `feature/resizable`) | finestra ridimensionabile; Alt+Invio a schermo intero nitido alla risoluzione dello schermo; disegno, Annulla, Starter ed etichette adattati alla nuova tela; plugin Halftone, Foam e Glass Tile con la tela che cambia; due leak (§5bis, ASIS) |
| Icone SVG | `a34374b`, `b9e7dfb` (su `feature/svg-icons`) | con pulsanti più grandi di 48×48, le icone di strumenti e forme vengono da SVG (§5bis, ASIS) |
| Icone SVG, seconda parte | `c7414af`…`922b762` (su `feature/more-svg-icons`) | `load_icon()` nell'API dei plugin e sua versione 0x00010003; SVG per 39 icone delle magie e 10 dell'interfaccia (§5bis, ASIS) |
| Dialoghi alla nuova dimensione | `6bfe48f`, `41af788` (su `feature/dialog-resize`) | ogni dialogo si rifà quando la finestra cambia o con Alt+Invio; copia del testo di Tux (§5bis, ASIS) |
| Traduzioni, cartina, documentazione | `79764ea`…`8783ffa` (su `content/l10n-more`) | tutti i cataloghi allineati al modello, con i buchi riempiti dalle traduzioni del Tux Paint di oggi; frasi del fork in 52 lingue in più; lanciatore rigenerato dai cataloghi; Starter con la cartina dell'Italia e le regioni; OPTIONS e FAQ in italiano (§5quater, ASIS) |
| Strumenti e magie | `799621f`…`6f79f5d` (su `feature/tools`) | Blocks, Chalk, Cartoon, Emboss e Puzzle a tutta immagine; Punto croce (plugin nuovo); Schiuma colorata; Mezzatinta con un angolo per inchiostro; suoni per Halftone, Puzzle, Color & White; tastiera a schermo con i caratteri di Maiuscolo e AltGr, e i caratteri oltre U+FFFF; etichette lunghe su due righe; rettangolo da aggiornare in 10 plugin; due leak (§5quinquies, ASIS) |

- **Cartelle di supporto in `~/.cache`** (sull'host; al 2026-11-03):
  - `tuxpaint-baseline/`: worktree git con il binario di riferimento
    (`ec9ebe3`, la 0.9.22 che compila) e i suoi plugin in `plugins-0922/`
    (§5bis);
  - `tuxpaint-test/`: cartella di salvataggio delle prove;
    `tuxpaint-test-canon/`, con due disegni, si copia lì prima delle prove
    dei dialoghi;
  - `tuxpaint-test-xdg/`: Cestino di prova;
  - `tuxpaint-test-data/` (con `plugins/README` senza punto e un modello
    magenta) e `tuxpaint-test-data2/` (solo il modello): cartelle dati di
    prova per `--datadir`. Il riferimento va in crash con la prima;
  - `tuxpaint-asan/` (staccato a `41af788`, i dialoghi alla nuova
    dimensione) e `tuxpaint-asan-base/` (`e5a0cdc`, un `master` del
    2026-10-30): worktree con build AddressSanitizer (§5ter), da portare
    al commit da provare; `tp-asan/`, i loro rapporti; `nodlclose.so`,
    compilata da `devtools/ui-test/nodlclose.c`;
  - `tp-magic/`: `magic_run` e le immagini di prova dei plugin
    (§5quinquies);
  - `tp-tools/`: potrace (`bin/`, `lib/`) e gli script di confronto delle
    icone tracciate (§5bis);
  - `tp-map/`: confini Istat (`istat-2026/`) e paesi di Natural Earth
    (`naturalearth/`) per la cartina (§5quater);
  - `tp-upstream/`: i cataloghi `po/` del Tux Paint di oggi e il commit da
    cui vengono (§5quater);
  - `tp-snd/` (spettrogrammi dei suoni sintetizzati) e `tp-idx/` (una
    copia di `onscreen_keyboard.c`): avanzi di lavori chiusi, si possono
    cancellare.

## 2. Mappa del repository

| Percorso | Contenuto |
|----------|-----------|
| [src/](src/) | Sorgente C. Cuore in [src/tuxpaint.c](src/tuxpaint.c) (~24.500 righe, monolitico) più moduli: `fonts.c`, `i18n.c`, `onscreen_keyboard.c`, `postscript_print.c`, `dirwalk.c`, `pixels.c`, `playsound.c`, … |
| [src/po/](src/po/) | 119 traduzioni gettext (inclusi `it.po`, `ca.po`, `ca@valencia.po`), tutte allineate al modello `tuxpaint.pot`, più gli script upstream (servono intltool) |
| [src/tuxpaint.conf](src/tuxpaint.conf) | Configurazione di default installata in `/etc` |
| [magic/src/](magic/src/) | 48 plugin "Magic" (`.so` caricati a runtime), tra cui `crossstitch.c` del fork; API in `src/tp_magic_api.h.in` |
| [data/](data/) | Risorse: 53 pennelli, font, immagini UI, suoni |
| [stamps/](stamps/) | Solo pochi timbri (`cartoon/`); la collezione completa è il pacchetto separato `tuxpaint-stamps`, che si aggiunge con `./dev.sh stamps` (§4) |
| [starters/](starters/) | 64 immagini "Starter" (contorni/cornici da colorare), tra cui `clock.svg`, `school.svg` e la cartina `worldmap_italy.svg` del fork |
| [templates/](templates/) | 23 immagini "Template" (sfondi fotografici), tra cui lavagna e quaderni SVG del fork |
| [osk/](osk/) | Layout della tastiera a schermo (`--onscreen-keyboard`) |
| [im/](im/) | Metodi di input per giapponese, coreano, thai, cinese tradizionale |
| [fonts/](fonts/) | Font specifici per locale (arabo, tibetano, greco, …) |
| [docs/](docs/) | Documentazione upstream (EN + traduzioni), vedi §3 |
| [custom/](custom/) | Hook di personalizzazione (solo macOS/Windows; Linux non implementato) |
| `win32/`, `macosx/`, `haiku/`, `hildon/`, `maemo/`, `visualc/` | Port per altre piattaforme (non rilevanti per Linux) |
| [Makefile](Makefile) | Build system unico, niente autotools |
| [tuxpaint.spec](tuxpaint.spec) | Spec RPM |
| [dev.sh](dev.sh) | *Aggiunto nel fork*: build, installazione in `~/.local` e avvio sull'host (§4) |
| [devtools/ui-test/](devtools/ui-test/) | *Aggiunto nel fork*: prove automatiche dell'interfaccia (`regress.sh`, `dialogs.sh`, `erase.sh`, `compare.py`, `tp_session.py`, `segv_backtrace.c`, `nodlclose.c`), §5bis |
| [devtools/print-test/](devtools/print-test/) | *Aggiunto nel fork*: `ps_check.sh`, verifica della stampa PostScript con Ghostscript (§5ter) |
| [devtools/po/](devtools/po/) | *Aggiunto nel fork*: `update-po.sh` (rigenera il modello delle traduzioni senza intltool), `fill-from-upstream.sh` (allinea i cataloghi e li completa con quelli del Tux Paint di oggi), `update-desktop.py` (rifà `src/tuxpaint.desktop` dai cataloghi) (§5quater) |
| [devtools/content/](devtools/content/) | *Aggiunto nel fork*: `school_svgs.py` (Starter e modelli per la scuola, §5quater), `italy_map.py` (la cartina dell'Italia, dai confini Istat, §5quater), `shape_icons.py` (icone SVG delle forme) e `trace_icons.py` (icone SVG degli strumenti, con potrace) (§5bis), `crossstitch_icon.py` e `magic_sounds.py` (icona di Punto croce e suoni sintetizzati, §5quinquies), `svg_icons.py` (rifà tutte le icone tracciate, §5bis) |
| [devtools/magic-test/](devtools/magic-test/) | *Aggiunto nel fork*: `magic_run.c`, fa girare un plugin Magia su un'immagine, senza interfaccia (§5quinquies) |
| `HANDOFF.md`, `TODO.md`, `ASIS.md` | *Aggiunti nel fork*: file di progetto (vedi in cima a questo file) |

## 3. Documentazione letta

Tutta in [docs/](docs/), formato testo (con versione HTML in `docs/html/`):

- [docs/README.txt](docs/README.txt) — uso del programma, descrizione di tutti gli strumenti.
- [docs/INSTALL.txt](docs/INSTALL.txt) — dipendenze e compilazione.
- [docs/OPTIONS.txt](docs/OPTIONS.txt) — opzioni da riga di comando e `tuxpaint.conf`.
- [docs/EXTENDING.txt](docs/EXTENDING.txt) — come aggiungere pennelli, timbri, starter, template, font.
- [docs/ADVANCED-STAMPS-HOWTO.txt](docs/ADVANCED-STAMPS-HOWTO.txt) — creazione di timbri avanzati.
- [docs/FAQ.txt](docs/FAQ.txt) — problemi noti (stampa, salvataggio, audio, fullscreen).
- [docs/CHANGES.txt](docs/CHANGES.txt) — changelog completo 2002-2014.
- [docs/PNG.txt](docs/PNG.txt), [docs/SVG.txt](docs/SVG.txt) — formati immagine supportati.
- [docs/it/](docs/it/) — traduzione italiana: manuale (`README`) ed `EXTENDING` della 0.9.22, con le note sul fork (2026-10-31); `PNG.txt` e `COPIATURA.txt` vecchi ma validi; OPTIONS, INSTALL, AUTHORS (0.9.14-0.9.15) superati, con un avviso in testa che rimanda all'inglese.

Nessun `CLAUDE.md`, nessun file di design o di decisioni interne: tutta la
documentazione è quella upstream.

## 4. Build: requisiti e situazione dell'ambiente

Dipendenze richieste (da INSTALL.txt e tuxpaint.spec):
SDL **1.2** (≥ 1.2.4), SDL_image, SDL_mixer, SDL_ttf, SDL_Pango (opzionale),
libpng, librsvg2 + cairo (SVG), fribidi, libpaper, gettext, gperf.

Comando di build standard: `make` → `make install` (variabili `PREFIX`, `DESTDIR`,
`SVG_LIB:=` per disattivare SVG).

Verifica eseguita il 2026-10-29 nella shell di VS Code (storica: il problema
è risolto compilando sull'host):

| Componente | Stato |
|------------|-------|
| sdl, SDL_image, SDL_mixer, SDL_ttf, SDL_Pango (1.2) | **MANCANTI** |
| SDL2 / SDL2_mixer | presenti (non usabili da questo codice) |
| librsvg-2.0 2.63.3, cairo 1.18.4, fribidi 1.0.17, libpng 1.6.59 | presenti |
| gcc 15.2.0, gperf, msgfmt | presenti |

Attenzione: la shell di VS Code gira nel **runtime Flatpak Freedesktop SDK
25.08**, non direttamente sull'host. Le librerie vanno installate e la build
va eseguita **sull'host** (decisione del 2026-10-29). Dalla shell di VS Code
si raggiunge l'host con `flatpak-spawn --host <comando>`.

### Host di build

Verifica eseguita il 2026-10-29 sull'host:

- **Sistema**: Debian GNU/Linux 13.7 (trixie), 4 CPU.
- **Strumenti presenti**: gcc 14.2.0, make, pkg-config, gettext/msgfmt,
  libpng-dev, zlib1g-dev.
- **Mancanti, tutti disponibili nei repository Debian 13**:

| Pacchetto | Versione candidata | Serve per |
|-----------|--------------------|-----------|
| `libsdl1.2-dev` | 1.2.68-3 (sdl12-compat) | SDL 1.2 (`pkg-config sdl`) |
| `libsdl-image1.2-dev` | 1.2.12-14 | `-lSDL_image` |
| `libsdl-mixer1.2-dev` | 1.2.12-19+b1 | `-lSDL_mixer` (audio) |
| `libsdl-ttf2.0-dev` | 2.0.11-6+b2 | `-lSDL_ttf` |
| `libsdl-pango-dev` | 0.1.2-8+b3 | `-lSDL_Pango` (testo complesso) |
| `librsvg2-dev`, `libcairo2-dev` | 2.60.0, 1.18.4 | timbri e starter SVG |
| `libfribidi-dev` | 1.0.16 | testo bidirezionale |
| `libpaper-dev` | 2.2.5 | formato carta per la stampa |
| `gperf` | 3.2.1 | genera il parser delle opzioni (`src/parse.gperf`) |

Comando di installazione (da un terminale dell'host, richiede la password
di sudo):

```sh
sudo apt install libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev \
  libsdl-ttf2.0-dev libsdl-pango-dev librsvg2-dev libcairo2-dev \
  libfribidi-dev libpaper-dev gperf
```

Le dipendenze GTK2/libgsf/libxml2 elencate in `tuxpaint.spec` servono solo
per la build Windows: il Makefile non le usa su Linux.

Pacchetti installati dall'utente il 2026-10-29; verificati con `pkg-config`
(sdl 1.2.68, SDL_image 1.2.12, SDL_mixer 1.2.12, SDL_ttf 2.0.11,
SDL_Pango 0.1.2, librsvg 2.60.0, cairo 1.18.4, fribidi 1.0.16).

### Comandi di build

Si usa lo script [dev.sh](dev.sh) nella root. Funziona sia dall'host sia
dalla shell di VS Code: se si accorge di girare nel sandbox Flatpak, si
riesegue da solo sull'host con `flatpak-spawn --host`.

```sh
./dev.sh build      # compila (da zero se PREFIX è cambiato)
./dev.sh install    # compila e installa in $PREFIX, con lanciatore nel menu
./dev.sh run        # installa e avvia in finestra; altre opzioni in coda
./dev.sh stamps     # aggiunge in $PREFIX la raccolta completa dei timbri
./dev.sh uninstall  # rimuove ciò che è installato in $PREFIX
./dev.sh clean      # rimuove gli artefatti di build
```

- Variabili: `PREFIX` (default `~/.local`), `JOBS` (default: numero di CPU).
- Lo script passa al Makefile `COMPLETIONDIR`, `GNOME_PREFIX` e
  `KDE_ICON_PREFIX` dentro `PREFIX`. Così l'installazione non tocca `/etc` e
  installa il lanciatore e le icone nel menu dell'utente.
- Corregge `Exec=` del lanciatore con il percorso assoluto, perché
  `~/.local/bin` non è nel `PATH` della sessione grafica.
- Ricorda in `obj/.build-prefix` il `PREFIX` dell'ultima build e ricompila
  da zero se cambia. Il Makefile da solo non se ne accorgerebbe.
- Per lanciare `make` a mano dal sandbox:
  `flatpak-spawn --host bash -c 'cd /home/paolo/Sviluppo/tuxpaint && make'`.
  Usare `bash -c`, non `sh -c`: su Debian `sh` è dash, che non ha `time` né
  le altre funzioni di bash.
- `make clean` cancella solo file generati, gli stessi elencati in
  `.gitignore`.
- Prodotti della build: il binario `./tuxpaint`, 48 plugin in `magic/*.so`,
  119 cataloghi in `trans/*.mo`, `src/tp_magic_api.h` e `tp-magic-config`.
- I percorsi di installazione sono **fissati nel binario** al momento della
  compilazione (`DATA_PREFIX`, `MAGIC_PREFIX`, `CONFDIR`, … derivano da
  `PREFIX`, default `/usr/local`). Per installare altrove bisogna
  ricompilare con lo stesso `PREFIX` che si usa per `make install`.
- `install-bash-completion` scrive sempre in `/etc/bash_completion.d`
  (`COMPLETIONDIR`), anche con un `PREFIX` utente: in quel caso va
  sovrascritto anche `COMPLETIONDIR`.

### Warning della build

Il 2026-10-29 erano 96: 52 in `src/tuxpaint.c`, 13 in `src/im.c`, il resto
nei plugin. Dal 2026-10-31 sono **0** (branch `quality/warnings`): una
decina indicavano difetti veri (doppio `free`, comportamento indefinito,
`sprintf` oltre i buffer, una stringa di formato, maschere dei colori), il
resto era codice inutilizzato. Con `OPTFLAGS="-O1 …"` (build ASan) GCC fa
altre analisi: anche lì 0.

## 5. Rischi e punti di attenzione

1. **SDL 1.2 è obsoleta.** Le distribuzioni moderne la forniscono solo tramite
   `sdl12-compat` (sopra SDL2); SDL_Pango 1.2 potrebbe non essere più
   disponibile. Upstream Tux Paint è passato a SDL2 dalla 0.9.24.
   Restare su SDL 1.2 è una scelta voluta (§1): la build userà
   `sdl12-compat`. SDL_Pango 1.2 è ancora disponibile in Debian 13
   (`libsdl-pango-dev`).
2. **GCC moderni e codice C del 2014.** ~~Rischio aperto~~ **Risolto il
   2026-10-29**: con GCC 14.2 gli errori erano solo due, un tipo di
   puntatore a funzione incompatibile e una dichiarazione implicita in
   `parse.gperf`, più `-lm` mancante al link. Tutti corretti nel codice
   (§1). I problemi di C23 riguarderebbero solo GCC 15, come quello del
   runtime Flatpak, che però non si usa per compilare.
3. **OpenCandy** (adware) integrato negli script di installazione Windows
   (`win32/`, vedi CHANGES 0.9.22). Non rilevante per Linux, ma da rimuovere
   se il fork verrà distribuito anche su Windows.
4. **Codifica dei file**: alcuni documenti (es. `docs/CHANGES.txt`) contengono
   caratteri Latin-1 mescolati a UTF-8.
5. **Marcatori FIXME/TODO/XXX** nel sorgente (`src/` e `magic/src/`):
   erano 167, 155 il 2026-11-01 prima di "Feature e miglioramenti
   strumenti" e 141 dopo (contando i soli `.c` e `.h`). Le otto voci
   scelte per il TODO sono state chiuse il 2026-10-31 (§5ter, ASIS); gli
   altri sono minori.
6. **Fork vs upstream**: il codice è fermo al 2014; upstream (tuxpaint.org) è
   oggi alla serie 0.9.3x con molte funzionalità nuove. Deciso il 2026-10-29
   di restare sulla 0.9.22: l'upstream resta una fonte di idee da portare a
   mano, non una base da cui ripartire.
7. **Identità git**: ~~non configurata~~ **risolto il 2026-10-29**.
   Impostata solo nella config del repository; `~/.gitconfig` non esiste,
   quindi negli altri repository va configurata a parte.

## 5bis. UI scalabile con la finestra: note tecniche

Feature richiesta il 2026-10-29: su schermi ad alta risoluzione pulsanti e
icone restavano a 48 px, minuscoli. Si è scelta la scala nativa
dell'interfaccia, a fasi. L'alternativa scartata era l'ingrandimento globale
con `SDL12COMPAT_WINDOW_SCALING`, che riduce la risoluzione della tela.
L'upstream ha introdotto una soluzione simile (`buttonsize`, `auto`) dalla
0.9.27.

### Modello

In `setup_normal_screen_layout()` (`src/tuxpaint.c`):

- `scala = max(1, min(max(L,A) / 800, min(L,A) / 600))`;
- `button_w = button_h = floor(48 × scala)`, ridotta da `buttonsize` se
  questo è più piccolo;
- `button_scale = button_w / 48`; `SCALED(x)` converte le misure del
  design 48×48.

Fino a 800×600 non cambia nulla. Esempi: 1600×1000 → 80 px, 1600×1200 →
96 px, 2400×1500 → 120 px, 2560×1600 a schermo intero → 128 px. La
finestra è fissa per tutta la sessione, quindi la scala si calcola una volta
sola, all'avvio. `HEIGHTOFFSET` e `TOOLOFFSET` derivano da `buttons_tall`,
le righe di pulsanti del layout: `HEIGHTOFFSET = (buttons_tall - 7) *
button_h`.

### Convenzioni per il codice

| Prima (design 48×48) | Dopo |
|----------------------|------|
| `48` (pulsante) | `button_w` / `button_h` |
| `96` (due colonne) | `button_w * 2` |
| `40` (altezza titolo) | `r_ttools.h` / `r_ttoolopt.h` |
| `24` (mezzo pulsante, frecce di scorrimento) | `button_h / 2` |
| margini e misure interne (`2`, `4`, `40`, `44`…) | `SCALED(n)` |
| `+ 96` / `- 96` (scostamento della tela) | `r_canvas.x` |
| `WINDOW_WIDTH - 96 - 96`, `48 * 7 + 40 + HEIGHTOFFSET` | `r_canvas.w`, `r_canvas.h` |
| `loadimage()` di immagini dell'interfaccia | `loadimagerb()` |
| superfici già caricate (es. icone dei plugin) | `scale_ui_image()` |
| dimensioni dei font dell'interfaccia | `SCALED(punti)` |

### Parti dell'interfaccia

- **Schermata principale** (fase 1): barre, selettori, palette, titoli,
  area di Tux, etichette, font, icone delle magie, miniature dei timbri,
  pulsanti audio dei timbri.
- **Finestre di dialogo** (fase 2):
  - Le richieste sì/no e il selettore colore sono disegnati in un'area di
    design di 640×480 centrata.
    `PROMPTOFFSETX = (WINDOW_WIDTH - SCALED(640)) / 2`;
    `PROMPTOFFSETY = HEIGHTOFFSET / 2`.
  - La geometria del riquadro resta in unità di design: la variabile `w`
    dell'animazione conta pixel di design. Si scala solo il risultato, per
    esempio `SCALED(PROMPT_LEFT + 96 - w) + PROMPTOFFSETX`.
  - Apri, Nuovo e presentazione hanno la griglia di miniature da
    `r_canvas.x`, le frecce alte `button_h / 2` e la riga di pulsanti a
    `r_canvas.h - button_h`.
    `THUMB_H = (r_canvas.h - button_h / 2 - button_h) / 4`.
  - Le miniature salvate accanto ai disegni (`saved/.thumbs/`) misurano
    `THUMB_W - SCALED(20)` × `THUMB_H - SCALED(20)`, come quelle della
    griglia; se non coincidono, Apri le ridimensiona a ogni apertura.
  - Nella richiesta "Cancella" la miniatura, se è più alta di
    `SCALED(64)`, si riduce dentro `SCALED(80)` × `SCALED(64)` con un
    calcolo esplicito delle proporzioni. Non usare la modalità
    `keep_aspect` di `thumbnail()`: centra bene solo in riquadri quadrati.
- **Resto dell'interfaccia** (fase 3):
  - **Cursori**: `get_cursor()` ingrandisce le bitmap XBM di un fattore
    intero `k = round(button_scale)`, con punto attivo `x·k + k/2`; il
    buffer è dinamico.
  - **Schermata iniziale**: immagini con `loadimagerb()`, margini con
    `SCALED()`. La barra di avanzamento (`src/progressbar.c`) ricava il
    modulo dall'immagine (`img_progress->w / 2` × `img_progress->h`).
  - **Tastiera a schermo**: i tasti sono i pulsanti piccoli già scalati
    (`img_btnsm_*`). Il font (`12 · altezza tasto / 24`) e il margine
    della scritta seguono il tasto (`src/onscreen_keyboard.c`).
- **Rifiniture** (2026-10-30):
  - **`buttonsize=auto|24-192`** (`button_size_wanted`): può solo
    rimpicciolire rispetto ad `auto`. Il layout ha bisogno di almeno 7
    righe di pulsanti; se il valore è troppo grande c'è un avviso su
    stderr. Un valore non valido fa uscire con codice 91.
  - **Finestra iniziale**: se `windowsize` non è indicato
    (`window_size_given`, impostato anche da `--1024x768`) e non si è a
    schermo intero, 800×600 viene moltiplicato per
    `k = min(90% larghezza schermo / 800, 85% altezza / 600)`, con k
    intero ≥ 2 e schermo letto da `SDL_GetVideoInfo()`. Sullo schermo
    dell'utente (2560×1600) dà 1600×1200.
  - **Mouse da tastiera**: passi `SCALED(16)` / `SCALED(24)` in
    `handle_keymouse()`.
  - **Icone più nitide**: `enlarge_lanczos()` (filtro separabile Lanczos-3
    su alfa premoltiplicato), usato da `scale_ui_image()` solo se entrambe
    le dimensioni crescono. Altrimenti, o se manca memoria, si usa
    `thumbnail2()`. `zoom()` (bilineare) resta per miniature, timbri e
    Starter. Immagini ad alta risoluzione non esistono, nemmeno
    nell'upstream.
- **Non scalati di proposito**: i pennelli nel selettore (mostrano la
  dimensione reale della punta); timbri, testo e disegni sulla tela, che
  sono contenuto; i passi del joystick, configurabili con le sue opzioni.

### Schermo intero (2026-10-31)

- **Alt+Invio** (anche Alt+Invio del tastierino) passa da finestra a
  schermo intero e viceversa, in ogni ciclo di eventi: schermata
  principale e dialoghi. Tutti i cicli chiamano `poll_event()` invece di
  `SDL_PollEvent()`; `poll_event()` intercetta il tasto, le sue ripetizioni
  e il suo rilascio, quindi nessun ciclo lo vede e lo strumento Testo non
  va a capo. F11 non si poteva usare: nella finestra Apri e con il mouse
  da tastiera sposta la selezione.
- *Dal 2026-11-01 vale solo nei dialoghi, vedi la sezione seguente.*
  `toggle_fullscreen()` usa `SDL_WM_ToggleFullScreen()`, che tiene la
  stessa superficie: disegno e disposizione restano, e a schermo intero
  sdl12-compat ingrandisce l'immagine con le proporzioni giuste. Sullo
  schermo dell'utente 1600×1200 diventa 2133×1600 da x=213, con bande nere
  ai lati. Il mouse viene riportato da solo alle coordinate logiche
  (verificato con un clic su "Forme").
  Aggiorna `fullscreen`, che decide anche se mostrare la scelta della
  stampante, visibile solo in finestra.
- Se la superficie è grande quanto il desktop (avvio con
  `fullscreen=native`, o `fullscreen` senza dimensione), Alt+Invio non fa
  nulla. Una finestra così grande non starebbe tra le barre di GNOME, e
  mutter la terrebbe comunque a tutto schermo: prima di questo controllo,
  lo stato interno diceva "finestra" mentre lo schermo restava pieno.
- **`fullscreen` senza `windowsize`** (né `--WIDTHxHEIGHT`, né `orient`)
  imposta `native_screensize`: si apre alla risoluzione dello schermo e la
  UI scala, invece di ingrandire 800×600.
- **`native`** chiede la dimensione del desktop (`desktop_w`, `desktop_h`,
  letti una volta con `SDL_GetVideoInfo()` prima di aprire la finestra),
  non più 0×0: con sdl12-compat una finestra creata a 0×0, uscendo dallo
  schermo intero, diventa di 2×2 pixel.
- **`--fullscreen` e `-f` senza valore** ora valgono "yes"
  (`src/parse.gperf`). Prima uscivano con "needs a value" (codice 52),
  anche se `--usage` li mostra così.
- **Lanciatore**: `src/tuxpaint.desktop` ha l'azione `fullscreen` ("Full
  screen", in italiano "Schermo intero") con `--fullscreen=native`; in
  GNOME compare col clic destro sull'icona. `dev.sh install` corregge
  anche la sua riga `Exec=`.

### Ridisegno alla nuova dimensione (2026-11-01)

- **Cosa**: la finestra si ridimensiona, e Alt+Invio passa a uno schermo
  intero vero, alla risoluzione dello schermo. In entrambi i casi
  `change_screen()` rifà tutto per la nuova dimensione, come se Tux Paint
  fosse partito lì.
- **Chi lo fa**: il ciclo principale, in testa a ogni giro, quando
  `screen_change_wanted()` dice che serve e nessun tasto del mouse è
  premuto. `poll_event()` registra le richieste: Alt+Invio
  (`fullscreen_request`) e `SDL_VIDEORESIZE` (`resize_w`/`resize_h`, usati
  250 ms dopo l'ultimo evento). Gli eventi di ridimensionamento arrivati
  a schermo intero si ignorano. Nei dialoghi Alt+Invio fa come prima
  (immagine ingrandita) e il ciclo principale rende nitido al ritorno. Un
  ridimensionamento durante un dialogo mostra l'immagine tagliata o con
  bande nere fino al ritorno; se si torna alla stessa dimensione, il
  ciclo principale ridisegna e basta.
- **Prima di cambiare** (nel ciclo principale): testo in corso completato
  come al cambio di strumento; rotazione di una forma annullata (è solo
  XOR sullo schermo); `magic_switchout()`; tastiera a schermo liberata
  (usa le immagini dei pulsanti). `old_x`/`old_y` vanno a -1: i contorni
  di timbro e gomma sotto il mouse sono XOR, e il primo movimento dopo il
  ridisegno li "cancellerebbe" dove non ci sono più.
- **`change_screen()`**: `free_ui_images()`, `free_ui_fonts()`,
  `setup_screen_layout()`, poi di nuovo font, `load_ui_images()`,
  `render_ui_titles()`, `create_color_buttons()`, icone delle magie da
  `get_icon()` dei plugin, `create_button_labels()`, `create_cursors()`
  (il puntatore corrente sostituito prima di liberare i vecchi).
  Timbri: miniature liberate e `processed = 0`, così dimensioni e limiti
  si ricalcolano quando servono. `magic_api_struct->canvas_w/h`
  aggiornati.
- **`resize_canvas()`**: `get_picture_rect()` prende `canvas_content`
  (la parte con il disegno), allargata a quello che è stato disegnato o
  etichettato fuori; quel rettangolo viene scalato per stare nella nuova
  tela, centrato. Intorno: lo sfondo dello Starter o del modello
  (allungato come fa `autoscale_copy_smear_free()`) o il colore della
  tela. Stessa sorte per sfondo, contorno dello Starter (trasparente
  intorno), buffer di Annulla in uso (da `oldest_undo` a `newest_undo`) ed
  etichette (posizione, bitmap scalata, dimensione del testo più vicina).
  `canvas_content` si azzera a tutta la tela quando nasce un disegno
  nuovo (avvio, Apri, Nuovo). Così andata e ritorno ridanno il disegno
  di prima. Il ricampionamento (`resample_rect()`) usa un filtro
  triangolare, largo quanto un pixel d'origine quando riduce, con alfa
  premoltiplicato.
- **sdl12-compat 1.2.68 e mutter**: `SDL_RESIZABLE` funziona e arriva
  `SDL_VIDEORESIZE`, ma `TP_EventFilter()` lo scartava. Passare da e verso
  lo schermo intero con il solo `SDL_SetVideoMode()` lascia la finestra
  altrove e più bassa (1600×1126 invece di 1600×1200), con una raffica di
  ridimensionamenti spuri. Passando prima da `SDL_WM_ToggleFullScreen()`
  mutter rimette la finestra com'era, salvo se una finestra non c'è mai
  stata (`been_windowed`): da uno schermo intero di partenza, il toggle
  dà una finestra grande quanto il desktop, che mutter tiene a tutto
  schermo, quindi lì si usa solo `SDL_SetVideoMode()`. A ogni andata e
  ritorno mutter abbassa un po' la finestra (74 e poi 52 pixel). I test
  con programmini SDL a parte sono stati decisivi: il comportamento di
  mutter dipende anche dai tempi.
- **`fullscreen`** valeva 11 con `--fullscreen` (`strcmp()`), ora 0 o 1.
- **Plugin Magia**: Halftone, Foam e Glass Tile creavano una volta sola
  copie o maschere grandi quanto la tela, ora le rifanno se la tela è
  cambiata; gli altri le fanno in `switchin()`.
- **Icone SVG**: con pulsanti più grandi di 48×48, `loadimagerb()` usa
  l'SVG con lo stesso nome del PNG (stessa dimensione di disegno),
  disegnato da `load_svg_at()` alla scala dei pulsanti. A 48×48 restano i
  PNG, identici. Forme: `devtools/content/shape_icons.py`, a mano dalle
  misure dei PNG. Strumenti: `devtools/content/trace_icons.py`, con
  potrace (`apt-get download potrace libpotrace0`, `dpkg-deb -x`, poi una
  cartella con `bin/` e `lib/`), in tre livelli: parti chiare, inchiostro
  leggero (nero al 40%: le icone sono nere con trasparenza, non grigie),
  nero. Non convertiti: altoparlante e cuffia (sfumati come foto), le
  cornici dei pulsanti (sfumature a gel, già rese bene dal Lanczos: a
  2,67× non si vede differenza).
- **Icone SVG, seconda parte (2026-11-01)**: tutte le icone tracciate le
  rifà `devtools/content/svg_icons.py POTRACE_DIR` (le 16 degli strumenti
  escono identiche), con l'elenco di quelle che tracciano bene. Le icone
  al tratto con i due livelli di prima; quelle a grigi piatti con
  `trace_icons.py --tones`, che trova i toni nell'istogramma lontano dai
  bordi e fa uno strato per tono con l'opacità che, sovrapposta, lo
  ridà. Scelta guardando ogni icona a 2,67×, PNG ingrandito accanto alle
  due tracciature: una misura numerica alla misura originale non ha
  funzionato (potrace sposta di mezzo pixel). Restano PNG le icone con
  sfumature, luci dentro zone scure o foto: 31 magie, i pulsanti a gel,
  i tasti della tastiera a schermo, `magic_paint` con
  `magic_fullscreen` (il secondo traccia male, e sono affiancati).
- **Icone delle magie**: le carica il plugin, quindi serve l'API:
  `load_icon(percorso del PNG)` (in fondo a `magic_api`) dà il PNG o,
  con pulsanti più grandi, l'SVG già alla scala; `get_magic_icon()` lo
  riconosce (`magic_icon_at_scale`) e non lo scala di nuovo. Tutti i 48
  plugin la usano. I plugin così fatti dicono versione 0x00010003: un
  Tux Paint 0.9.22 li rifiuta con un avviso, invece di andare in crash
  chiamando un puntatore che non ha (è successo con il binario di
  riferimento); il fork accetta anche quelli 0x00000003
  (`TP_MAGIC_API_VERSION_0922`). Nel Makefile i plugin ora dipendono da
  `src/tp_magic_api.h`, altrimenti un cambio dell'API non li ricompilava.

### Dialoghi alla nuova dimensione (2026-11-01)

- **Cosa**: ridimensionando o con Alt+Invio mentre un dialogo è aperto,
  il dialogo si rifà alla nuova dimensione. Prima restava tagliato o
  ingrandito fino alla chiusura.
- **Come**: i sei cicli dei dialoghi (richieste sì/no, selettore colore,
  Apri, Nuovo, scelta delle diapositive, presentazione) usano
  `poll_event_dialog()` (Alt+Invio rimandato come nel ciclo principale,
  quindi nitido) e, tra un giro di eventi e l'altro,
  `dialog_screen_change()`: fa il cambio (`change_screen()`, prima
  `finish_typing()` e liberata la tastiera a schermo), ridisegna lo
  schermo principale (`redraw_main_screen()`) e il testo di Tux.
- **Poi il dialogo**: richieste e selettore ripartono da dove finisce la
  loro animazione (`goto redraw`), con la cornice che l'animazione
  lasciava; le immagini dell'interfaccia ricevute dal chiamante si
  riprendono dalle variabili che le tengono (`ui_image_slot()`), perché
  `change_screen()` le rifà. Apri, Nuovo e scelta delle diapositive
  ricominciano (le miniature sono della misura vecchia): Apri col suo
  ciclo esterno, gli altri con `goto start_again`, conservando
  selezione, scorrimento, disegni scelti e velocità. La presentazione
  rifà la diapositiva corrente.
- **Contatori**: `screen_layouts` (nuova misura: il ciclo principale
  rifà ciò che sa solo lui, `real_r_tools`, scorrimenti, timbro) e
  `screen_redraws` (qualcuno ha ridisegnato: il ciclo principale, o un
  dialogo sotto una richiesta, si ridisegna). Finché il ciclo principale
  non ha fatto la sua parte, non legge altri eventi.
- **Sotto i dialoghi**: Apri, Nuovo e il selettore colore spengono
  colori e selettore (`screen_wiped_for_dialog`, che anche
  `redraw_main_screen()` rispetta, con il titolo grigio che
  `draw_colors()` disegna solo cambiando stato); sotto Salva, Stampa ed
  Esci resta lo strumento di prima (`old_tool`).
- **Limite**: una richiesta dentro Apri ("Cancella"), ridimensionata, ha
  dietro lo schermo principale invece della griglia, finché non si
  chiude; poi Apri si rifà.
- **Testo di Tux**: `draw_tux_text()` ora ne tiene una copia; teneva il
  puntatore del chiamante, che Apri libera subito (trovato con
  AddressSanitizer al primo ridisegno).
- **Leak nelle librerie a ogni cambio di misura**: SDL_Pango crea una
  fontmap per contesto, e `change_screen()` ricrea i font
  dell'interfaccia; i risultati del thread con cui Pango abbina i font
  (FcFontSetMatch) si perdono quando la fontmap muore. Da pochi byte a
  circa 3 KB a ridimensionamento, secondo i tempi (TODO).

### Prove automatiche (`devtools/ui-test/`)

Si lanciano dalla shell di VS Code e pilotano Tux Paint sull'host
(XWayland). Sull'host servono `xwininfo`, `xprop`, `xwd`, `ffmpeg`,
`python3` con PIL, `libXtst` e `libXfixes`. Dettagli d'uso in
[devtools/ui-test/README.md](devtools/ui-test/README.md).

- `regress.sh OUT BIN DIMENSIONE PULSANTE` cattura una schermata per
  strumento: pennello, timbro, linee, forme, testo, etichetta, magie,
  gomma. Inoltra `TP_ARGS` e `TP_SOUND`.
- `dialogs.sh OUT BIN [SCALA]` attraversa tutti i dialoghi a 800×600 per
  SCALA (intera), con `--savedir` su una copia di
  `~/.cache/tuxpaint-test-canon`: uscita, Apri con selezione,
  presentazione e riproduzione, Nuovo, selettore colore.
- `erase.sh OUT BIN [SCALA]`: disegna un punto, salva, apre, chiede di
  cancellare il primo disegno e risponde "No", con Cestino e cartella di
  salvataggio di prova. Poi stampa le dimensioni delle miniature salvate
  e il numero di file nel Cestino di prova, che deve essere 0.
- `compare.py` confronta due serie di catture pixel per pixel.
- `tp_session.py` è il motore.
  - Azioni: `click`, `tool`, `move`, `drag`, `wait`, `shot` (finestra),
    `cursor` (cursore via XFixes), `key` (tasti X, es. `Alt_L+Return`,
    con durata), `info` (posizione, dimensione e stato della finestra).
  - Dimensione `-`: niente `--windowed --windowsize`, opzioni solo da
    `TP_ARGS` (per esempio `--fullscreen=native`).
  - Variabili: `TP_BIN`, `TP_BUTTON`, `TP_ARGS`, `TP_SCALE`,
    `TP_START_WAIT`, `TP_LOG`, `TP_WRAP`, `TP_SOUND` (audio col driver
    SDL `dummy`).
  - Usa solo la finestra del processo che ha avviato (`_NET_WM_PID`), la
    porta in primo piano e non clicca mai se sotto il puntatore c'è
    un'altra finestra. Non preme tasti se il focus della tastiera non è
    lì. In entrambi i casi scrive "STOP".
  - Rilegge la posizione della finestra prima di ogni azione del
    puntatore: cambia passando a schermo intero.
- `segv_backtrace.c`: libreria per `LD_PRELOAD` che stampa la pila delle
  chiamate ai crash, anche nei processi figli. Indirizzi da tradurre con
  `addr2line -f -e BINARIO 0xOFFSET` su un binario compilato con `-g`.

**Binario di riferimento**: worktree git in `~/.cache/tuxpaint-baseline`,
a `ec9ebe3` (prima della UI scalabile) più la sola correzione `_exit(0)` in
`src/fonts.c`, non committata nel worktree, così l'ordine dei font coincide.
Dal 2026-11-01 usa i **suoi plugin**, in
`~/.cache/tuxpaint-baseline/plugins-0922`: quelli installati hanno la
versione 0x00010003 e lui li rifiuterebbe, restando senza magie. Si
ricompila così (non con `./dev.sh build`, che rimetterebbe i plugin di
`~/.local`):
`make PREFIX=$HOME/.local MAGIC_PREFIX=$HOME/.cache/tuxpaint-baseline/plugins-0922 tuxpaint magic-plugins`
e poi `cp magic/*.so plugins-0922/`. Dati, timbri e traduzioni restano
quelli di `~/.local`. Il pannello delle magie a 800×600 differisce
comunque (etichette su due righe del fork). Si rimuove con
`git worktree remove --force ~/.cache/tuxpaint-baseline`. Le serie di
riferimento vanno rigenerate a ogni sessione: le catture stanno in una
cartella temporanea.

### Insidie delle prove automatiche

- **Mouse dell'utente**: se l'utente usa mouse o rotella sopra la finestra
  di prova, la cattura si sporca (linee disegnate, elenchi scorsi). Prima
  di una prova chiedere di non toccare nulla. Se un confronto fallisce,
  guardare le immagini prima di cercare un bug.
- **"mutter guard window"**: quando in primo piano c'è una finestra
  Wayland, GNOME copre le finestre X con una finestra invisibile e i clic
  finirebbero lì. Lo script la rileva e si ferma ("STOP"). Si ripete la
  prova.
- **Primo clic**: serve a dare il focus e a volte lasciava un punto sulla
  tela. Gli script portano prima il puntatore sul titolo e aspettano.
- **Trascinamenti simulati**: poco affidabili, il puntatore reale
  interferisce. Per verificare la tela usare clic singoli.
- **Chiusura**: Tux Paint ignora SIGTERM (SDL lo trasforma in una
  richiesta di uscita, con conferma). Usare SIGKILL. Per cercare processi
  usare `pgrep -x tuxpaint`, non `pkill -f`, che colpisce anche le shell.
- **Sandbox e host**: l'host non vede la `/tmp` del sandbox, quindi i dati
  passano su stdout (tar). Con `flatpak-spawn` passare `--directory=$HOME`
  se la cartella corrente non esiste sull'host.
- **Finestre troppo grandi**: il gestore delle finestre le accorcia (per
  esempio 2400×1500 diventa 2400×1462) e possono finire senza nessuna
  finestra sotto il puntatore: STOP, si ripete.
- **"Cancella" in Apri**: provarla solo con
  `TP_WRAP="env XDG_DATA_HOME=$HOME/.cache/tuxpaint-test-xdg"` e
  `--savedir` di prova, come fa `erase.sh`. Altrimenti un "Sì" sposta file
  veri nel Cestino dell'utente.
- **Coordinate dei pulsanti di Apri**: a 800×600 la riga dei pulsanti va
  da y=424 a y=472 (escluso). Cliccare al centro, y=448: un clic a y=472
  cade fuori e la prova prosegue senza errori, ma la cattura mostra
  un'altra schermata.
- **Output perso**: stdout è bufferizzato e il processo muore con
  SIGKILL. Usare `TP_WRAP="stdbuf -oL -eL"` e `TP_LOG`.
- **Pulizie**: mai `cd DIR && rm -rf *`, perché se il `cd` fallisce cancella
  la cartella corrente; il controllo di sicurezza l'ha già bloccato una
  volta. Usare cartelle di output nuove o percorsi espliciti.
- **Schermo intero**: la finestra di prova copre tutto lo schermo; dirlo
  all'utente quando gli si chiede di non toccare nulla. Con l'immagine
  ingrandita (da finestra ad Alt+Invio), le coordinate dei clic sono
  fisiche: x = 213 + x·4/3, y = y·4/3 per 1600×1200 su 2560×1600. Alla
  risoluzione nativa coincidono con quelle logiche (`TP_BUTTON=128`).
  All'avvio a schermo intero serve `TP_START_WAIT=7`.
- **Uscendo dallo schermo intero** la finestra torna leggermente più in
  basso (y da 274 a 348): la sistema mutter, non è un errore.
- **Sessioni senza `--savedir`** usano `~/.tuxpaint` dell'utente: vanno
  bene solo se non salvano e non cancellano nulla.

## 5ter. Qualità del codice: strumenti e note (2026-10-31)

- **AddressSanitizer**: build a parte in un worktree (`~/.cache/tuxpaint-asan`)
  con `make PREFIX=$HOME/.local OPTFLAGS="-O1 -g -fsanitize=address
  -fno-omit-frame-pointer" tuxpaint`. Usa i dati e i plugin installati in
  `~/.local`. Il rapporto dei leak arriva solo se Tux Paint esce da sé:
  la sessione deve cliccare Esci e poi Sì, a (205, 250) a 800×600.
  Comandi in `devtools/ui-test/README.md`. Valgrind sull'host non c'è.
- **Pile complete**: le librerie (SDL2, sdl12-compat, glib) sono senza
  frame pointer, e la pila di un blocco perso si ferma a `malloc`. Con
  `ASAN_OPTIONS=…:fast_unwind_on_malloc=0:malloc_context_size=12` la
  pila è completa, ma tutto è molto più lento: dare più tempo prima di
  Esci e dopo Sì (in un tentativo il programma non ha fatto in tempo a
  uscire, e senza uscita non c'è rapporto). Per sapere se è uscito da sé:
  `current_id.txt` nella cartella di salvataggio viene scritto solo alla
  chiusura normale.
- **Leak che restano** (2026-10-31, sessione con Testo, Apri, Nuovo,
  selettore colore, Esci): 432 byte in 4 blocchi senza pila, nelle
  librerie. Erano 3,46 MB, quasi tutti di Tux Paint e a ogni uso.
- **Cestino su un altro filesystem**: `/tmp` e `/home` sono partizioni
  diverse, quindi `TP_TEST_XDG=/tmp/… erase.sh OUT BIN 1 yes` costringe
  `trash()` a copiare invece di rinominare.
- **Senza finestra**: `SDL_VIDEODRIVER=dummy` fa partire Tux Paint senza
  aprire nulla. Basta per i crash all'avvio, non per cliccare: senza
  input non si può nemmeno farlo uscire in modo pulito (SIGTERM apre la
  richiesta d'uscita e un secondo SIGTERM risponde "No").
- **Stampa**: `devtools/print-test/ps_check.sh [OUTDIR]` compila un
  programmino con `obj/postscript_print.o` e misura i margini con
  Ghostscript. Prova anche un formato carta sconosciuto e i comandi di
  stampa riusciti e falliti. `OBJ=DIR` usa gli oggetti di un altro albero,
  per esempio `~/.cache/tuxpaint-baseline/obj`.
- **Finestra Nuovo da tastiera**: F7 scende di una riga (4 elementi) e si
  ferma all'ultimo, F11 torna indietro di uno, Invio apre. L'elenco è:
  colori, Starter personali, Starter, modelli personali, modelli (19).
- **Commit di più argomenti in un file**: niente `git add -p` (non
  interattivo); si possono selezionare i blocchi del diff con uno script
  e `git apply --cached`. Per correggere un commit non pubblicato:
  `git commit --fixup=…` e poi
  `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash BASE`.

## 5quater. Contenuti e traduzioni: note (2026-10-31)

- **Timbri**: `./dev.sh stamps` usa `apt-get download
  tuxpaint-stamps-default` (circa 80 MB, nessun permesso di root) e
  `dpkg-deb -x` in una cartella temporanea, poi copia solo
  `usr/share/tuxpaint/stamps/`. Accetta anche un `.deb` o una cartella che
  si chiami `stamps` o ne contenga una (l'archivio sorgente estratto);
  rifiuta le altre. La versione 2025.03.31: 957 timbri (PNG e SVG, con i
  doppioni PNG/SVG e le varianti `_mirror` contati una volta), 951 con la
  descrizione, 932 in italiano, nessuna descrizione parlata in italiano.
  La 0.9.22 all'avvio legge solo l'elenco dei file; miniature, `.dat` e
  `.txt` si caricano quando il timbro compare nel selettore.
- **Gruppi di timbri**: le frecce del selettore passano da una cartella di
  primo livello all'altra (`animals`, `cartoon`, …); dentro un gruppo si
  scorre con le frecce su e giù.
- **Traduzioni**: intltool non c'è sull'host, quindi `src/po/update-po.sh`
  non funziona. `devtools/po/update-po.sh it` fa la stessa cosa con
  `xgettext`/`msguniq`/`msgmerge` (stesso modello, verificato sul vecchio
  `tuxpaint.pot`) e solo per le lingue indicate. Non rigenera
  `src/tuxpaint.desktop`: le traduzioni di nome e azione vanno tenute
  allineate a mano ai `.po`. Un'emulazione di `intltool-merge` sui `.po`
  ha dato lo stesso file. Per contare le stringhe mancanti di un
  catalogo: `LC_ALL=C msgcmp --use-untranslated X.po tuxpaint.pot`.
- **Commenti estratti**: xgettext (`--add-comments`) mette nel modello,
  come nota per i traduttori, ogni commento subito prima di un
  `gettext()`. Un commento per gli sviluppatori in quella posizione finisce
  in tutti i cataloghi.
- **Etichette dei pulsanti**: una riga sola, schiacciata in orizzontale
  fino alla larghezza del pulsante. Fino a 15 caratteri circa si leggono;
  oltre i 20 no. Nella revisione di `it.po` i nomi delle magie sono stati
  tenuti entro questa misura. Le magie sono in ordine alfabetico del nome
  tradotto, e ogni clic sulla freccia scorre di una riga.
- **Finestra Nuovo per le prove** (800×600, griglia 4×4, freccia giù a
  (400, 436), "Apri" a (120, 448)): ogni clic sulla freccia scorre di una
  riga. Dopo 4 righe l'orologio è a (628, 174); dopo 12 la scuola è a
  (172, 174); dopo 18 la lavagna è a (172, 74) e i quaderni sono nella
  terza riga (pentagrammato, a righe, a quadretti a x = 324, 476, 628).
- **Documentazione italiana**: l'HTML è il sorgente, i `.txt` si fanno con
  `lynx -dump -nolist -width=80 -display_charset=utf-8
  -assume_charset=utf-8 html/X.html > X.txt` in `docs/it`.
  `docs/Makefile` userebbe `links`, che sull'host non c'è. Immagini e
  documenti inglesi si raggiungono con `../../html/…`, come nella cartella
  installata (`share/doc/tuxpaint/it/html`).
- **SVG per Starter e modelli**: proporzioni 608×472. La 0.9.22 li
  disegna alla dimensione della tela, quindi restano nitidi a ogni scala.
  Per vederli senza Tux Paint, sull'host ci sono pycairo e librsvg via
  `gi` (`Rsvg.Handle.render_document`).
- **Cataloghi allineati** (2026-11-02): `devtools/po/update-po.sh`, poi
  `devtools/po/fill-from-upstream.sh ~/.cache/tp-upstream/po`, cioè la
  cartella `src/po` del Tux Paint di oggi (git.code.sf.net, commit
  `8ec0dc4` del 2026-09-21, scritto in `~/.cache/tp-upstream/COMMIT`).
  Lo script usa i loro messaggi tradotti come compendio di `msgmerge`:
  riempie un messaggio che qui non ha traduzione, ma **non sostituisce
  una voce "fuzzy" con lo stesso msgid**, né una traduzione già fatta. Per
  cambiarle si toglie prima la voce, o la si modifica a mano. Quattro
  frasi del fork ("your entire picture") vengono dalla stessa frase
  dell'originale con "the entire picture". Per contare le traduzioni,
  dopo l'allineamento, serve `msgfmt --statistics`: `msgcmp` non conta più
  le voci vuote, che ora ci sono tutte.
- **Frasi del fork nelle altre lingue**: tradotte in 52 lingue, quelle
  che si potevano fare con sicurezza, con le parole che ogni catalogo usa
  già per gli stessi strumenti. Restano in inglese nelle altre (lingue
  poco diffuse) e Punto croce in bs, mk, sq. Nelle etichette, i nomi più
  lunghi di Punto croce vanno su due righe (lituano, russo, ucraino,
  slovacco, rumeno).
- **Lanciatore**: `devtools/po/update-desktop.py` rifà
  `src/tuxpaint.desktop` dai cataloghi, come `intltool-merge -d`; dai
  cataloghi di prima dà lo stesso file. Va rilanciato dopo ogni modifica
  ai `.po` di nome, commento o azione.
- **Cartina dell'Italia** (`starters/worldmap_italy.svg` e `-back.svg`):
  `devtools/content/italy_map.py REG.shp PAESI.shp`, con i confini Istat
  generalizzati delle regioni al 1° gennaio 2026 (`Limiti01012026_g.zip`,
  UTM 32N, CC BY 4.0) e i paesi di Natural Earth 1:10m (pubblico dominio),
  entrambi in `~/.cache/tp-map/`. I confini tra regioni sono spezzati in
  archi tra i punti dove si incontrano tre confini, e ogni arco si
  semplifica una volta sola (Douglas-Peucker, 0,25 px): le due regioni
  restano attaccate e il secchiello non esce. San Marino è un buco tra due
  regioni, con la riga sottile. Il secchiello (magia "Riempi") separa mare
  azzurro, paesi vicini grigi e regioni bianche anche dove le righe non ci
  sono; i paesi vicini, senza confini tra loro, si riempiono tutti insieme.
- **Prove della cartina a 800×600**: nella finestra Nuovo, dopo 16 clic
  sulla freccia giù, la cartina è a (628, 174). Nell'elenco delle magie in
  italiano, dopo 17 clic sulla freccia giù (752, 410), "Riempi" è a
  (727, 328); la Toscana a (340, 160), l'Umbria a (382, 177). In
  Tux Paint, la tela comincia a x = 96.
- **Errori nelle traduzioni di altri, visti di passaggio** e lasciati
  (TODO): in `hr.po` la magia Gesso si chiama "Izmješaj" ("mescola"); in
  `zh_CN.po` la descrizione a pennello di Fumetto parla di gesso; in
  `ko.po` la frase di Blocchi a tutta immagine è approssimativa.

## 5quinquies. Strumenti e magie: note (2026-11-01)

- **Provare un plugin senza interfaccia**: `devtools/magic-test/magic_run`
  (README accanto) carica il `.so`, prende un'immagine come tela, fa clic,
  trascinamenti o la modalità a tutta immagine con copie delle funzioni
  dell'API di Tux Paint, e salva un BMP. Si compila sull'host (in
  `~/.cache/tp-magic/`); con `-fsanitize=address` sia lui sia i plugin
  danno il controllo della memoria, senza finestre. Va collegato a
  SDL_mixer con `--no-as-needed`: i plugin la usano attraverso il
  programma che li carica.
- **Modalità a tutta immagine**: un plugin la offre con `MODE_FULLSCREEN`
  in `modes()` (per strumento: Drip resta solo a pennello) e una
  descrizione per modalità in `get_description()`. In `click()` con
  `mode == MODE_FULLSCREEN` lavora su tutta la tela da `last` e aggiorna
  tutto il rettangolo; Tux Paint mostra da solo i pulsanti delle due
  modalità.
- **Rettangolo da aggiornare**: Tux Paint lo azzera prima di ogni
  `drag()`; l'altezza si calcola dal suo `y`. L'esempio della guida
  sbagliava (`- update_rect->h`) e l'errore era passato a 10 plugin.
- **Punto croce**: quadretti di 8 px allineati alla tela, quindi i tratti
  successivi combaciano; un quadretto è ricamato se almeno 1/16 dei suoi
  pixel non è bianco (≥ 235 sui tre canali), col colore medio di quelli
  (in luce lineare). Con 1/3 le linee sottili sparivano, con 1/8 si
  interrompevano a ogni gradino. L'aspetto del quadretto (copertura e
  ombre delle due diagonali, fori della tela) si calcola una volta in
  `init()`.
- **Schiuma**: tiene le bolle bianche ridimensionate (`foam_white[]`) e ne
  fa copie tinte a ogni `set_color()`; `set_color()` arriva prima di
  `switchin()`, quando le bolle possono ancora non esserci.
- **Puzzle**: lato dei pezzi = 5 × MCD dei lati della tela se sta tra 1/20
  e 1/8 del lato corto, se no 1/12 (a 608×472: 40 px come prima). A tutta
  immagine i pezzi più stretti a destra e in basso si scambiano solo tra
  loro (quattro gruppi: interi, colonna, riga, angolo).
- **Mezzatinta**: per ogni pixel e inchiostro, il punto della griglia
  ruotata in cui cade, il colore medio attorno al centro del punto (9
  campioni) e un punto di raggio `0,58 × passo × √quantità`, con bordo
  morbido; gli inchiostri moltiplicano la luce della carta. Il pennello
  resta a quadrati di 16 px su griglia di 8, che ora combaciano.
- **Suoni**: `devtools/content/magic_sounds.py` (numpy, oggenc) li sintetizza
  con rumore filtrato a fasce e toni smorzati, normalizzati a −4 dB di
  picco come gli altri; seme fisso e `--serial` di oggenc, quindi i file
  escono identici. Ogni pezzo finisce con 5 ms di dissolvenza: i tagli
  netti si sentono come clic (si vedono nello spettrogramma di ffmpeg,
  `showspectrumpic`).
- **Tastiera a schermo**: scritte negli angoli con un secondo font a 6/10
  della misura (`osk_fonty_small`, aperto da `open_osk_font()`), solo
  senza Maiuscolo né AltGr attivi; non per le lettere (`shiftcaps`), né
  per i caratteri uguali a quello già mostrato. `--onscreen-keyboard-layout`
  vuole il nome del file con `.layout`.
- **Caratteri oltre U+FFFF**: la tastiera li manda come coppia surrogata
  (due `SDL_KEYDOWN`), `im_event_c()` li ricompone se `wchar_t` è a 32
  bit. I font di Testo ed Etichetta su questo sistema sono di tipo
  SDL_ttf (`typ` 1), quelli dell'interfaccia SDL_Pango (`typ` 0); SDL_ttf
  2.0.11 disegna solo caratteri a 16 bit, quindi `wcstou16()` mette
  U+FFFD. Provato con un layout di prova con un tasto `U1D11E` (chiave di
  violino): nel testo arriva U+1D11E (prima U+D11E, una sillaba coreana).
- **Etichette su due righe** (`do_render_tool_label()`): solo strumenti,
  magie e forme; una riga se larga al più 1,5 volte il pulsante, se no
  due a 10 punti (`label_font`), spezzate allo spazio che rende più corta
  la riga più lunga, con passo 4/5 dell'altezza della prima. L'icona
  piccola (`make_small_icon()`, `img_tools_small[]` e simili) si fa
  quando l'etichetta è più alta di una riga, e per gli strumenti viene
  ricolorata come l'altra.
- **Insidia di sdl12-compat**: per le superfici di SDL_Pango (maschere
  R=`ff000000`… A=`000000ff`) `SDL_GetRGBA()` legge i canali come ARGB:
  l'alfa torna 0 e finisce nel blu. `SDL_MapRGBA()` sbaglia allo stesso
  modo, quindi chi legge e riscrive (per esempio `thumbnail2()`) non se
  ne accorge; chi confronta valori decodificati sì. Con superfici dello
  stesso formato conviene confrontare i bit grezzi (`p & Amask`).
- **Prove senza finestra**: con `SDL_VIDEODRIVER=dummy` anche il testo di
  SDL_Pango risulta senza alfa, quindi non dice nulla sul disegno.
  `timeout` manda SIGTERM, che Tux Paint ignora: usare `timeout -s KILL`.

## 6. Prossimi passi consigliati

Le prove a mano 2 e 3 riguardano lavoro già in `master`, unito su
richiesta dell'utente prima di farle: un difetto trovato lì si corregge su
un branch nuovo.

1. Provare a mano `content/l10n-more`: la cartina dell'Italia (finestra
   Nuovo, poi la magia Riempi), OPTIONS e FAQ in italiano
   (`docs/it/html/`), e magari Tux Paint in un'altra lingua
   (`--lang=dutch`, …) per Punto croce. Poi unire in `master` con
   avanzamento rapido.
2. Provare a mano la finestra ridimensionabile e Alt+Invio, anche con un
   dialogo aperto (Apri, Nuovo, il selettore colore, la richiesta
   d'uscita, una presentazione), e le icone delle magie a 1600×1200.
3. Provare a mano le magie cambiate e Punto croce (anche a tutta
   immagine), la Schiuma con un colore, la tastiera a schermo
   (`--onscreen-keyboard`), e ascoltare i suoni nuovi (Mezzatinta, Puzzle,
   Colore e bianco, Punto croce).
4. Provare a mano i timbri nuovi e gli Starter e i modelli per la scuola
   (finestra Nuovo, dopo i colori).
5. Usare Tux Paint con `./dev.sh run` e annotare cosa non convince.
6. Suddividere `src/tuxpaint.c` (`TODO.md`, P3): solo con un piano a
   parte, magari partendo dall'unione dei tre dialoghi gemelli.

---

## 7. Diario

Le voci si aggiungono in fondo, in ordine cronologico. Formato:
`### AAAA-MM-GG — titolo` seguito da cosa è stato fatto, cosa si è scoperto,
cosa resta aperto.

### 2002-06-14 → 2014-08-05 — Storia upstream (sintesi da CHANGES.txt)

Sviluppo originale di Bill Kendrick (New Breed Software) e Tux4Kids, con
molti contributori. Tappe principali:

| Data | Versione | Novità principali |
|------|----------|-------------------|
| 2002-06-14 | — | Prima versione di Tux Paint |
| 2002-11-12 | 0.9.0 | Prima release della serie 0.9 |
| 2004-09-28 | 0.9.14 | Immagini "Starter" immutabili, lockfile, opzione `--nosave` |
| 2005-11-25 | 0.9.15 | Avvio molto più rapido, minor uso di memoria, nuovo sistema di tinta dei timbri |
| 2006-10-19 | 0.9.16 | Presentazione "Slides", testo Unicode 16 bit |
| 2007-07-01 | 0.9.17 | `--hidecursor`, autosave, orientamento verticale, timbri SVG, libpaper |
| 2007-11-17 | 0.9.18 | Nuove finestre Nuovo/Apri, contagocce, ottagono, **API plugin Magic** |
| 2008-02-25 | 0.9.19 | Molte nuove localizzazioni |
| 2008-06-26 | 0.9.20 | Aggiornamenti di traduzioni |
| 2009-06-28 | 0.9.21 | Nuovi Starter e strumenti Magic, testo bidirezionale (FriBiDi) |
| 2014-08-05 | 0.9.22 | Strumento **Label**; Magic: Blinds, Pattern, Perspective, Mosaic, Tiles, Zoom, Puzzle, Rainbow, Symmetry, Wet Paint, Xor; **Template**; accessibilità (`--mouse-accessibility`, `--onscreen-keyboard`, `--keyboard`, joystick); metadati inclusi nel PNG; supporto touchscreen; ~40 nuove lingue (tra cui valenciano) |

### 2018-10-16 — Import nel fork LliureX

- Commit `5550718 "Ported from Ubuntu"` di jrpelegrina: import integrale del
  sorgente Tux Paint 0.9.22 come distribuito da Ubuntu, nel repository
  `github.com/lliurex/tuxpaint`.
- Nessuna modifica successiva nel repository.

### 2026-10-29 — Analisi iniziale e impostazione dei file di progetto

Fatto:
- Letta la documentazione di progetto in `docs/` (README, INSTALL, OPTIONS,
  EXTENDING, FAQ, CHANGES, custom/README) e lo `tuxpaint.spec`.
- Analizzata la struttura del repository e contate le risorse incluse
  (vedi §2).
- Verificate le dipendenze di build nella shell di VS Code (vedi §4): mancano
  le librerie SDL 1.2; l'ambiente è un runtime Flatpak con GCC 15.2.
- Censiti i marcatori FIXME/TODO nel sorgente (167) e ricavate da questi
  alcune idee per `TODO.md`.
- Creati `HANDOFF.md` (questo file), `TODO.md` e `ASIS.md`.

Scoperte:
- Il repository è una copia "congelata" dell'upstream 2014, senza modifiche
  LliureX visibili oltre all'import.
- La build richiederà un ambiente dedicato e probabilmente correzioni per GCC
  moderni (§5).

Aperto:
- Strategia fork/upstream da decidere.
- Prima build non ancora tentata.

### 2026-10-29 — Decisioni su strategia e obiettivo del fork

Fatto:
- **Strategia**: si resta sulla 0.9.22 con SDL 1.2 e la si corregge; niente
  riallineamento all'upstream né porting SDL2 per ora.
- **Obiettivo**: sperimentazione personale, solo Linux.
- Le due voci sono passate da `TODO.md` ad `ASIS.md`.
- `TODO.md` aggiornato di conseguenza:
  - il porting SDL2 è sceso a P3, con la nota che per ora è escluso;
  - CI, AppStream, pacchetti e rimozione di OpenCandy sono passati in una
    nuova sezione "Distribuzione (fuori obiettivo per ora)";
  - aggiunta l'idea di un plugin Magic di prova, partendo da
    `magic/docs/tp_magic_example.c`.
- Aggiornati §1, §5 e §6 di questo file.

Aperto:
- Prima build non ancora tentata: è il prossimo passo (§6).

### 2026-10-29 — Ambiente di build: scelto l'host

Fatto:
- **Decisione**: la build si fa direttamente sull'host, non in un container.
- Verificato che dalla shell di VS Code (runtime Flatpak) si raggiunge l'host
  con `flatpak-spawn --host`.
- Censito l'host: Debian 13.7, GCC 14.2, make, pkg-config, gettext, libpng
  e zlib già presenti.
- Ricavate dal Makefile le librerie davvero necessarie su Linux: SDL 1.2,
  SDL_image, SDL_mixer, SDL_ttf, SDL_Pango, png, z, paper, fribidi, librsvg e
  cairo, più gperf. Lo `.spec` elenca anche GTK2/libgsf/libxml2, ma servono
  solo per Windows.
- Tutti i pacchetti mancanti sono disponibili in Debian 13, compreso
  `libsdl-pango-dev`: il rischio "SDL_Pango non più disponibile" è chiuso.
- Comando di installazione documentato in §4.

Scoperte:
- GCC dell'host (14.2) è diverso da quello del runtime Flatpak (15.2): per
  compilare si usa sempre quello dell'host.
- `sudo` sull'host chiede la password, quindi i pacchetti li installa
  l'utente.

Aperto:
- Installazione dei pacchetti (in attesa dell'utente), poi la prima build.

### 2026-10-29 — Prima build riuscita sull'host

Fatto:
- L'utente ha installato i pacchetti; verificati con `pkg-config` sull'host.
- **Build 1** (`make -k`): 12 errori di due soli tipi, tutti dovuti a GCC 14
  che ora tratta come errori dei vecchi warning:
  - `-Wincompatible-pointer-types` in `src/tuxpaint.c`: alla funzione
    `load_starter_helper()` si passava `&IMG_Load`, che accetta
    `const char *`, mentre il parametro voleva `(char *)`.
  - `-Wimplicit-function-declaration` in `src/parse.gperf`:
    `show_version()` e `show_usage()` si usavano senza prototipo.
  - Tutti i 47 plugin Magic compilavano già senza errori.
- Correzioni:
  - i loader interni passano a `const char *`;
  - i prototipi sono spostati in `src/parse.h`, condiviso tra parser e
    `tuxpaint.c`. Tolte le dichiarazioni duplicate in `tuxpaint.c`, per non
    far scattare `-Wredundant-decls`.
- **Build 2**: compilazione ok, link fallito con
  `undefined reference to symbol 'log@@GLIBC_2.29'` (DSO missing). Corretto
  aggiungendo `-lm` a `linux_ARCH_LINKS` nel Makefile.
- **Build 3** e poi **build da zero** (`make clean && make -j4`): riuscite,
  ~12 s, 0 errori, 96 warning. Prodotti: binario `tuxpaint`, 47 plugin,
  119 file `.mo`.
- Analizzati i warning: individuati bug veri e probabili, registrati in
  `TODO.md`.
- Creato `.gitignore` per gli artefatti di build; `git status` torna pulito
  (restano solo le modifiche volute).
- Documentati in §4 i comandi di build e le insidie dell'installazione:
  percorsi fissati nel binario, `COMPLETIONDIR` in `/etc`.

Scoperte:
- **Bug reale**: doppio `free(unc_buff)` in `src/tuxpaint.c:21399/21403` e
  `:21456/21460`. Succede quando fallisce il recupero dello sfondo o del
  primo piano incorporati in un PNG salvato, e può causare un crash.
- Il warning `-Wsizeof-pointer-memaccess` in `src/parse.gperf:295` è un
  falso positivo: copia di proposito il valore di un puntatore.
- `make clean` non cancella file versionati: `obj/.keep` resta.

Aperto:
- Commit delle modifiche (non ancora fatto).
- Installazione e primo avvio del programma.

### 2026-10-29 — Script di sviluppo, installazione in ~/.local, primo avvio

Fatto:
- Simulato `make install` con `make -n`: con `PREFIX=$HOME/.local` e
  `COMPLETIONDIR` sovrascritto, nessun file finisce fuori da `~/.local`.
  `install-gnome` e `install-kde-icons` venivano saltati, perché
  `gnome-config`/`kde-config` non esistono più.
- Creato [dev.sh](dev.sh) con i comandi `build`, `install`, `run`,
  `uninstall` e `clean` (dettagli in §4). Se gira nel sandbox Flatpak si
  riesegue sull'host.
- `./dev.sh install`:
  - ricompilazione da zero con il nuovo `PREFIX`;
  - installati binario, 47 plugin, 15 MB di dati, lanciatore con
    `Exec=/home/paolo/.local/bin/tuxpaint`, icone hicolor, completamento
    bash e `tuxpaint.conf`, tutto in `~/.local`.
- Prova di avvio sull'host: `timeout 10 tuxpaint --windowed --nolockfile`
  ha girato 10 s senza crash, chiuso da `timeout`; nessun processo rimasto.
  Messaggi innocui:
  - nessun joystick;
  - avvisi libpng su profili colore iCCP/bKGD di alcuni PNG dei dati;
  - `current_id.txt` mancante, normale al primo avvio.
- Il primo avvio ha creato `~/.tuxpaint/current_id.txt`.

Scoperte:
- Nessuna identità git configurata: i commit richiedono `user.name` e
  `user.email` (§5, punto 7).
- Il completamento bash viene installato come `tuxpaint-completion.bash`.
  Il caricamento automatico di bash-completion cerca un file `tuxpaint`,
  quindi non si attiva da solo.
- Il primo comando di prova ha superato il timeout di 60 s dello strumento,
  anche se `timeout 10` aveva chiuso Tux Paint. Causa non chiarita: forse un
  processo figlio (audio?) teneva aperto l'output. Da tenere d'occhio.

Aperto:
- Commit (serve l'identità git).
- Prova manuale degli strumenti da parte dell'utente.

### 2026-10-29 — Primi commit

Fatto:
- Configurata l'identità git solo per questo repository, su scelta
  dell'utente: `Paolo <lymphalab@outlook.it>`.
- Creato il branch `build/host-debian13` da `master`.
- Commit:
  - `b92a7d1` — Fix build with GCC 14 and current linkers (`src/tuxpaint.c`,
    `src/parse.h`, `Makefile`, `.gitignore`);
  - `93fc7df` — Add dev.sh to build, install and run for development;
  - commit successivo — file di progetto `HANDOFF.md`, `TODO.md`, `ASIS.md`.

Aperto:
- Unire il branch in `master` (decisione dell'utente).
- Nessun push su `origin` (`github.com/lliurex/tuxpaint`, repository di
  LliureX).

### 2026-10-29 — UI scalabile con la finestra: fase 1 (schermata principale)

Richiesta dell'utente: le icone funzionali devono ingrandirsi in proporzione
alla finestra, perché su schermi ad alta risoluzione restano minuscole.

Analisi:
- Lo schermo dell'utente è 2560×1600 (circa 224 dpi), GNOME al 200%, con
  `xwayland-native-scaling`. Tux Paint gira via XWayland a pixel fisici,
  quindi una finestra 800×600 appare grande come una 400×300 e i pulsanti
  da 48 px sono larghi circa 5 mm.
- La finestra ha una dimensione fissa per la sessione (`windowsize`, oppure
  schermo intero nativo). "Proporzionale alla finestra" vuol dire quindi
  calcolare la scala all'avvio.
- Nel codice ci sono centinaia di costanti di design. Circa 200 riguardano
  la schermata principale e circa 230 le finestre di dialogo.
- Si poteva ingrandire tutta la finestra con `SDL12COMPAT_WINDOW_SCALING`
  di sdl12-compat: verificato che funziona (800×600 diventa 1600×1200), ma
  la tela perderebbe risoluzione.
- **Decisione dell'utente**: scala nativa dell'interfaccia, a fasi.

Fatto (branch `feature/ui-scaling`, commit `d346e60`):
- Modello e convenzioni descritti in §5bis.
- Sostituzioni nelle funzioni di disegno fatte con script a coppie esatte
  (con controllo del numero di occorrenze), poi riviste nel diff.
- Correzioni emerse durante il lavoro:
  - l'icona di "Colori XOR" (PNG a palette) diventava bianca una volta
    scalata, perché `thumbnail2()` non copia la palette: ora viene prima
    convertita in RGBA;
  - il ciclo fisso 48×48 in `search_label_list` scriveva oltre il bordo
    del pulsante del colore personalizzato.
- Creati gli strumenti di test in `devtools/ui-test/` (commit `22ba70e`) e
  un binario di riferimento in `~/.cache/tuxpaint-baseline`.

Verifiche:
- Build: 0 errori, 52 warning in `tuxpaint.c` come prima.
- **800×600**: le otto schermate (pennello, timbri, linee, forme, testo,
  etichetta, magie, gomma) sono identiche al pixel al binario originale.
- **1600×1000** (pulsanti da 80 px) e **2400×1500** (120 px): schermata
  principale proporzionata; etichette, titoli, palette, area di Tux e
  icone sono a posto.
- Tela: clic con un pennello grande in (800,400), (300,200), (1400,700) e
  (170,10); i punti cadono esattamente lì e un timbro risulta centrato in
  (600,550).

Scoperte:
- **Testo ed Etichetta non si attivano**, anche col binario originale:
  problema preesistente, registrato nel TODO (sezione Bug).
- Tux Paint ignora SIGTERM (chiede conferma per uscire): è la causa del
  blocco di 60 s notato nella prova di avvio precedente.
- Altre insidie dei test automatici in §5bis.

Aperto:
- Fase 2 (finestre di dialogo, oggi sballate a scala > 1) e fase 3 (tastiera
  a schermo, cursori, schermata iniziale).
- Pulsanti audio dei timbri da verificare con l'audio attivo.

### 2026-10-29 — UI scalabile con la finestra: fase 2 (finestre di dialogo)

Fatto (branch `feature/ui-scaling`, commit `321db8b` e `a92db23`):
- Prima di toccare il codice, catture di riferimento di tutti i dialoghi
  col binario originale:
  - uscita, Apri (con selezione), presentazione (selezione multipla e
    riproduzione), Nuovo, selettore colore;
  - creata la cartella di prova `~/.cache/tuxpaint-test-canon` con due
    disegni salvati; si usa con `--savedir`, per non toccare
    `~/.tuxpaint`.
- Convertite circa 450 righe di dialoghi, con script a coppie esatte:
  - Apri, Nuovo e presentazione condividono le stesse regole;
  - nelle richieste e nel selettore colore si scalano con `SCALED()` le
    espressioni di design (regole in §5bis).
- Lo script trovava inizialmente il prototipo di `play_slideshow`, che è su
  più righe, invece della definizione. Nessun danno: lo script si ferma
  prima di scrivere se una regola non trova corrispondenza.

Verifiche:
- Build: 0 errori, 52 warning in `tuxpaint.c` come prima.
- **800×600**: nove schermate dei dialoghi e otto della schermata
  principale identiche al pixel al binario originale.
- **1600×1200** (scala 2): tutti i dialoghi proporzionati e funzionanti.
  Anche i clic con coordinate raddoppiate funzionano: "No" nella richiesta,
  selezione delle miniature, Diapositive, Indietro, Mostra.
- **1600×1000** (scala 1,67, proporzioni diverse): richiesta d'uscita
  centrata. Il clic su "No", calcolato dal codice in (476,503), funziona e
  il selettore colore si apre correttamente.
- Selettore colore a scala 2: il colore scelto finisce nel pulsante del
  colore personalizzato e nel disegno.

Aperto:
- Fase 3: tastiera a schermo, cursori del mouse, schermata iniziale.
- Da provare a mano: la richiesta "Cancella" e i pulsanti audio dei timbri.
- Passo del mouse da tastiera non scalato (TODO, P3).

### 2026-10-29 — UI scalabile, fase 3, e correzione di Testo ed Etichetta

Fatto (branch `feature/ui-scaling`):
- **Fase 3** (`0c7bcf9`): cursori, schermata iniziale con la barra di
  avanzamento, tastiera a schermo (regole in §5bis).
- Strumenti di test (`5fa458d`): azioni `move` e `cursor` (XFixes),
  variabili `TP_START_WAIT`, `TP_LOG` e `TP_WRAP`.
- **Bug di Testo ed Etichetta** (`6d3f130`), su scelta dell'utente:
  - con `TP_WRAP="stdbuf -oL -eL"` è comparso il messaggio
    `child killed by signal 11`: il processo figlio che cerca i font,
    creato con `fork()` all'avvio (`FORKED_FONTS`), va in crash;
  - Tux Paint riceve quindi zero font: in `mainloop` si finisce nel ramo
    "Problem using fonts!", che rimette lo strumento precedente;
  - sull'host non ci sono `gdb` né `coredumpctl`, quindi niente traccia
    del crash. La causa probabile è la `fork()` di un processo che ha
    già avviato SDL2/X11 con i suoi thread;
  - correzione: `FORKED_FONTS` disattivato, i font si caricano in un
    thread. Un esperimento temporaneo l'aveva già confermato prima del
    commit.
- La correzione è stata applicata con `cherry-pick` anche al binario di
  riferimento, così i confronti coprono anche i pannelli di Testo ed
  Etichetta.

Verifiche:
- **Cursori**: 32×32 a scala 1 e 64×64 a scala 2, con punto attivo
  (4,28) → (9,57). La forma è corretta (mano, pennello).
- **Schermata iniziale**: identica al riferimento a 800×600; a scala 2
  loghi, scritte e barra di avanzamento sono raddoppiati.
- **Tastiera a schermo a scala 2**: tasti, scritte e icone scalati. Clic
  sulla tela e poi sui tasti c, i, a, o: compare "ciao" nel punto
  cliccato.
- **800×600**: le otto schermate della schermata principale (Testo ed
  Etichetta ora funzionanti) e le nove dei dialoghi sono identiche al
  riferimento.
- **Scala 2**: Testo ed Etichetta con elenco dei font, scorrimento e
  controlli corretti.
- Build: 0 errori. Warning in `tuxpaint.c` invariati (52); in `fonts.c`
  c'è una variabile inutilizzata in più (`font_scanner_pid`).

Scoperte:
- Una prova è stata sporcata dall'uso reale del mouse nella finestra di
  test. Ripetuta, è risultata identica. Annotato tra le insidie (§5bis).

Aperto:
- Prove manuali: richiesta "Cancella", pulsanti audio dei timbri.
- Rifiniture opzionali (TODO): `buttonsize`, finestra iniziale su HiDPI,
  icone più nitide, passo del mouse da tastiera.

### 2026-10-29 — Analisi del crash del processo figlio dei font

Richiesta dell'utente: analizzare il bug rimasto nel TODO, cioè perché il
processo figlio che cerca i font (`FORKED_FONTS`) va in crash.

Metodo, senza `gdb` sull'host:
- worktree di debug `~/.cache/tuxpaint-debug`, da `feature/ui-scaling`
  con `FORKED_FONTS` riattivato, compilato con `OPTFLAGS="-O0 -g"`;
- `devtools/ui-test/segv_backtrace.c`, caricato con `LD_PRELOAD`: al
  SIGSEGV stampa la pila delle chiamate;
- indirizzi tradotti con `addr2line`.

Risultato:
- Pila del crash nel figlio: `main` → `setup` → `run_font_scanner`
  (`src/fonts.c:1143`, cioè `exit(0)`) → `exit` → gestore di chiusura di
  `libgallium-25.0.7` (Mesa) → `pthread_join` → SIGSEGV.
- Quindi il figlio **completa** la scansione e **invia** i dati. Muore solo
  all'uscita, perché `exit()` esegue i gestori `atexit` ereditati dal
  genitore. Mesa ha registrato il suo quando SDL2 (sotto sdl12-compat) ha
  attivato OpenGL; nel figlio fa `pthread_join()` su un thread che dopo la
  `fork()` non esiste più.
- Il genitore (`receive_some_font_info`) vede `WIFSIGNALED` e scarta dati
  validi, per cui zero font.
- Nel 2014, con SDL 1.2 originale, Mesa non veniva caricato: per questo
  il bug non si vedeva.

Correzione mirata provata (solo nel worktree di debug):
- `exit(0)` → `_exit(0)` nel figlio. Dopo una `fork()` in un programma con
  più thread, il figlio deve uscire con `_exit()`.
- Risultato: nessun crash nel log.
- Non verificato: che Testo mostri i font. Le prove automatiche sono
  state disturbate: i clic simulati non arrivavano e sulla tela sono
  comparsi tratti disegnati a mano, quindi qualcuno stava usando il mouse
  nelle finestre di prova. Prove automatiche sospese.

Altro:
- `tp_session.py` reso più sicuro: porta in primo piano la finestra e
  non clicca se Tux Paint non è la finestra in cima sotto il puntatore.
- La prima prova del binario di debug non applicava la correzione:
  `addr2line` indicava la riga 1144 (indirizzo di ritorno), mentre
  `exit(0)` è alla 1143.

Aperto (decisione dell'utente):
- Sostituire la correzione attuale `6d3f130` (thread) con `_exit(0)` e
  `FORKED_FONTS` attivo. Prima va verificata a mano:
  `~/.cache/tuxpaint-debug/tuxpaint --windowed`, poi clic su Testo.

### 2026-10-30 — Correzione definitiva del crash dei font

Fatto:
- L'utente ha provato a mano il binario di debug con `FORKED_FONTS` e
  `_exit(0)`: il pannello di Testo compare, si scrive e si cambia font.
- Commit `b7021ac` su `feature/ui-scaling`: `_exit(0)` nel figlio
  (`src/fonts.c`, con commento sul perché) e `FORKED_FONTS` di nuovo
  attivo in `src/fonts.h`. Così si ritira il ripiego col thread
  (`6d3f130`).
- Binario di riferimento allineato: riportato a `ec9ebe3` con la sola
  modifica `_exit(0)`, così l'ordine dei font è uguale a quello della
  build nuova.
- Rimossi il worktree di debug e i file temporanei in `~/.cache`.

Problemi negli strumenti di test, scoperti e corretti:
- **Lo script poteva usare la finestra Tux Paint dell'utente**: prendeva
  la prima trovata. Probabilmente è la causa dei tratti a mano visti
  nelle catture del 2026-10-29: l'utente stava provando un suo Tux Paint.
  Ora usa solo quella con `_NET_WM_PID` uguale al processo avviato.
- **"mutter guard window"**: una volta il punto da cliccare era coperto
  da questa finestra (GNOME la mette sopra le finestre X quando in primo
  piano c'è una finestra Wayland). Il controllo aggiunto ieri ha fermato
  lo script senza cliccare.
- Verifiche rifatte col desktop fermo, su richiesta all'utente.

Verifiche:
- **800×600**: le otto schermate della schermata principale, compresi
  Testo ed Etichetta, sono identiche al riferimento. Dei nove dialoghi,
  otto sono identici. La richiesta d'uscita differisce solo per il tasto
  Annulla attivo: è l'effetto noto del primo clic, che a volte lascia un
  segno sulla tela, e non dipende dal codice.
- **Scala 2**: Testo con l'elenco dei font, scorrimento e controlli
  corretti.
- Build: 0 errori; warning come in origine (`fonts.c` 2, `tuxpaint.c` 52).

Aperto:
- Effetto del primo clic negli script: a volte il clic di messa a fuoco
  lascia un punto sulla tela. Si potrebbe eliminare con uno spostamento
  del puntatore prima del clic.

### 2026-10-30 — UI scalabile: rifiniture e unione in master

Fatto:
- **Mouse da tastiera**: passi proporzionali alla scala.
- **Opzione `buttonsize`**: parser, interpretazione, layout e
  documentazione (OPTIONS txt/html, man, `tuxpaint.conf`, `--usage`,
  completamento bash). Regole in §5bis.
- **Finestra iniziale su schermi grandi**: multiplo intero di 800×600
  (§5bis).
- Commit `c06ba8f` (codice e documentazione) e `ed4a2f8` (script di
  prova).
- Unione in `master` per avanzamento rapido (vedi §1).

Verifiche (desktop fermo, su richiesta all'utente):
- **800×600**: le otto schermate principali, i nove dialoghi e Timbro con
  l'audio attivo sono identici al riferimento.
- **`--buttonsize=48` a 1600×1000**: identico al pixel al programma
  originale alla stessa dimensione. `--buttonsize=64` a 1600×1000: layout
  regolare, con più righe.
- Valori non validi (`300`, `abc`): rifiutati con messaggio e codice
  d'uscita 91.
- **Finestra iniziale**: senza `windowsize` il programma originale apre
  800×600, il nuovo 1600×1200.
- **Pulsanti audio dei timbri a scala 2** (driver `dummy`): scalati, con
  Tux sotto di loro.
- **Richiesta "Cancella" a scala 2**, con un Cestino di prova: corretta.
  Dopo "No" i file restano e il Cestino di prova è vuoto.

Scoperte:
- **Barra nera sopra la miniatura nella richiesta "Cancella"**: c'è anche
  nel programma originale, quindi è un difetto preesistente. Registrato
  nel TODO (Bug, P3).
- Prove disturbate ancora una volta (rotella del mouse sopra la finestra
  di prova). Le prove definitive sono state fatte dopo aver chiesto
  all'utente di non usare il computer.
- Un comando con `cd ... && rm -rf *` è stato bloccato dal controllo di
  sicurezza prima di partire: se il `cd` fosse fallito, avrebbe cancellato
  la cartella corrente. Da ora nessuna pulizia con glob relativi: si usano
  solo cartelle di output nuove.

Aperto:
- Icone più nitide: servono nuove immagini (TODO, P3).

### 2026-10-30 — Icone più nitide: ingrandimento Lanczos

Fatto:
- **Ricerca di immagini ad alta risoluzione nell'upstream**: non ce ne
  sono. Il repository git ha in `data/images/tools/` solo PNG, e
  `brush.png` è ancora 40×30, come qui. L'upstream ha introdotto
  `buttonsize` e `auto` con la stessa formula su 800×600, ma ingrandisce le
  stesse bitmap.
- **Confronto degli algoritmi** con PIL sull'host, su icone reali a scala
  2 e 2,67: bilineare (l'attuale `zoom()`), bicubico, Lanczos, Lanczos con
  maschera di contrasto. Scelto Lanczos: bordi netti senza aloni; la
  nitidezza aggiuntiva è più una questione di gusto.
- `enlarge_lanczos()` in `src/tuxpaint.c`, usato da `scale_ui_image()`
  (commit `7cb40aa`).
- Il commit era finito per errore su `master`. Spostato sul branch nuovo
  `feature/sharper-icons` e riportato `master` a `f0f9036`
  (`git branch -f`, senza toccare i file).

Verifiche (desktop fermo, su richiesta all'utente):
- Build: 0 errori, warning invariati (52 in `tuxpaint.c`).
- **800×600**: le otto schermate principali sono identiche al riferimento;
  a scala 1 il codice nuovo non viene eseguito.
- **Prima e dopo a scala 2 (1600×1200) e 2,5 (2000×1500)**, schermata
  delle magie: icone e scritte nettamente più definite (Linee, Forme,
  Blocchi, Bordi di fili), senza aloni e con le sfumature dei pulsanti
  pulite.
- Una cattura a 2,5 si è fermata da sola con "STOP": sotto il puntatore
  non c'era nessuna finestra, perché la finestra era troppo alta per lo
  schermo. Ripetuta, è andata a buon fine.

Aperto:
- Unire `feature/sharper-icons` in `master`.
- Icone davvero nitide solo con nuove immagini (lavoro grafico, P3).

### 2026-10-30 — Documentazione di progetto aggiornata

Richiesta dell'utente: aggiornare tutta la documentazione di progetto e
prepararsi alla compressione del contesto.

Fatto:
- `HANDOFF.md`:
  - nuova §0 "Come riprendere": lettura, branch, sandbox/host, prove
    con desktop fermo, chiusura delle attività, lingue;
  - §1 riscritta: stato al 2026-10-30, tabella dei branch, tabella delle
    modifiche rispetto a 0.9.22 con i commit, cartelle di supporto in
    `~/.cache`;
  - §5bis riordinata. Tolte le istruzioni superate, per esempio "non
    automatizzare Cancella", che ora si prova col Cestino di prova.
- `TODO.md`: numeri di riga aggiornati nella sezione "Qualità del codice".
- `devtools/ui-test/README.md`: uso degli script, azioni e variabili.

Stato alla chiusura della sessione:
- Branch attivo `feature/sharper-icons` (icone Lanczos), da unire in
  `master`.
- Nessuna modifica in sospeso nel repository, a parte `.vscode/` di
  VS Code, che non va committata.

### 2026-10-31 — Barra nera nella richiesta "Cancella"

Richiesta dell'utente: lavorare sul bug trovato, cioè la voce della
sezione "Bug" del TODO.

Analisi:
- La richiesta "Cancella" di Apri mostra la miniatura del disegno, una
  freccia e il cestino. Se la miniatura è più alta di `SCALED(64)`,
  `do_prompt_image_flash_snd()` la riduceva con
  `thumbnail(img1, SCALED(80), SCALED(64), 1)`.
- In `thumbnail2()` la modalità `keep_aspect` calcola scala e spostamento
  come se il riquadro fosse quadrato. Con 80×64 e una miniatura di
  132×80, lo spostamento verticale risulta ((132 − 80) / 1,65) / 2 ≈ 15
  pixel invece di 8: il disegno scende, la parte bassa viene tagliata e le
  prime 15 righe non vengono scritte. Su una superficie senza alfa
  restano nere.
- Gli altri chiamanti con `keep_aspect` = 1 usano riquadri quadrati
  (timbri 40×40, pulsanti); i plugin Magia passano sempre 0. Il difetto
  di `thumbnail2()` è quindi latente: annotato nel TODO (Bug, P3), non
  corretto, per non rischiare differenze di arrotondamento a 800×600.

Fatto (branch `fix/erase-prompt-thumbnail`, da `feature/sharper-icons`):
- `4f95ada`: dimensione con le proporzioni giuste calcolata a mano dentro
  `SCALED(80)` × `SCALED(64)` e riduzione esatta con `keep_aspect` = 0.
  Nella stessa occasione `do_save()` crea la miniatura salvata con
  margine `SCALED(20)` invece di 20: era un residuo della UI scalabile, e
  a scala 2 Apri ridimensionava ogni volta la miniatura da 284×180 a
  264×160.
- `784729b`: script `devtools/ui-test/erase.sh`.
- Build installata in `~/.local`.

Verifiche (desktop fermo, con il permesso dell'utente):
- A 800×600, tra il riferimento e il nuovo binario, la richiesta
  "Cancella" cambia solo nella colonna delle immagini a destra (80×167
  pixel da (527, 152)): la barra nera è sparita e freccia e cestino
  salgono.
  Finestra Apri prima e dopo la risposta: identica.
- `dialogs.sh` a 800×600: tutte e 9 le catture identiche al riferimento.
- A scala 2: richiesta corretta, miniatura salvata 264×160.
- In tutte le prove, rispondendo "No", i 3 disegni restano e il Cestino
  di prova è vuoto.

Scoperte:
- Il primo tentativo cliccava "Cancella" a y=472, che è il bordo
  inferiore escluso del pulsante. La richiesta non compariva e il
  confronto dava "identico" senza errori. Annotato tra le insidie (§5bis);
  lo script usa y=448.

Stato alla chiusura:
- Branch attivo `fix/erase-prompt-thumbnail`, da unire in `master` insieme
  a `feature/sharper-icons` (avanzamento rapido).

### 2026-10-31 — Documentazione di progetto aggiornata

Richiesta dell'utente: aggiornare tutta la documentazione di progetto.

Fatto:
- Controllati `HANDOFF.md`, `TODO.md`, `ASIS.md` e
  `devtools/ui-test/README.md` dopo la correzione della richiesta
  "Cancella": stato, branch, prossimi passi e numeri di riga del TODO
  erano già aggiornati.
- §2: aggiunti alla mappa del repository i file del fork (`dev.sh`,
  `devtools/ui-test/`, file di progetto); `src/tuxpaint.c` è passato da
  ~24.100 a ~24.400 righe (anche in `TODO.md`).
- §5: il riferimento agli handle dei plugin mai scaricati puntava a una
  riga vecchia (1271); ora indica `magic_handle`, riga 1303.
- §1 e §4: warning ricontati con `./dev.sh clean` e una build da zero: 96,
  di cui 52 in `src/tuxpaint.c` e 13 in `src/im.c`, come alla prima build.
  Build reinstallata in `~/.local`: il binario installato coincide con
  quello compilato.

Stato alla chiusura: invariato. Branch attivo
`fix/erase-prompt-thumbnail`, da unire in `master` con avanzamento rapido.

### 2026-10-31 — Icone nitide e correzione di "Cancella" unite in master

Richiesta dell'utente: continuare con la sezione "UI scalabile con la
finestra" del TODO.

Fatto:
- `master` portato con avanzamento rapido (`git merge --ff-only`) a
  `fix/erase-prompt-thumbnail`, che contiene anche
  `feature/sharper-icons`. Nessun push.
- Nessuna nuova prova a schermo prima dell'unione: le modifiche erano già
  verificate sui loro branch. Le icone Lanczos con `regress.sh` e
  `dialogs.sh`: a 800×600 identiche al riferimento, a scala 2 e 2,5 nitide.
  La correzione di "Cancella" con `dialogs.sh` ed `erase.sh`. La
  correzione tocca solo la richiesta e la miniatura salvata, che a 800×600
  non cambia (`SCALED(20)` = 20), quindi non può influire sulla schermata
  principale.
- `TODO.md`: tolta la voce dell'unione. Nella sezione resta solo la voce
  P3 sulle icone davvero nitide, che richiede immagini nuove.

Stato alla chiusura:
- Branch attivo `master`; `fix/erase-prompt-thumbnail` e
  `feature/sharper-icons` sono già uniti. Il prossimo lavoro va su un
  branch nuovo.
- La sezione "UI scalabile con la finestra" è chiusa per tutto ciò che si
  può fare via codice.

### 2026-10-31 — Schermo intero

Richiesta dell'utente: "manca la funzionalità per impostare a tutto
schermo l'applicazione".

Situazione trovata:
- Lo schermo intero c'era solo all'avvio (`fullscreen=yes`,
  `fullscreen=native`, `--native`): niente comando mentre il programma è
  aperto, finestra non ridimensionabile né massimizzabile.
- `fullscreen=yes` senza dimensione apriva 800×600 e lo lasciava
  ingrandire a sdl12-compat: interfaccia sfocata.
- F11 era già usato (finestra Apri, mouse da tastiera).

Scelta dell'utente fra tre proposte: **Alt+Invio + avvio nitido**.
Scartate: solo avvio a schermo intero; cambio al volo con interfaccia
ridisegnata, lavoro grande e rischioso, rimasto nel TODO come P3.

Fatto (branch `feature/fullscreen`, da `master`):
- `3f43e1a`: `toggle_fullscreen()` e `poll_event()`, usata dai 9 cicli di
  eventi; `fullscreen` senza dimensione → risoluzione dello schermo;
  `native` con la dimensione del desktop; azione "Full screen"/"Schermo
  intero" nel lanciatore; `dev.sh` corregge anche il suo `Exec=`; OPTIONS
  (testo e HTML), pagina di manuale e `tuxpaint.conf` aggiornati.
- `65874c7`: `--fullscreen` e `-f` senza valore accettati.
- `77a1be3`: `tp_session.py` con azioni `key` e `info` e dimensione `-`.
- Build installata in `~/.local`. Warning invariati (52 in
  `src/tuxpaint.c`).

Verifiche (desktop fermo, con il permesso dell'utente; diverse prove
perché a schermo intero la finestra copre tutto):
- A 800×600 `regress.sh` e `dialogs.sh`: tutto identico al riferimento.
- Da finestra 1600×1200: Alt+Invio → 2560×1600 con l'immagine in
  x=213…2345; di nuovo Alt+Invio → finestra identica a prima. Tenuto
  premuto 1,5 s cambia una volta sola. Funziona anche con un dialogo
  aperto. Un clic a schermo intero sceglie il pulsante giusto.
- Avvio con `--fullscreen` e con `--fullscreen=native`: stessa schermata a
  2560×1600, nitida, pulsanti da 128 px, clic corretti.
- Senza opzioni la finestra è ancora 1600×1200.

Scoperte:
- `--fullscreen` senza valore usciva con "needs a value": le prime prove
  di avvio a schermo intero non trovavano la finestra perché il programma
  non partiva affatto. Difetto già nella 0.9.22.
- Avvio nativo e Alt+Invio: la finestra diventava di 2×2 pixel al centro
  dello schermo, perché la modalità era chiesta a 0×0. Chiedendo la
  dimensione del desktop la finestra restava grande quanto lo schermo, e
  mutter la teneva a tutto schermo. Si è deciso che in questo caso
  Alt+Invio non fa nulla.
- Nel primo script la richiesta a `sed` per `Exec=` non funzionava: con
  `|` come separatore, `\|` non vale come alternativa. Usate due
  espressioni.

Da fare: prova a mano della voce "Schermo intero" dal menu dell'icona,
che le prove automatiche non coprono; poi unire in `master`.

### 2026-10-31 — Qualità del codice: FIXME nel sorgente

Richiesta dell'utente: lavorare sulla sezione "Qualità del codice (dai
FIXME nel sorgente)" del TODO.

Fatto (branch `quality/fixme`, da `feature/fullscreen`, per avere
installata una build con lo schermo intero), voce per voce:
1. **Plugin Magia, 512 handle mai scaricati** (`3ff7788`): array che
   crescono, plugin scaricati in `cleanup()`. Leggendo il caricatore:
   nessun controllo dei limiti, e `strcpy(strchr(objname, '.'), "")` con
   un file senza punto (es. `README` in `~/.tuxpaint/plugins/`) mandava in
   crash l'avvio. Il primo tentativo usciva sempre con "Out of memory":
   `grow_magic_arrays(0)` non allocava `magics`. L'ho visto subito con
   la prova senza finestra; corretto prima di proseguire.
2. **Leak dei font segnalati da Valgrind** (`bc2b4c7`): con il processo
   figlio dei font, `cleanup()` liberava solo l'array dei puntatori. Il
   primo tentativo, tenere i blocchi in variabili statiche, non serviva:
   il compilatore elimina variabili solo scritte, e ASan li dava ancora
   persi. Ora `free_received_font_info()` chiude i font e libera tutto.
   Corretto anche l'errore di lettura dal processo figlio.
3. **Barriera di memoria** nel thread dei font (stesso commit): aggiunta
   prima dei flag; chi legge aspetta già il thread con `SDL_WaitThread()`.
   Su Linux il thread non si usa.
4. **Stampa PostScript** (`b96ae5d`): centratura già giusta, misurata;
   libpaper lasciata dov'è; trovati e corretti il crash con un formato
   carta sconosciuto e l'esito sbagliato dei comandi di stampa. Il
   confronto col riferimento conferma che i due difetti c'erano.
5. **`get_fname()`** (`fe89e9c`): lasciata com'è (30 chiamate, nessuna in
   un ciclo di disegno). Esaminando i chiamanti: `load_template()`
   cercava i modelli personali nella cartella sbagliata.
6. **`--lang help` dalla tabella** (`a2c83b1`).
7. **Barra di avanzamento**: il FIXME non chiedeva di riattivare la
   barra, che funziona, ma `eat_sdl_events()`. Lasciata spenta, con il
   motivo nel codice (`fe89e9c`).
8. **Ordinamento senza maiuscole** (`902e403`).
9. **Suddividere `src/tuxpaint.c`**: non fatto, resta nel TODO.

Difetti trovati lungo la strada, oltre a quelli già detti:
- `13ff28c`: nella finestra Nuovo un'immagine bitmap veniva nascosta da
  qualunque SVG il cui nome cominciasse con il suo: `frame_heart.png`
  non compariva mai, per via di `frame_hearts.svg`.
- `4a09172`: i modelli personali non si aprivano mai. `first_template`
  veniva spostato sui modelli di sistema e quelli personali erano presi
  per Starter. È saltato fuori nella prova a schermo: con il primo
  correttivo la tela restava bianca anche nella versione nuova.

Verifiche:
- Senza finestra (`SDL_VIDEODRIVER=dummy`, `--datadir` con un `README`
  tra i plugin): riferimento in crash (139), nuovo vivo dopo 20 s.
- `ps_check.sh`: margini uguali in tutti i casi; carta "foo" → A4 con
  avviso (il riferimento va in crash); `cat` e `gzip` riusciti, `false`
  e uscita 1 falliti (il riferimento dava fallite anche quelle riuscite).
- `--lang help`: due sole righe diverse, attese; stesse 175 coppie.
- A schermo (desktop fermo, con il permesso dell'utente, due giri):
  `regress.sh` e `dialogs.sh` a 800×600 identici al riferimento; modello
  personale magenta aperto dalla finestra Nuovo (prima: tela bianca);
  AddressSanitizer chiuso con Esci: nessun errore di memoria; leak
  scesi da 513 KB (master) a 379 KB, e i 260 KB in più che restano
  vengono dai plugin (con `nodlclose.so` scendono a 117 KB).
- Warning invariati (52 in `src/tuxpaint.c`). Build installata.

Da fare: unire in `master` (con `feature/fullscreen`); la suddivisione di
`src/tuxpaint.c` e i leak dei plugin restano nel TODO.

### 2026-10-31 — Qualità del codice: build senza warning, leak

Richiesta dell'utente: continuare con la qualità del codice. Fatta la
sezione dei warning e chiuse due voci P3 dei FIXME (leak dei plugin,
`magic_api_struct`). Branch `quality/warnings`, da `quality/fixme`.

Metodo: ogni warning guardato nel contesto, non solo zittito. Su 96, una
decina erano difetti veri; il resto codice inutilizzato o formati. Per i
leak: sessioni AddressSanitizer chiuse con Esci, poi con le pile complete
(`fast_unwind_on_malloc=0`) per vedere chi alloca dentro le librerie.

Difetti trovati, oltre a quelli dei warning (dettagli in ASIS):
- `load_embedded_data()`: oltre al doppio `free` del TODO, il blocco
  dello sfondo cercato col nome sbagliato, lo sfondo non assegnato nel
  caso comune (dimensione uguale alla tela), le maschere blu/verde
  scambiate. Con il doppio `free` erano quattro difetti nella stessa
  funzione.
- `trash()`: `mkdir(…, 0x777)` (esadecimale) e la copia a blocchi interi:
  con il Cestino su un altro filesystem il disegno cancellato andava
  perso del tutto.
- Leak a ogni uso: la finestra Apri perdeva una tela intera a ogni
  disegno aperto senza blocchi propri; il selettore colore uno schermo
  intero a ogni uso; i tre dialoghi il loro elenco di file.
- Piega: una superficie grande quanto la tela persa a ogni piega. Erba:
  l'immagine di 256×256 mai liberata (erano i ~260 KB "dei plugin").

Verifiche (desktop fermo, con il permesso dell'utente; cinque giri, due
ripetuti: una volta Tux Paint ha perso il primo piano e lo script si è
fermato da solo, un'altra il programma, rallentato dalle pile complete,
non ha fatto in tempo a uscire):
- `regress.sh` e `dialogs.sh` a 800×600: identici al riferimento.
- `erase.sh` con risposta Sì e Cestino in `/tmp`: vecchio → cartella
  `Trash` con modo 1565, disegno perso; nuovo → modi 0700, disegno intero.
- Disegno da un modello personale, salvato, poi modello tolto, riaperto e
  gomma: vecchio bianco, nuovo magenta.
- ASan, stessa sessione (Testo, Apri, Nuovo, selettore colore annullato,
  Esci): da 3,46 MB in 233 blocchi a 432 byte in 4, nessun errore.
- Senza finestra: `joystick-buttons-ignore` con un valore fuori
  intervallo, valido, e con 257 valori.
- librsvg: confronto pixel per pixel di vecchie e nuove chiamate sui 19
  SVG installati, a quattro dimensioni; nessuna delle due perde memoria.

Stato alla chiusura: branch attivo `quality/warnings`, installato. Resta
nel TODO la suddivisione di `src/tuxpaint.c`.

### 2026-10-31 — Contenuti e localizzazione

Richiesta dell'utente: la sezione "Contenuti e localizzazione" del TODO.
Fatte tutte e quattro le voci; branch `content/l10n`, da
`quality/warnings`. Per la documentazione l'utente ha scelto, tra le
opzioni proposte, manuale più EXTENDING (circa 80 KB su 190 KB di HTML
inglese); gli altri file italiani hanno solo un avviso.

Timbri: invece di copiare la raccolta nel repository (142 MB), un comando
la prende dal pacchetto Debian. Prima di integrarla ho controllato la
compatibilità con la 0.9.22: formati e parole chiave dei `.dat` sono tutti
noti al loader. Ne è uscito un difetto della 0.9.22, l'ultima riga di un
file senza a capo ignorata, che nella raccolta tocca un file. Le prove del
comando hanno trovato due difetti miei, corretti prima del commit: la
cartella temporanea non veniva cancellata (variabile `local` nella trap) e
una cartella qualsiasi veniva accettata e copiata tra i timbri.

`it.po` risultava completo, ma solo rispetto a un modello del 2014.
Rigenerato il modello (senza intltool, che manca), è emerso che il
campione di punteggiatura non ha mai funzionato in nessuna lingua (`\%` in
C). Le 292 stringhe rilette hanno dato 44 correzioni. Il `.po` upstream più
recente (0.9.23, 2017) ha le stesse traduzioni, quindi non serviva da
riferimento. L'azione "Schermo intero", scritta a mano nel `.desktop`, si
sarebbe persa al primo `update-po.sh`: ora è nel modello.

Starter e modelli: sei SVG generati da uno script, controllati prima con
librsvg e poi aperti in Tux Paint.

Verifiche (desktop fermo, con il permesso dell'utente; una sessione
ripetuta perché la finestra non era ancora in primo piano, e lo script si
è fermato senza cliccare):
- `regress.sh` e `dialogs.sh` a 800×600: identici al riferimento.
- Interfaccia in italiano: tutte le pagine delle magie a 800×600, poi la
  fine dell'elenco a 1600×1200 dopo aver accorciato i cinque nomi
  illeggibili. Un timbro mostra la descrizione italiana ("Una rosella
  adelaide."), la freccia passa alla categoria dopo.
- Finestra Nuovo: scuola, lavagna, quaderno a righe, a quadretti,
  pentagrammato e orologio aperti; l'orologio è nitido anche a scala 2.
- Senza finestra: l'avvio con la raccolta completa resta immediato.

Stato alla chiusura: branch attivo `content/l10n`, installato con i timbri.
Nuove voci P3 nel TODO: il resto della documentazione italiana, gli altri
cataloghi da allineare, etichette su due righe, una cartina dell'Italia.

### 2026-11-01 — UI scalabile: unione, ridisegno alla nuova dimensione, icone SVG

Richiesta dell'utente: la sezione "UI scalabile con la finestra" del
TODO. Alle tre domande (unione, ridisegno, icone) l'utente ha risposto:
prova a mano fatta, quindi unire; finestra ridimensionabile più Alt+Invio
nitido; cornici dei pulsanti più icone di strumenti e forme.

- **Unione**: `master` portato con avanzamento rapido a `content/l10n`
  (`0787bf2`), nessun push.
- **Ridisegno** (branch `feature/resizable`): il caricamento delle cose
  fatte per la dimensione dei pulsanti è uscito da `setup()` in funzioni,
  che `change_screen()` usa per rifarle; `resize_canvas()` adatta disegno,
  livelli, Annulla ed etichette (§5bis). Trovati e corretti lungo la
  strada: due leak (nomi dei timbri PNG con un SVG, percorso della
  miniatura a ogni salvataggio), tre plugin che non reggevano una tela
  più grande, il titolo "Colori" non ridisegnato, i contorni XOR fantasma.
  Il punto più lungo è stato capire sdl12-compat e mutter: filtro degli
  eventi, ordine delle chiamate per tornare in finestra, il caso di chi
  parte a schermo intero (§5bis).
- **Icone** (branch `feature/svg-icons`): 16 icone delle forme in SVG
  disegnato a mano, 16 degli strumenti vettorializzate con potrace. Le
  cornici dei pulsanti, a differenza di quanto previsto, sono rimaste
  PNG: a 2,67× il Lanczos le rende senza difetti visibili, perché sono
  sfumature morbide; rifarle avrebbe solo cambiato il loro aspetto.

Verifiche (desktop fermo, con il permesso dell'utente, in più giri):
- A 800×600 schermata principale e dialoghi identici al riferimento, a
  ogni passo (anche con gli SVG: lì restano i PNG).
- Ridimensionamenti 800×600 → 1600×1200 → 1000×700 → 800×600: il disegno
  torna allo stesso posto e della stessa misura; Ctrl+Z annulla l'ultimo
  tratto, quindi anche la cronologia è stata adattata.
- Alt+Invio da finestra e ritorno, due volte: la finestra torna a
  1600×1200. Da schermo intero di partenza: finestra 1600×1200, poi di
  nuovo schermo intero. Dalla finestra Nuovo: immagine ingrandita, nitida
  dopo Esc.
- Con AddressSanitizer: Mezzatinta, Schiuma e Vetrocemento usati prima e
  dopo un ingrandimento, testo durante Alt+Invio, etichetta durante un
  ridimensionamento, timbri, uscita pulita: nessun errore di memoria,
  persi 882 byte nelle librerie. Una prima sessione era partita con un
  binario ASan vecchio, che non vedeva i ridimensionamenti: va sempre
  ricopiato il sorgente nel worktree prima di ricompilare.
- Icone: prima e dopo a 1600×1200, e le forme a schermo intero.

Stato alla chiusura: branch attivo `feature/svg-icons`, installato; da
provare a mano e unire in `master`.

### 2026-11-01 — Feature e miglioramenti strumenti

Richiesta dell'utente: la sezione "Feature e miglioramenti strumenti" del
TODO, nove voci. Unica domanda: l'effetto del plugin di prova; scelto
Punto croce. Branch `feature/tools`, da `feature/svg-icons` perché tre dei
plugin da toccare erano cambiati lì.

- **Magie a tutta immagine** (Blocks, Chalk, Cartoon, Emboss, poi
  Puzzle): l'effetto per un punto in una funzione, chiamata attorno al
  mouse o su tutta la tela. Chalk ripassa la tela 6 volte, come un
  trascinamento.
- **Punto croce**: prima un prototipo in Python per misure e ombre, poi il
  C dall'esempio della guida; icona e suono da script. Provato
  nell'interfaccia vera: un tratteggio sottile spariva, la soglia è scesa
  da 1/3 a 1/16 del quadretto.
- **Schiuma, Puzzle, Mezzatinta**: vedi §5quinquies. Per Mezzatinta il
  confronto fra la versione vecchia e un prototipo ha mostrato che la
  media dei colori sovrapposti falsava i colori (il blu diventava lilla).
- **Suoni**: mancavano davvero quelli di Halftone e Puzzle (file mai
  esistiti) e Color & White usava quello di Fold. Il "clic" di Tornado
  manca ma è commentato apposta, Mosaic ha un suono suo: lasciati.
- **Tastiera a schermo**: scritte negli angoli; caratteri oltre U+FFFF
  seguiti con stampe di prova fino al testo (§5quinquies). Il FIXME
  indicato nel TODO (`onscreen_keyboard.c:1074`) era in una copia
  commentata di `wcstou16()`: il punto vero era quella di `tuxpaint.c`.
- **Etichette su due righe**: prima prototipi con PIL, che hanno mostrato
  che due righe senza rimpicciolire l'icona si sovrappongono a lei. Nel C
  la prima versione non mostrava nulla: l'alfa delle superfici di
  SDL_Pango, letta con `SDL_GetRGBA()` di sdl12-compat, torna 0
  (§5quinquies).
- **Trovati lungo la strada**: altezza del rettangolo da aggiornare in 10
  plugin e nell'esempio; direzioni di Puzzle; confronto con lunghezza 0
  per `NoSymbol`; leak del suono di Drip e del nome del layout della
  tastiera (questo con AddressSanitizer).

Verifiche (desktop fermo, con il permesso dell'utente, due giri):
- A 800×600 schermata principale e dialoghi identici al riferimento, salvo
  il pannello delle magie: "Arcobaleno vero", "Cambia colore", "Colore e
  bianco" su due righe.
- `magic_run` su un disegno e una foto, anche 1003×701 (il MCD dei lati è
  1), e sotto AddressSanitizer per i 10 plugin toccati: puliti.
- Nell'interfaccia: Punto croce a pennello e a tutta immagine, a
  1600×1200; tastiera a 800×600 e 1600×1200, con Maiuscolo; il layout di
  prova con la chiave di violino; sotto AddressSanitizer una sessione con
  tastiera, magia con colore, ridimensionamento a 1600×1200 e ritorno,
  uscita pulita: nessun errore, 432 byte persi nelle librerie e 15 di
  Tux Paint (il nome del layout), corretti dopo; quella correzione non è
  stata riprovata con AddressSanitizer.
- I suoni sono stati controllati con spettrogrammi e misure di volume,
  non ascoltati: da sentire a mano.

Stato alla chiusura: branch attivo `feature/tools`, installato in
`~/.local`; il layout di prova `bmptest` è stato tolto da
`~/.local/share/tuxpaint/osk/`. Da provare a mano e unire in `master`.

### 2026-11-01 — UI scalabile: unione, altre icone SVG, dialoghi alla nuova dimensione

Richiesta dell'utente: di nuovo la sezione "UI scalabile con la finestra",
con le tre voci rimaste. Risposte alle tre domande: unire tutto; icone
delle magie e dei dialoghi; tutti i dialoghi.

- **Unione**: `master` portato con avanzamento rapido a `feature/tools`
  (`baead7c`), nessun push.
- **Icone** (branch `feature/more-svg-icons`): `load_icon()` nell'API e
  i 48 plugin aggiornati in modo meccanico; 70 icone delle magie e 20
  dell'interfaccia tracciate e guardate una per una. La stima iniziale
  ("circa 60 al tratto") era ottimista: la tracciatura a due livelli
  perdeva i grigi piatti e ingrossava le linee sottili, quindi è nato
  `--tones`; ne sono uscite 39 magie e 10 immagini dell'interfaccia
  migliori del PNG ingrandito. Le altre restano PNG (§5bis).
- **Versione dell'API**: il binario di riferimento delle prove andava in
  crash all'avvio, perché caricava i plugin nuovi; è il caso di qualunque
  0.9.22. Da qui la versione 0x00010003, e il riferimento con i plugin
  suoi.
- **Dialoghi** (branch `feature/dialog-resize`): §5bis. Lungo la strada:
  il pannello di destra sotto i dialoghi (spento sotto Apri, Nuovo e il
  selettore, lo strumento di prima sotto le richieste), la cornice delle
  richieste, il titolo grigio dei colori; il testo di Tux letto dopo
  essere stato liberato (AddressSanitizer).

Verifiche (desktop fermo, con il permesso dell'utente, in più giri):
- A 800×600 schermata principale e dialoghi identici al riferimento,
  salvo il pannello delle magie (etichette su due righe), anche sul
  binario finale.
- Ogni dialogo (Apri, richiesta d'uscita, selettore colore) portato a
  1600×1200 e di nuovo a 800×600 è identico al pixel a com'era prima. A
  1600×1200: Apri con il secondo disegno ancora scelto, Nuovo con lo
  scorrimento, la scelta delle diapositive con i disegni segnati, una
  diapositiva in corso, la richiesta "Cancella" dentro Apri (risposta No:
  disegni e Cestino di prova intatti); Alt+Invio dentro Nuovo dà lo
  schermo intero nitido a 2560×1600 e torna.
- Icone delle magie nell'interfaccia a 1600×1200, quattro pagine.
- AddressSanitizer, sessione con tutti i dialoghi ridimensionati e uscita
  pulita: nessun errore dopo la correzione del testo di Tux; persi circa
  19 KB dentro Pango/fontconfig, legati alla ricreazione dei font a ogni
  cambio di misura (§5bis, TODO), più i 112 byte di SDL2 di sempre.

Stato alla chiusura: branch attivo `feature/dialog-resize`, installato in
`~/.local`; da provare a mano e unire in `master`.

### 2026-11-01 — Pubblicazione sulla repo GitHub dell'utente

Richiesta dell'utente: sincronizzare tutto su
`https://github.com/saulusprime/Tux-Paint2`, che era vuota.

- Aggiunto il remote `github` (SSH: la chiave dell'host autentica già
  come saulusprime; `gh` non c'è e per HTTPS non ci sono credenziali).
- Push di `master` per primo, così è il branch predefinito, poi di tutti
  i 14 branch con `-u`: ognuno segue il suo su `github`, anche `master`
  (prima seguiva `origin/master`). Nessun tag. `origin` non è toccato.
- Al primo push `master` era a `baead7c`. Subito dopo l'utente ha chiesto
  di portare tutto su `master`: avanzamento rapido a
  `feature/dialog-resize` (contiene `feature/more-svg-icons`), caricato su
  `github`. La prova a mano prevista prima dell'unione non c'è stata e
  resta tra i prossimi passi (§6).

Stato alla chiusura: `master` uguale a `feature/dialog-resize`, tutti i
branch in pari su `github`; il lavoro nuovo parte da `master` su un
branch nuovo.

### 2026-11-01 — L'utente tra i contributori

Richiesta dell'utente: aggiungere anche sé stesso, Paolo Pierno, come
contributore.

- `docs/AUTHORS.txt`, in fondo a "Design and Coding", come gli altri
  contributori: una voce per questo fork, con il link alla repo GitHub e
  in breve il lavoro fatto, firmata Paolo Pierno. Niente email (quella
  dell'utente serve solo per l'identità git).
- `magic/src/crossstitch.c`, l'unico plugin nuovo del fork, che non aveva
  autore nell'intestazione: "by Paolo Pierno".
- `docs/it/AUTHORS.txt` non è toccato: è di una versione vecchia e
  rimanda già a quello inglese.
- Branch `docs/authors`, unito in `master` con avanzamento rapido e
  caricato su `github`. L'identità git resta `Paolo`.

### 2026-11-02 → 2026-11-03 — Contenuti e localizzazione: le voci rimaste

Richiesta dell'utente: la sezione "Contenuti e localizzazione", con le tre
voci P3 rimaste. Risposte alle domande: tradurre OPTIONS e FAQ (non
ADVANCED-STAMPS-HOWTO e INSTALL); per le altre lingue, traduzioni del
Tux Paint di oggi più le mie, solo dove sicure; cartina senza nomi. Branch
`content/l10n-more`, da `master`.

- **Cataloghi** (`79764ea`): tutti allineati al modello. Il Tux Paint di
  oggi non ha documentazione italiana, ma ha cataloghi più completi: 571
  messaggi in 28 lingue presi da lì (§5quater).
- **Frasi del fork** (`146bf3e`): 350 traduzioni in 52 lingue, scritte da
  due agenti con il confronto delle traduzioni di ogni catalogo, più 8
  correzioni a traduzioni dell'originale che dicevano altro (per esempio
  "fai clic e trascina" per le modalità a un clic). Lasciati fuori i casi
  dubbi (Punto croce in bs, mk, sq; in hr il Gesso a tutta immagine ha la
  traduzione fedele, anche se il pulsante si chiama "Izmješaj").
  Lanciatore rigenerato: "Schermo intero" in 57 lingue,
  `desktop-file-validate` senza errori.
- **Cartina** (`f888862`): la proposta diceva solo regioni e mare; ho
  aggiunto i paesi vicini in grigio (Natural Earth), perché senza quelli
  il mare arrivava fino alle Alpi. Isole sotto i 2 pixel quadrati tolte.
- **Documentazione** (`8783ffa`): OPTIONS e FAQ tradotti da due agenti,
  con le regole del manuale già tradotto; letti e controllati (ancore,
  link, tag, frasi inglesi rimaste). Nella FAQ due note "In questa
  versione" (timbri con `./dev.sh stamps`, `--fullscreen` senza
  dimensione). La FAQ del 2009 ha due punti che il codice non rispecchia
  più (`LOW_QUALITY_FLOOD_FILL`, il messaggio del lockfile): tradotti così
  come sono, nel TODO.

Verifiche (desktop fermo, con il permesso dell'utente, in due giri):
- `regress.sh` e `dialogs.sh` a 800×600: identici al riferimento, salvo il
  pannello delle magie (etichette su due righe), come prima. Il
  riferimento legge gli stessi dati installati, quindi anche la finestra
  Nuovo con la cartina è uguale.
- Cartina aperta dalla finestra Nuovo; Toscana, Umbria, Sardegna, Sicilia,
  mare e paesi vicini riempiti con la magia Riempi, ognuno entro i suoi
  confini; a 1600×1200 la cartina resta proporzionata.
- Punto croce in olandese, russo, giapponese e lituano: etichetta (su due
  righe in russo e lituano) e le due descrizioni, con i caratteri giusti.
- Tutti i cataloghi passano `msgfmt --check`.

Stato alla chiusura: branch attivo `content/l10n-more`, installato in
`~/.local`; da provare a mano e unire in `master`. Su richiesta
dell'utente, il 2026-11-03 il branch è caricato su `github`, dove `master`
resta a `ab1c9b8`.
