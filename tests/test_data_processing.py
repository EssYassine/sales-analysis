import pandas as pd
import numpy as np
import pytest
from src.functions import (
    load_data,
    groupby_aggregate,
    groupby_aggregate_multi,
    filter_by_value,
    groupby_size,
)

# === FIXTURES ===
@pytest.fixture
def sample_data():
    """Crée un DataFrame d'exemple pour les tests."""
    return pd.DataFrame({
        "SELLER": ["Alice", "Bob", "Alice", "Bob", "Alice"],
        "DATE": pd.to_datetime([
            "2023-01-10", "2023-04-12", "2024-02-20", "2024-05-15", "2023-03-08"
        ]),
        "QUANTITY": [10, 20, 15, 5, 8],
        "UNIT_PRICE": [100, 200, 150, 300, 90],
        "TOTAL": [1000, 4000, 2250, 1500, 720],
    })


# === TESTS ===
def test_load_data(tmp_path):
    """Teste la fonction load_data avec un fichier Excel temporaire."""
    # Préparation : créer un mini fichier Excel
    df = pd.DataFrame({
        "DATE": ["2023-01-01", "2023-04-15"],
        "SELLER": ["Alice", "Bob"],
        "TOTAL": [100, 200],
    })
    file_path = tmp_path / "data.xlsx"
    df.to_excel(file_path, index=False)

    # Exécution
    loaded = load_data(file_path, "DATE", "YEAR", "QUARTER")

    # Vérifications
    assert "YEAR" in loaded.columns
    assert "QUARTER" in loaded.columns
    assert loaded.loc[0, "YEAR"] == 2023
    assert str(loaded.loc[0, "QUARTER"]).startswith("2023Q")


def test_groupby_aggregate(sample_data):
    result = groupby_aggregate(sample_data, ["SELLER"], "TOTAL", "sum")
    expected = {"Alice": 3970, "Bob": 5500}
    for _, row in result.iterrows():
        assert np.isclose(row["TOTAL"], expected[row["SELLER"]])


def test_groupby_aggregate_multi(sample_data):
    result = groupby_aggregate_multi(sample_data, ["SELLER"], {"TOTAL": ["mean", "sum"]})
    assert "TOTAL" in result.columns
    assert "mean" in result.columns.levels[1] or isinstance(result.columns, pd.MultiIndex)


def test_filter_by_value(sample_data):
    result = filter_by_value(sample_data, "SELLER", "Alice")
    assert result["SELLER"].eq("Alice").all()
    assert len(result) == 3


def test_groupby_size(sample_data):
    result = groupby_size(sample_data, ["SELLER"])
    assert "COUNT" in result.columns
    assert result[result["SELLER"] == "Alice"]["COUNT"].iloc[0] == 3
