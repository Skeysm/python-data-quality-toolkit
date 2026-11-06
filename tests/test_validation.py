
from data_quality.validation import (
    validate_email_format,
    validate_numeric_range,
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


def test_valid_numeric_range():
    assert validate_numeric_range(25, "age", 18, 100) is None


def test_value_below_minimum():
    error = validate_numeric_range(15, "age", 18, 100)

    assert "below" in error


def test_value_above_maximum():
    error = validate_numeric_range(120, "age", 18, 100)

    assert "exceeds" in error


def test_value_equal_to_minimum():
    assert validate_numeric_range(18, "age", 18, 100) is None


def test_value_equal_to_maximum():
    assert validate_numeric_range(100, "age", 18, 100) is None


def test_invalid_numeric_type():
    error = validate_numeric_range("abc", "age", 18, 100)

    assert "not numeric" in error


def test_boolean_is_not_numeric():
    error = validate_numeric_range(True, "age", 18, 100)

    assert "not numeric" in error


def test_infinite_value():
    error = validate_numeric_range(float("inf"), "price", 0)

    assert "not finite" in error

def test_nan_value():
    error = validate_numeric_range(float("nan"), "price", 0)

    assert "not finite" in error


def test_value_without_line_number():
    error = validate_numeric_range(5, "age", 18)

    assert error.startswith("Field 'age'")