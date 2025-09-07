import os
import fitz  # PyMuPDF
import pandas as pd
import argparse
from tqdm import tqdm

# Keywordgruppen für Modulbeschreibung
GROUPS = {
    "modul_title": ["modul", "modulname", "module", "module title", "course", "course title"],
    "learning_outcomes": ["lernziele", "learning outcomes", "kompetenzen", "learning objectives"],
    "content": ["inhalte", "content", "themen", "topics", "syllabus"],
    "credits_workload": ["ects", "workload", "sws", "credits", "umfang"],
    "assessment": ["prüfungsform", "pruefungsform", "assessment", "prüfung", "exam", "evaluation"],
}

MIN_TEXT_LENGTH = 100  # wenn weniger Text extrahiert, misstrauisch

def extract_text_from_pdf(path):
    try:
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Fehler beim Öffnen/Lesen: {e}")

def score_text(text_lower):
    found_groups = []
    for group_name, keywords in GROUPS.items():
        for kw in keywords:
            if kw in text_lower:
                found_groups.append(group_name)
                break  # pro Gruppe nur einmal zählen
    score = len(set(found_groups)) / len(GROUPS)
    return score, sorted(list(set(found_groups)))

def should_skip(text, error):
    if error is not None:
        return True, "error"
    if not text or len(text.strip()) == 0:
        return True, "kein extrahierbarer text"
    if len(text.strip()) < MIN_TEXT_LENGTH:
        return False, "kurzer text (geringe verlässlichkeit)"
    return False, None

def scan_directory(base_dir, output_csv):
    records = []
    total = 0
    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not fname.lower().endswith(".pdf"):
                continue
            total += 1
            path = os.path.join(root, fname)
            status = "scanned"
            reason = ""
            score = 0.0
            matched_groups = []
            error = None
            try:
                text = extract_text_from_pdf(path)
                lower = text.lower() if text else ""
                skip, skip_reason = should_skip(text, None)
                if skip and skip_reason == "error":
                    status = "skipped"
                    reason = skip_reason
                elif skip and skip_reason == "kein extrahierbarer text":
                    status = "skipped"
                    reason = skip_reason
                else:
                    score, matched_groups = score_text(lower)
                    if skip_reason == "kurzer text (geringe verlässlichkeit)":
                        reason = skip_reason
                # keine Exception: normal weiter
            except Exception as e:
                status = "skipped"
                reason = f"error: {e}"
                text = ""
                score = 0.0
                matched_groups = []
                error = e

            records.append({
                "filepath": path,
                "status": status,
                "reason": reason,
                "score": round(score, 3),
                "matched_groups": ";".join(matched_groups),
                "matched_group_count": len(matched_groups),
            })

    df = pd.DataFrame.from_records(records)

    # Haupt-CSV
    df.to_csv(output_csv, index=False)

    # Gefilterte: <=2 Gruppen (also wahrscheinlich keine vollständige Modulbeschreibung)
    filtered_csv = (
        output_csv.replace(".csv", "_filtered.csv")
        if output_csv.lower().endswith(".csv")
        else output_csv + "_filtered.csv"
    )
    df_filtered = df[df["matched_group_count"] <= 2]
    df_filtered.to_csv(filtered_csv, index=False)

    summary = {
        "total_pdfs": total,
        "skipped": int((df["status"] == "skipped").sum()),
        "scanned": int((df["status"] == "scanned").sum()),
        "avg_score_all": df["score"].mean() if not df.empty else 0,
        "avg_score_scanned": df.loc[df["status"] == "scanned", "score"].mean() if not df[df["status"] == "scanned"].empty else 0,
        "likely_module_count": int((df["score"] >= 0.6).sum()),
        "filtered_count": len(df_filtered),
        "filtered_path": filtered_csv,
    }

    # Ausgabe Zusammenfassung
    print("=== Zusammenfassung ===")
    print(f"Insgesamt gefundene PDF-Dateien: {summary['total_pdfs']}")
    print(f"Übersprungen (skipped): {summary['skipped']}")
    print(f"Erfolgreich gescannte: {summary['scanned']}")
    print(f"Durchschnittlicher Score (alle): {summary['avg_score_all']:.3f}")
    print(f"Durchschnittlicher Score (nur gescannte): {summary['avg_score_scanned']:.3f}")
    print(f"Anzahl mit Score >= 0.6 (vermutlich Modulbeschreibungen): {summary['likely_module_count']}")
    print(f"Anzahl Dateien mit <=2 Gruppen (in gefilterter Datei): {summary['filtered_count']}")
    print(f"Haupt-CSV: {output_csv}")
    print(f"Gefilterte CSV: {filtered_csv}")

    return df, df_filtered, summary

def main():
    parser = argparse.ArgumentParser(description="PDFs scannen auf Modulbeschreibungen.")
    parser.add_argument("basedir", help="Hauptverzeichnis, darin wird rekursiv nach PDFs gesucht.")
    parser.add_argument("-o", "--output", default="modulbeschreibung_scan.csv", help="Pfad zur Ausgabe-CSV.")
    args = parser.parse_args()

    scan_directory(args.basedir, args.output)

if __name__ == "__main__":
    main()

