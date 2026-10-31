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

## UI scalabile con la finestra

Completa e unita in `master`: scala nativa, rifiniture e icone ingrandite
con Lanczos. Schermo intero (Alt+Invio, avvio alla risoluzione dello
schermo) sul branch `feature/fullscreen`. Vedi [ASIS.md](ASIS.md) e
`HANDOFF.md` §5bis.

- [ ] [P2] Unire `feature/fullscreen` in `master` (avanzamento rapido).
- [ ] [P3] Schermo intero nitido anche partendo in finestra, e finestra
  ridimensionabile. Oggi Alt+Invio ingrandisce l'immagine della finestra
  (sullo schermo dell'utente 1600×1200 diventa 2133×1600, con bande nere
  ai lati e un po' meno nitida). Per ridisegnare l'interfaccia alla nuova
  dimensione bisognerebbe ricaricare tutte le immagini scalate e
  ridimensionare tela, livelli e cronologia di Annulla. È l'opzione
  scartata il 2026-10-31 perché grande e rischiosa.
- [ ] [P3] Icone davvero nitide a scala > 1: servirebbero immagini nuove
  (PNG grandi o SVG) per pulsanti, strumenti, forme e magie, cioè un lavoro
  grafico. Nemmeno l'upstream le ha: nella versione attuale le icone degli
  strumenti sono ancora PNG da 40×30.

## Bug

- [ ] [P3] `thumbnail2()` con `keep_aspect` centra bene solo in un
  riquadro quadrato: in uno rettangolare sposta l'immagine e lascia una
  fascia vuota (nera se non c'è alfa). Era la causa della barra nera nella
  richiesta "Cancella", corretta lì senza toccare `thumbnail2()`. Oggi è
  latente: gli altri chiamanti usano riquadri quadrati e i plugin Magia passano
  `keep_aspect` = 0. Correggerlo prima di usarlo con un riquadro
  rettangolare.

I difetti trovati nei warning sono nella sezione "Qualità del codice".

## Build e ambiente

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

Numeri di riga aggiornati al 2026-10-31 (branch `quality/fixme`);
se si spostano, cercare il testo o la funzione indicati.

- [ ] [P2] **Doppio `free(unc_buff)`** nei percorsi di errore del
  caricamento di sfondo/primo piano incorporati nel PNG
  (`src/tuxpaint.c:21768/21772` e `:21825/21829`, funzione `load_embedded_data`) — crash possibile
  aprendo un disegno salvato danneggiato.
- [ ] [P2] Operazioni su `cm.section` con comportamento indefinito
  (`-Wsequence-point`) in `src/im.c:899`, `:1085`, `:1271`, `:1481` —
  metodi di input giapponese/coreano/cinese.
- [ ] [P2] `strtok` su stringa `const` e argomenti in più per `printf`
  (`src/tuxpaint.c:22509`, `:22513`).
- [ ] [P3] Variabili forse non inizializzate `left_y`, `right_x` nel
  plugin Fold (`magic/src/fold.c:172`, `:178`).
- [ ] [P3] `abs()` intera usata su un `float` nel plugin Flower
  (`magic/src/flower.c:398`), si perde la parte decimale.
- [ ] [P3] Confronto sempre vero sull'indirizzo di `filename`
  (`src/fonts.c:1290`).
- [ ] [P3] Indentazione fuorviante (`src/tuxpaint.c:17046`) e parentesi
  mancanti in un `|` (`:17276`) — verificare che il comportamento sia
  quello voluto.
- [ ] [P3] API librsvg deprecate: `rsvg_handle_get_dimensions` e
  `rsvg_handle_render_cairo` (`src/tuxpaint.c:17759`, `:17836`).
- [ ] [P3] Ripulire i restanti ~80 warning innocui (variabili e funzioni
  inutilizzate, confronti con e senza segno).

## Qualità del codice (dai FIXME nel sorgente)

Le otto voci scelte il 2026-10-29 sono chiuse (branch `quality/fixme`,
vedi [ASIS.md](ASIS.md)). Nel sorgente restano altri FIXME minori, non
elencati qui.

- [ ] [P3] Suddividere `src/tuxpaint.c` (~24.500 righe) in moduli. Non
  fatto il 2026-10-31: è un lavoro lungo, da pianificare a parte (per
  esempio estraendo prima le parti più isolate: dialoghi Apri/Nuovo/
  presentazione, stampa, caricamento dei timbri, plugin Magia).
- [ ] [P3] Plugin Magia che nel loro `shutdown()` non liberano tutto:
  circa 260 KB a ogni uscita. Lo si vede con AddressSanitizer da quando i
  plugin vengono scaricati (`3ff7788`); con `dlclose()` reso nullo
  (`devtools/ui-test/nodlclose.c`) quei blocchi tornano raggiungibili.
  Per sapere quali plugin sono, serve una build ASan dei plugin.
- [ ] [P3] `magic_api_struct`: ne viene allocata una per ogni cartella di
  plugin, e quella delle cartelle precedenti si perde (circa 300 byte);
  `shutdown()` e gli altri richiami ricevono sempre l'ultima, con la
  `data_directory` dell'ultima cartella. Tenerne una per cartella e
  liberarle all'uscita.

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
  (`src/onscreen_keyboard.c:1219`, `:1074`).
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
