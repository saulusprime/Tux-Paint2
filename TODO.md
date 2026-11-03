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

Completa: le voci del 2026-11-01 sono chiuse e unite in `master` (vedi
[ASIS.md](ASIS.md) e `HANDOFF.md` §5bis).

- [ ] [P2] Prova a mano, ora che è in `master` (unito su richiesta
  dell'utente prima della prova): ridimensionamenti e Alt+Invio anche con
  un dialogo aperto, icone delle magie a 1600×1200.
- [ ] [P3] Ogni cambio di misura perde da pochi byte a circa 3 KB dentro
  Pango/fontconfig: SDL_Pango crea una fontmap per ogni font, e
  `change_screen()` ricrea quelli dell'interfaccia. Rimedio possibile:
  tenere i font dell'interfaccia per misura invece di ricrearli.
- [ ] [P3] Una richiesta dentro Apri ("Cancella"), se la finestra cambia
  mentre è aperta, ha dietro lo schermo principale invece della griglia
  di Apri, finché non si chiude.

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

## Qualità del codice (dai warning della build)

Fatto il 2026-10-31 (branch `quality/warnings`, vedi [ASIS.md](ASIS.md)):
la build è senza warning, anche quella con AddressSanitizer a `-O1`. Un
warning nuovo va guardato subito.

## Qualità del codice (dai FIXME nel sorgente)

Le otto voci scelte il 2026-10-29 sono chiuse (branch `quality/fixme`),
così come i leak dei plugin e di `magic_api_struct` (`quality/warnings`);
vedi [ASIS.md](ASIS.md). Nel sorgente restano altri FIXME minori, non
elencati qui.

- [ ] [P3] Suddividere `src/tuxpaint.c` (~24.500 righe) in moduli. Non
  fatto il 2026-10-31: è un lavoro lungo, da pianificare a parte (per
  esempio estraendo prima le parti più isolate: dialoghi Apri/Nuovo/
  presentazione, stampa, caricamento dei timbri, plugin Magia). I tre
  dialoghi sono copie quasi uguali (un FIXME chiede di unirli): i leak di
  `fs` erano in tutti e tre.

## Feature e miglioramenti strumenti

Le nove voci del 2026-10-29 sono chiuse e unite in `master` (branch
`feature/tools`, vedi [ASIS.md](ASIS.md) e `HANDOFF.md` §5quinquies).

- [ ] [P2] Prova a mano, ora che è in `master` (unito il 2026-11-01 su
  scelta dell'utente prima della prova): le quattro magie a tutta
  immagine, Punto croce, Schiuma colorata, Puzzle, Mezzatinta, i suoni
  nuovi, la tastiera a schermo, le etichette su due righe.
- [ ] [P3] Testo ed Etichetta: i caratteri oltre U+FFFF arrivano giusti
  nel testo, ma i font di questi strumenti passano da SDL_ttf 2.0.11, che
  sa disegnare solo i caratteri a 16 bit (ora mette il carattere di
  sostituzione). Si potrebbero disegnare con SDL_Pango, che li sa fare
  (`render_text_w()`).
- [ ] [P3] Tastiera a schermo: a 800×600 i tasti misurano 24 px e le
  scritte di Maiuscolo e AltGr negli angoli sono minuscole; si leggono da
  1600×1200 in su.
- [ ] [P3] Mezzatinta anche a tutta immagine: ora ogni pixel si calcola da
  solo, quindi è facile (va solo tenuto d'occhio il tempo su una tela
  grande).
- [ ] [P3] Documentazione delle magie (`magic/magic-docs/`): quattro non
  hanno una pagina (Fretwork, Halftone, Tornado, Xor Colors); tutte sono
  solo in inglese.

## Contenuti e localizzazione

Le voci del 2026-10-29 sono chiuse (branch `content/l10n`), e così le tre
rimaste, il 2026-11-03 (branch `content/l10n-more`): vedi
[ASIS.md](ASIS.md) e `HANDOFF.md` §5quater.

- [ ] [P2] Unire `content/l10n-more` in `master` con avanzamento rapido,
  dopo una prova a mano: la cartina dell'Italia (finestra Nuovo e magia
  Riempi), OPTIONS e FAQ in italiano, Punto croce in un'altra lingua.
- [ ] [P3] Le frasi del fork ("Schermo intero", Punto croce, le modalità a
  tutta immagine) sono in inglese in una sessantina di lingue poco
  diffuse, e Punto croce anche in bs, mk e sq: servirebbe chi le parla.
- [ ] [P3] Errori nelle traduzioni esistenti, visti di passaggio: in
  `hr.po` la magia Gesso si chiama "Izmješaj" ("mescola"); in `zh_CN.po`
  la descrizione a pennello di Fumetto parla di gesso; in `ko.po` la frase
  di Blocchi a tutta immagine è approssimativa.
- [ ] [P3] La FAQ (del 2009, inglese e italiana) cita
  `LOW_QUALITY_FLOOD_FILL`, che nel sorgente non c'è più, e un messaggio
  del lockfile diverso da quello vero ("You have already started tuxpaint
  less than 30 seconds ago…").
- [ ] [P3] Il Tux Paint di oggi ha dieci lingue in più (bn, brx, doi, kab,
  ks, ks@devanagari, sc, sd, sd@devanagari, ur), tra cui il sardo:
  servirebbero anche nella tabella delle lingue di `src/i18n.c`.
- [ ] [P3] ADVANCED-STAMPS-HOWTO e INSTALL restano in inglese (scelta
  dell'utente del 2026-11-02); i vecchi file italiani hanno l'avviso.

## Distribuzione (fuori obiettivo per ora)

Da riprendere solo se il fork smette di essere un progetto personale.

- [ ] [P3] Integrazione continua (GitHub Actions) che compila su Debian/Ubuntu.
- [ ] [P3] Metadati AppStream e verifica del file `.desktop` per i software
  center moderni.
- [ ] [P3] Pacchetto Flatpak o `.deb` per una distribuzione semplice.
- [ ] [P3] Rimuovere OpenCandy dagli script di installazione Windows
  (`win32/`, vedi `docs/CHANGES.txt` 0.9.22) — serve solo per distribuire
  su Windows.
