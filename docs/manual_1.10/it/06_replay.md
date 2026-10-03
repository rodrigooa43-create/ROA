# Replay: vedere la registrazione come un'animazione

> Manuale dell'utente → Capitolo "Rivedere una registrazione" → nuova sezione "Replay" (dopo "Referto PDF").

Aprendo una registrazione di **muscoli**, **cuore** o **occhi**, il pulsante
**▶ Replay** diventa disponibile (resta disattivato per le registrazioni del
cervello). Si apre una finestra con un lettore comune ai tre esami:
**▶ Riproduci / ⏸ Pausa**, **⏮ Inizio**, la linea del tempo trascinabile e
l'orologio "0:05 / 0:30". Nel Completo ci sono anche la velocità (da 0,25× a
4×) e *In loop*.

> L'animazione **simula** ciò che è stato registrato: non è il video della
> persona, e non è un referto né una diagnosi. Il sigillo in alto nella
> finestra lo ripete.

## Muscoli

Una figura articolata vista di lato (tronco, spalla, gomito, avambraccio,
polso, mano con le dita) rifà il **movimento segnato** sulla linea del tempo, e
ogni muscolo si accende con l'intensità misurata in quell'istante. Supinazione
e pronazione sono inconfondibili: il palmo chiaro rivolto verso l'alto o il
dorso rivolto verso il basso, con il testo "palmo in su/in giù".

La linea del tempo (da 2 a 4 tracce) nasce dai **marcatori e dalle fasi**
della registrazione ("Flessione", "Estensione", "Riposo"…); senza marcatori,
le **contrazioni rilevate** diventano tratti "da definire". Le tracce nello
stesso istante si **sommano** (per esempio, chiudere la mano mentre il gomito
si flette). Movimenti disponibili: flessione ed estensione del gomito,
supinazione, pronazione, flessione ed estensione del polso, aprire e chiudere
la mano, pinza, flessione ed estensione della spalla, riposo.

Nel **Semplice** vedi il lettore, la figura e l'elenco dei tratti. Nel
**Completo** la linea del tempo è modificabile: trascina un blocco per
spostarlo, tira il bordo per allungarlo, clicca con il tasto destro per *Cambia
movimento*, *Dividi qui*, *Elimina*, *Aggiungi/Rimuovi traccia*; Ctrl+Z
annulla. *Compito predefinito* inserisce, a partire dal cursore, una sequenza
con l'oggetto afferrato dalla mano: **sollevare il manubrio**,
**aprire/chiudere la porta con la chiave**, **prendere il bicchiere dal tavolo
e portarlo alla bocca**. Quando i muscoli attivi non corrispondono al movimento
scelto (per esempio, tricipite attivo in un tratto di flessione), compare un
avviso. *Salva* scrive `movimentos.json` accanto alla registrazione; alla
chiusura il programma chiede se ci sono marcature non salvate.

## Cuore

Un cuore disegnato **batte al ritmo registrato**, accanto al tracciato con il
cursore e ai battiti al minuto. La striscia in basso mostra **tutti** i
battiti: quello regolare è un trattino sottile; il **battito anticipato** è un
triangolo arancione; la **pausa più lunga** è un rettangolo vuoto rosso (colore
e forma, per chi non distingue i colori). L'elenco a parole ("0:13 battito
anticipato", "0:25 pausa più lunga (1,7 s)") è cliccabile e porta il lettore
fin lì. I battiti sono gli stessi del report PDF. Nel Completo, il tasto destro
sulla striscia permette di **correggere** (rimuovi battito, aggiungi battito
qui, segna come regolare / anticipato / pausa più lunga); *Salva* scrive
`batidas.json`.

## Occhi

Due occhi disegnati **sbattono le palpebre agli ammiccamenti e guardano** dove
indicano i segnali. *Inverti orizzontale* e *Inverti verticale* scambiano i
lati, nel caso gli elettrodi siano stati posizionati al contrario. La linea del
tempo dice a parole che cosa è successo ("0:03 ha sbattuto le palpebre", "0:05
ha guardato a destra") e i contatori sommano ammiccamenti e movimenti di lato e
in alto/in basso. Nel Completo, il tasto destro sull'elenco rimuove un evento o
cambia la direzione; *Salva* scrive `olhos.json`.
