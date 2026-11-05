from typing import Any

def count_missing_values(records):
    missing_counts = {}

    # Step 1: Discover all columns
    for record in records:
        for key in record:
            if key not in missing_counts:
                missing_counts[key] = 0

    # Step 2: Count missing values
    for record in records:
        for key in missing_counts:
            if key not in record or record[key] is None:
                missing_counts[key] += 1

    return missing_counts

def analyze_columns(records: list[dict[str, Any]]) -> dict:
    """
    Analyze each column in a dataset.

    Returns statistics about missing values,
    present values, distinct values, and missing rates.
    """

    if not records:
        return {}

    # Step 1: Discover columns while preserving their order
    columns = dict.fromkeys(
        key
        for record in records
        for key in record
    )

    # Step 2: Initialize statistics
    column_stats = {}

    for column in columns:
        column_stats[column] = {
            "total": len(records),
            "present": 0,
            "missing": 0,
            "missing_rate": 0.0,
            "unique": 0,
        }

    # Step 3: Analyze values
    for column in columns:
        unique_values = set()

        for record in records:
            value = record.get(column)

            if value is None:
                column_stats[column]["missing"] += 1
            else:
                column_stats[column]["present"] += 1

                try:
                    unique_values.add(value)
                except TypeError as error:
                    raise TypeError(
                        f"Column '{column}' contains an "
                        f"unhashable value: {value!r}"
                    ) from error

        # Step 4: Calculate statistics
        stats = column_stats[column]

        stats["unique"] = len(unique_values)
        stats["missing_rate"] = (
            stats["missing"] / stats["total"]
        ) * 100

    return column_stats
