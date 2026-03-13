"""Tests for DataDEX connectors."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from datadex.connectors.csv_file import CsvFileConnector
from datadex.connectors.postgres import PostgresConnector
from datadex.connectors.s3 import S3Connector


class TestCsvFileConnector:
    """Tests for CsvFileConnector."""

    def test_read_csv(self, tmp_path: Path) -> None:
        """Read a CSV file and return list of dicts."""
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("id,name,value\n1,alpha,10\n2,beta,20\n")

        conn = CsvFileConnector(str(csv_path))
        conn.connect()
        data = conn.read()

        assert len(data) == 2
        assert data[0]["id"] == "1"
        assert data[0]["name"] == "alpha"

    def test_write_csv(self, tmp_path: Path) -> None:
        """Write list of dicts to a CSV file."""
        csv_path = tmp_path / "output.csv"
        conn = CsvFileConnector(str(csv_path))
        conn.connect()

        data = [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}]
        count = conn.write(data)

        assert count == 2
        assert csv_path.exists()

        # Verify written content
        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["name"] == "a"

    def test_write_empty(self, tmp_path: Path) -> None:
        """Write empty data returns 0."""
        csv_path = tmp_path / "empty.csv"
        conn = CsvFileConnector(str(csv_path))
        assert conn.write([]) == 0

    def test_read_missing_file(self, tmp_path: Path) -> None:
        """Read raises FileNotFoundError for missing files."""
        conn = CsvFileConnector(str(tmp_path / "nope.csv"))
        with pytest.raises(FileNotFoundError):
            conn.read()

    def test_connect_validates_parent(self) -> None:
        """Connect raises FileNotFoundError if parent dir missing."""
        conn = CsvFileConnector("/no/such/dir/file.csv")
        with pytest.raises(FileNotFoundError):
            conn.connect()

    def test_round_trip(self, tmp_path: Path) -> None:
        """Write then read produces the same data."""
        csv_path = tmp_path / "roundtrip.csv"
        conn = CsvFileConnector(str(csv_path))
        conn.connect()

        original = [{"x": "1", "y": "hello"}, {"x": "2", "y": "world"}]
        conn.write(original)

        result = conn.read()
        assert result == original


class TestPostgresConnector:
    """Tests for PostgresConnector stub."""

    def test_connect_raises(self) -> None:
        conn = PostgresConnector()
        with pytest.raises(NotImplementedError, match="psycopg"):
            conn.connect()

    def test_read_raises(self) -> None:
        conn = PostgresConnector()
        with pytest.raises(NotImplementedError, match="psycopg"):
            conn.read()

    def test_write_raises(self) -> None:
        conn = PostgresConnector()
        with pytest.raises(NotImplementedError, match="psycopg"):
            conn.write([])


class TestS3Connector:
    """Tests for S3Connector stub."""

    def test_connect_raises(self) -> None:
        conn = S3Connector()
        with pytest.raises(NotImplementedError, match="boto3"):
            conn.connect()

    def test_read_raises(self) -> None:
        conn = S3Connector()
        with pytest.raises(NotImplementedError, match="boto3"):
            conn.read()

    def test_write_raises(self) -> None:
        conn = S3Connector()
        with pytest.raises(NotImplementedError, match="boto3"):
            conn.write([])
