"""Abstract base class for data transforms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTransform(ABC):
    """Base class for all data transforms."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this transform."""

    @abstractmethod
    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Apply transform to data and return the result."""
