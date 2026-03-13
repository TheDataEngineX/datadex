"""CSV file connector — reads and writes local CSV files."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from datadex.connectors.base import BaseConnector


class CsvFileConnector(BaseConnector):
    """Read and write CSV files on the local filesystem."""

    name: str = "csv_file"

    def __init__(self, path: str) -> None:
        self._path = Path(path)

    def connect(self) -> None:
        """Validate the file path exists (for reads) or parent dir exists (for writes)."""
        if not self._path.parent.exists():
            msg = f"Parent directory does not exist: {self._path.parent}"
            raise FileNotFoundError(msg)

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Read CSV file and return list of dicts."""
        if not self._path.exists():
            msg = f"CSV file not found: {self._path}"
            raise FileNotFoundError(msg)

        with open(self._path, newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        """Write list of dicts to CSV file. Returns number of rows written."""
        if not data:
            return 0

        fieldnames = list(data[0].keys())
        with open(self._path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return len(data)
