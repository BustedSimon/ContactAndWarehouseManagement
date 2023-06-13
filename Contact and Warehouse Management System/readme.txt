Sehr geehrter Herr Teuschler,
Hier ist meine Abgabe zu dem Thema Projektplanung, etwa verspĂ¤tet, da ich durch eine Corona-Infektion letzte Woche ein paar Tage lang flach lag. Mein Programm „Contact and Warehouse Management System“ ermöglicht Benutzern Kontaktdaten von Kunden, ein Inventar und Daten der Benutzeraccounts zu verwalten. Im echten Leben könnte somit in fast jedem Betrieb das Programm von nutzen sein. 
Bei der Entwicklung sind mir immer wieder neue Ideen gekommen, die ich dann versucht habe zu implementieren. Dadurch wurde dieses Projekt ziemlich ausführlich und aufwendig. Insgesamt kam ich so auf einen Arbeitsaufwand von circa 25 Stunden. 
Ich hoffe Ihnen gefällt es.

Mit freundlichen Grüßen,
Simon Clüsserath

Login:
- Benutzername: admin
- Passwort: admin
- wenn ein neuer Account erstellt wird, wird bei dem ersten Login-Versuch ein neues Passwort festgelegt, womit man sich dann einloggen kann

Besonderheiten:
- Passwörter werden verschlüsselt gespeichert und abgefragt
- Daten werden im Dashboard visualisiert
- Anzahl der Kunden wird immer zum Vortag verglichen (-> numbers.txt), Differenz wird im Dashboard angezeigt
- Daten werden übersichtlich in einer Tabelle angezeigt (ttk.Treeview)
- Daten können hinzugefügt, gelöscht und überschrieben werden
- es kann nach Schlüsselwörtern in den Daten gesucht werden
- moderne Farbpalette und moderner Style
- alle Ereignisse werden in „logs.txt“ dokumentiert (logging)

Probleme:
- Header-Modul funktioniert nur teilweise: Uhr geht nicht auf jedem Tab -> Problem mit Tickrate und Update (nicht behoben)
- Zugriff auf Datenbank: Problem durch mehrere Zugriffe gleichzeitig durch dataTable-Modul und main.py (behoben: Verbindung nach jedem Zugriff schließen, dann wieder neu aufbauen)
- Kuchendiagramm stellt keine Daten dar, weil Proportionen nie gestimmt haben (nicht behoben)

Quellen:
- Kuchendiagramm: https://developer.mozilla.org/de/docs/Web/API/Canvas_API/Tutorial/Drawing_shapes
- Tabs: https://djangocentral.com/creating-tabbed-widget-with-python-for-gui-application/
- Encoding/Decoding der Passwörter: https://www.base64encoder.io/python/,  https://swharden.com/blog/2021-05-15-python-credentials/