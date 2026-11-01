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

Completa. In `master` fino all'unione del 2026-11-01; finestra
ridimensionabile, schermo intero nitido e icone SVG di strumenti e forme
sui branch `feature/resizable` e `feature/svg-icons`. Vedi [ASIS.md](ASIS.md)
e `HANDOFF.md` §5bis.

- [ ] [P2] Unire in `master`, dopo una prova a mano di ridimensionamento e
  Alt+Invio: `feature/svg-icons` (contiene `feature/resizable`) è ora
  contenuto in `feature/tools`, e un solo avanzamento rapido a quest'ultimo
  li porta tutti (vedi la sezione seguente).
- [ ] [P3] Icone che restano PNG ingrandite: quelle delle magie
  (`magic/icons/`, 94, spesso fotografiche), altoparlante e cuffia, e le
  immagini dei dialoghi (Sì/No, frecce, cestino…). Le cornici dei
  pulsanti no: sono sfumature, già rese bene.
- [ ] [P3] Durante un dialogo il ridimensionamento mostra l'immagine
  tagliata o con bande nere fino al ritorno al disegno: i dialoghi non
  sanno rifare la loro disposizione.

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

Le nove voci del 2026-10-29 sono chiuse (branch `feature/tools`, vedi
[ASIS.md](ASIS.md) e `HANDOFF.md` §5quinquies).

- [ ] [P2] Unire `feature/tools` in `master` dopo una prova a mano: le
  quattro magie a tutta immagine, Punto croce, Schiuma colorata, Puzzle,
  Mezzatinta, i suoni nuovi, la tastiera a schermo, le etichette su due
  righe. Parte da `feature/svg-icons`, quindi lo contiene: basta un
  avanzamento rapido fino a qui.
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

Le quattro voci del 2026-10-29 sono chiuse (branch `content/l10n`, vedi
[ASIS.md](ASIS.md)): raccolta completa dei timbri con `./dev.sh stamps`,
`it.po` rivisto, manuale ed EXTENDING in italiano, sei Starter e modelli
per la scuola.

- [ ] [P3] Tradurre il resto della documentazione italiana (OPTIONS, FAQ,
  ADVANCED-STAMPS-HOWTO, INSTALL): scelto di non farlo il 2026-10-31. I
  vecchi file italiani hanno in testa un avviso che rimanda all'inglese.
- [ ] [P3] Allineare le altre traduzioni al modello attuale
  (`devtools/po/update-po.sh LINGUA…`): oggi solo `it.po` è allineato.
  Dei 119 cataloghi, oltre a `it` hanno tutte le stringhe `ca`, `de`, `es`
  e `fr`; a cento manca solo "Full screen" (l'azione del lanciatore),
  quattordici più vecchi hanno da 2 a 16 stringhe in meno (per esempio
  `si.po`, `bm.po`, `zu.po`).
- [ ] [P3] Cartina dell'Italia con le regioni come Starter: servono dati
  geografici con una licenza adatta (per esempio ISTAT, CC BY).

## Distribuzione (fuori obiettivo per ora)

Da riprendere solo se il fork smette di essere un progetto personale.

- [ ] [P3] Integrazione continua (GitHub Actions) che compila su Debian/Ubuntu.
- [ ] [P3] Metadati AppStream e verifica del file `.desktop` per i software
  center moderni.
- [ ] [P3] Pacchetto Flatpak o `.deb` per una distribuzione semplice.
- [ ] [P3] Rimuovere OpenCandy dagli script di installazione Windows
  (`win32/`, vedi `docs/CHANGES.txt` 0.9.22) — serve solo per distribuire
  su Windows.
