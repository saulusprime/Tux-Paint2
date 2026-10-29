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
- [x] 2026-10-29 — Bug: il ricolore del pulsante del colore personalizzato
  (`search_label_list`) scriveva oltre il bordo dell'immagine (ciclo fisso
  48×48) — corretto in `d346e60`.
