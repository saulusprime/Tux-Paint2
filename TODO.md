# TODO — idee, feature e attività

Attività aperte, raggruppate per area e ordinate per priorità
(**P1** = bloccante/subito, **P2** = importante, **P3** = quando possibile).
Quando un'attività è conclusa, va **spostata** in [ASIS.md](ASIS.md) con data
ed esito, e annotata nel diario di [HANDOFF.md](HANDOFF.md).

Formato: `- [ ] [Pn] Titolo — dettaglio (riferimenti)`

Contesto (decisioni del 2026-10-29): fork per **sperimentazione personale**,
si resta sulla **0.9.22 con SDL 1.2** e la si corregge. Target: solo Linux.

---

## Decisioni da prendere

Nessuna aperta. Le decisioni prese sono in [ASIS.md](ASIS.md) e in
`HANDOFF.md` §1.

## UI scalabile con la finestra (feature in corso)

Decisa il 2026-10-29: scala nativa dell'interfaccia, a fasi, sul branch
`feature/ui-scaling` (parte da `build/host-debian13`). Le fasi 1 (schermata
principale) e 2 (finestre di dialogo) sono fatte, vedi [ASIS.md](ASIS.md).
Dettagli tecnici in `HANDOFF.md` §5bis.

- [ ] [P2] **Fase 3 — resto dell'interfaccia**: tastiera a schermo
  (`src/onscreen_keyboard.c` e icone `img_osk*`, oggi non scalate di
  proposito), cursori del mouse (bitmap a dimensione fissa, minuscoli su
  HiDPI), schermata iniziale.
- [ ] [P2] Pulsanti audio dei timbri (`r_sfx`) a scala > 1: da verificare
  con l'audio attivo (i test girano con `--nosound`).
- [ ] [P3] Opzione `buttonsize=auto|N` (come l'upstream, dalla 0.9.27) per
  forzare la dimensione dei pulsanti: `src/parse.gperf`, `tuxpaint.conf`,
  `docs/OPTIONS.txt`, completamento bash.
- [ ] [P3] Finestra di default 800×600 minuscola sugli schermi HiDPI:
  valutare una dimensione iniziale ricavata dallo schermo.
- [ ] [P3] Icone più nitide a scala > 1: oggi sono bitmap da 48 px
  ingrandite (bilineare); servirebbero originali più grandi o SVG.
- [ ] [P3] Mouse da tastiera e joystick (`handle_keymouse(..., 24, ...)`):
  il passo è fisso in pixel, quindi a scala > 1 il puntatore si muove più
  lentamente rispetto all'interfaccia. Valutare `SCALED(24)`.
- [ ] [P3] Richiesta "Cancella" in Apri non provata automaticamente (un clic
  sbagliato sposterebbe un file nel Cestino): è la stessa funzione delle
  altre richieste, ma va provata a mano a scala > 1.
- [ ] [P2] Unire `feature/ui-scaling` in `master` quando la fase 3 è
  fatta, o anche prima, visto che a scala 1 non cambia nulla.

## Bug

- [ ] [P1] **Strumenti Testo ed Etichetta non si attivano** sull'host:
  dopo il clic resta il messaggio del Testo ma lo strumento non si
  seleziona e il pannello dei font resta vuoto, anche dopo 40 s e un
  secondo clic. Succede anche col binario originale, quindi è un problema
  preesistente. Ipotesi: caricamento dei font (461 sull'host, scanner in
  un processo separato, `FORKED_FONTS`) che non termina. Da verificare a
  mano, fuori dai test automatici.

## Build e ambiente

- [ ] [P2] Unire il branch `build/host-debian13` in `master`.
- [ ] [P2] Prova manuale di tutti gli strumenti (`./dev.sh run`): disegno,
  timbri, Magic, testo/etichette, salvataggio/apertura, stampa, audio.
- [ ] [P3] Completamento bash non caricato automaticamente: installarlo come
  `$(COMPLETIONDIR)/tuxpaint` invece di `tuxpaint-completion.bash` (target
  `install-bash-completion` e `uninstall` del Makefile).
- [ ] [P3] Avvisi libpng all'avvio (profili iCCP e bKGD non validi in
  alcuni PNG dei dati): individuare i file e ripulirne i metadati.

## Modernizzazione

- [ ] [P3] Hook di personalizzazione per Linux — `custom/linux.sh` richiamato
  dal Makefile, come già avviene per macOS (vedi `custom/README.txt`).
- [ ] [P3] Convertire in UTF-8 i documenti con caratteri Latin-1
  (es. `docs/CHANGES.txt`).
- [ ] [P3] Porting a SDL2 — escluso per ora (decisione del 2026-10-29); da
  riconsiderare solo se `sdl12-compat` dovesse dare problemi seri.

## Qualità del codice (dai warning della build del 2026-10-29)

- [ ] [P2] **Doppio `free(unc_buff)`** nei percorsi di errore del
  caricamento di sfondo/primo piano incorporati nel PNG
  (`src/tuxpaint.c:21399/21403` e `:21456/21460`) — crash possibile
  aprendo un disegno salvato danneggiato.
