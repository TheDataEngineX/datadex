"""Deduplicate transform — remove duplicate rows."""

from __future__ import annotations

import json
from typing import Any

from datadex.transforms.base import BaseTransform


class DeduplicateTransform(BaseTransform):
    """Remove duplicate rows based on specified columns."""

    def __init__(self, columns: list[str]) -> None:
        self._columns = columns

    @property
    def name(self) -> str:
        return "deduplicate"

    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove rows with duplicate values in the specified columns."""
        seen: set[str] = set()
        result: list[dict[str, Any]] = []
        for row in data:
            key = json.dumps([row.get(c) for c in self._columns], sort_keys=True)
            if key not in seen:
                seen.add(key)
                result.append(row)
        return result
