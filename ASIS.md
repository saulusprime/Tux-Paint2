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
