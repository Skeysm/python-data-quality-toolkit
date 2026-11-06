from data_quality.report import generate_quality_report
from data_quality.validation import validate_numeric_range


def test_generate_quality_report():
    records = [
        {"age": 25},
        {"age": 15},
        {"age": 150},
        {"age": 40},
    ]

    rules = {
        "age": [
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            )
        ],
    }

    report = generate_quality_report(records, rules)

    assert report["total_records"] == 4
    assert report["valid_records"] == 2
    assert report["invalid_records"] == 2
    assert report["total_issues"] == 2
    assert report["validity_rate"] == 50.0
    assert report["errors_by_field"] == {"age": 2}


def test_report_with_all_valid_records():
    records = [
        {"age": 25},
        {"age": 40},
    ]

    rules = {
        "age": [
            lambda value: validate_numeric_range(
                value, "age", 18, 100
            )
        ],
    }

    report = generate_quality_report(records, rules)

    assert report["valid_records"] == 2
    assert report["invalid_records"] == 0
    assert report["total_issues"] == 0
    assert report["validity_rate"] == 100.0
    assert report["errors_by_field"] == {}


def test_report_with_empty_dataset():
    report = generate_quality_report([], {})

    assert report["total_records"] == 0
    assert report["valid_records"] == 0
    assert report["invalid_records"] == 0
    assert report["total_issues"] == 0
    assert report["validity_rate"] == 0.0
    assert report["errors_by_field"] == {}


def test_report_counts_errors_by_field():
    records = [
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

    report = generate_quality_report(records, rules)

    assert report["errors_by_field"]["age"] == 2