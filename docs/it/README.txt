                                  Tux Paint
                               versione 0.9.22

                Un semplice programma di disegno per bambini

                  Copyright 2002-2014 Bill Kendrick e altri
                        New Breed Software & Tux4Kids

                          bill@newbreedsoftware.com
                          http://www.tuxpaint.org/

                       14 giugno 2002 - 5 agosto 2014

     Traduzione italiana della versione 0.9.22, aggiornata nel 2026 per
     questo fork di Tux Paint. La traduzione precedente, della versione
             0.9.14, era di Flavio "Iron Bishop" Pastore (2004).
     __________________________________________________________________

        Indice
     * Informazioni
     * Differenze di questa versione
     * Usare Tux Paint
     * Caricare altre immagini in Tux Paint
     * Altra documentazione
     * Come ottenere aiuto
     __________________________________________________________________

                                  Informazioni

Che cos'è Tux Paint?

     Tux Paint è un programma di disegno libero pensato per i bambini
     piccoli (dai 3 anni in su). Ha un'interfaccia semplice e facile da
     usare, effetti sonori divertenti e una mascotte a fumetti che
     incoraggia i bambini e li guida mentre usano il programma. Mette a
     disposizione una tela bianca e diversi strumenti di disegno per
     aiutare il bambino a esprimere la sua creatività.

Licenza

     Tux Paint è un progetto Open Source, software libero distribuito con
     la GNU General Public License (GPL). È gratuito, e il «codice
     sorgente» del programma è disponibile. (Questo permette ad altri di
     aggiungere funzioni, correggere errori e usare parti del programma
     nel proprio software distribuito con la GPL.)

     Il testo completo della licenza GPL è nel file COPYING.txt (in
     inglese, l'unico con valore legale); una traduzione italiana non
     ufficiale è in COPIATURA.txt.

Obiettivi

   Facile e divertente
          Tux Paint vuole essere un semplice programma di disegno per
          bambini piccoli, non uno strumento di disegno per ogni uso.
          Vuole essere divertente e facile da usare. Gli effetti sonori e
          un personaggio a fumetti aiutano a capire che cosa sta
          succedendo e tengono compagnia. Anche i puntatori del mouse sono
          grandi e in stile fumetto.

   Espandibilità
          Tux Paint si può espandere: pennelli e «timbri» si possono
          aggiungere e togliere. Per esempio, un insegnante può aggiungere
          una raccolta di animali e chiedere agli alunni di disegnare un
          ecosistema. Ogni timbro può avere un suono, che viene
          riprodotto, e una descrizione, che viene mostrata, quando il
          bambino lo sceglie.

   Portabilità
          Tux Paint funziona su diversi sistemi: Windows, Macintosh,
          Linux, ecc. L'interfaccia è la stessa su tutti. Tux Paint
          funziona bene anche sui computer vecchi (come un Pentium 133), e
          si può compilare in modo da andare meglio sui sistemi lenti.

   Semplicità
          Non c'è accesso diretto ai dettagli del computer. Il disegno
          corrente viene conservato quando si esce dal programma e
          ricompare al riavvio. Per salvare i disegni non serve inventare
          nomi di file né usare la tastiera. Per aprire un disegno basta
          sceglierlo da una raccolta di miniature. L'accesso agli altri
          file del computer è limitato.
     __________________________________________________________________

                         Differenze di questa versione

     Questa è una versione modificata (un «fork») di Tux Paint 0.9.22,
     pensata per Linux. Rispetto alla 0.9.22 originale:
     * Interfaccia che si adatta alla finestra. Fino a 800x600 tutto è
       come nell'originale; nelle finestre più grandi pulsanti, testi,
       cursori e finestre di dialogo crescono in proporzione, invece di
       restare piccoli in un angolo. L'opzione buttonsize permette di
       scegliere pulsanti più piccoli. Se non si indica la dimensione
       della finestra, sugli schermi grandi Tux Paint si apre in una
       finestra più grande (vedi "Caricare altre immagini" per le
       dimensioni della tela).
     * Schermo intero. [Alt] + [Invio] passa dalla finestra allo schermo
       intero e viceversa. Con l'opzione --fullscreen (o fullscreen=yes
       nel file di configurazione) senza indicare una dimensione,
       Tux Paint si apre direttamente alla risoluzione dello schermo. Nel
       menu del desktop, l'icona di Tux Paint ha anche la voce "Schermo
       intero" (clic destro sull'icona).
     * Raccolta completa dei timbri. Il programma comprende solo pochi
       timbri di esempio. La raccolta completa (quasi mille timbri, quasi
       tutti con la descrizione in italiano) si installa con il comando
       ./dev.sh stamps dalla cartella del sorgente: vedi EXTENDING.
     * Starter e modelli per la scuola. Nella finestra "Nuovo" ci sono
       anche un orologio e una scuola da colorare, una lavagna, un
       quaderno a righe, un quaderno a quadretti e un quaderno
       pentagrammato.
     * Correzioni. Molti difetti della 0.9.22 sono stati corretti: tra gli
       altri, il Cestino che poteva perdere i disegni cancellati, i
       disegni fatti da uno Starter che perdevano lo sfondo se lo Starter
       non c'era più, i modelli personali che non si aprivano e la
       traduzione italiana, rivista.
     __________________________________________________________________

                                Usare Tux Paint

