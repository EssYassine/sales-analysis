# ==========================
# CONFIGURATION FILE
# ==========================

# ==========================
# Paramètres génériques pour l'analyse des ventes
# ==========================

FILE_PATH = "../data/Data_Load.xlsx"      # Chemin du fichier Excel à analyser

# Noms de colonnes standards
SELLER_COL = "SELLER"
DATE_COL = "DATE"
YEAR_COL = "YEAR"
QUARTER_COL = "QUARTER"
TOTAL_COL = "TOTAL"
QUANTITY_COL = "QUANTITY"
UNIT_PRICE_COL = "UNIT_PRICE"

# ==========================
# Paramètres spécifiques par question/statistique
# ==========================

QUESTIONS = {
    "Q1": {
        "group_cols": [SELLER_COL, YEAR_COL],
        "agg_col": TOTAL_COL,
        "agg_func": "sum",
        "title": "Chiffre d'affaires total par vendeur et par année"
    },
    "Q2": {
        "group_cols": [SELLER_COL, QUARTER_COL],
        "agg_col": TOTAL_COL,
        "agg_func": "mean",
        "title": "Chiffre d'affaires moyen par trimestre et vendeur"
    },
    "Q3": {
        "group_cols": [SELLER_COL],
        "agg_col": QUANTITY_COL,
        "agg_func": "mean",
        "title": "Quantité moyenne vendue par transaction et vendeur"
    },
    "Q4": {
        "year": 2023,
        "group_cols": [SELLER_COL],
        "agg_col": UNIT_PRICE_COL,
        "agg_func": "std",
        "title": "Dispersion des prix unitaires des vendeurs en 2023"
    },
    "Q5": {
        "year": 2025,
        "group_cols": [SELLER_COL],
        "agg_col": TOTAL_COL,
        "agg_func": "mean",
        "title": "Classement CA moyen par transaction en 2025"
    },
    "Q6": {
        "group_cols": [SELLER_COL],
        "agg_dict": {TOTAL_COL: ["min", "max", "mean"]},
        "title": "Min, Max, Moy du CA par vendeur"
    },
    "Q7": {
        "year": 2023,
        "group_cols": [SELLER_COL],
        "agg_col": TOTAL_COL,
        "agg_func": "median",
        "title": "Médiane du CA en 2023 par vendeur"
    },
    "Q8": {
        "group_cols": [SELLER_COL, YEAR_COL],
        "count_name": "TRANSACTIONS",
        "title": "Nombre total de transactions par vendeur et par année"
    }
}