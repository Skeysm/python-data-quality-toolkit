from data_quality.analyzer import analyze_columns
import pytest

def test_analyze_columns():
    records = [
        {"name": "Alice", "age": 28},
        {"name": "Bob", "age": None},
        {"name": "Charlie"},
    ]

    result = analyze_columns(records)

    assert result["name"]["missing"] == 0
    assert result["name"]["unique"] == 3

    assert result["age"]["total"] == 3
    assert result["age"]["present"] == 1
    assert result["age"]["missing"] == 2
    assert result["age"]["missing_rate"] == pytest.approx(200 / 3)
    assert result["age"]["unique"] == 1

def test_empty_dataset():
    assert analyze_columns([]) == {}


def test_all_values_missing():
    records = [
        {"age": None},
        {"age": None},
    ]

    result = analyze_columns(records)

    assert result["age"]["missing"] == 2
    assert result["age"]["missing_rate"] == 100.0