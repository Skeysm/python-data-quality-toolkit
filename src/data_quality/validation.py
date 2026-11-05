
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