Avviare Tux Paint

  Linux/Unix

     Tux Paint dovrebbe aver aggiunto un'icona nel menu del desktop
     (GNOME, KDE e altri), tra i programmi di "Grafica" o di
     "Istruzione". Facendo clic destro sull'icona si trova anche la voce
     "Schermo intero".

     In alternativa, si può dare questo comando in un terminale (dopo il
     prompt, per esempio "$"):

     $ tuxpaint

     Se ci sono errori, vengono mostrati nel terminale (su "stderr").
       _______________________________________________________________

  Windows

                                                                   [Icona]
                                                                 Tux Paint

     Se Tux Paint è stato installato con il programma di installazione,
     questo ha chiesto se aggiungere un collegamento nel menu "Start" e/o
     sul desktop. In questo caso basta avviare Tux Paint dalla sezione
     "Tux Paint" del menu "Start" (per esempio in "Tutti i programmi" su
     Windows XP), oppure con un doppio clic sull'icona "Tux Paint" del
     desktop.

     Se Tux Paint è stato installato dal file ZIP, oppure con il
     programma di installazione ma senza collegamenti, bisogna fare
     doppio clic sull'icona "tuxpaint.exe" nella cartella di Tux Paint.

     Il programma di installazione mette la cartella di Tux Paint in
     "C:\Program Files\", a meno che non sia stata scelta un'altra
     cartella durante l'installazione.

     Con il file ZIP, la cartella di Tux Paint è dove la si è estratta.
       _______________________________________________________________

  Mac OS X

     Basta fare doppio clic sull'icona "Tux Paint".
       _______________________________________________________________

Schermata iniziale

     All'avvio, Tux Paint mostra una schermata con il titolo e i
     riconoscimenti.

                             [Schermata iniziale]

     Quando il caricamento è finito, premi un tasto o fai clic con il
     mouse per continuare. (Altrimenti, dopo circa 30 secondi la
     schermata iniziale si chiude da sola.)
       _______________________________________________________________

