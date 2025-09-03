# WWNW-Paper-Coding-Dataset

## GERMAN
**english below**

### Daten sammeln
Die Daten wurden mit Hilfe von [Hochschulkompass](https://www.hochschulkompass.de/home.html) gesammelt. Durchgeführt von einer studentischen Hilfskraft. 
Eine Stichprobe der Dokumente hat ergeben, dass nicht alle Dokumente Modulhandbücher waren. Daher wurde mit Hilfe von NLP-Techniken eine weitere Eingrenzung vorgenommen:
1. 01_first_sort.py
   
    Zunächst wurden die PDF-Dokumente nach bestimmten Schlüsselwörtern (modulhandbuch, modul handbook, module handbook, modulübersicht, modulkatalog, module catalog) gescannt. Dabei wurden explizit Studien- und Prüfungsordnungen ausgeschlossen. Geprüft wurde hier der Dateiname, als auch der Inhalt der PDF-Dateien. Außerdem wurden Dokumente aufgrund ihrer Seitenzahl aussortiert. Dateien mit weniger als 20 Seiten wurden ausgeschlossen. Die Ergebnisse wurden dann in 4 CSV-Dateien geschrieben:
   * (1) studienordnung.csv,
   * (2) module_handbooks.csv,
   * (3)non_handbooks_large.csv und
   * (4) pdf_errors.csv.
     
   (1) enthält die Dokumente, die als Studien- oder Prüfungsordnungen identifiziert wurden. Diese wurden händisch geprüft. (2) enthält die Liste von Modulhandbüchern. (3) enthält die Ergebnisse aller Dateien und (4) nur die Dateien, bei denen es zu einem Fehler gekommen ist. Diese wurden ebenfalls händisch geprüft.
   
    Ausführung der Datei: `python 01_first_sort.py`
   
3. 02_second_sort.py
   
    Nach der ersten Filterung wurde ein zweiter Filter angewandt, um die Modulhandbücher weiter zu untersuchen. Dabei wurden die PDF-Dateien auf wiederkehrende Abschnitte untersucht, wie z. B. Modulname/Titel, Inhalte Lerninhalte, Lernziele/Kompetenzen, Workload/SWS (Semesterwochenstunden), Prüfungsform und ECTS-Credits. Die Dateien sind nach Studiengang sortiert, sodass hier alle Unterordner mitdurchsucht werden. Für jedes Dokument wird der Inhalt (Text) extrahiert und heuristisch bewertet, Gründe für möglicherweise übersprungene Dateien dokumentiert und als CSV-Dateien ausgegeben. Details zur Heuristik: Die Wahrscheinlichkeit basiert auf dem Vorkommen folgender Keyword-Gruppen:
   * (1) Modul-Titel (Modul, Modulname, ...),
   * (2) Lernziele / Kompetenzen,
   * (3) Inhalte / Inhalte des Moduls,
   * (4) ECTS/Workload/Umfang und
   * (5) Prüfungsform/Bewertung.
   
     Der Score berechnet sich wie folgt: `score = Anzahl gefundener Gruppen / 5`. Das Ergebnis ist ein Wert zwischen 0.0 und 1.0. Konnte kein Text extrahiert werden oder die Anzahl der Zeichen zu gering ist ( < 100 Zeichen), wurde die Datei als "Kein Modulhandbuch" bewertet und als übersprungen markiert. Ausgegeben werden zwei CSV-Dateien, `ergebnis.csv` und `ergebnis_filtered.csv`, die nur die Ergebnisse mit <= 2 Gruppen beinhaltet. Diese wurden händisch geprüft.
      
    Ausführung der Datei: `python 02_second_sort.py /pfad/zum/hauptverzeichnis -o ergebnis.csv`

### Analyse

1. 03_keyword_search.py

2. 04_create_heatmap.py



## ENGLISH

### Data Collection

### Analysis
