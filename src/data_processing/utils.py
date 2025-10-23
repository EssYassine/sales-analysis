"""
Fonctions utilitaires pour le projet data_processing
"""

import os
import pandas as pd

"""
Génération des fichiers de test nécessaires pour valider le module `data_processing.loader`.

ce script crée trois fichiers dans le dossier `data/input` :
    - test_data.xlsx  (avec deux feuilles)
    - test_data.csv
    - test_data.json

Chaque fichier contient des données simples et cohérentes pour les tests unitaires.
"""
def ensure_test_data():
    """
    Vérifie si les fichiers de test existent, sinon les crée automatiquement.
    Fichiers créés :
        - test_data.xlsx
        - test_data.csv
        - test_data.json
    """
    excel_path = "data/input/test_data.xlsx"
    csv_path = "data/input/test_data.csv"
    json_path = "data/input/test_data.json"

    os.makedirs("data/input", exist_ok=True)

    # Excel
    if not os.path.exists(excel_path):
        df1 = pd.DataFrame({
            "ColA": [1,2,3,4],
            "ColB": [5,6,7,8],
            "ColC": [9,10,11,12]
        })
        df2 = pd.DataFrame({
            "Name": ["Alice", "Bob", "Chloé"],
            "Age": [25,30,22],
            "City": ["Paris","Lyon","Marseille"]
        })
        with pd.ExcelWriter(excel_path) as writer:
            df1.to_excel(writer, index=False, sheet_name="Sheet1")
            df2.to_excel(writer, index=False, sheet_name="Sheet2")

    # CSV
    if not os.path.exists(csv_path):
        df_csv = pd.DataFrame({
            "Name": ["Alice", "Bob", "Chloé"],
            "Score": [85,72,55],
            "Passed": [True, True, False]
        })
        df_csv.to_csv(csv_path, index=False)

    # JSON
    if not os.path.exists(json_path):
        df_csv = pd.read_csv(csv_path)
        df_csv.to_json(json_path, orient="records", indent=2)
