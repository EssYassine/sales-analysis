import os
from config import (
    FILE_PATH, SELLER_COL, DATE_COL, YEAR_COL, QUARTER_COL,
    TOTAL_COL, QUANTITY_COL, UNIT_PRICE_COL, QUESTIONS
)
import functions as fn

def main():
    # Charger les données
    df = fn.load_data(
        file_path=FILE_PATH,
        date_col=DATE_COL,
        year_col=YEAR_COL,
        quarter_col=QUARTER_COL
    )

    # Créer les dossiers de sortie si besoin
    os.makedirs("../data/output/tables", exist_ok=True)
    os.makedirs("../data/output/charts", exist_ok=True)
    os.makedirs("../data/output/reports", exist_ok=True)

    # Préparer les listes pour le PDF
    tables = []  # Liste des tables (DataFrame, titre)
    histograms = []  # Liste des histogrammes (DataFrame, colonne, titre)

    # Q1 - Pour chaque vendeur, quel est le chiffre d'affaires total par année? (Table-pdf)
    q1 = QUESTIONS["Q1"]

    result1 = fn.groupby_aggregate(df, q1["group_cols"], q1["agg_col"], q1["agg_func"])
    print(f"Q1 : {q1['title']}\n", result1)
    fn.save_table_image(result1, q1["title"], "../data/output/tables/Q1.png")
    tables.append((result1, q1["title"]))

    # Q2 - Pour chaque vendeur, quel est le chiffre d'affaires moyen par trimestre? (Table-odf)
    q2 = QUESTIONS["Q2"]
    result2 = fn.groupby_aggregate(df, q2["group_cols"], q2["agg_col"], q2["agg_func"])
    print(f"\nQ2 : {q2['title']}\n", result2)
    fn.save_table_image(result2, q2["title"], "../data/output/tables/Q2.png")
    tables.append((result2, q2["title"]))

    # Q3 - Pour chaque vendeur, quelle est la quantité moyenne (QUANTITY) vendue par transaction ?
    q3 = QUESTIONS["Q3"]
    result3 = fn.groupby_aggregate(df, q3["group_cols"], q3["agg_col"], q3["agg_func"])
    print(f"\nQ3 : {q3['title']}\n", result3)
    fn.save_table_image(result3, q3["title"], "../data/output/tables/Q3.png")
    tables.append((result3, q3["title"]))

    # Q4 - En 2023, quel est le vendeur ayant la plus grande dispersion des prix unitaires (UNIT_PRICE)? (Histo-pdf)
    q4 = QUESTIONS["Q4"]
    df_2023 = fn.filter_by_value(df, YEAR_COL, q4["year"])
    result4 = fn.groupby_aggregate(df_2023, q4["group_cols"], q4["agg_col"], q4["agg_func"])
    print(f"\nQ4 : {q4['title']}\n", result4)
    fn.save_histogram_image(result4, q4["agg_col"], q4["title"], "../output/charts/Q4.png")
    histograms.append((result4, q4["agg_col"], q4["title"]))

    # Q5 - En 2025, quel est le classement des vendeurs par chiffre d'affaires moyen par transaction ? (Table-pdf)
    q5 = QUESTIONS["Q5"]
    df_2025 = fn.filter_by_value(df, YEAR_COL, q5["year"])
    result5 = fn.groupby_aggregate(df_2025, q5["group_cols"], q5["agg_col"], q5["agg_func"])
    result5 = result5.sort_values(by=q5["agg_col"], ascending=False)
    print(f"\nQ5 : {q5['title']}\n", result5)
    fn.save_table_image(result5, q5["title"], "../data/output/tables/Q5.png")
    tables.append((result5, q5["title"]))

    # Q6 - Pour chaque vendeur, quelles sont les valeurs min, max et moyennes du chiffre d'affaires (TOTAL) sur toute la période? (Table-pdf)
    q6 = QUESTIONS["Q6"]
    result6 = fn.groupby_aggregate_multi(df, q6["group_cols"], q6["agg_dict"])
    print(f"\nQ6 : {q6['title']}\n", result6)
    fn.save_table_image(result6, q6["title"], "../data/output/tables/Q6.png")
    tables.append((result6, q6["title"]))

    # Q7 - Quel vendeur a obtenu la médiane de chiffre d'affaires (TOTAL) la plus élevée en 2023 ? (Table-pdf)
    q7 = QUESTIONS["Q7"]
    df_2023b = fn.filter_by_value(df, YEAR_COL, q7["year"])
    result7 = fn.groupby_aggregate(df_2023b, q7["group_cols"], q7["agg_col"], q7["agg_func"])
    result7 = result7.sort_values(by=q7["agg_col"], ascending=False)
    print(f"\nQ7 : {q7['title']}\n", result7)
    fn.save_table_image(result7, q7["title"], "../data/output/tables/Q7.png")
    tables.append((result7, q7["title"]))

    # Q8 - Pour chaque vendeur, quel est le nombre total de transactions par année? (bisto-pdf)
    q8 = QUESTIONS["Q8"]
    result8 = fn.groupby_size(df, q8["group_cols"], q8["count_name"])
    print(f"\nQ8 : {q8['title']}\n", result8)
    #fn.save_table_image(result8, q8["title"], "../output/tables/Q8.png")
    fn.save_histogram_image(result8, q8["count_name"], q8["title"], "../output/charts/Q8.png")
    histograms.append((result8, q8["count_name"], q8["title"]))

    # --- Générer le PDF unique avec toutes les tables et histogrammes ---
    pdf_path = "../data/output/reports/rapport_statistiques.pdf"
    fn.generate_pdf(pdf_path, tables, histograms)

    print(f"\nPDF généré avec succès : {pdf_path}")

if __name__ == "__main__":
    main()