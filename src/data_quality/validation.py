
import math
import re
from typing import Any


def validate_required_fields(
    records: list[dict[str, Any]],
    required_fields: list[str],
) -> list[dict[str, Any]]:
    """
    Check that all required fields are present and non-empty.

    A field is considered missing if:
    - The key does not exist.
    - Its value is None.
    - Its value is an empty or whitespace-only string.

    Returns a list of validation issues.
    """

    issues = []

    for row_number, record in enumerate(records, start=1):

        for field in required_fields:

            value = record.get(field)

            if (
                field not in record
                or value is None
                or (isinstance(value, str) and not value.strip())
            ):
                issues.append({
                    "row": row_number,
                    "field": field,
                    "error": "missing_required_field",
                    "message": f"Required field '{field}' is missing or empty.",
                })

    return issues


EMAIL_PATTERN = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def validate_email_format(
    records: list[dict[str, Any]],
    email_fields: list[str],
) -> list[dict[str, Any]]:
    """
    Validate the format of email addresses.

    Missing or empty values are ignored because they are
    handled separately by validate_required_fields().
    """

    issues = []

    for row_number, record in enumerate(records, start=1):
        for field in email_fields:
            value = record.get(field)

            # Missing values are handled by required-field validation.
            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                continue

            if not isinstance(value, str) or not EMAIL_PATTERN.fullmatch(value):
                issues.append({
                    "row": row_number,
                    "field": field,
                    "error": "invalid_email",
                    "message": f"Field '{field}' contains an invalid email address.",
                })

    return issues

def validate_numeric_range(
    value: float,
    field: str,
    min_value: float | None = None,
    max_value: float | None = None,
    line: int | None = None,
) -> str | None:
    """Validate that a numeric value is within the allowed range."""

    location = f"Line {line}, field '{field}'" if line else f"Field '{field}'"

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return f"{location}: value '{value}' is not numeric."

    if not math.isfinite(value):
        return f"{location}: value '{value}' is not finite."

    if min_value is not None and value < min_value:
        return (
            f"{location}: value '{value}' is below "
            f"the minimum allowed value ({min_value})."
        )

    if max_value is not None and value > max_value:
        return (
            f"{location}: value '{value}' exceeds "
            f"the maximum allowed value ({max_value})."
        )

    return None