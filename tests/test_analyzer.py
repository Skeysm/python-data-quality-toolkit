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

    
def test_missing_keys_are_counted():
    records = [
        {"name": "Alice", "age": 28},
        {"name": "Bob"},
        {"name": "Charlie", "age": None},
    ]

    result = analyze_columns(records)

    assert result["age"]["total"] == 3
    assert result["age"]["present"] == 1
    assert result["age"]["missing"] == 2
    assert result["age"]["missing_rate"] == pytest.approx(200 / 3)


def test_duplicate_values_are_counted_once():
    records = [
        {"city": "Paris"},
        {"city": "Paris"},
        {"city": "Lyon"},
        {"city": "Paris"},
    ]

    result = analyze_columns(records)

    assert result["city"]["present"] == 4
    assert result["city"]["unique"] == 2


def test_mixed_scalar_types():
    records = [
        {"value": "Python"},
        {"value": 42},
        {"value": 3.14},
    ]

    result = analyze_columns(records)

    assert result["value"]["present"] == 3
    assert result["value"]["missing"] == 0
    assert result["value"]["unique"] == 3


def test_column_order_is_preserved():
    records = [
        {"name": "Alice", "age": 28, "city": "Paris"},
        {"name": "Bob", "age": 35, "city": "Lyon"},
    ]

    result = analyze_columns(records)

    assert list(result.keys()) == ["name", "age", "city"]


def test_unhashable_values_raise_clear_error():
    records = [
        {"name": "Alice"},
        {"name": ["Bob", "Charlie"]},
    ]

    with pytest.raises(TypeError, match="Column 'name'"):
        analyze_columns(records)
