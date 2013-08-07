Conways Spiel des Lebens
========================

[Conways Spiel des Lebens](http://de.wikipedia.org/wiki/Conways_Spiel_des_Lebens)
mit [Python 3](http://www.python.org/) und [Tk](http://www.tkdocs.com/).

Regeln
------

Das Spiel des Lebens wird in Generationen auf einem Gitter gespielt. Auf einem
Gitterplatz kann sich eine Zelle befinden oder auch nicht. Die
Anfangspopulation besteht aus einigen Zellen, die bereits zu beginn des Spieles
existieren. In jeder neuen Generation (Runde) überleben Zellen, sterben Zellen
und werden neue Zellen geboren in Abhängigkeit von den Zellen der vorherigen
Generation. Um zu entscheiden, ob ein Gitterplatz in der nächsten Generation
von einer Zelle belegt ist oder nicht, ist der aktuelle Zustand dieses
Gitterplatzes und die acht umligenden Zellen (die Nachbarschaft) dieses Platzes
wichtig.

* Befindet sich auf dem Gitterplatz keine Zelle, so wird dort eine neue Zelle
  geboren, wenn sich in der Nachbarschaft genau drei Zellen befinden.
* Befindet sich auf dem Gitterplatz eine Zelle, so überlebt diese, wenn sich
  in ihrer Nachbarschaft zwei oder drei Zellen befinden. Sonst stirbt die
  Zelle an Vereinsamung oder Überbevölkerung ab.

Summer Camp 2013
----------------

Diese Software entstand im Rahmen des Informatik Summer Camps 2013 an der
Universität zu Lübeck. Die Klasse `GameOfLife` war vorgegeben, die Funktion
`step` ist daraus ausgelagert und modelliert den Schritt von einer Generation
zur nächsten. Der Code dieser Funktion zwischen den Kommentarzeilen
`Beginn/Ende der Lösung` wurde von den Teilnehmer selbst erarbeitet.

Bedienung
---------

Python ist auf vielen Systemen bereits installiert, sodass die Software über

    python3 gameoflife.py

gestartet werden kann. Bei der Verwendung in interaktiven Systemen wie IDLE muss
die folgende Zeile am Ende der Datei `gameoflife.py` auskommentiert werden:

    app.run()

In diesem Fall übernehmen diese Systeme die Ausführung der Mainloop.

Die Bedienung kann über das Menü oder die im Menü angegebenen Tastaturbefehle
erfolgen.

Solange das automatische Weiterschalten der Generationen deaktiviert ist,
können einzelnen Zellen durch Klicken mit der Maus hinzugefügt bzw. entfernt
werden.

### Zurücksetzen (R)

Setzt wieder die Anfangspopulation auf das Gitter. Das ist die Population,
die zuletzt geladen oder gespeichert wurde.

### Öffnen (O)

Lädt eine Population aus einer Datei im Plaintext-Dateiformat und setzt diese
als aktuelle Population.

### Speichern (S)

Speichert die aktuelle Population in einer Datei im Plaintext-Dateiformat.

### Einstellungen (E)

Öffnet einen Konfigurationsdialog, in dem die Größe des Gitters, die Größe
einer Zelle in der Darstellung und die Verzögerung für das automatische
Weiterschalten der Generationen eingestellt werden kann.

### Beenden (Q)

Beendet das Programm.

### nächste Generation (N oder Leertaste)

Wechselt in die nächste Generation.

### Play (P)

Aktiviert oder deaktiviert das automatische Weiterschalten der Generationen.

Plaintext-Dateiformat
---------------------

Das Plaintext-Dateiformat orientiert sich an dem im LifeWiki unter
[Plaintext](http://www.conwaylife.com/wiki/Plaintext)
beschriebenen Format, dass auch im LifeWiki selbst verwendet wird.
Zeilen, die mit einem Ausrufezeichen (`!`) beginnen sind Kommentarzeilen
und werden ignoriert. Jede andere Zeile der Datei entspricht einer Zeile
des Gitters. Ein Gitterplatzt ohne Zelle wird durch einen Punkt (`.`)
und ein Gitterplatzt mit Zelle durch den Großbuchstaben O (`O`) dargestellt.
Plätze ohne Zelle am Ende des Zeile müssen nicht angegeben werden. Die
Dimension des Gitters ergibt sich aus der Anzahl Zeilen und der längsten
Zeile in der Datei.

Ein Rand bestehend aus zwei Zellen zu jeder Seite wird nicht gespeichert
und nicht geladen. Dieser Rand sollte in Anfangspopulationen immer frei
von Zellen bleiben, damit Approximation an ein unendlich großes Gitter
durch den Rand nicht zu sehr verfälscht wird.

License
-------

This software is released under the
[MIT License](http://www.opensource.org/licenses/MIT). Some of
the configurations in the data folder are taken from
the [LifeWiki](http://www.conwaylife.com/wiki/). These are
licensed as described on the wiki pages linked in the header
section of these files.
