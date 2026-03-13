"""Tests for DataDEX transforms."""

from __future__ import annotations

import pytest

from datadex.transforms.cast import CastTransform
from datadex.transforms.deduplicate import DeduplicateTransform
from datadex.transforms.derive import DeriveTransform


class TestDeduplicateTransform:
    """Tests for DeduplicateTransform."""

    def test_removes_exact_duplicates(self) -> None:
        data = [
            {"id": "1", "name": "a"},
            {"id": "1", "name": "a"},
            {"id": "2", "name": "b"},
        ]
        t = DeduplicateTransform(columns=["id"])
        result = t.apply(data)
        assert len(result) == 2
        assert result[0]["id"] == "1"
        assert result[1]["id"] == "2"

    def test_preserves_first_occurrence(self) -> None:
        data = [
            {"id": "1", "name": "first"},
            {"id": "1", "name": "second"},
        ]
        t = DeduplicateTransform(columns=["id"])
        result = t.apply(data)
        assert len(result) == 1
        assert result[0]["name"] == "first"

    def test_multi_column_dedup(self) -> None:
        data = [
            {"a": "1", "b": "x"},
            {"a": "1", "b": "y"},
            {"a": "1", "b": "x"},
        ]
        t = DeduplicateTransform(columns=["a", "b"])
        result = t.apply(data)
        assert len(result) == 2

    def test_empty_data(self) -> None:
        t = DeduplicateTransform(columns=["id"])
        assert t.apply([]) == []

    def test_name_property(self) -> None:
        t = DeduplicateTransform(columns=["id"])
        assert t.name == "deduplicate"


class TestCastTransform:
    """Tests for CastTransform."""

    def test_cast_int(self) -> None:
        data = [{"val": "42"}]
        t = CastTransform(column_types={"val": "int"})
        result = t.apply(data)
        assert result[0]["val"] == 42

    def test_cast_float(self) -> None:
        data = [{"price": "9.99"}]
        t = CastTransform(column_types={"price": "float"})
        result = t.apply(data)
        assert result[0]["price"] == 9.99

    def test_cast_str(self) -> None:
        data = [{"code": 123}]
        t = CastTransform(column_types={"code": "str"})
        result = t.apply(data)
        assert result[0]["code"] == "123"

    def test_cast_bool(self) -> None:
        data = [{"flag": 1}]
        t = CastTransform(column_types={"flag": "bool"})
        result = t.apply(data)
        assert result[0]["flag"] is True

    def test_unsupported_type_raises(self) -> None:
        data = [{"x": "1"}]
        t = CastTransform(column_types={"x": "datetime"})
        with pytest.raises(ValueError, match="Unsupported cast type"):
            t.apply(data)

    def test_missing_column_ignored(self) -> None:
        data = [{"a": "1"}]
        t = CastTransform(column_types={"missing": "int"})
        result = t.apply(data)
        assert result == [{"a": "1"}]

    def test_name_property(self) -> None:
        t = CastTransform(column_types={})
        assert t.name == "cast"


class TestDeriveTransform:
    """Tests for DeriveTransform stub."""

    def test_raises_not_implemented(self) -> None:
        t = DeriveTransform(expressions={"new_col": "col_a + col_b"})
        with pytest.raises(NotImplementedError, match="Expression evaluation"):
            t.apply([{"col_a": 1, "col_b": 2}])
