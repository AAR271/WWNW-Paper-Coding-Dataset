# WWNW-Paper-Coding-Dataset

## GERMAN
**english below**

### Vorbereitungen
Um die Skripte auszuführen, wird Python benötigt. Auf Linux oder Mac kann dazu nach Installation von Python (`sudo apt install python3`) eine virtuelle Umgebung eingerichtet werden. Dazu im Terminal `python3 -m venv .venv`ausführen und im Anschluss `source .venv/bin/activate`. Nun sollte die virtuelle Umgebung geladen sein. Wichtig ist nun, dass wir alle benötigten Pakete installieren. Dazu einfach `pip install -r requirements.txt` ins Terminal eingeben. Damit sollten alle Pakete installiert werden und die Skripte können ausgeführt werden.

### Daten sammeln
Die Daten wurden mit Hilfe von [Hochschulkompass](https://www.hochschulkompass.de/home.html) gesammelt. Durchgeführt von einer studentischen Hilfskraft.
Eine Stichprobe der Dokumente hat ergeben, dass nicht alle Dokumente Modulhandbücher waren. Daher wurde mit Hilfe von NLP-Techniken eine weitere Eingrenzung vorgenommen:
1. 01_first_filter.py
   
    Zunächst wurden die PDF-Dokumente nach bestimmten Schlüsselwörtern (modulhandbuch, modul handbook, module handbook, modulübersicht, modulkatalog, module catalog) gescannt. Dabei wurden explizit Studien- und Prüfungsordnungen ausgeschlossen. Geprüft wurde hier der Dateiname, als auch der Inhalt der PDF-Dateien. Außerdem wurden Dokumente aufgrund ihrer Seitenzahl aussortiert. Dateien mit weniger als 20 Seiten wurden ausgeschlossen. Die Ergebnisse wurden dann in 4 CSV-Dateien geschrieben:
   * (1) studienordnung.csv,
   * (2) module_handbooks.csv,
   * (3)non_handbooks_large.csv und
   * (4) pdf_errors.csv.
     
   (1) enthält die Dokumente, die als Studien- oder Prüfungsordnungen identifiziert wurden. Diese wurden händisch geprüft. (2) enthält die Liste von Modulhandbüchern. (3) enthält die Ergebnisse aller Dateien und (4) nur die Dateien, bei denen es zu einem Fehler gekommen ist. Diese wurden ebenfalls händisch geprüft.
   
    Ausführung der Datei: `python 01_first_filter.py`
   
3. 02_second_filter.py
   
    Nach der ersten Filterung wurde ein zweiter Filter angewandt, um die Modulhandbücher weiter zu untersuchen. Dabei wurden die PDF-Dateien auf wiederkehrende Abschnitte untersucht, wie z. B. Modulname/Titel, Inhalte Lerninhalte, Lernziele/Kompetenzen, Workload/SWS (Semesterwochenstunden), Prüfungsform und ECTS-Credits. Die Dateien sind nach Studiengang sortiert, sodass hier alle Unterordner mitdurchsucht werden. Für jedes Dokument wird der Inhalt (Text) extrahiert und heuristisch bewertet, Gründe für möglicherweise übersprungene Dateien dokumentiert und als CSV-Dateien ausgegeben. Details zur Heuristik: Die Wahrscheinlichkeit basiert auf dem Vorkommen folgender Keyword-Gruppen:
   * (1) Modul-Titel (Modul, Modulname, ...),
   * (2) Lernziele / Kompetenzen,
   * (3) Inhalte / Inhalte des Moduls,
   * (4) ECTS/Workload/Umfang und
   * (5) Prüfungsform/Bewertung.
   
     Der Score berechnet sich wie folgt: `score = Anzahl gefundener Gruppen / 5`. Das Ergebnis ist ein Wert zwischen 0.0 und 1.0. Konnte kein Text extrahiert werden oder die Anzahl der Zeichen zu gering ist ( < 100 Zeichen), wurde die Datei als "Kein Modulhandbuch" bewertet und als übersprungen markiert. Ausgegeben werden zwei CSV-Dateien, `ergebnis.csv` und `ergebnis_filtered.csv`, die nur die Ergebnisse mit <= 2 Gruppen beinhaltet. Diese wurden händisch geprüft.
      
    Ausführung der Datei: `python 02_second_filter.py /pfad/zum/hauptverzeichnis -o ergebnis.csv`

### Analyse
Die Analyse der PDF-Dokumente kann nun auf Basis der vorherigen Filterung erfolgen.

1. 03_keyword_analysis.py

    Als Basis für dieses Script dient die `ergebnis.csv`, die Ausgabe aus dem vorherigen Script `02_second_filter.py`. Hier wird nach den Schlüsselwörtern
    * sustainability
    * nachhaltigkeit
    mit Nachhaltigkeitsbezug und mit Entrepreneurship-Bezug
    * entrepreneurship
    * unternehmertum
    * handlungsorientiert
    gesucht, für jedes Dokument notiert, ob Schlüsselwörter gefunden wurden, eine Co-Occurence Analyse durchgeführt und eine detaillierte Ausgabe erstellt. Dabei werden nur Ergebnisse mit Score >= 0.6 aus der `ergebnis.csv` berücksichtigt. Ausgegeben werden zwei Dateien, `keyword_detail.csv` und `keyword_summary.csv`. Die erste Datei enthält boolsche Werte (wahr/falsch) für jedes Schlüsselwort pro Dokument. Das zweite Dokument enthält die Statistik.  

Ausführung der Datei: `python 03_keyword_analysis.py ergebnis.csv -d keyword_detail.csv -s keyword_summary.csv`
    

2. 04_create_heatmap.py

    Zuletzt wird noch eine Heatmap erstellt und als `heatmap.png` abgespeichert. Dieses Script erzeugt eine visuelle Darstellung der Schlüsselwortkombinationen.

Ausführen der Datei: `python 04_create_heatmap.py keyword_detail.csv -o heatmap.png`

## ENGLISH

### Preparations
Python is required to run the scripts. On Linux or Mac, a virtual environment can be set up after installing Python (`sudo apt install python3`). To do this, run `python3 -m venv .venv` in the terminal and then `source .venv/bin/activate`. The virtual environment should now be loaded. It is now important that we install all the necessary packages. To do this, simply enter `pip install -r requirements.txt` in the terminal. This should install all packages and allow the scripts to be executed.


### Data Collection
The data was collected using [Hochschulkompass](https://www.hochschulkompass.de/home.html), conducted by a student assistant.  
A sample of the documents showed that not all of them were actual module handbooks. Therefore, further filtering was applied using NLP techniques:

1. **01_first_filter.py**

   First, the PDF documents were scanned for specific keywords (modulhandbuch, modul handbook, module handbook, modulübersicht, modulkatalog, module catalog).  
   Study and examination regulations were explicitly excluded. Both the file name and the PDF file content were checked. Documents with fewer than 20 pages were also discarded.  
   The results were written into 4 CSV files:
   * (1) `studienordnung.csv`
   * (2) `module_handbooks.csv`
   * (3) `non_handbooks_large.csv`
   * (4) `pdf_errors.csv`
   
   (1) contains documents identified as study or examination regulations, which were checked manually.  
   (2) contains the list of module handbooks.  
   (3) contains the results of all processed files, and  
   (4) only contains files that caused errors, which were also checked manually.  

   Run the script:  
   ```bash
   python 01_first_filter.py
   ```

2. **02_second_filter.py**

   After the first filtering step, a second filter was applied to further analyze the module handbooks. The PDF files were checked for recurring sections such as Module Name/Title, Learning Content, Learning Objectives/Competences, Workload/Credit Hours, Examination Format, and ECTS credits.  
   The files are organized by study program, so all subfolders are scanned as well. For each document, the text content is extracted and heuristically evaluated. Reasons for skipped files are documented, and the results are written to CSV files.  

   **Heuristic details:**  
   The probability is based on the occurrence of the following keyword groups:
   * (1) Module Title (Modul, Modulname, …)
   * (2) Learning Objectives / Competences
   * (3) Learning Content
   * (4) ECTS/Workload/Extent
   * (5) Examination Format/Evaluation  

   The score is calculated as:  
   ```
   score = number of detected groups / 5
   ```  
   The result is a value between 0.0 and 1.0.  
   If no text could be extracted, or if the text length was too short (< 100 characters), the file was classified as “Not a module handbook” and skipped.  

   Two CSV files are created:  
   * `ergebnis.csv` – contains all results  
   * `ergebnis_filtered.csv` – only contains results with ≤ 2 detected groups (manually checked)  

   Run the script:  
   ```bash
   python 02_second_filter.py /path/to/main/folder -o ergebnis.csv
   ```

### Analysis

1. **03_keyword_analysis.py**

   Based on the output file `ergebnis.csv` from `02_second_filter.py`, this script searches for the keywords:
   * sustainability  
   * nachhaltigkeit  
   (for sustainability references), and  
   * entrepreneurship  
   * unternehmertum  
   * handlungsorientiert  
   (for entrepreneurship references).  

   For each document, it records whether keywords were found, performs a co-occurrence analysis, and produces a detailed output. Only results with a score ≥ 0.6 from `ergebnis.csv` are considered.  

   Two files are generated:  
   * `keyword_detail.csv` – contains boolean values (true/false) for each keyword per document  
   * `keyword_summary.csv` – contains overall statistics  

   Run the script:  
   ```bash
   python 03_keyword_analysis.py ergebnis.csv -d keyword_detail.csv -s keyword_summary.csv
   ```

2. **04_create_heatmap.py**

   Finally, a heatmap is created and saved as `heatmap.png`. This script generates a visual representation of keyword combinations.  

   Run the script:  
   ```bash
   python 04_create_heatmap.py keyword_detail.csv -o heatmap.png
   ```

