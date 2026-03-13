"""Filter transform — filter rows by condition."""

from __future__ import annotations

from typing import Any

from datadex.transforms.base import BaseTransform


class FilterTransform(BaseTransform):
    """Filter rows by a condition expression (stub)."""

    def __init__(self, condition: str) -> None:
        self._condition = condition

    @property
    def name(self) -> str:
        return "filter"

    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError("Filter expression evaluation not yet implemented")
