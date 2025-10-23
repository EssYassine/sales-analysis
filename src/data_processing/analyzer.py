"""
Module pour analyser les DataFrames et répondre à des requêtes simples
ou complexes (filtrage, agrégations, statistiques, regroupements, etc.)
"""

import pandas as pd

class DataAnalyzer:
    """
    Classe pour manipuler un DataFrame et répondre à des requêtes dynamiques.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialise avec un DataFrame existant.

        Parameters
        ----------
        df : pd.DataFrame
        """
        self.df = df


    # -------------------------------------------------
    # Statistiques simples
    # -------------------------------------------------

    def mean(self, column: str) -> float:
        """Retourne la moyenne d'une colonne numérique."""
        if column not in self.df.columns:
            raise ValueError(f"La colonne '{column}' n'existe pas dans le DataFrame")
        return self.df[column].mean()

    def count_rows(self, condition: str = None) -> int:
        """
        Compte le nombre de lignes.
        Si `condition` est spécifiée, filtre selon cette condition (ex: "Score > 50").
        """
        if condition is None:
            return len(self.df)
        else:
            filtered = self.df.query(condition)
            return len(filtered)


    # -------------------------------------------------
    # Filtrage
    # -------------------------------------------------

    def filter(self, condition: str) -> pd.DataFrame:
        """
        Retourne un DataFrame filtré selon la condition.
        Ex: "Age > 25 and City == 'Paris'"
        """
        return self.df.query(condition)


    # -------------------------------------------------
    # Agrégations
    # -------------------------------------------------

    def groupby(self, by_columns: list, agg_dict: dict) -> pd.DataFrame:
        """
        Retourne un DataFrame agrégé.

        Parameters
        ----------
        by_columns : list
            Colonnes pour le groupby
        agg_dict : dict
            Dictionnaire {colonne: fonction} pour l'agrégation
        """
        return self.df.groupby(by_columns).agg(agg_dict).reset_index()


    # -------------------------------------------------
    # Statistiques complètes
    # -------------------------------------------------

    def describe(self) -> pd.DataFrame:
        """Retourne des statistiques descriptives du DataFrame"""
        return self.df.describe(include='all')
