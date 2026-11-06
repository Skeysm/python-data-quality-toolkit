
import pytest

from data_quality.data_io import load_csv


def test_load_csv_returns_list_of_dictionaries(tmp_path):
    csv_file = tmp_path / "customers.csv"

    csv_file.write_text(
        "name,email,age\n"
        "Alice,alice@example.com,32\n"
        "Bob,bob@example.com,45\n",
        encoding="utf-8",
    )

    result = load_csv(csv_file)

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[1]["age"] == "45"


def test_load_csv_raises_error_when_file_does_not_exist(tmp_path):
    csv_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(csv_file)


def test_load_csv_rejects_empty_headers(tmp_path):
    csv_file = tmp_path / "invalid.csv"

    csv_file.write_text(
        "name,,age\n"
        "Alice,alice@example.com,32\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="empty column"):
        load_csv(csv_file)


def test_load_csv_rejects_duplicate_headers(tmp_path):
    csv_file = tmp_path / "duplicate.csv"

    csv_file.write_text(
        "name,email,name\n"
        "Alice,alice@example.com,32\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate"):
        load_csv(csv_file)

def test_load_csv_rejects_directory_path(tmp_path):
    with pytest.raises(ValueError, match="not a file"):
        load_csv(tmp_path)


def test_load_csv_handles_utf8_bom(tmp_path):
    csv_file = tmp_path / "bom.csv"

    csv_file.write_text(
        "name,email\n"
        "Alice,alice@example.com\n",
        encoding="utf-8-sig",
    )

    result = load_csv(csv_file)

    assert result[0]["name"] == "Alice"
    assert result[0]["email"] == "alice@example.com"