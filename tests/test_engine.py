import pytest

from data_quality.engine import validate_record, validate_records
from data_quality.validation import validate_numeric_range


def required(value):
    if value is None or not str(value).strip():
        return "Value is required."

    return None


def test_valid_record():
    record = {
        "name": "John",
        "age": 30,
    }

    rules = {
        "name": [required],
        "age": [
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            )
        ],
    }

    assert validate_record(record, rules) == []


def test_multiple_validation_errors():
    record = {
        "name": "",
        "age": 15,
    }

    rules = {
        "name": [required],
        "age": [
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            )
        ],
    }

    result = validate_record(record, rules)

    assert len(result) == 2
    assert result[0]["field"] == "name"
    assert result[1]["field"] == "age"


def test_missing_field():
    record = {"age": 30}

    rules = {
        "name": [required],
    }

    result = validate_record(record, rules)

    assert len(result) == 1
    assert result[0]["field"] == "name"


def test_multiple_validators_on_same_field():
    record = {"age": 150}

    rules = {
        "age": [
            required,
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            ),
        ],
    }

    result = validate_record(record, rules)

    assert len(result) == 1
    assert result[0]["field"] == "age"


def test_validator_exception_does_not_stop_execution():
    def broken_validator(value):
        raise ValueError("Unexpected error")

    def another_validator(value):
        return "Second validation failed."

    record = {"age": 25}

    rules = {
        "age": [broken_validator, another_validator],
    }

    result = validate_record(record, rules)

    assert len(result) == 2
    assert "ValueError" in result[0]["message"]
    assert "Second validation failed." in result[1]["message"]


def test_invalid_validator_configuration():
    record = {"age": 25}
    rules = {"age": ["not a function"]}

    with pytest.raises(TypeError):
        validate_record(record, rules)


def test_validator_invalid_return_type():
    record = {"age": 25}
    rules = {"age": [lambda value: 123]}

    result = validate_record(record, rules)

    assert len(result) == 1
    assert "string or None" in result[0]["message"]


def test_validate_multiple_records():
    records = [
        {"age": 25},
        {"age": 15},
        {"age": 150},
    ]

    rules = {
        "age": [
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            )
        ],
    }

    result = validate_records(records, rules)

    assert len(result) == 2
    assert result[0]["record_index"] == 1
    assert result[1]["record_index"] == 2


def test_validate_records_empty_list():
    assert validate_records([], {}) == []