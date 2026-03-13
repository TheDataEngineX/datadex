"""Quality check functions — completeness, uniqueness, freshness."""

from __future__ import annotations

from datetime import timedelta
from typing import Any


def check_completeness(data: list[dict[str, Any]], columns: list[str]) -> float:
    """Return ratio of non-null values across the specified columns.

    Returns 1.0 for fully complete data, 0.0 for all nulls.
    Returns 1.0 when data or columns are empty.
    """
    if not data or not columns:
        return 1.0

    total = len(data) * len(columns)
    filled = sum(
        1 for row in data for col in columns if row.get(col) is not None and row.get(col) != ""
    )
    return filled / total


def check_uniqueness(data: list[dict[str, Any]], columns: list[str]) -> float:
    """Return ratio of unique value-tuples across the specified columns.

    Returns 1.0 when every row is unique on those columns, 0.0 when all identical.
    Returns 1.0 when data or columns are empty.
    """
    if not data or not columns:
        return 1.0

    keys = [tuple(row.get(c) for c in columns) for row in data]
    return len(set(keys)) / len(keys)


def check_freshness(
    data: list[dict[str, Any]],
    timestamp_column: str,
    max_age: timedelta,
) -> bool:
    """Check whether the most recent timestamp is within max_age (stub)."""
    raise NotImplementedError("Freshness check not yet implemented")
