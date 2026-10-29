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

## 1. Stato attuale (al 2026-10-29)

- **Progetto**: Tux Paint, programma di disegno per bambini (3+ anni), GPL v2.
- **Versione del codice**: 0.9.22 (upstream del 5 agosto 2014),
  `MAGIC_API_VERSION 0x00000003` (vedi [Makefile](Makefile) riga 12-14).
- **Origine del repository**: fork di LliureX, `origin` =
  `https://github.com/lliurex/tuxpaint.git`. Un solo commit
  (`5550718 Ported from Ubuntu`, jrpelegrina, 2018-10-16): import del
  sorgente 0.9.22 così come pacchettizzato in Ubuntu.
- **Branch** (nessuno unito a `master` né pubblicato su `origin`):
  - `build/host-debian13`, creato da `master`: correzioni di build,
    `dev.sh`, file di progetto;
  - `feature/ui-scaling`, creato da `build/host-debian13`: UI scalabile con
    la finestra (fasi 1 e 2 fatte, §5bis). **È il branch attivo.**
- **Identità git**: `Paolo <lymphalab@outlook.it>`, configurata solo nel
  repository (`.git/config`).
- **Compilazione**: **riuscita sull'host** (2026-10-29): build da zero in
  ~12 s, 0 errori, 96 warning (vedi §4).
- **Installazione**: in `~/.local` sull'host, tramite `./dev.sh install`.
  Primo avvio riuscito, con lanciatore nel menu. Dati utente in
  `~/.tuxpaint/`.
- **Modifiche locali rispetto a 0.9.22** (commit `b92a7d1` e `93fc7df`):
  - `src/tuxpaint.c`: `load_kpx`, `load_svg`, `myIMG_Load`,
    `myIMG_Load_RWops` accettano `const char *`. `load_starter_helper` vuole
    un loader `(const char *)`, compatibile con `IMG_Load`. Tolte le
    dichiarazioni di `show_version` e `show_usage`, spostate in `parse.h`.
  - `src/parse.h`: dichiarazioni di `show_version()` e `show_usage()`,
    usate dal parser generato da `src/parse.gperf`.
  - `Makefile`: `-lm` aggiunto a `linux_ARCH_LINKS`.
  - `.gitignore` nuovo, per gli artefatti di build.
  - `dev.sh` nuovo: build, installazione e avvio per lo sviluppo (§4).
  - Su `feature/ui-scaling` (`d346e60`, `321db8b`, più gli strumenti di
    test in `devtools/ui-test/`): schermata principale e finestre di dialogo
    scalate con la finestra (§5bis).
- **Installato in `~/.local`**: la build di `feature/ui-scaling`. Restano
  non scalati la tastiera a schermo, i cursori del mouse e la schermata
  iniziale (fase 3).
- **Decisioni prese** (2026-10-29):
  - **Strategia**: si resta sulla **0.9.22 con SDL 1.2** e la si corregge.
    Niente riallineamento all'upstream né porting a SDL2, per ora.
  - **Obiettivo**: **sperimentazione personale**. Target solo Linux;
    packaging, distribuzione e altre piattaforme non sono priorità.

## 2. Mappa del repository

| Percorso | Contenuto |
|----------|-----------|
| [src/](src/) | Sorgente C. Cuore in [src/tuxpaint.c](src/tuxpaint.c) (~24.100 righe, monolitico) più moduli: `fonts.c`, `i18n.c`, `onscreen_keyboard.c`, `postscript_print.c`, `dirwalk.c`, `pixels.c`, `playsound.c`, … |
| [src/po/](src/po/) | 126 traduzioni gettext (inclusi `it.po`, `ca.po`, `ca@valencia.po`) |
| [src/tuxpaint.conf](src/tuxpaint.conf) | Configurazione di default installata in `/etc` |
| [magic/src/](magic/src/) | 47 plugin "Magic" (`.so` caricati a runtime), API in `src/tp_magic_api.h.in` |
| [data/](data/) | Risorse: 53 pennelli, font, immagini UI, suoni |
| [stamps/](stamps/) | Solo pochi timbri (`cartoon/`); la collezione completa è il pacchetto separato `tuxpaint-stamps` |
| [starters/](starters/) | 61 immagini "Starter" (contorni/cornici da colorare) |
| [templates/](templates/) | 19 immagini "Template" (sfondi fotografici) |
| [osk/](osk/) | Layout della tastiera a schermo (`--onscreen-keyboard`) |
| [im/](im/) | Metodi di input per giapponese, coreano, thai, cinese tradizionale |
| [fonts/](fonts/) | Font specifici per locale (arabo, tibetano, greco, …) |
| [docs/](docs/) | Documentazione upstream (EN + traduzioni), vedi §3 |
| [custom/](custom/) | Hook di personalizzazione (solo macOS/Windows; Linux non implementato) |
| `win32/`, `macosx/`, `haiku/`, `hildon/`, `maemo/`, `visualc/` | Port per altre piattaforme (non rilevanti per Linux) |
| [Makefile](Makefile) | Build system unico, niente autotools |
| [tuxpaint.spec](tuxpaint.spec) | Spec RPM |

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
- [docs/it/](docs/it/) — traduzione italiana **parziale e datata** (README, FAQ, INSTALL, OPTIONS, PNG, AUTHORS; manca EXTENDING).

