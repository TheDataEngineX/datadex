"""Cast transform — cast column values to specified types."""

from __future__ import annotations

from typing import Any

from datadex.transforms.base import BaseTransform

_CASTERS: dict[str, type] = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
}


class CastTransform(BaseTransform):
    """Cast columns to specified types (int, float, str, bool)."""

    def __init__(self, column_types: dict[str, str]) -> None:
        self._column_types = column_types

    @property
    def name(self) -> str:
        return "cast"

    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Cast each specified column to its target type."""
        result: list[dict[str, Any]] = []
        for row in data:
            new_row = dict(row)
            for col, type_name in self._column_types.items():
                if col in new_row:
                    caster = _CASTERS.get(type_name)
                    if caster is None:
                        msg = f"Unsupported cast type: {type_name}"
                        raise ValueError(msg)
                    new_row[col] = caster(new_row[col])
            result.append(new_row)
        return result
