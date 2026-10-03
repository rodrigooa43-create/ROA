# Replay: die Aufzeichnung als Animation sehen

> Benutzerhandbuch → Kapitel „Eine Aufnahme ansehen“ → neuer Abschnitt „Replay“ (nach „PDF-Bericht“).

Beim Öffnen einer Aufzeichnung von **Muskeln**, **Herz** oder **Augen** wird
die Schaltfläche **▶ Replay** verfügbar (bei Aufzeichnungen des Gehirns
bleibt sie ausgeschaltet). Sie öffnet ein Fenster mit einem Abspieler, der
für alle drei Untersuchungen gleich ist: **▶ Abspielen / ⏸ Pause**,
**⏮ Anfang**, die ziehbare Zeitleiste und die Uhr „0:05 / 0:30“. In
Vollständig gibt es außerdem die Geschwindigkeit (0,25× bis 4×) und
*Wiederholen*.

> Die Animation **simuliert**, was aufgezeichnet wurde: Sie ist kein Video
> des Patienten und weder Befund noch Diagnose. Das Siegel oben im Fenster
> wiederholt das.

## Muskeln

Eine Gliederfigur in Seitenansicht (Rumpf, Schulter, Ellenbogen, Unterarm,
Handgelenk, Hand mit Fingern) führt die in der Zeitleiste **markierte
Bewegung** nach, und jeder Muskel leuchtet mit der in diesem Moment gemessenen
Intensität auf. Supination und Pronation sind unverwechselbar: die helle
Handfläche nach oben oder der Handrücken nach unten, mit dem Text
„Handfläche nach oben/unten“.

Die Zeitleiste (2 bis 4 Spuren) entsteht aus den **Markern und Phasen** der
Aufzeichnung („Flexion“, „Extension“, „Ruhe“…); ohne Marker werden die
**erkannten Kontraktionen** zu Abschnitten „Noch festzulegen“. Spuren im
selben Moment **addieren sich** (zum Beispiel die Hand schließen, während der
Ellenbogen beugt). Verfügbare Bewegungen: Ellenbogenflexion und -extension,
Supination, Pronation, Handgelenkflexion und -extension, Hand öffnen und
schließen, Pinzettengriff, Schulterflexion und -extension, Ruhe.

In **Einfach** sehen Sie den Abspieler, die Figur und die Liste der
Abschnitte. In **Vollständig** ist die Zeitleiste bearbeitbar: Ziehen Sie
einen Block, um ihn zu verschieben, ziehen Sie am Rand, um ihn zu dehnen,
klicken Sie mit der rechten Maustaste für *Bewegung wechseln*, *Hier teilen*,
*Löschen*, *Spur hinzufügen/entfernen*; Strg+Z macht rückgängig.
*Vorgefertigte Aufgabe* fügt ab dem Cursor eine Sequenz mit einem Gegenstand
in der Hand ein: **die Hantel heben**, **die Tür mit dem Schlüssel
öffnen/schließen**, **den Becher vom Tisch nehmen und zum Mund führen**. Wenn
die aktiven Muskeln nicht zur gewählten Bewegung passen (zum Beispiel ein
aktiver Trizeps in einem Flexionsabschnitt), erscheint ein Hinweis.
*Speichern* schreibt `movimentos.json` neben die Aufzeichnung; beim Schließen
fragt das Programm, ob es ungespeicherte Markierungen gibt.

## Herz

Ein gezeichnetes Herz **schlägt im aufgezeichneten Rhythmus**, neben der
Kurve mit dem Cursor und den Schlägen pro Minute. Der Streifen darunter zeigt
**alle** Schläge: Der regelmäßige ist ein dünner Strich; der **verfrühte
Schlag** ist ein orangefarbenes Dreieck; die **längere Pause** ist ein rotes,
nicht ausgefülltes Rechteck (Farbe und Form, für Menschen, die Farben nicht
unterscheiden). Die Liste in Worten („0:13 verfrühter Schlag“, „0:25 längere
Pause (1,7 s)“) ist anklickbar und bringt den Abspieler dorthin. Die Schläge
sind dieselben wie im PDF-Bericht. In Vollständig erlaubt die rechte
Maustaste auf dem Streifen das **Korrigieren** (Schlag entfernen, Schlag hier
hinzufügen, als regelmäßig / verfrüht / längere Pause markieren); *Speichern*
schreibt `batidas.json`.

## Augen

Zwei gezeichnete Augen **blinzeln bei den Lidschlägen und blicken** dorthin,
wohin die Signale es vorgeben. *Horizontal spiegeln* und *Vertikal spiegeln*
tauschen die Seiten, falls die Elektroden vertauscht angebracht wurden. Die
Zeitleiste sagt in Worten, was passiert ist („0:03 blinzelt“, „0:05 blickt
nach rechts“), und die Zähler summieren Lidschläge und Bewegungen zur Seite
und nach oben/unten. In Vollständig entfernt die rechte Maustaste in der
Liste ein Ereignis oder wechselt die Richtung; *Speichern* schreibt
`olhos.json`.
