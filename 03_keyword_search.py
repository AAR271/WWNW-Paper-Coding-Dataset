import pandas as pd
import fitz  # PyMuPDF
import os
import argparse

# Definition der Keywords und Kategorien
SUSTAINABILITY_KEYWORDS = ["sustainability", "nachhaltigkeit"]
ENTREPRENEURSHIP_KEYWORDS = ["entrepreneurship", "unternehmertum", "handlungsorientiert"]

ALL_KEYWORDS = SUSTAINABILITY_KEYWORDS + ENTREPRENEURSHIP_KEYWORDS

SCORE_THRESHOLD = 0.6  # Nur Dokumente mit Score >= 0.6

def extract_text(path):
    try:
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text.lower()
    except Exception:
        return ""  # im Fehlerfall leerer Text

def classify_keywords(text_lower):
    hits = {}
    for kw in ALL_KEYWORDS:
        hits[kw] = (kw in text_lower)
    # Kategorien
    sustainability_hit = any(hits[k] for k in SUSTAINABILITY_KEYWORDS)
    entrepreneurship_hit = any(hits[k] for k in ENTREPRENEURSHIP_KEYWORDS)
    return hits, sustainability_hit, entrepreneurship_hit

def main(input_csv, output_detail_csv, output_summary_csv):
    df_in = pd.read_csv(input_csv)

    # Filter: Nur Score >= 0.6
    if "score" not in df_in.columns:
        raise ValueError("Die Eingabedatei muss eine 'score'-Spalte enthalten.")
    df_in = df_in[df_in["score"] >= SCORE_THRESHOLD].reset_index(drop=True)

    records = []
    for _, row in df_in.iterrows():
        path = row.get("filepath", "")
        if not isinstance(path, str) or not os.path.isfile(path):
            record = {
                "filepath": path,
                "exists": False,
                **{kw: False for kw in ALL_KEYWORDS},
                "sustainability_flag": False,
                "entrepreneurship_flag": False,
            }
        else:
            text_lower = extract_text(path)
            hits, sust_flag, entre_flag = classify_keywords(text_lower)
            record = {
                "filepath": path,
                "exists": True,
                **{kw: hits[kw] for kw in ALL_KEYWORDS},
                "sustainability_flag": sust_flag,
                "entrepreneurship_flag": entre_flag,
            }
        records.append(record)

    df_hits = pd.DataFrame.from_records(records)

    # Detail-CSV
    df_hits.to_csv(output_detail_csv, index=False)

    # Aggregierte Statistik
    total = len(df_hits)
    only_sustain = df_hits[(df_hits["sustainability_flag"]) & (~df_hits["entrepreneurship_flag"])].shape[0]
    only_entre = df_hits[(~df_hits["sustainability_flag"]) & (df_hits["entrepreneurship_flag"])].shape[0]
    both = df_hits[(df_hits["sustainability_flag"]) & (df_hits["entrepreneurship_flag"])].shape[0]
    neither = df_hits[(~df_hits["sustainability_flag"]) & (~df_hits["entrepreneurship_flag"])].shape[0]

    summary = {
        "total_documents": total,
        "only_sustainability": only_sustain,
        "only_entrepreneurship": only_entre,
        "both_categories": both,
        "neither": neither,
        **{f"count_{kw}": int(df_hits[kw].sum()) for kw in ALL_KEYWORDS},
        "pct_only_sustainability": only_sustain / total if total else 0,
        "pct_only_entrepreneurship": only_entre / total if total else 0,
        "pct_both": both / total if total else 0,
        "pct_neither": neither / total if total else 0,
    }

    # Summary-CSV
    pd.DataFrame([summary]).to_csv(output_summary_csv, index=False)

    # Konsole
    print("=== Co-Occurrence Zusammenfassung (nur Score >= 0.6) ===")
    print(f"Gesamtanzahl Dokumente: {total}")
    print(f"Nur Nachhaltigkeitsbezug: {only_sustain} ({summary['pct_only_sustainability']:.1%})")
    print(f"Nur Entrepreneurship: {only_entre} ({summary['pct_only_entrepreneurship']:.1%})")
    print(f"Beide Kategorien: {both} ({summary['pct_both']:.1%})")
    print(f"Keine der beiden: {neither} ({summary['pct_neither']:.1%})")
    print("\nEinzelkeyword-Häufigkeiten:")
    for kw in ALL_KEYWORDS:
        print(f" - {kw}: {summary[f'count_{kw}']}")
    print(f"\nDetail-CSV: {output_detail_csv}")
    print(f"Zusammenfassung-CSV: {output_summary_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyword-Analyse auf Modulbeschreibungsergebnis (nur Score >= 0.6).")
    parser.add_argument("input_csv", help="Die ergebnis.csv mit score-Spalte.")
    parser.add_argument("-d", "--detail", default="keyword_detail.csv", help="Ausgabe Detail-CSV.")
    parser.add_argument("-s", "--summary", default="keyword_summary.csv", help="Ausgabe Zusammenfassung.")
    args = parser.parse_args()
    main(args.input_csv, args.detail, args.summary)