Schermata principale

     La schermata principale è divisa in queste parti:

   A sinistra: gli strumenti
          La barra degli strumenti contiene i comandi per disegnare e per
          modificare il disegno.

          [Strumenti: Pittura, Timbro, Linee, Forme, Testo, Magie,
          Etichetta, Annulla, Ripeti, Gomma, Nuovo, Apri, Salva, Stampa,
          Esci]

   Al centro: la tela
          La parte più grande dello schermo, al centro, è la tela.
          Ovviamente è qui che si disegna!

          [(Tela)]

          Nota: la dimensione della tela dipende dalla dimensione di
          Tux Paint. La si può cambiare con il programma di configurazione
          Tux Paint Config. o in altri modi: vedi la documentazione delle
          opzioni (in inglese) per i dettagli. In questa versione la
          finestra si apre già più grande sugli schermi grandi, e
          [Alt] + [Invio] passa allo schermo intero.

   A destra: il selettore
          Il selettore mostra cose diverse a seconda dello strumento
          scelto. Per esempio, con lo strumento Pittura mostra i pennelli
          disponibili; con lo strumento Timbro mostra i timbri che si
          possono usare.

          [Selettori: Pennelli, Lettere, Forme, Timbri]

   In basso: i colori
          Verso il fondo dello schermo c'è una tavolozza con i colori
          disponibili.

          [Colori: nero, bianco, rosso, rosa, arancione, giallo, verde,
          azzurro, blu, viola, marrone, grigio]

          (Nota: si possono definire colori propri per Tux Paint. Vedi la
          documentazione delle opzioni.)

   In fondo: l'area dei suggerimenti
          In fondo allo schermo, Tux, il pinguino di Linux, dà consigli e
          altre informazioni mentre disegni.

          (Per esempio: 'Scegli una forma. Fai clic per scegliere il
          centro, trascina e poi rilascia il pulsante quando è grande
          quanto desideri. Muovi il mouse per ruotare la forma e fai clic
          per completare.')
       _______________________________________________________________

Gli strumenti

  Strumenti di disegno

   Pittura (pennello)
          Lo strumento Pittura permette di disegnare a mano libera, con
          diversi pennelli (scelti nel selettore a destra) e colori
          (scelti nella tavolozza in basso).

          Tenendo premuto il pulsante del mouse e muovendo il mouse, si
          disegna seguendo il movimento.

          Mentre disegni si sente un suono: più il pennello è grande, più
          il suono è grave.
            ___________________________________________________________

   Timbro
          Lo strumento Timbro è come una serie di timbri o di adesivi:
          permette di incollare nel disegno immagini già pronte, disegnate
          o fotografiche (per esempio un cavallo, un albero o la luna).

          Mentre muovi il mouse sulla tela, un contorno lo segue e mostra
          dove verrà messo il timbro e quanto sarà grande.

          I timbri possono essere divisi in molte categorie (per esempio
          animali, piante, spazio, veicoli, persone, ecc.). Con le frecce
          a sinistra e a destra si passa da una raccolta all'altra.

          Alcuni timbri si possono colorare o tingere. Se la tavolozza
          sotto la tela è attiva, puoi fare clic sui colori per cambiare
          la tinta o il colore del timbro prima di metterlo nel disegno.

          I timbri si possono rimpicciolire e ingrandire, e molti si
          possono capovolgere o mostrare allo specchio, con i comandi in
          basso a destra dello schermo.

          Ogni timbro può avere i suoi effetti sonori e/o una descrizione
          parlata. I pulsanti in basso a sinistra (vicino a Tux, il
          pinguino di Linux) permettono di riascoltare l'effetto sonoro e
          la descrizione del timbro scelto.

          (Nota: con l'opzione "nostampcontrols", Tux Paint non mostra i
          comandi per specchiare, capovolgere, rimpicciolire e ingrandire
          i timbri. Vedi la documentazione delle opzioni.)

          (Nota: in questa versione la raccolta completa dei timbri si
          installa con ./dev.sh stamps; vedi "Differenze di questa
          versione".)
            ___________________________________________________________

   Linee
          Questo strumento permette di disegnare linee dritte, con gli
          stessi pennelli e colori dello strumento Pittura.

          Fai clic e tieni premuto il pulsante del mouse per scegliere il
          punto di partenza della linea. Mentre muovi il mouse, una linea
          sottile «elastica» mostra dove verrà disegnata.

          Rilascia il pulsante per completare la linea. Si sentirà un
          «sproing!».
            ___________________________________________________________

   Forme
          Questo strumento permette di disegnare semplici forme, piene o
          vuote.

          Scegli una forma nel selettore a destra (cerchio, quadrato,
          ellisse, ecc.).

          Sulla tela, fai clic e tieni premuto il pulsante del mouse per
          allargare la forma a partire dal punto in cui hai fatto clic.
          Alcune forme possono cambiare proporzioni (per esempio il
          rettangolo e l'ellisse), altre no (per esempio il quadrato e il
          cerchio).

          Rilascia il pulsante quando la forma è grande quanto vuoi.

        Modo normale
                Ora puoi muovere il mouse sulla tela per ruotare la forma.

                Fai di nuovo clic e la forma verrà disegnata con il colore
                scelto.

        Modo forme semplici
                Se le forme semplici sono attive (per esempio con
                l'opzione "--simpleshapes"), la forma viene disegnata
                sulla tela appena rilasci il pulsante del mouse, senza il
                passo della rotazione.
            ___________________________________________________________

   Testo ed Etichetta
          Scegli un tipo di carattere (tra le "Lettere" a destra) e un
          colore (dalla tavolozza in basso). Fai clic sul disegno e
          comparirà un cursore. Scrivi, e il testo comparirà sullo
          schermo.

          Premi [Invio] e il testo verrà scritto sul disegno, mentre il
          cursore scenderà di una riga.

          Oppure premi [Tab]: il testo verrà scritto sul disegno, ma il
          cursore si sposterà alla destra del testo invece di andare a
          capo. (Così si può scrivere una riga di testo con colori,
          caratteri, stili e dimensioni diversi: come questa.)

          Facendo clic in un altro punto del disegno mentre stai ancora
          scrivendo, la riga di testo si sposta lì (e puoi continuare a
          modificarla).

        Testo o Etichetta?
                Lo strumento Testo è quello originale di Tux Paint per
                scrivere. Il testo scritto con questo strumento non si può
                modificare né spostare dopo, perché diventa parte del
                disegno. Proprio per questo, però, ci si può disegnare
                sopra o lo si può trasformare con gli effetti dello
                strumento Magie (sfumarlo, tingerlo, metterlo in rilievo,
                ecc.).

                Con lo strumento Etichetta (aggiunto in Tux Paint 0.9.22),
                il testo «galleggia» sopra il disegno, e i dati
                dell'etichetta (il testo, la posizione, il tipo di
                carattere e il colore) vengono conservati a parte. Così
                l'etichetta si può spostare o modificare anche in seguito.

                Lo strumento Etichetta si può disattivare (per esempio con
                "Disable 'Label' Tool" in Tux Paint Config. o avviando
                Tux Paint con l'opzione "--nolabel").

        Caratteri delle altre lingue
                Tux Paint permette di scrivere caratteri di lingue
                diverse. La maggior parte dei caratteri latini (A-Z, ñ, è,
                ecc.) si può scrivere direttamente. Alcune lingue
                richiedono di passare a un metodo di scrittura diverso
                prima di scrivere, e alcuni caratteri si compongono con
                più tasti.

                Quando la lingua di Tux Paint è una di quelle che hanno
                metodi di scrittura particolari, un tasto permette di
                passare dal modo normale (caratteri latini) a quello o
                quelli della lingua.

                Ecco le lingue supportate, i metodi di scrittura
                disponibili e il tasto che li cambia. Nota: molti tipi di
                carattere non contengono tutti i caratteri di tutte le
                lingue, quindi a volte bisogna cambiare carattere per
                vedere quello che si sta scrivendo.

               o Giapponese — Hiragana e Katakana in caratteri latini —
                 [Alt] destro
               o Coreano — Hangul 2-Bul — [Alt] destro o [Alt] sinistro
               o Cinese tradizionale — [Alt] destro o [Alt] sinistro
               o Thailandese — [Alt] destro
            ___________________________________________________________

   Magie (effetti speciali)
          Lo strumento Magie è in realtà un insieme di strumenti speciali.
          Scegli uno degli effetti «magici» nel selettore a destra. Poi, a
          seconda dello strumento, puoi fare clic e trascinare sul
          disegno, oppure fare un solo clic sul disegno, per applicare
          l'effetto.

          Se lo strumento si usa facendo clic e trascinando, sotto
          l'elenco delle magie a destra c'è, a sinistra, un pulsante
          «pennello». Se lo strumento può cambiare tutto il disegno in una
          volta, c'è a destra un pulsante «tutto il disegno».

          Vedi le istruzioni di ogni magia (nella cartella "magic-docs",
          in inglese).
            ___________________________________________________________

   Gomma
          Questo strumento è simile al pennello. Dove fai clic (o fai clic
          e trascini), il disegno viene cancellato. (Al suo posto può
          comparire il bianco, un altro colore o un'immagine di sfondo, a
          seconda del disegno.)

          Ci sono gomme di diverse dimensioni, sia rotonde sia quadrate.

          Mentre muovi il mouse, un contorno segue il puntatore e mostra
          quale parte del disegno verrà cancellata.

          Mentre cancelli si sente il suono di una gomma che strofina.
       _______________________________________________________________

  Altri comandi

   Annulla
          Questo pulsante annulla l'ultima azione di disegno. Si può
          annullare anche più di una volta!

          Nota: per annullare puoi anche premere [Ctrl] + [Z] sulla
          tastiera.
            ___________________________________________________________

   Ripeti
          Questo pulsante rifà l'azione di disegno che hai appena
          annullato con il pulsante "Annulla".

          Finché non disegni di nuovo, puoi ripetere tante volte quante
          hai annullato!

          Nota: per ripetere puoi anche premere [Ctrl] + [R] sulla
          tastiera.
            ___________________________________________________________

   Nuovo
          Il pulsante "Nuovo" fa iniziare un nuovo disegno. Si apre una
          finestra dove puoi scegliere di iniziare con uno sfondo di un
          solo colore, con uno «Starter» o con un «modello» (vedi sotto).
          Prima ti verrà chiesto se vuoi davvero farlo.

          Nota: per iniziare un nuovo disegno puoi anche premere
          [Ctrl] + [N] sulla tastiera.

          Starter e modelli

     Gli «Starter» possono essere come la pagina di un album da colorare
     (il contorno in bianco e nero di un'immagine, da colorare), oppure
     come una fotografia in 3D, dove si disegna nelle parti in mezzo. Il
     contorno resta sempre sopra quello che disegni.
     I «modelli» sono immagini di sfondo su cui disegnare: ci puoi
     disegnare sopra dappertutto, e la gomma fa ricomparire l'immagine
     originale.
     Quando apri uno Starter o un modello, ci disegni e poi fai clic su
     "Salva", viene creato un nuovo disegno (l'originale non viene
     sovrascritto, così lo puoi usare di nuovo).
     Per crearne di nuovi, vedi EXTENDING.
            ___________________________________________________________

   Apri
          Mostra l'elenco di tutti i disegni che hai salvato. Se non
          entrano tutti nello schermo, usa le frecce "su" e "giù" in cima
          e in fondo all'elenco per scorrerlo.

          Fai clic su un disegno per sceglierlo, poi...

          + Fai clic sul pulsante verde "Apri", in basso a sinistra
            dell'elenco, per aprire il disegno scelto.
            (In alternativa, puoi fare doppio clic sulla miniatura del
            disegno.)
          + Fai clic sul pulsante marrone "Cancella" (il cestino), in
            basso a destra dell'elenco, per cancellare il disegno scelto.
            (Ti verrà chiesta una conferma.)
            Nota: dalla versione 0.9.22, su Linux il disegno finisce nel
            Cestino del desktop, da dove si può ancora recuperare.
          + Fai clic sul pulsante blu "Diapositive" (il proiettore), in
            basso a sinistra, per passare alla presentazione. Vedi
            "Diapositive", più avanti, per i dettagli.
          + Oppure fai clic sulla freccia rossa "Indietro", in basso a
            destra dell'elenco, per tornare al disegno che stavi facendo
            senza aprirne un altro.

          Se scegli di aprire un disegno e quello corrente non è stato
          salvato, ti verrà chiesto se vuoi salvarlo. (Vedi "Salva", più
          avanti.)

          Nota: per aprire la finestra "Apri" puoi anche premere
          [Ctrl] + [O] sulla tastiera.
            ___________________________________________________________

   Salva
          Salva il disegno corrente.

          Se non l'hai mai salvato, viene aggiunto all'elenco dei disegni
          salvati (cioè viene creato un nuovo file).

          Nota: non ti viene chiesto niente (per esempio un nome di file).
          Il disegno viene semplicemente salvato, con il rumore dello
          scatto di una macchina fotografica.

          Se invece avevi già salvato il disegno, o se è un disegno appena
          aperto con "Apri", prima ti viene chiesto se vuoi sostituire la
          versione precedente o crearne una nuova (un nuovo file).

          (Nota: con le opzioni "saveover" o "saveovernew" la domanda non
          viene fatta. Vedi la documentazione delle opzioni.)

          Nota: per salvare puoi anche premere [Ctrl] + [S] sulla
          tastiera.
            ___________________________________________________________

   Stampa
          Fai clic su questo pulsante e il disegno verrà stampato!

          Sulla maggior parte dei sistemi si può anche tenere premuto il
          tasto [Alt] ([Opzione] sui Mac) mentre si fa clic su "Stampa",
          per aprire una finestra di stampa. Questo potrebbe non
          funzionare a schermo intero; vedi sotto.

        Disattivare la stampa
                Con l'opzione "noprint" (cioè "noprint=yes" nel file di
                configurazione di Tux Paint, o "--noprint" sulla riga di
                comando), il pulsante "Stampa" è disattivato.

                Vedi la documentazione delle opzioni.

        Limitare la stampa
                Con l'opzione "printdelay" (cioè "printdelay=SECONDI" nel
                file di configurazione, o "--printdelay=SECONDI" sulla
                riga di comando), si può stampare solo una volta ogni
                SECONDI secondi.

                Per esempio, con "printdelay=60" si può stampare solo una
                volta al minuto.

                Vedi la documentazione delle opzioni.

        Comandi di stampa
                (Solo Linux e Unix)

                Tux Paint stampa creando una versione PostScript del
                disegno e mandandola a un programma esterno. Il programma
                predefinito è:

     lpr

                Il comando si può cambiare con il valore "printcommand"
                nel file di configurazione di Tux Paint.

                Se mentre fai clic su "Stampa" tieni premuto il tasto
                [Alt], e non sei a schermo intero, viene usato un
                programma alternativo. Quello predefinito è la finestra di
                stampa di KDE:

     kprinter

                Il comando si può cambiare con il valore "altprintcommand"
                nel file di configurazione di Tux Paint.

                Per sapere come cambiare i comandi di stampa, vedi la
                documentazione delle opzioni.

        Impostazioni della stampante
                (Windows e Mac OS X)

                Normalmente, quando si preme "Stampa", Tux Paint stampa
                sulla stampante predefinita con le impostazioni
                predefinite.

                Se però tieni premuto il tasto [Alt] (o [Opzione]) mentre
                premi il pulsante, e non sei a schermo intero, compare la
                finestra di stampa del sistema operativo, dove puoi
                cambiare le impostazioni.

                Con l'opzione "printcfg" (cioè "--printcfg" sulla riga di
                comando o "printcfg=yes" nel file di configurazione di
                Tux Paint, "tuxpaint.cfg"), le impostazioni cambiate
                vengono conservate.

                Con l'opzione "printcfg", le impostazioni della stampante
                vengono lette dal file "print.cfg" nella tua cartella
                personale (vedi sotto), dove vengono salvate anche le
                modifiche.

                Vedi la documentazione delle opzioni.

        Quando compare la finestra di stampa
                Normalmente Tux Paint mostra la finestra di stampa (o, su
                Linux/Unix, usa "altprintcommand", per esempio "kprinter"
                invece di "lpr") solo se si tiene premuto il tasto [Alt]
                (o [Opzione]) mentre si fa clic su "Stampa".

                Questo comportamento si può cambiare. Per far comparire
                sempre la finestra di stampa si usa "--altprintalways"
                sulla riga di comando, o "altprint=always" nel file di
                configurazione. Per fare in modo che il tasto
                [Alt]/[Opzione] non abbia effetto si usa
                "--altprintnever", o "altprint=never".

                Vedi la documentazione delle opzioni.
            ___________________________________________________________

   Diapositive (nella finestra "Apri")
          Il pulsante "Diapositive" si trova nella finestra "Apri", e
          mostra l'elenco dei disegni salvati, proprio come "Apri".

          Fai clic, uno alla volta, sui disegni che vuoi mostrare in una
          presentazione. Su ogni disegno compare un numero, che indica in
          che ordine verrà mostrato.

          Facendo clic su un disegno già scelto lo togli dalla
          presentazione.

          Una barra in basso a sinistra (vicino al pulsante "Mostra")
          regola la velocità della presentazione, dalla più lenta alla più
          veloce.

          Nota: con l'impostazione più lenta, quella più a sinistra, le
          diapositive non avanzano da sole: per passare alla successiva
          bisogna premere un tasto o fare clic (vedi sotto). Usala quando
          vuoi andare avanti a mano.

          Quando sei pronto, fai clic su "Mostra" per iniziare la
          presentazione. (Nota: se non hai scelto NESSUN disegno, vengono
          mostrati TUTTI.)

          Durante la presentazione, premi [Spazio], [Invio] o la
          [freccia a destra], o fai clic sul pulsante "Avanti" in basso a
          sinistra, per passare alla diapositiva successiva. Premi la
          [freccia a sinistra] per tornare a quella precedente.

          Premi [Esc], o fai clic sul pulsante "Indietro" in basso a
          destra, per uscire dalla presentazione e tornare alla scelta dei
          disegni.

          Nella scelta dei disegni, fai clic su "Indietro" per tornare
          alla finestra "Apri".

   Esci
          Facendo clic sul pulsante "Esci", chiudendo la finestra di
          Tux Paint o premendo il tasto [Esc], si esce da Tux Paint.

          Prima ti viene chiesto se vuoi davvero uscire.

          Se scegli di uscire e non hai salvato il disegno corrente, ti
          viene chiesto se vuoi salvarlo. Se non è un disegno nuovo, ti
          viene poi chiesto se vuoi sostituire la versione precedente o
          crearne una nuova. (Vedi "Salva", sopra.)

          Nota: se il disegno viene salvato, verrà riaperto
          automaticamente la prossima volta che avvii Tux Paint!

          Nota: il pulsante "Esci" e il tasto [Esc] si possono disattivare
          (per esempio con "Disable 'Quit' Button" in Tux Paint Config. o
          avviando Tux Paint con l'opzione "--noquit").

          In questo caso, per uscire si può usare il pulsante di chiusura
          nella barra del titolo della finestra di Tux Paint (se non è a
          schermo intero) o la combinazione di tasti [Alt] + [F4].

          Se nessuna delle due è possibile, si può usare la combinazione
          [Maiusc] + [Ctrl] + [Esc]. (Vedi la documentazione delle
          opzioni.)

   Togliere l'audio
          Per ora non c'è un pulsante sullo schermo, ma premendo
          [Alt] + [S] si possono disattivare e riattivare gli effetti
          sonori mentre il programma è in uso.

          Se però l'audio è disattivato del tutto (per esempio togliendo
          "Enable Sound Effects" in Tux Paint Config o avviando Tux Paint
          con l'opzione "--nosound"), [Alt] + [S] non ha effetto. (Cioè
          non si può usare per riattivare l'audio quando un genitore o un
          insegnante l'ha disattivato.)

   Schermo intero
          (Solo in questa versione)

          Premendo [Alt] + [Invio] si passa dalla finestra allo schermo
          intero, e viceversa. Se Tux Paint è partito in una finestra, a
          schermo intero l'immagine della finestra viene ingrandita per
          riempire lo schermo. Per avere l'interfaccia alla piena
          risoluzione dello schermo, avvia Tux Paint direttamente a
          schermo intero: con la voce "Schermo intero" del menu
          dell'icona, o con l'opzione "--fullscreen".
     __________________________________________________________________

                      Caricare altre immagini in Tux Paint

     La finestra "Apri" di Tux Paint mostra solo i disegni fatti con
     Tux Paint. Come fare per caricare un'altra immagine, o una
     fotografia, e modificarla in Tux Paint?

     Basta convertire l'immagine in un file PNG (Portable Network
     Graphic) e metterla nella cartella "saved" di Tux Paint:

   Windows Vista
          Nella cartella "AppData" dell'utente, per esempio:
          "C:\Users\(nome utente)\AppData\Roaming\TuxPaint\saved\"

   Windows 95, 98, ME, 2000, XP
          Nella cartella "Application Data" dell'utente, per esempio:
          "C:\Documents and Settings\(nome utente)\Application
          Data\TuxPaint\saved\"

   Mac OS X
          Nella cartella "Library" dell'utente:
          "/Users/(nome utente)/Library/Application
          Support/Tux Paint/saved/"

   Linux/Unix
          Nella cartella nascosta ".tuxpaint", dentro la cartella
          personale dell'utente: "$(HOME)/.tuxpaint/saved/"

     Nota: è sempre da questa cartella che puoi copiare o aprire con
     altri programmi i disegni fatti con Tux Paint.

Con 'tuxpaint-import'

     Su Linux e Unix si può usare lo script "tuxpaint-import", che viene
     installato insieme a Tux Paint. Usa alcuni programmi di NetPBM per
     convertire l'immagine ("anytopnm"), ridimensionarla perché entri
     nella tela di Tux Paint ("pnmscale") e convertirla in PNG
     ("pnmtopng").

     Usa anche il comando "date" per avere la data e l'ora, perché i
     disegni salvati da Tux Paint hanno come nome proprio la data e
     l'ora. (Ricorda: quando salvi o apri un disegno, non ti viene mai
     chiesto un nome di file!)

     Per usare 'tuxpaint-import' basta lanciarlo da un terminale,
     dandogli il nome del file o dei file da convertire.

     I file vengono convertiti e messi nella cartella 'saved' di
     Tux Paint. (Nota: se lo fai per un altro utente, per esempio tuo
     figlio, devi lanciare il comando con il suo account.)

     Esempio:

     $ tuxpaint-import nonna.jpg
     nonna.jpg -> /home/nomeutente/.tuxpaint/saved/20020921123456.png
     jpegtopnm: WRITING A PPM FILE

     La prima riga ("tuxpaint-import nonna.jpg") è il comando da dare. Le
     due righe seguenti sono i messaggi del programma mentre lavora.

     Ora puoi avviare Tux Paint: una versione dell'immagine originale
     sarà nella finestra "Apri". Basta un doppio clic sulla sua
     miniatura!

