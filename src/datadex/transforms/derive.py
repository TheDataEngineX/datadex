"""Derive transform — create new columns from expressions."""

from __future__ import annotations

from typing import Any

from datadex.transforms.base import BaseTransform


class DeriveTransform(BaseTransform):
    """Derive new columns from expressions (stub)."""

    def __init__(self, expressions: dict[str, str]) -> None:
        self._expressions = expressions

    @property
    def name(self) -> str:
        return "derive"

    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError("Expression evaluation not yet implemented")
