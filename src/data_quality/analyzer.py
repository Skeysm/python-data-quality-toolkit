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

def analyze_columns(records):
    """
    Analyze each column in a dataset.

    Returns statistics about missing values,
    present values, distinct values, and missing rates.
    """

    if not records:
        return {}

    # Step 1: Discover all columns
    columns = set()

    for record in records:
        columns.update(record.keys())

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
                unique_values.add(value)

        # Step 4: Calculate statistics
        stats = column_stats[column]

        stats["unique"] = len(unique_values)
        stats["missing_rate"] = (
            stats["missing"] / stats["total"]
        ) * 100

    return column_stats