# === IMPORTS ===
import os               #gestion des chemins et répertoires
import pandas as pd          # Pour la manipulation des données tabulaires
import matplotlib.pyplot as plt  # Pour la génération des graphiques et tableaux
from pathlib import Path
from typing import Union
from matplotlib.axes import Axes
from matplotlib.backends.backend_pdf import PdfPages

# === DATA LOADING ===
def load_data(file_path: Union[str, Path], date_col: str, year_col: str, quarter_col: str) -> pd.DataFrame:
    """
    Charge un fichier Excel, ajoute les colonnes année et trimestre.

    Params:
        file_path (str): chemin du fichier Excel
        date_col (str): nom de la colonne contenant la date
        year_col (str): nom de la colonne à créer pour l'année
        quarter_col (str): nom de la colonne à créer pour le trimestre

    Scripts:
        1. lecture du fichier Excel et conversion de la colonne de date (date_col) en objets datetime
        2. Création d'une nouvelle colonne (nommée year_col) et extraction de l'année
        3. Création d'une nouvelle colonne (nommée quarter_col)
            et extraction du trimestre sous la forme "YYYYQn" (par exemple "2023Q1").

    Returns:
        pd.DataFrame: DataFrame pandas enrichi
    """
    df = pd.read_excel(str(file_path), parse_dates=[date_col])
    df[year_col] = df[date_col].dt.year
    df[quarter_col] = df[date_col].dt.to_period('Q')
    return df

# === GENERIC FUNCTIONS ===
def groupby_aggregate(df: pd.DataFrame, group_cols: list[str], agg_col: str, agg_func: str) -> pd.DataFrame:
    """
    Regroupe le DataFrame selon group_cols et applique une agrégation agg_func sur agg_col.

    Params:
        df (pd.DataFrame): DataFrame source
        group_cols (list[str]): colonnes pour le groupement
        agg_col (str): colonne à agréger
        agg_func (str): fonction d'agrégation ('sum', 'mean', etc.)

    Returns:
        pd.DataFrame: DataFrame agrégé
    """
    return df.groupby(group_cols)[agg_col].agg(agg_func).reset_index()

def groupby_aggregate_multi(df: pd.DataFrame, group_cols: list[str], agg_dict: dict) -> pd.DataFrame:
    """
    Regroupe le DataFrame selon group_cols et applique les agrégations du dictionnaire agg_dict.

    Params:
        df (pd.DataFrame): DataFrame source
        group_cols (list[str]): colonnes pour le groupement
        agg_dict (dict): dictionnaire des agrégations {colonne: [fonctions]}

    Returns:
        pd.DataFrame: DataFrame agrégé
    """
    return df.groupby(group_cols).agg(agg_dict).reset_index()

def filter_by_value(df: pd.DataFrame, col: str, value) -> pd.DataFrame:
    """
    Filtre le DataFrame sur une colonne et une valeur donnée.

    Params:
        df (DataFrame): DataFrame source
        col (str): colonne à filtrer
        value: valeur à conserver

    Returns:
        DataFrame: DataFrame filtré
    """
    mask: pd.Series[bool] = df[col] == value
    return df[mask]

def groupby_size(df: pd.DataFrame, group_cols: list[str], count_name: str = "COUNT") -> pd.DataFrame:
    """
    Compte le nombre de lignes par groupe.

    Params:
        df (pd.DataFrame): DataFrame source
        group_cols (list[str]): colonnes pour le groupement
        count_name (str): nom de la colonne résultat

    Returns:
        pd.DataFrame: DataFrame avec les tailles des groupes
    """
    return df.groupby(group_cols).size().reset_index(name=count_name)

# === TABLE & CHART EXPORT FUNCTIONS ===
def save_table_image(df: pd.DataFrame, title: str, img_path_or_pdf, max_rows: int = 30) -> None:
    """
    Sauvegarde un DataFrame sous forme de tableau image (png ou PDF).
    """
    display_df = df.copy()
    note = ""
    if display_df.shape[0] > max_rows:
        display_df = display_df.head(max_rows)
        note = f"Affichage limité à {max_rows} lignes sur {df.shape[0]}."

    nrows, ncols = display_df.shape
    fig_height = min(18.0, 1.5 + nrows * 0.6)
    fig_width = min(18.0, 2.5 + ncols * 1.3)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    # ax: Axes  # type hint si tu veux calmer le linter
    ax: Axes
    ax.axis('off')
    ax.set_title(title, fontsize=17, weight='bold', pad=18, color="#2563eb")

    if note:
        ax.text(0.5, 1.02, note,
                fontsize=11, color='gray', va='center', ha='center', transform=ax.transAxes)

    tbl = ax.table(
        cellText=display_df.values,
        colLabels=display_df.columns,
        cellLoc='center',
        loc='center',
        colColours=['#dbeafe'] * ncols
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(13)
    tbl.scale(1.3, 1.4)

    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor('black')
        if row == 0:
            cell.set_text_props(weight='bold', color='#1e293b')
            cell.set_facecolor('#dbeafe')
        elif row % 2 == 1:
            cell.set_facecolor('#f3f4f6')
        else:
            cell.set_facecolor('white')

    for col in range(ncols):
        tbl.auto_set_column_width(col)

    plt.tight_layout()

    if isinstance(img_path_or_pdf, PdfPages):
        img_path_or_pdf.savefig(fig, bbox_inches='tight')
    else:
        os.makedirs(os.path.dirname(img_path_or_pdf), exist_ok=True)
        fig.savefig(img_path_or_pdf, bbox_inches='tight')

    plt.close(fig)

def save_histogram_image(df: pd.DataFrame, col: str, title: str, output, bins=10) -> None:
    """
    Sauvegarde un histogramme soit en image PNG, soit directement dans un PDF (PdfPages).

    Params:
        df (pd.DataFrame): DataFrame source
        col (str): colonne à afficher en histogramme
        title (str): titre du graphique
        img_path (str): chemin de l'image à sauvegarder
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    n, bins, patches = ax.hist(df[col].dropna(), bins=10, color="#2563eb", alpha=0.7, edgecolor="black")
    ax.set_title(title, fontsize=16, weight='bold', pad=15, color="#2563eb")
    ax.set_xlabel(col, fontsize=13)
    ax.set_ylabel('Fréquence', fontsize=13)
    ax.grid(True, linestyle='--', alpha=0.5)
    for i in range(len(n)):
        ax.text(float((bins[i] + bins[i + 1]) / 2), float(n[i]), f"{int(n[i])}",
                ha='center', va='bottom', fontsize=11, color='#334155')
    plt.tight_layout()
    if isinstance(output, str):
        os.makedirs(os.path.dirname(output), exist_ok=True)
        fig.savefig(output, bbox_inches="tight")
    else:
        output.savefig(fig, bbox_inches="tight")
    plt.close(fig)

def generate_pdf(path: str, dataframes: list[tuple], histograms: list[tuple]):
    """
    Génère un PDF unique contenant des tables et histogrammes.

    Params:
        path (str): chemin complet du PDF à sauvegarder
        dataframes (list of tuple): liste de tuples (df, title) pour les tables
        histograms (list of tuple): liste de tuples (df, col, title) pour les histogrammes
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with PdfPages(path) as pdf:
        # Tables
        for table_df, table_title in dataframes:
            save_table_image(table_df, table_title, pdf)

        # Histogrammes
        for hist_df, col_name, hist_title in histograms:
            save_histogram_image(hist_df, col_name, hist_title, pdf)