# ASIS — attività completate

Archivio delle attività concluse, spostate da [TODO.md](TODO.md).
Ordine cronologico, le più recenti in fondo. Il racconto dettagliato di ogni
sessione è nel diario di [HANDOFF.md](HANDOFF.md).

Formato: `- [x] AAAA-MM-GG — Titolo — esito/note`

---

## Baseline (stato ereditato)

- [x] 2014-08-05 — Tux Paint 0.9.22 upstream — base del codice attuale
  (vedi `docs/CHANGES.txt`).
- [x] 2018-10-16 — Import nel fork LliureX — commit `5550718` "Ported from
  Ubuntu", sorgente 0.9.22 senza ulteriori modifiche.

## 2026-10

- [x] 2026-10-29 — Lettura della documentazione di progetto — letti README,
  INSTALL, OPTIONS, EXTENDING, FAQ, CHANGES, custom/README e tuxpaint.spec.
- [x] 2026-10-29 — Analisi della struttura del repository — mappa in
  `HANDOFF.md` §2.
- [x] 2026-10-29 — Verifica delle dipendenze di build nell'ambiente VS Code —
  mancano le librerie SDL 1.2; runtime Flatpak con GCC 15.2 (`HANDOFF.md` §4).
- [x] 2026-10-29 — Censimento FIXME/TODO nel sorgente — 167 marcatori; i più
  rilevanti riportati in `TODO.md`.
- [x] 2026-10-29 — Creazione dei file di progetto `HANDOFF.md`, `TODO.md`,
  `ASIS.md`.
- [x] 2026-10-29 — Decisione: strategia del fork — si resta sulla 0.9.22
  con SDL 1.2 e la si corregge; niente riallineamento all'upstream né
  porting SDL2 per ora.
- [x] 2026-10-29 — Decisione: obiettivo del fork — sperimentazione personale;
  target solo Linux, distribuzione e altre piattaforme fuori obiettivo
  (spostate in una sezione dedicata di `TODO.md`).
- [x] 2026-10-29 — Decisione: ambiente di build — build direttamente
  sull'host Debian 13.7, raggiunto dalla shell di VS Code con
  `flatpak-spawn --host`.
- [x] 2026-10-29 — Verifica disponibilità di SDL_Pango — presente in
  Debian 13 (`libsdl-pango-dev` 0.1.2-8+b3); niente build senza Pango.
- [x] 2026-10-29 — Elenco delle dipendenze di build per l'host — ricavato
  dal Makefile, tutti i pacchetti disponibili in Debian 13; comando di
  installazione in `HANDOFF.md` §4.
- [x] 2026-10-29 — Installazione dei pacchetti di sviluppo sull'host —
  fatta dall'utente, verificata con `pkg-config`.
- [x] 2026-10-29 — Compatibilità con GCC 14 — corretti nel codice i due
  errori: tipo del puntatore a funzione in `load_starter_helper`, prototipi
  di `show_version`/`show_usage` in `src/parse.h`. Non è servito
  `-fpermissive`.
- [x] 2026-10-29 — Prima build completa sull'host — riuscita dopo aver
  aggiunto `-lm` nel Makefile; build da zero in ~12 s, 0 errori, 96 warning
  (analizzati, i rilevanti sono in `TODO.md`).
- [x] 2026-10-29 — `.gitignore` per gli artefatti di build — copre tutto
  ciò che `make clean` rimuove.
- [x] 2026-10-29 — Script di build/run documentato — `dev.sh` con `build`,
  `install`, `run`, `uninstall` e `clean`; funziona anche dal sandbox
  Flatpak di VS Code (`HANDOFF.md` §4).
- [x] 2026-10-29 — Installazione in un prefisso utente e primo avvio —
  installato in `~/.local` con lanciatore e icone. Prova di avvio di 10 s
  in finestra senza crash.
- [x] 2026-10-29 — Commit delle correzioni di build, di `dev.sh` e dei file
  di progetto — sul branch `build/host-debian13` (`b92a7d1`, `93fc7df` e il
  commit dei file di progetto); identità git configurata solo nel repo.
- [x] 2026-10-29 — Decisione: UI scalabile con la finestra — scala nativa
  dell'interfaccia (non ingrandimento globale con sdl12-compat), a fasi, sul
  branch `feature/ui-scaling`.
