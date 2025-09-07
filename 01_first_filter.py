import os
import csv
import re
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# Schlüsselwörter für Modulhandbücher und Ausschlüsse
KEYWORDS_HANDBOOK = [
    'modulhandbuch', 'modul handbook', 'module handbook',
    'modulübersicht', 'modulkatalog', 'module catalog'
]
KEYWORDS_EXCLUDE = ['studienordnung', 'prüfungsordnung']

studienordnungen = []

def get_keyword_context(text, keyword):
    """Findet die Position des Keywords im Text und gibt einen Ausschnitt zurück"""
    match = re.search(keyword, text, re.IGNORECASE)
    if not match:
        return None
    start = max(0, match.start() - 50)
    end = min(len(text), match.end() + 50)
    return text[start:end].replace('\n', ' ').strip()

def is_module_handbook(text, filename):
    """Prüft, ob es sich um ein Modulhandbuch handelt (ohne Studienordnung)"""
    text_lower = text.lower()
    filename_lower = filename.lower()
    
    # Ausschlusskriterien (Studienordnung etc.)
    if any(exclude in text_lower or exclude in filename_lower for exclude in KEYWORDS_EXCLUDE):
        studienordnungen.append({'filename': filename_lower})
        return False
    
    # Positive Kriterien
    handbook_match = any(
        (keyword in text_lower or keyword in filename_lower)
        for keyword in KEYWORDS_HANDBOOK
    )
    
    # Strukturelle Merkmale (z.B. "Modul WI 123")
    patterns = [
        r'modul\s*[a-z]{2,3}\s*\d+',
        r'leistungspunkte\s*\d+',
        r'studienverlaufsplan',
        r'semesterwochenstunden\s*\d+'
    ]
    pattern_match = any(re.search(p, text_lower, re.IGNORECASE) for p in patterns)
    
    return handbook_match or pattern_match

def analyze_pdf(filepath):
    """Analysiert eine PDF-Datei und gibt Metadaten zurück"""
    filename = os.path.basename(filepath)
    result = {
        'filepath': filepath,
        'filename': filename,
        'is_handbook': False,
        'page_count': 0,
        'keyword_context': None,
        'error': None
    }
    
    try:
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            page_count = len(reader.pages)
            result['page_count'] = page_count
            
            if page_count <= 20:  # Überspringe kleine PDFs
                return result
                
            text = " ".join(page.extract_text() or "" for page in reader.pages[:50])  # Nur erste 50 Seiten scannen
            if not text.strip():
                return result
            
            if is_module_handbook(text, filename):
                result['is_handbook'] = True
                # Finde das erste vorkommende Keyword für den Kontext
                for keyword in KEYWORDS_HANDBOOK + ['modul\s*[a-z]{2,3}\s*\d+']:
                    context = get_keyword_context(text, keyword)
                    if context:
                        result['keyword_context'] = f"...{context}..."
                        break
    except Exception as e:
        result['error'] = str(e)
    
    return result

def scan_pdfs(root_dir):
    """Durchsucht Verzeichnis nach PDFs und gibt Ergebnisse zurück"""
    handbooks = []
    non_handbooks = []
    errors = []
    
    pdf_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(root_dir)
        for file in files
        if file.lower().endswith('.pdf')
    ]
    
    total_files = len(pdf_files)
    print(f"Starte Analyse von {total_files} PDFs...")
    
    for i, filepath in enumerate(pdf_files, 1):
        result = analyze_pdf(filepath)
        
        if result['error']:
            errors.append(result)
        elif result['is_handbook']:
            handbooks.append(result)
        elif result['page_count'] > 20:  # Nur relevante Nicht-Handbücher speichern
            non_handbooks.append(result)
        
        # Fortschrittsanzeige
        if i % 100 == 0 or i == total_files:
            print(f"Fortschritt: {i}/{total_files} – Modulhandbücher: {len(handbooks)}")
    
    return handbooks, non_handbooks, errors

def write_csv(filename, data, columns):
    """Schreibt Daten in eine CSV-Datei"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

def main():
    root_dir = input("Pfad zum Verzeichnis mit PDFs: ").strip()
    if not os.path.isdir(root_dir):
        print("Ungültiger Pfad!")
        return
    
    handbooks, non_handbooks, errors = scan_pdfs(root_dir)
    
    # CSV-Dateien erstellen
    write_csv("studienordnungen.csv", studienordnungen, ['filename'])
    write_csv('module_handbooks.csv', handbooks,['filepath', 'filename', 'page_count', 'keyword_context', 'is_handbook', 'error']) 
    write_csv('non_handbooks_large.csv', non_handbooks, ['filepath', 'filename', 'page_count', 'keyword_context', 'is_handbook', 'error'])
    write_csv('pdf_errors.csv', errors,  ['filepath', 'filename', 'page_count', 'keyword_context', 'is_handbook', 'error'])
    
    print(f"\nErgebnis:\n- Modulhandbücher: {len(handbooks)}\n- Andere PDFs (>20 Seiten): {len(non_handbooks)}\n- Fehlerhafte Dateien: {len(errors)}")

if __name__ == "__main__":
    print("Installiere benötigte Bibliotheken...")
    os.system("pip install PyPDF2 pycryptodome > /dev/null 2>&1")
    main()
