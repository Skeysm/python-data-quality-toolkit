from collections.abc import Callable
from typing import Any

Validator = Callable[[Any], str | None]


def validate_record(
    record: dict[str, Any],
    rules: dict[str, list[Validator]],
) -> list[dict[str, str]]:
    """Validate a record against multiple field-level rules."""

    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary.")

    if not isinstance(rules, dict):
        raise TypeError("rules must be a dictionary.")

    issues = []

    for field, validators in rules.items():
        if not isinstance(field, str):
            raise TypeError("Rule field names must be strings.")

        if not isinstance(validators, list):
            raise TypeError(f"Validators for '{field}' must be a list.")

        value = record.get(field)

        for validator in validators:
            if not callable(validator):
                raise TypeError(
                    f"Validator for '{field}' must be callable."
                )

            try:
                error = validator(value)

                if error is not None:
                    if not isinstance(error, str):
                        raise TypeError(
                            "Validator must return a string or None."
                        )

                    issues.append({
                        "field": field,
                        "message": error,
                    })

            except Exception as exc:  # noqa: BLE001
                issues.append({
                    "field": field,
                    "message": (
                        f"Validator failed: {type(exc).__name__}: {exc}"
                    ),
                })

    return issues


def validate_records(
    records: list[dict[str, Any]],
    rules: dict[str, list[Validator]],
) -> list[dict[str, Any]]:
    """Validate multiple records and collect their validation issues."""

    if not isinstance(records, list):
        raise TypeError("records must be a list.")

    results = []

    for index, record in enumerate(records):
        issues = validate_record(record, rules)

        if issues:
            results.append({
                "record_index": index,
                "issues": issues,
            })

    return results