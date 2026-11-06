import csv
from pathlib import Path
from typing import Any


def load_csv(file_path: str | Path) -> list[dict[str, Any]]:
    """Load a CSV file and return its rows as dictionaries."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    with path.open(
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header.")

        if any(not name.strip() for name in reader.fieldnames):
            raise ValueError("CSV contains an empty column name.")

        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV contains duplicate column names.")

        return list(reader)
