# Aprire il programma (schermata di avvio)

> Manuale dell'utente → Capitolo "Installazione e prima esecuzione" → dopo "Aprire il programma".

All'apertura di ROA compare una piccola schermata con il logo e una linea di
segnale che si disegna. Sotto di essa, a parole, il programma dice che cosa sta
facendo ("Caricamento delle librerie…", "Preparazione della schermata
iniziale…"). Questa schermata scompare da sola non appena la schermata iniziale
è pronta; non serve cliccare nulla.

**Prima apertura dopo l'installazione o un aggiornamento.** Il programma viene
preparato una volta sola (la schermata dice "Preparazione del programma per la
prima volta…") e salva il risultato nella cartella `.roa_cache`, accanto al
programma. Le volte successive l'apertura è molto più rapida. Se la cartella del
programma non permette la scrittura (per esempio in `Programmi`), la cache va
nella cartella dell'utente (`%LOCALAPPDATA%\ROA\cache`). Cancellare questa
cartella non crea problemi: viene ricreata all'apertura successiva.

**Se la schermata di avvio dà fastidio** (per esempio in un'automazione o su un
computer con problemi video), apri il programma con l'opzione `--sem-splash`
oppure imposta la variabile d'ambiente `ROA_SEM_SPLASH=1`.

**Aggiornamenti.** In *Aiuto → Controlla aggiornamenti* il programma continua a
scaricare solo il proprio codice, senza mai inviare dati tuoi. A partire da
questa versione può anche aggiornare il lanciatore (`EEG_Data_Collector.py`)
quando l'aggiornamento ne porta una versione nuova; se non ci riesce, avvisa e
il programma continua a funzionare con il lanciatore attuale.