Nessun `CLAUDE.md`, nessun file di design o di decisioni interne: tutta la
documentazione è quella upstream.

## 4. Build: requisiti e situazione dell'ambiente

Dipendenze richieste (da INSTALL.txt e tuxpaint.spec):
SDL **1.2** (≥ 1.2.4), SDL_image, SDL_mixer, SDL_ttf, SDL_Pango (opzionale),
libpng, librsvg2 + cairo (SVG), fribidi, libpaper, gettext, gperf.

Comando di build standard: `make` → `make install` (variabili `PREFIX`, `DESTDIR`,
`SVG_LIB:=` per disattivare SVG).

Verifica eseguita il 2026-10-29 nella shell di VS Code:

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
- Prodotti della build: il binario `./tuxpaint`, 47 plugin in `magic/*.so`,
  119 cataloghi in `trans/*.mo`, `src/tp_magic_api.h` e `tp-magic-config`.
- I percorsi di installazione sono **fissati nel binario** al momento della
  compilazione (`DATA_PREFIX`, `MAGIC_PREFIX`, `CONFDIR`, … derivano da
  `PREFIX`, default `/usr/local`). Per installare altrove bisogna
  ricompilare con lo stesso `PREFIX` che si usa per `make install`.
- `install-bash-completion` scrive sempre in `/etc/bash_completion.d`
  (`COMPLETIONDIR`), anche con un `PREFIX` utente: in quel caso va
  sovrascritto anche `COMPLETIONDIR`.

### Warning della build (2026-10-29)

96 in tutto: 52 in `src/tuxpaint.c`, 13 in `src/im.c`, il resto sparso nei
plugin. Quasi tutti sono innocui: variabili o funzioni inutilizzate, confronti
fra interi con e senza segno. Quelli che indicano bug possibili sono elencati
in `TODO.md`, sezione "Qualità del codice".

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
5. **167 marcatori FIXME/TODO/XXX** nel sorgente (`src/` e `magic/src/`),
   tra cui handle dei plugin mai scaricati (`src/tuxpaint.c:1271`) e leak
   segnalati da Valgrind in `src/fonts.c`.
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
dell'interfaccia, a fasi, sul branch `feature/ui-scaling`. L'alternativa
scartata era l'ingrandimento globale con `SDL12COMPAT_WINDOW_SCALING`, che
riduce la risoluzione della tela.

**Modello** (`setup_normal_screen_layout()` in `src/tuxpaint.c`):

- `scala = max(1, min(max(L,A) / 800, min(L,A) / 600))`;
- `button_w = button_h = floor(48 × scala)`;
- `button_scale = button_w / 48`.

Fino a 800×600 non cambia nulla. Esempi: 1600×1000 → 80 px,
2400×1500 → 120 px, 2560×1600 a schermo intero → 128 px. La finestra è
fissa per tutta la sessione, quindi la scala si calcola una volta sola,
all'avvio.

**Convenzioni per convertire il codice** (da seguire anche nella fase 2):

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

`HEIGHTOFFSET` e `TOOLOFFSET` ora derivano da `buttons_tall`, il numero di
righe del layout, con `HEIGHTOFFSET = (buttons_tall - 7) * button_h`.

**Finestre di dialogo** (fase 2):

