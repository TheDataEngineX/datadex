"""Join transform — join two datasets."""

from __future__ import annotations

from typing import Any

from datadex.transforms.base import BaseTransform


class JoinTransform(BaseTransform):
    """Join with another dataset (stub)."""

    def __init__(
        self,
        right_dataset: list[dict[str, Any]],
        on: str,
        how: str = "inner",
    ) -> None:
        self._right_dataset = right_dataset
        self._on = on
        self._how = how

    @property
    def name(self) -> str:
        return "join"

    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError("Join transform not yet implemented")