- [x] 2026-10-29 — UI scalabile, fase 1: schermata principale (`d346e60`):
  - pulsanti proporzionali alla finestra rispetto a 800×600, mai sotto i
    48 px: 1600×1000 → 80 px, 2400×1500 → 120 px;
  - scalati barra strumenti, selettori, palette, titoli, area di Tux,
    etichette, font, icone delle magie e miniature dei timbri;
  - tela e clic allineati;
  - a 800×600 le otto schermate di prova sono identiche al pixel al
    binario originale.
- [x] 2026-10-29 — Strumenti di test dell'interfaccia (`22ba70e`) —
  `devtools/ui-test/`: clic simulati via XTest, catture `xwd` e confronto
  pixel per pixel.
- [x] 2026-10-29 — UI scalabile, fase 2: finestre di dialogo (`321db8b`):
  - adattati richieste sì/no, Apri, Nuovo, presentazione (selezione,
    cursore della velocità, riproduzione) e selettore colore;
  - a 800×600 le nove schermate dei dialoghi sono identiche al pixel al
    binario originale;
  - corrette anche a 1600×1200 (scala 2) e a 1600×1000 (scala 1,67, con
    la richiesta centrata);
  - la scelta di un colore dal selettore funziona anche a scala 2;
  - script `devtools/ui-test/dialogs.sh` (`a92db23`).
- [x] 2026-10-29 — UI scalabile, fase 3: resto dell'interfaccia (`0c7bcf9`):
  - cursori del mouse ingranditi di un fattore intero: 64×64 a scala 2,
    con il punto attivo corretto (verificato via XFixes);
  - schermata iniziale e barra di avanzamento scalate;
  - tastiera a schermo: tasti, scritte e icone scalati; scrivere "ciao"
    con la tastiera a scala 2 funziona;
  - a 800×600 la schermata iniziale e tutte le schermate di prova sono
    identiche al riferimento. **La UI scalabile è completa.**
- [x] 2026-10-29 — Bug: Testo ed Etichetta non si attivavano (`6d3f130`):
  - causa: il processo figlio che cerca i font (`FORKED_FONTS`, creato
    con `fork()` all'avvio) va in crash (SIGSEGV) con sdl12-compat, quindi
    Tux Paint riceve zero font;
  - correzione: caricamento dei font in un thread;
  - verificati Testo ed Etichetta a 800×600 (identici al riferimento
    corretto) e a scala 2.
- [x] 2026-10-30 — Crash del processo figlio dei font: analisi e correzione
  definitiva (`1431866`, `b7021ac`):
  - pila del crash ottenuta senza `gdb` (libreria `LD_PRELOAD` più
    `addr2line`): il figlio finisce la scansione, poi `exit(0)` esegue il
    gestore di chiusura di Mesa ereditato dal genitore, che va in crash
    su `pthread_join`;
  - correzione: `_exit(0)` nel figlio e `FORKED_FONTS` di nuovo attivo; la
    soluzione col thread (`6d3f130`) è stata ritirata;
  - verifiche: prova manuale dell'utente (Testo: pannello, scrittura,
    cambio di font); a 800×600 schermata principale e dialoghi identici al
    riferimento; Testo a scala 2 corretto.
- [x] 2026-10-30 — Strumenti di test più sicuri:
  - `tp_session.py` usa solo la finestra del Tux Paint che ha avviato lui
    (`_NET_WM_PID`) e la porta in primo piano;
  - non clicca se in cima c'è un'altra finestra, per esempio la "mutter
    guard window".
- [x] 2026-10-29 — Bug: il ricolore del pulsante del colore personalizzato
  (`search_label_list`) scriveva oltre il bordo dell'immagine (ciclo fisso
  48×48) — corretto in `d346e60`.