- Le richieste sì/no e il selettore colore sono disegnati in un'area di
  design di 640×480 centrata. `PROMPTOFFSETX = (WINDOW_WIDTH - SCALED(640)) / 2`;
  `PROMPTOFFSETY = HEIGHTOFFSET / 2` resta invariato.
- La geometria del riquadro resta in unità di design: la variabile `w`
  dell'animazione conta pixel di design. Si scala solo il risultato, per
  esempio `SCALED(PROMPT_LEFT + 96 - w) + PROMPTOFFSETX`.
  `PROMPT_LEFT` (96) e `PROMPT_W` (440) restano valori di design.
- Apri, Nuovo e presentazione hanno la griglia di miniature da
  `r_canvas.x`, le frecce alte `button_h / 2` e la riga di pulsanti in
  basso a `r_canvas.h - button_h`.
  `THUMB_H = (r_canvas.h - button_h / 2 - button_h) / 4`.

**Non scalati di proposito**:

- i pennelli nel selettore, che mostrano la dimensione reale della punta;
- timbri, testo e disegni sulla tela, che sono contenuto e non interfaccia;
- la schermata iniziale;
- le icone della tastiera a schermo, perché la tastiera stessa non è
  ancora scalata (fase 3).

**Invariante e test**: a scala 1 l'interfaccia deve restare identica al
pixel. Gli strumenti sono in `devtools/ui-test/`:

- `regress.sh OUT BIN 800x600 48` cattura una schermata per strumento;
- `dialogs.sh OUT BIN [SCALA]` attraversa tutti i dialoghi: uscita, Apri,
  presentazione con riproduzione, Nuovo, selettore colore. La finestra è
  800×600 per SCALA, con SCALA intera, e i clic vengono moltiplicati di
  conseguenza. Usa come `--savedir` una copia di
  `~/.cache/tuxpaint-test-canon`, che contiene due disegni salvati, così
  i dati in `~/.tuxpaint` non vengono toccati;
- `compare.py` confronta due serie di catture;
- `tp_session.py` è il motore: clic, trascinamenti e catture. Si
  configura con le variabili `TP_BIN`, `TP_BUTTON`, `TP_ARGS` e
  `TP_SCALE`.

Il binario di riferimento, cioè il codice prima della feature, è in un
worktree git: `~/.cache/tuxpaint-baseline/tuxpaint`, ricavato da
`build/host-debian13`. Si ricompila con `./dev.sh build` lì dentro e si
rimuove con `git worktree remove ~/.cache/tuxpaint-baseline`.

**Insidie dei test automatici**:

- Il primo clic su una finestra non attiva serve solo a darle il focus:
  `regress.sh` fa un clic iniziale sul titolo "Strumenti".
- I **trascinamenti simulati non sono affidabili**: il puntatore reale
  dell'utente interferisce e produce linee "a ventaglio". Per verificare
  la tela usare clic singoli.
- **Tux Paint non si chiude con SIGTERM**: SDL lo trasforma in una
  richiesta di uscita e il programma chiede conferma. Negli script usare
  SIGKILL (`timeout -s KILL`, `kill -9`).
- `pkill -f` con il testo della riga di comando colpisce anche le shell che
  lo contengono: usare `pgrep -x tuxpaint`.
- L'host non vede la `/tmp` del sandbox: i dati passano su stdout (tar).
  Con `flatpak-spawn` passare `--directory=$HOME` se la cartella corrente
  non esiste sull'host.
- Se la finestra è più grande dello schermo, il gestore delle finestre la
  accorcia: per esempio 2400×1500 diventa 2400×1462.
- Non automatizzare il pulsante "Cancella" di Apri: un clic sul "Sì"
  sposterebbe un file nel Cestino dell'utente.

## 6. Prossimi passi consigliati

1. Indagare il bug di Testo ed Etichetta che non si attivano (`TODO.md`,
   sezione Bug, P1).
2. Provare a mano Tux Paint a finestra grande (`./dev.sh run
   --windowsize=1600x1000`), compresi la richiesta "Cancella" e i pulsanti
   audio dei timbri.
3. UI scalabile, fase 3: tastiera a schermo, cursori, schermata iniziale.
4. Decidere se unire `build/host-debian13` e `feature/ui-scaling` in
   `master`.
5. Correggere il doppio `free` di `unc_buff` (`TODO.md`, P2): è un crash
   possibile all'apertura di un disegno salvato.

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
