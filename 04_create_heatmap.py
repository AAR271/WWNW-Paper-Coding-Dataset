import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os

def main(detail_csv, output_png="keyword_heatmap.png"):
    df = pd.read_csv(detail_csv)

    # Nur existierende Dateien berücksichtigen
    df = df[df["exists"] == True]

    # Nur Keyword-Spalten auswählen (alle True/False-Spalten außer 'exists', 'filepath', Flags)
    keyword_cols = [col for col in df.columns if col not in ["filepath", "exists", "sustainability_flag", "entrepreneurship_flag"]]

    # Co-Occurrence Matrix berechnen
    co_matrix = pd.DataFrame(0, index=keyword_cols, columns=keyword_cols)
    for i in keyword_cols:
        for j in keyword_cols:
            co_matrix.loc[i, j] = ((df[i]) & (df[j])).sum()

    # Heatmap zeichnen
    plt.figure(figsize=(8, 6))
    sns.heatmap(co_matrix, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Keyword Co-Occurrence Heatmap")
    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    print(f"Heatmap gespeichert als: {output_png}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Erstellt eine Heatmap der Keyword-Co-Occurrences.")
    parser.add_argument("detail_csv", help="keyword_detail.csv aus der Keyword-Analyse.")
    parser.add_argument("-o", "--output", default="keyword_heatmap.png", help="Pfad zur Ausgabedatei (PNG).")
    args = parser.parse_args()
    main(args.detail_csv, args.output)

