# Das Programm öffnen (Ladebildschirm)

> Benutzerhandbuch → Kapitel „Installation und erster Start“ → nach „Das Programm öffnen“.

Beim Öffnen von ROA erscheint ein kleines Fenster mit dem Logo und einer
Signallinie, die sich gerade zeichnet. Darunter sagt das Programm in Worten,
was es gerade tut („Bibliotheken werden geladen…“, „Startbildschirm wird
aufgebaut…“). Dieses Fenster verschwindet von selbst, sobald der
Startbildschirm fertig ist; nichts muss angeklickt werden.

**Erstes Öffnen nach dem Installieren oder Aktualisieren.** Das Programm wird
einmal vorbereitet (das Fenster zeigt „Das Programm wird zum ersten Mal
vorbereitet…“) und legt das Ergebnis im Ordner `.roa_cache` neben dem Programm
ab. Bei den folgenden Malen geht das Öffnen deutlich schneller. Wenn der
Programmordner kein Schreiben erlaubt (zum Beispiel in `Arquivos de
Programas`), wandert der Cache in den Benutzerordner
(`%LOCALAPPDATA%\ROA\cache`). Diesen Ordner zu löschen ist unproblematisch:
Er wird beim nächsten Öffnen neu angelegt.

**Wenn der Ladebildschirm stört** (zum Beispiel in einer Automatisierung oder
auf einem Computer mit Grafikproblemen), öffnen Sie das Programm mit der
Option `--sem-splash` oder setzen Sie die Umgebungsvariable
`ROA_SEM_SPLASH=1`.

**Updates.** Unter *Hilfe → Nach Updates suchen* lädt das Programm weiterhin
nur seinen eigenen Code herunter und sendet nie Ihre Daten. Ab dieser Version
kann es auch den Starter (`EEG_Data_Collector.py`) aktualisieren, wenn das
Update eine neue Version davon mitbringt; gelingt das nicht, meldet es sich,
und das Programm läuft mit dem bisherigen Starter weiter.
