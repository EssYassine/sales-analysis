"""
Tests unitaires pour le module data_processing.loader
"""
import os
import pytest
import pandas as pd
from src.data_processing.loader import DataLoader
from src.data_processing.utils import ensure_test_data


# -----------------------------------------------------
# Chemins des fichiers de test
# -----------------------------------------------------

TEST_EXCEL = "data/input/test_data.xlsx"
TEST_CSV = "data/input/test_data.csv"
TEST_JSON = "data/input/test_data.json"
TEST_FAKE = "data/input/inexistant.xlsx"
TEST_INVALID = "data/input/test.unsupported"


# -----------------------------------------------------
# Fixture pour générer les fichiers de test
# -----------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """S'assure que tous les fichiers de test existent avant les tests."""
    ensure_test_data()


# -----------------------------------------------------
# Fixtures pour loaders
# -----------------------------------------------------

@pytest.fixture
def excel_loader():
    """Fixture pour un DataLoader Excel"""
    return DataLoader(TEST_EXCEL)

@pytest.fixture
def csv_loader():
    """Fixture pour un DataLoader CSV"""
    return DataLoader(TEST_CSV)

@pytest.fixture
def json_loader():
    """Fixture pour un DataLoader JSON"""
    return DataLoader(TEST_JSON)


# -----------------------------------------------------
# Tests type de fichier
# -----------------------------------------------------

def test_detect_file_type_excel(excel_loader):
    assert excel_loader.file_type == "excel"

def test_detect_file_type_csv(csv_loader):
    assert csv_loader.file_type == "csv"

def test_detect_file_type_json(json_loader):
    assert json_loader.file_type == "json"


# -----------------------------------------------------
# Tests chargement des données
# -----------------------------------------------------

def test_load_excel_data(excel_loader):
    df = excel_loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_excel_specific_sheet(excel_loader):
    df = excel_loader.load_data(sheet_name="Sheet2")
    assert isinstance(df, pd.DataFrame)
    assert "Name" in df.columns

def test_load_csv_data(csv_loader):
    df = csv_loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_json_data(json_loader):
    df = json_loader.load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# -----------------------------------------------------
# Tests listing sheets
# -----------------------------------------------------

def test_list_sheets_excel(excel_loader):
    sheets = excel_loader.list_sheets()
    assert isinstance(sheets, list)
    assert len(sheets) >= 1

def test_list_sheets_non_excel(csv_loader, json_loader):
    assert csv_loader.list_sheets() is None
    assert json_loader.list_sheets() is None


# -----------------------------------------------------
# Tests erreurs
# -----------------------------------------------------

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        loader = DataLoader(TEST_FAKE)
        loader.load_data()
def test_invalid_extension():
    """Teste qu'un fichier avec extension non supportée lève ValueError"""

    # Crée un fichier dummy pour le test
    with open(TEST_INVALID, "w") as f:
        f.write("dummy content")

    try:
        with pytest.raises(ValueError):
            DataLoader(TEST_INVALID)
    finally:
        # Supprime le fichier après le test
        os.remove(TEST_INVALID)