A mano

     Su Windows, Mac OS X e BeOS, per ora, la conversione va fatta a
     mano.

     Apri un programma di grafica che sappia aprire la tua immagine e
     salvarla in formato PNG. (Nel documento "PNG.txt" c'è un elenco di
     programmi consigliati e altre informazioni.)

     Quando Tux Paint apre un'immagine che non ha la stessa dimensione
     della tela, la ridimensiona (e a volte ne allunga i bordi) perché
     entri nella tela.

     Per evitare che l'immagine venga deformata o allungata, puoi
     ridimensionarla alla dimensione della tela di Tux Paint. Questa
     dipende dalla dimensione della finestra di Tux Paint, o dalla
     risoluzione dello schermo se è a schermo intero. (Nota: la
     dimensione predefinita è 800x600; in questa versione, sugli schermi
     grandi la finestra si apre più grande, vedi sotto.) Vedi "Calcolare
     la dimensione della tela", più avanti.

     Salva l'immagine in formato PNG. È vivamente consigliato dare al
     file come nome la data e l'ora, come fa Tux Paint:

     AAAAMMGGhhmmss.png

     * AAAA = anno
     * MM = mese (01-12)
     * GG = giorno (01-31)
     * hh = ora, da 00 a 23
     * mm = minuti (00-59)
     * ss = secondi (00-59)

     Per esempio:

     20020921130500 - per il 21 settembre 2002, alle 13:05:00

     Metti questo file PNG nella cartella 'saved' di Tux Paint (vedi
     sopra).

  Calcolare la dimensione della tela

     In questa versione pulsanti e margini crescono con la finestra,
     quindi il calcolo è diverso da quello della 0.9.22 originale (che
     vale ancora fino a 800x600). Indichiamo con L e A la larghezza e
     l'altezza della finestra (o dello schermo, a schermo intero):
    1. La scala è il più piccolo tra (lato lungo / 800) e (lato
       corto / 600), ma almeno 1.
    2. Il lato dei pulsanti P è 48 × scala, arrotondato per difetto. (Se
       si usa l'opzione buttonsize con un valore più piccolo, P è quel
       valore.)
    3. La larghezza della tela è L − 4 × P (due colonne di pulsanti a
       sinistra e due a destra).
    4. Per l'altezza servono due misure, arrotondate all'intero più
       vicino: il titolo T = 40 × P / 48 e l'area di Tux X = 56 × P / 48.
       Le righe di pulsanti sono (A − T − X − P) / P, arrotondato per
       difetto, e l'altezza della tela è T + righe × P.

     Esempi:
     * Finestra 800x600: scala 1, P = 48, tela larga 800 − 192 = 608;
       righe (600 − 40 − 56 − 48) / 48 = 9,5, cioè 9; altezza
       40 + 9 × 48 = 472. Tela: 608x472.
     * Finestra 1600x1200: scala 2, P = 96, tela larga 1600 − 384 = 1216;
       T = 80, X = 112, righe (1200 − 80 − 112 − 96) / 96 = 9,5, cioè 9;
       altezza 80 + 9 × 96 = 944. Tela: 1216x944, il doppio esatto.
     * Schermo intero 1440x900: scala 1,5 (900 / 600), P = 72, tela larga
       1440 − 288 = 1152; T = 60, X = 84, righe
       (900 − 60 − 84 − 72) / 72 = 9,5, cioè 9; altezza 60 + 9 × 72 = 708.
       Tela: 1152x708.

     Se non si sceglie la dimensione della finestra, sugli schermi grandi
     la finestra è il multiplo intero più grande di 800x600 che sta nel
     90% della larghezza e nell'85% dell'altezza dello schermo (per
     esempio 1600x1200 su uno schermo 2560x1600). Le immagini fatte per
     la tela di 800x600 (608x472) vanno bene a tutte queste dimensioni,
     perché la proporzione resta la stessa.
     __________________________________________________________________

                              Altra documentazione

     Altri documenti forniti con Tux Paint (nella cartella "docs"):
     * EXTENDING.html
       Come creare pennelli, timbri, Starter e modelli, e aggiungere tipi
       di carattere, per espandere Tux Paint (in italiano).
     * Documentazione delle magie ("magic-docs")
       La descrizione di ogni magia installata (in inglese).
     * AUTHORS.txt
       Elenco degli autori e dei collaboratori (di una versione
       precedente; quello aggiornato, in inglese, è in docs/AUTHORS.txt).
     * CHANGES.txt
       Le novità di ogni versione (in inglese).
     * COPIATURA.txt
       La licenza (GNU General Public License), in una traduzione italiana
       non ufficiale; l'originale inglese è in COPYING.txt.
     * INSTALL.txt
       Istruzioni per compilare e installare (in inglese).
     * OPTIONS.html
       Le opzioni della riga di comando e del file di configurazione, per
       chi non vuole usare Tux Paint Config. (in inglese).
     * PNG.txt
       Note sulla creazione di immagini PNG da usare in Tux Paint.
     * SVG.txt
       Note sulla creazione di immagini vettoriali SVG da usare in
       Tux Paint (in inglese).
     __________________________________________________________________

                              Come ottenere aiuto

     Se hai bisogno di aiuto, puoi contattare New Breed Software:

     http://www.newbreedsoftware.com/

     Puoi anche partecipare alle mailing list di Tux Paint:

     http://www.tuxpaint.org/lists/

     Le modifiche di questa versione non vengono dall'upstream: per
     problemi che riguardano solo questa versione non scrivere alle liste
     di Tux Paint.