- [ ] [P2] Operazioni su `cm.section` con comportamento indefinito
  (`-Wsequence-point`) in `src/im.c:899`, `:1085`, `:1271`, `:1481` —
  metodi di input giapponese/coreano/cinese.
- [ ] [P2] `strtok` su stringa `const` e argomenti in più per `printf`
  (`src/tuxpaint.c:22124`, `:22128`).
- [ ] [P3] Variabili forse non inizializzate `left_y`, `right_x` nel
  plugin Fold (`magic/src/fold.c:172`, `:178`).
- [ ] [P3] `abs()` intera usata su un `float` nel plugin Flower
  (`magic/src/flower.c:398`), si perde la parte decimale.
- [ ] [P3] Confronto sempre vero sull'indirizzo di `filename`
  (`src/fonts.c:1285`).
- [ ] [P3] Indentazione fuorviante (`src/tuxpaint.c:16728`) e parentesi
  mancanti in un `|` (`:16958`) — verificare che il comportamento sia
  quello voluto.
- [ ] [P3] API librsvg deprecate: `rsvg_handle_get_dimensions` e
  `rsvg_handle_render_cairo` (`src/tuxpaint.c:17441`, `:17518`).
- [ ] [P3] Ripulire i restanti ~80 warning innocui (variabili e funzioni
  inutilizzate, confronti con e senza segno).

## Qualità del codice (dai FIXME nel sorgente)

- [ ] [P2] Scaricare i plugin Magic all'uscita e togliere il limite fisso di
  512 handle (`src/tuxpaint.c:1268-1271`).
- [ ] [P2] Memory leak segnalati da Valgrind in `src/fonts.c:1166` e `:1218`.
- [ ] [P3] Barriera di memoria mancante nel thread di caricamento font
  (`src/fonts.c:1010`).
- [ ] [P3] Centratura della stampa PostScript (`src/postscript_print.c:198`)
  e inizializzazione di libpaper all'avvio/chiusura (`:107`, `:158`).
- [ ] [P3] Allocazioni ripetute in `src/get_fname.c:54`.
- [ ] [P3] Rendere array-based la gestione dei locale (`src/i18n.c:403`).
- [ ] [P3] Barra di avanzamento da riattivare (`src/progressbar.c:70`).
- [ ] [P3] Ordinamento case-insensitive di Starter/file
  (`src/dirwalk.c:261`, es. `Jigsaw*` vs `jigsaw*`).
- [ ] [P3] Suddividere `src/tuxpaint.c` (~24.100 righe) in moduli.

## Feature e miglioramenti strumenti

- [ ] [P2] Plugin Magic di prova — scriverne uno nuovo partendo da
  `magic/docs/tp_magic_example.c` e dalla guida `magic/docs/README.txt`;
  buon primo esercizio di sperimentazione sull'API dei plugin.
- [ ] [P2] Magic "Blocks", "Chalk", "Cartoon", "Emboss" anche come effetto
  sull'intera immagine (`magic/src/blocks_chalk_drip.c:338`,
  `cartoon.c:262`, `emboss.c:219`).
- [ ] [P3] Magic "Foam": bolle colorabili (`magic/src/foam.c:434`).
- [ ] [P3] Magic "Puzzle": modalità a schermo intero (`magic/src/puzzle.c:37`).
- [ ] [P3] Effetti sonori mancanti o provvisori: Fade/Darken, Glass Tile,
  Halftone, Mosaic, Tint (`fade_darken.c:240`, `glasstile.c:282`,
  `halftone.c:92`, `mosaic.c:94`, `tint.c:64`).
- [ ] [P3] Tastiera a schermo: etichette AltGr e caratteri non-BMP
  (`src/onscreen_keyboard.c:1215`, `:1070`).
- [ ] [P3] Halftone: angolo per canale colore (`magic/src/halftone.c:277`).

## Contenuti e localizzazione

- [ ] [P2] Integrare o documentare il pacchetto `tuxpaint-stamps` (nel repo
  ci sono solo i timbri `cartoon/`).
- [ ] [P2] Revisione della traduzione italiana (`src/po/it.po`) — stringhe
  mancanti o fuzzy.
- [ ] [P3] Aggiornare la documentazione italiana in `docs/it/` e tradurre
  `EXTENDING.txt` (manca).
- [ ] [P3] Nuovi Starter/Template a tema scolastico (formati PNG/SVG, vedi
  `docs/EXTENDING.txt`).

## Distribuzione (fuori obiettivo per ora)

Da riprendere solo se il fork smette di essere un progetto personale.

- [ ] [P3] Integrazione continua (GitHub Actions) che compila su Debian/Ubuntu.
- [ ] [P3] Metadati AppStream e verifica del file `.desktop` per i software
  center moderni.
- [ ] [P3] Pacchetto Flatpak o `.deb` per una distribuzione semplice.
- [ ] [P3] Rimuovere OpenCandy dagli script di installazione Windows
  (`win32/`, vedi `docs/CHANGES.txt` 0.9.22) — serve solo per distribuire
  su Windows.
