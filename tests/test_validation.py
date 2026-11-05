
from data_quality.validation import validate_required_fields


def test_missing_required_field():
    records = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob"},
    ]

    result = validate_required_fields(
        records,
        ["name", "email"],
    )

    assert len(result) == 1
    assert result[0]["row"] == 2
    assert result[0]["field"] == "email"


def test_none_value_is_invalid():
    records = [
        {"name": "Alice", "email": None},
    ]

    result = validate_required_fields(
        records,
        ["name", "email"],
    )

    assert len(result) == 1
    assert result[0]["field"] == "email"


def test_whitespace_only_value_is_invalid():
    records = [
        {"name": "   ", "email": "alice@example.com"},
    ]

    result = validate_required_fields(
        records,
        ["name"],
    )

    assert len(result) == 1
    assert result[0]["field"] == "name"


def test_valid_records_return_empty_list():
    records = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
    ]

    result = validate_required_fields(
        records,
        ["name", "email"],
    )

    assert result == []
