"""Abstract base class for all DataDEX connectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """Base class for data connectors (sources and sinks)."""

    name: str = "base"

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source/sink."""

    @abstractmethod
    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Read data from the source."""

    @abstractmethod
    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        """Write data to the sink. Returns number of records written."""

    def close(self) -> None:
        """Close the connection."""

    def health_check(self) -> bool:
        """Check if the connector is healthy."""
        return True
