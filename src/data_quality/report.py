from collections import Counter
from typing import Any

from data_quality.engine import Validator, validate_records


def generate_quality_report(
    records: list[dict[str, Any]],
    rules: dict[str, list[Validator]],
) -> dict[str, Any]:
    """Generate a quality report for a dataset."""

    validation_results = validate_records(records, rules)

    total_records = len(records)
    invalid_records = len(validation_results)
    valid_records = total_records - invalid_records

    total_issues = sum(
        len(result["issues"])
        for result in validation_results
    )

    error_counts = Counter(
        issue["field"]
        for result in validation_results
        for issue in result["issues"]
    )

    validity_rate = (
        (valid_records / total_records) * 100
        if total_records > 0
        else 0.0
    )

    return {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "total_issues": total_issues,
        "validity_rate": round(validity_rate, 2),
        "errors_by_field": dict(error_counts),
        "details": validation_results,
    }