- [x] 2026-10-30 — UI scalabile, rifiniture (`c06ba8f`, `ed4a2f8`):
  - opzione `buttonsize=auto|24-192` (OPTIONS, man, `tuxpaint.conf`,
    `--usage`, completamento bash); può solo rimpicciolire rispetto ad
    `auto`. Con `--buttonsize=48` a 1600×1000 l'interfaccia è identica al
    pixel al programma originale; valori non validi rifiutati (codice
    d'uscita 91);
  - finestra iniziale su schermi grandi: senza `windowsize`, il più grande
    multiplo intero di 800×600 che sta comodamente nello schermo
    (1600×1200 sul 2560×1600 dell'utente; il programma originale apriva
    800×600);
  - passo del mouse da tastiera proporzionale (`SCALED(16)`, `SCALED(24)`);
  - verificati a scala 2 i pulsanti audio dei timbri (audio attivo col
    driver SDL "dummy", senza suoni reali) e la richiesta "Cancella" (con
    un Cestino di prova, `XDG_DATA_HOME` dedicato: rispondendo "No" i file
    restano);
  - a 800×600 schermata principale, dialoghi e Timbro con audio identici
    al riferimento.
- [x] 2026-10-30 — Uniti `build/host-debian13` e `feature/ui-scaling` in
  `master` (avanzamento rapido, nessun push).
- [x] 2026-10-30 — Icone più nitide a scala > 1 (`7cb40aa`, branch
  `feature/sharper-icons`):
  - verificato che neanche l'upstream ha immagini ad alta risoluzione:
    icone degli strumenti PNG 40×30, nessun SVG;
  - confronto di bilineare, bicubico, Lanczos e Lanczos con nitidezza
    sulle icone reali: scelto Lanczos, senza nitidezza aggiuntiva per
    evitare aloni;
  - `enlarge_lanczos()`: filtro separabile Lanczos-3 su alfa
    premoltiplicato, usato da `scale_ui_image()` solo quando
    l'immagine si ingrandisce;
  - prima e dopo a scala 2 e 2,5: bordi netti, senza aloni; a 800×600
    identico al riferimento.
- [x] 2026-10-30 — Documentazione di progetto aggiornata per la ripresa:
  - `HANDOFF.md`: nuova §0 "Come riprendere"; §1 riscritta, con stato al
    30, tabelle di branch e modifiche, cartelle di supporto; §5bis
    riordinata (modello, convenzioni, parti dell'interfaccia, prove,
    insidie), senza istruzioni superate;
  - `TODO.md`: numeri di riga della sezione "Qualità del codice"
    aggiornati;
  - nuovo `devtools/ui-test/README.md` con esempi d'uso.

- [x] 2026-10-31 — Barra nera sopra la miniatura nella richiesta "Cancella"
  di Apri (`4f95ada`, branch `fix/erase-prompt-thumbnail`):
  - causa: la miniatura veniva ridotta a 80×64 con la modalità
    `keep_aspect` di `thumbnail()`, che centra bene solo in un riquadro
    quadrato. Il disegno finiva spostato in basso (di 15 pixel a 800×600)
    e la fascia sopra restava nera. Difetto già presente nella 0.9.22;
  - correzione: si calcola la dimensione che mantiene le proporzioni
    dentro 80×64 e si riduce la miniatura esattamente a quella. Freccia e
    cestino salgono di conseguenza;
  - in più: la miniatura salvata accanto a ogni disegno ha il margine
    `SCALED(20)`, come quelle della finestra Apri. A scala 2 ora misura
    264×160 invece di 284×180, e Apri non la deve più ridimensionare a
    ogni apertura;
  - nuovo script `devtools/ui-test/erase.sh` (`784729b`) per la richiesta
    "Cancella", con Cestino e cartella di salvataggio di prova;
  - verifiche: barra sparita a 800×600 e a scala 2; a 800×600 cambia solo
    la colonna delle immagini nella richiesta, mentre Apri prima e dopo e
    tutti gli altri dialoghi restano identici al riferimento; rispondendo
    "No" il Cestino di prova resta vuoto.
- [x] 2026-10-31 — Documentazione di progetto aggiornata:
  - `HANDOFF.md`: nella mappa del repository (§2) aggiunti `dev.sh`,
    `devtools/ui-test/` e i file di progetto; `src/tuxpaint.c` ora ~24.400
    righe; riferimento a `magic_handle` aggiornato (§5); warning ricontati
    con una build da zero, sempre 96 (52 in `src/tuxpaint.c`);
  - `TODO.md`: dimensione di `src/tuxpaint.c` aggiornata.
- [x] 2026-10-31 — Uniti `feature/sharper-icons` e
  `fix/erase-prompt-thumbnail` in `master` (avanzamento rapido, nessun
  push): icone ingrandite con Lanczos, correzione della richiesta
  "Cancella", script `erase.sh` e file di progetto. Prima dell'unione
  ogni modifica era già verificata sul suo branch; la build installata in
  `~/.local` ha lo stesso codice di `master`.
- [x] 2026-10-31 — Schermo intero (branch `feature/fullscreen`, `3f43e1a`;
  scelta dell'utente: "Alt+Invio + avvio nitido"):
  - **Alt+Invio** passa da finestra a schermo intero e viceversa mentre si
    disegna, anche nei dialoghi, senza perdere nulla. A schermo intero la
    finestra viene ingrandita (1600×1200 → 2133×1600, bande nere ai lati);
    tenendo premuto il tasto la modalità cambia una volta sola;
  - **avvio a schermo intero nitido**: voce "Schermo intero" nel menu
    dell'icona (`--fullscreen=native`); `fullscreen` senza dimensione usa
    ora la risoluzione dello schermo (2560×1600, pulsanti da 128 px)
    invece di ingrandire 800×600. Partito così, Alt+Invio resta a schermo
    intero, perché una finestra grande quanto lo schermo non ci starebbe;
  - corretti due difetti: `--fullscreen` e `-f` senza valore venivano
    rifiutati (`65874c7`, già nella 0.9.22); con `native` la finestra,
    uscendo dallo schermo intero, diventava di 2×2 pixel;
  - strumenti di prova: azioni `key` e `info`, sessioni senza dimensione
    (`77a1be3`);
  - verifiche: a 800×600 schermata principale e dialoghi identici al
    riferimento; andata e ritorno con Alt+Invio identici; clic a schermo
    intero ingrandito arrivato al pulsante giusto; avvio con
    `--fullscreen` e `--fullscreen=native` identici; finestra iniziale
    ancora 1600×1200; lanciatore installato valido
    (`desktop-file-validate`).
- [x] 2026-10-31 — Qualità del codice, dai FIXME nel sorgente (branch
  `quality/fixme`, da `feature/fullscreen`). Otto voci su nove chiuse,
  più cinque difetti trovati lungo la strada:
  - **Plugin Magia** (`3ff7788`): niente più limite fisso di 512 (gli
    array crescono, prima si poteva scrivere oltre la fine); plugin
    scaricati all'uscita; un file senza punto nella cartella dei plugin
    (es. `README`) faceva andare in crash l'avvio. Verificato senza
    finestra: il riferimento va in crash (codice 139), il nuovo parte;
  - **Font** (`bc2b4c7`): i "leak" di Valgrind erano i dati ricevuti dal
    processo dei font e i font aperti, mai liberati all'uscita ("we'll
    leak the bodies"): ora `free_received_font_info()`. Un errore di
    lettura dal processo dei font ora viene gestito. Barriera di memoria
    nel thread dei font (build senza processo figlio). Con
    AddressSanitizer i leak dei font (circa 395 KB) sono spariti;
  - **Stampa PostScript** (`b96ae5d`): la centratura era già giusta
    (verificata con il nuovo `devtools/print-test/ps_check.sh` e
    Ghostscript); corretti due difetti della 0.9.22: un formato carta
    sconosciuto mandava in crash la stampa, e una stampa riuscita poteva
    risultare fallita (risultato di `pclose()` usato come un PID, `errno`
    vecchio); libpaper resta inizializzata solo durante la stampa;
  - **`get_fname()`** e **barra di avanzamento** (`fe89e9c`): lasciate
    come sono, con il motivo scritto al posto del FIXME (le allocazioni
    non costano nulla; riattivare `eat_sdl_events()` farebbe uscire senza
    salvare). Nello stesso commit: i modelli personali si caricavano dalla
    cartella di salvataggio invece che da quella dei dati;
  - **lingue** (`a2c83b1`): `--lang help` generato dalla tabella delle
    lingue, stesse 175 coppie nome/locale; cambiano solo due righe
    d'impaginazione;
  - **ordinamento** (`902e403`): Starter, modelli, timbri e pennelli
    ordinati ignorando maiuscole e minuscole (`Jigsaw_*` accanto a
    `jigsaw`);
  - **finestra Nuovo**: lo Starter `frame_heart.png` non compariva mai,
    nascosto da `frame_hearts.svg` (`13ff28c`); i modelli personali non si
    aprivano mai, scambiati per Starter (`4a09172`). Verificato a schermo
    con un modello di prova: prima tela bianca, ora il modello;
  - verifiche: a 800×600 schermata principale e dialoghi identici al
    riferimento; nessun errore di memoria con AddressSanitizer, uscita
    pulita;
  - non fatto: la suddivisione di `src/tuxpaint.c` in moduli, rimasta nel
    TODO come lavoro da pianificare.
- [x] 2026-10-31 — Qualità del codice, dai warning della build (branch
  `quality/warnings`, da `quality/fixme`): **0 warning** (erano 96), anche
  nella build AddressSanitizer a `-O1`. Difetti veri trovati e corretti:
  - **disegni salvati** (`b80ff08`): il recupero degli strati incorporati
    nel PNG cercava lo sfondo come `tpBK` invece di `tpBG`, non assegnava
    uno sfondo grande quanto la tela (puntatore a memoria liberata),
    scambiava le maschere blu/verde, liberava due volte i dati nei
    percorsi d'errore e poteva leggere oltre la fine di un file
    danneggiato. Verificato a schermo: un disegno fatto da un modello che
    poi manca, riaperto, con la gomma mostra il bianco nella versione
    vecchia e il modello in quella nuova;
  - **Cestino** (`806b445`): cartelle create con modo `0x777` (senza
    scrittura per il proprietario), copia di ripiego troncata a multipli
    di 1024 byte, percorsi con `sprintf` in 256 byte. Verificato con il
    Cestino su un altro filesystem: prima il disegno andava perso, ora è
    nel Cestino intero (5324 byte);
  - **memoria a ogni uso** (`11824a3`, `5a9f15f`): elenco dei file dei tre
    dialoghi, copia dello schermo del selettore colore, copia della tela
    a ogni apertura di un disegno, immagini dei cursori, errori di
    librsvg, immagine del plugin Erba, superficie del plugin Piega a ogni
    piega (`c1f5562`). Con ASan, la stessa sessione: da 3,46 MB a 432
    byte (nelle librerie);
  - **altro**: stringa di formato in Mosaic Shaped (`c1f5562`);
    comportamento indefinito nei metodi di input e `strtok` su una
    stringa non nostra, con overflow oltre 256 pulsanti
    (`joystick-buttons-ignore`, `ed77f9c`); parentesi in
    `handle_active()` e graffe in `handle_keymouse()` (`364af89`);
    percorsi di Starter e modelli (`d346c78`); una `magic_api` sola e
    percorsi delle cartelle dei plugin liberati (`b7cd9f9`);
  - **librsvg** (`7d499fb`): API non deprecate; i 19 SVG installati
    rendono identici al pixel a quattro dimensioni;
  - pulizia (`060141d`): codice morto, formati `size_t`, `sound_fnames[]`
    spostato in `tuxpaint.c` come chiedeva il suo FIXME;
  - verifiche: a 800×600 schermata principale e dialoghi identici al
    riferimento; nessun errore di memoria con ASan; `erase.sh` ora può
    rispondere Sì e usare un Cestino di prova altrove (`7c3066f`).
- [x] 2026-10-31 — Contenuti e localizzazione (branch `content/l10n`, da
  `quality/warnings`), le quattro voci della sezione:
  - **timbri** (`13d8635`): `./dev.sh stamps` aggiunge la raccolta
    completa da `tuxpaint-stamps-default` di Debian (2025.03.31),
    scaricato con `apt-get download` e non installato, o da un `.deb` o
    una cartella `stamps`. 957 timbri, 932 con la descrizione in
    italiano; formati e opzioni dei `.dat` tutti noti alla 0.9.22.
    L'avvio non rallenta (immagini e descrizioni si caricano quando
    servono). Corretto un difetto della 0.9.22 (`0aca7bd`): l'ultima riga
    di un `.dat` o `.txt` senza a capo veniva ignorata. Installata in
    `~/.local`;
  - **`it.po`** (`07ce1b1`): allineato al modello, rilette tutte le 292
    stringhe e corrette 44 (refusi, due magie con lo stesso
    nome, significati sbagliati, nomi troppo lunghi per i pulsanti;
    dettagli nel commit). Il campione di punteggiatura per i font non
    corrispondeva in nessuna lingua per un `\%` nel sorgente
    (`af760fb`). Il modello si rigenera senza intltool con
    `devtools/po/update-po.sh` (`481440f`), e l'azione "Schermo intero"
    del lanciatore è nel modello e tradotta in ca/de/es/fr/it;
  - **documentazione** (`bb2b180`): manuale (`README`) ed `EXTENDING`
    tradotti dalla 0.9.22, con le novità del fork; agli altri file
    italiani, della 0.9.14-0.9.15, un avviso che rimanda all'inglese
    (scelta dell'utente: non tradurre OPTIONS, FAQ e il resto);
  - **Starter e modelli** (`abca762`): orologio e scuola da colorare;
    lavagna, quaderno a righe, a quadretti e pentagrammato. SVG nitidi a
    ogni dimensione, generati da `devtools/content/school_svgs.py`;
  - verifiche: a 800×600 schermata principale e dialoghi identici al
    riferimento; a schermo in italiano le etichette di tutte le magie, un
    timbro con la descrizione italiana e i sei file nuovi aperti dalla
    finestra Nuovo, anche a 1600×1200.
- [x] 2026-11-01 — UI scalabile con la finestra, le tre voci della
  sezione:
  - **unione in `master`**: avanzamento rapido a `content/l10n`
    (`0787bf2`), dopo la prova a mano dello schermo intero da parte
    dell'utente;
  - **finestra ridimensionabile e schermo intero nitido** (branch
    `feature/resizable`, `54b36d4`…`7672e81`): era l'opzione scartata il
    2026-10-31. L'interfaccia si rifà alla nuova dimensione; il disegno,
    lo Starter o il modello, la cronologia di Annulla e le etichette si
    adattano alla nuova tela senza deformarsi, e tornando alla dimensione
    di prima tornano com'erano. Corretti lungo la strada due leak, tre
    plugin Magia (Halftone, Foam, Glass Tile) e il valore di
    `fullscreen` (11 invece di 1);
  - **icone nitide** (branch `feature/svg-icons`, `a34374b`, `b9e7dfb`):
    con pulsanti più grandi di 48×48 le icone di strumenti (16, con
    potrace) e forme (16, disegnate a mano) vengono da SVG. Le cornici dei
    pulsanti sono rimaste PNG: a 2,67× non c'è differenza visibile;
  - verifiche: a 800×600 identico al riferimento; ridimensionamenti e
    Alt+Invio a schermo; AddressSanitizer senza errori (882 byte persi,
    nelle librerie).
- [x] 2026-11-01 — Feature e miglioramenti strumenti, le nove voci della
  sezione (branch `feature/tools`, `799621f`…`6f79f5d`):
  - **plugin di prova**: Punto croce (`7eb3530`, scelto dall'utente tra
    tre proposte), scritto da `tp_magic_example.c`. Ricama il disegno su
    una tela con i fori: una "x" del colore del disegno in ogni quadretto
    di 8×8, a pennello o a tutta immagine; il bianco resta tela, una
    linea sottile diventa una fila di punti. Icona e suono generati da
    script (`devtools/content/`);
  - **Blocks, Chalk, Cartoon, Emboss a tutta immagine** (`799621f`);
  - **Foam colorabile** (`a901766`): bolle del colore scelto, col bianco
    identiche a prima;
  - **Puzzle a tutta immagine** (`6b634fb`), con pezzi adatti a ogni
    tela: col MCD dei lati, ora che la finestra cambia, venivano anche di
    5 px. Corrette due direzioni di scambio sbagliate;
  - **suoni** (`dcbc3c8`): nuovi per Halftone e Puzzle (muti: file
    inesistenti) e per Color & White (usava quello di Fold), sintetizzati
    da `devtools/content/magic_sounds.py`; Fade/Darken e Glass Tile ora
    suonano anche a tutta immagine. Mosaic lasciato com'è: il suo
    `mosaic.ogg` segnato FIXME è un suono vero, della stessa famiglia di
    Picasso, e il FIXME non dice che cosa non va;
  - **tastiera a schermo** (`b953dbb`, `e5a4fe7`): sui tasti anche i
    caratteri di Maiuscolo e AltGr, negli angoli; i caratteri oltre
    U+FFFF arrivano interi nel testo (coppia surrogata), ma i font del
    Testo, di SDL_ttf 2.0.11, li disegnano come carattere di sostituzione
    (resta nel TODO). Corretto un confronto con lunghezza 0 (`NoSymbol`);
  - **Halftone** (`58995a0`): una griglia di punti per inchiostro, ruotata
    al suo angolo, con gli inchiostri che si moltiplicano come sulla
    carta; prima la media dei colori faceva diventare lilla il blu;
  - **etichette su due righe** (`e90f53a`): i nomi che verrebbero
    schiacciati oltre 2/3 vanno su due righe a 10 punti, con l'icona più
    piccola sopra (in italiano per esempio "Arcobaleno vero", "Colore e
    bianco");
  - trovati lungo la strada: in 10 plugin, e nell'esempio della guida, il
    rettangolo da aggiornare durante il trascinamento aveva l'altezza
    sbagliata (`a2c6ef2`); due leak (suono di Drip, nome del layout della
    tastiera a ogni Testo, `6f79f5d`);
  - traduzioni (`7916a3f`): le sette stringhe nuove in it, ca, de, es, fr;
    pagine di `magic-docs` aggiornate, nuove per Punto croce e Puzzle
    (`b80699b`); `devtools/magic-test/magic_run.c` per provare i plugin
    senza interfaccia (`779d631`);
  - verifiche: a 800×600 schermata principale e dialoghi identici al
    riferimento, salvo il pannello delle magie (etichette su due righe);
    i plugin cambiati provati con `magic_run` su due immagini e sotto
    AddressSanitizer; in Tux Paint, anche a 1600×1200 e con
    ridimensionamenti, sotto AddressSanitizer: nessun errore di memoria,
    432 byte persi nelle librerie più i 15 del layout, poi corretti.
- [x] 2026-11-01 — UI scalabile con la finestra, le tre voci rimaste:
  - **unione in `master`**: avanzamento rapido a `feature/tools`
    (`baead7c`), che conteneva anche `feature/svg-icons` e
    `feature/resizable` (scelta dell'utente: unire tutto);
  - **icone ancora PNG** (branch `feature/more-svg-icons`, `c7414af`…
    `922b762`): `load_icon()` nell'API dei plugin, perché le icone delle
    magie le carica il plugin; SVG tracciati per 39 icone delle magie e
    10 dell'interfaccia (frecce, grassetto/corsivo, capovolgi,
    diapositive…), scelte una per una. Restano PNG quelle con sfumature,
    luci dentro zone scure o foto (31 magie, pulsanti a gel, tasti della
    tastiera a schermo, cestino, stampante, mouse, altoparlante, cuffia);
    i plugin hanno ora la versione 0x00010003, che Tux Paint 0.9.22
    rifiuta invece di andare in crash;
  - **dialoghi durante il ridimensionamento** (branch
    `feature/dialog-resize`, `6bfe48f`, `41af788`): richieste, selettore
    colore, Apri, Nuovo, scelta delle diapositive e presentazione si
    rifanno alla nuova dimensione, anche con Alt+Invio, conservando
    selezione e scorrimento;
  - verifiche: a 800×600 identico al riferimento (salvo il pannello delle
    magie, come prima); ogni dialogo portato a 1600×1200 e ritorno è
    identico al pixel a prima; AddressSanitizer: un uso dopo `free` del
    testo di Tux trovato e corretto, poi nessun errore; circa 19 KB persi
    in Pango/fontconfig, ricreando i font a ogni cambio di misura (resta
    nel TODO).
- [x] 2026-11-01 — Pubblicazione sulla repo GitHub dell'utente — remote
  `github` (`saulusprime/Tux-Paint2`, via SSH), tutti i 14 branch
  caricati e collegati al loro; `master` predefinito; `origin` (LliureX)
  non toccato.
- [x] 2026-11-01 — Unione in `master` di `feature/dialog-resize` —
  avanzamento rapido (contiene `feature/more-svg-icons`), su richiesta
  dell'utente prima della prova a mano, che resta nel TODO; caricato su
  `github`.
- [x] 2026-11-01 — Paolo Pierno tra i contributori — voce per il fork in
  `docs/AUTHORS.txt` e autore di `crossstitch.c`; branch `docs/authors`,
  unito in `master` e caricato su `github`.
