"""
Module responsable du chargement de données depuis différents formats
(Excel, CSV, JSON, etc.).

Renvoie toujours un DataFrame pour faciliter l'analyse.
"""

import os
import pandas as pd


class DataLoader:
    """
    Classe responsable du chargement et de la gestion des données.
    """

    SUPPORTED_EXTENSIONS = (".xlsx", ".xls", ".csv", ".json")

    def __init__(self, file_path: str):
        """
        Initialise le DataLoader avec un chemin de fichier.

        Parameters
        ----------
        file_path : str
            Chemin complet du fichier de données à charger.
        """
        self.file_path = file_path
        self._check_file()
        self.file_type = self._detect_file_type()

    # -----------------------------
    # Vérifications de base
    # -----------------------------

    def _check_file(self):
        """Vérifie que le fichier existe et que l'extension est supportée."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Fichier introuvable : {self.file_path}")

        ext = os.path.splitext(self.file_path)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Extension non supportée : {ext}")

    def _detect_file_type(self) -> str:
        """Retourne le type du fichier : 'excel', 'csv', 'json'."""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext in (".xlsx", ".xls"):
            return "excel"
        elif ext == ".csv":
            return "csv"
        elif ext == ".json":
            return "json"
        else:
            raise ValueError(f"Type de fichier inconnu : {ext}")

    # -----------------------------------------------------
    # Méthodes principales
    # -----------------------------------------------------

    def list_sheets(self) -> list | None:
        """
        Liste les feuilles disponibles dans un fichier Excel.
        Retourne None si le fichier n'est pas de type Excel.
        """
        if self.file_type != "excel":
            print("❌ Lister les feuilles n’est disponible que pour les fichiers Excel.")
            return None

        try:
            excel_file = pd.ExcelFile(self.file_path)
            return excel_file.sheet_names
        except Exception as e:
            print(f"Erreur lors de la lecture des feuilles : {e}")
            return None

    def load_data(self, sheet_name: str | None = None) -> pd.DataFrame:
        """
        Charge les données du fichier dans un DataFrame.

        Parameters
        ----------
        sheet_name : str | None
            Nom de la feuille à lire (si Excel). Si None, la première feuille est chargée.

        Returns
        -------
        pd.DataFrame
            Données chargées dans un DataFrame.
        """
        if self.file_type == "excel":
            return self._load_excel(sheet_name)
        elif self.file_type == "csv":
            return pd.read_csv(self.file_path)
        elif self.file_type == "json":
            return pd.read_json(self.file_path)
        else:
            raise ValueError(f"Format de fichier non supporté : {self.file_type}")

    # -----------------------------
    # Méthodes internes
    # -----------------------------

    def _load_excel(self, sheet_name: str | None = None) -> pd.DataFrame:
        """
        Charge un fichier Excel et retourne un DataFrame.
        Si sheet_name=None et plusieurs feuilles, prend la première feuille.
        """
        excel_file = pd.ExcelFile(self.file_path)
        if sheet_name is None:
            sheet_name = excel_file.sheet_names[0]

        df = pd.read_excel(self.file_path, sheet_name=sheet_name)
        return df

