"""
Tests unitaires pour le module data_processing.analyzer
"""

import pytest
import pandas as pd
from src.data_processing.analyzer import DataAnalyzer
from src.data_processing.utils import ensure_test_data
from src.data_processing.loader import DataLoader


# -----------------------------------------------------
# Préparation des fichiers de test
# -----------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """S'assure que tous les fichiers de test existent avant les tests."""
    ensure_test_data()


# -----------------------------------------------------
# Fixtures pour charger les données
# -----------------------------------------------------

@pytest.fixture
def df_excel():
    loader = DataLoader("data/input/test_data.xlsx")
    # Charger seulement la première feuille pour le test
    return loader.load_data(sheet_name="Sheet1")

@pytest.fixture
def df_csv():
    loader = DataLoader("data/input/test_data.csv")
    return loader.load_data()


@pytest.fixture
def analyzer_excel(df_excel):
    return DataAnalyzer(df_excel)

@pytest.fixture
def analyzer_csv(df_csv):
    return DataAnalyzer(df_csv)


# -----------------------------------------------------
# Tests unitaires
# -----------------------------------------------------

def test_mean(analyzer_excel):
    mean_colA = analyzer_excel.mean("ColA")
    assert mean_colA == 2.5  # (1+2+3+4)/4

def test_count_rows_no_condition(analyzer_csv):
    count = analyzer_csv.count_rows()
    assert count == 3  # 3 lignes dans test_data.csv

def test_count_rows_with_condition(analyzer_csv):
    count = analyzer_csv.count_rows("Score > 70")
    assert count == 2  # Alice (85) et Bob (72)

def test_filter(analyzer_csv):
    filtered = analyzer_csv.filter("Passed == True")
    assert len(filtered) == 2
    assert all(filtered["Passed"] == True)

def test_groupby(analyzer_csv):
    grouped = analyzer_csv.groupby(
        by_columns=["Passed"],
        agg_dict={"Score": "mean"}
    )
    # Vérifie qu'on a deux groupes : True et False
    assert set(grouped["Passed"]) == {True, False}
    # Moyenne du groupe True
    mean_true = grouped.loc[grouped["Passed"]==True, "Score"].values[0]
    assert mean_true == (85+72)/2

def test_describe(analyzer_csv):
    desc = analyzer_csv.describe()
    # Vérifie que la colonne Score est dans le DataFrame descriptif
    assert "Score" in desc.columns
