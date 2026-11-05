
from data_quality.validation import (
    validate_email_format,
    validate_required_fields,
)


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


def test_valid_email_addresses():
    records = [
        {"email": "alice@example.com"},
        {"email": "bob.smith@example.co.uk"},
    ]

    result = validate_email_format(records, ["email"])

    assert result == []


def test_invalid_email_addresses():
    records = [
        {"email": "alice@example"},
        {"email": "bob.example.com"},
        {"email": "charlie @example.com"},
    ]

    result = validate_email_format(records, ["email"])

    assert len(result) == 3
    assert all(issue["error"] == "invalid_email" for issue in result)


def test_non_string_email_is_invalid():
    records = [
        {"email": 12345},
    ]

    result = validate_email_format(records, ["email"])

    assert len(result) == 1
    assert result[0]["row"] == 1
    assert result[0]["field"] == "email"


def test_missing_email_is_not_reported_twice():
    records = [
        {"name": "Alice"},
        {"name": "Bob", "email": None},
        {"name": "Charlie", "email": ""},
    ]

    result = validate_email_format(records, ["email"])

    assert result == []
