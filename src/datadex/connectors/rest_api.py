"""REST API connector — read-only HTTP data source."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector


class RestAPIConnector(BaseConnector):
    """REST API data connector (read-only source)."""

    name: str = "rest_api"

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def connect(self) -> None:
        """No-op — REST is stateless."""

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError("REST API read not yet implemented")

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        raise NotImplementedError("REST API connector is read-only")

    def close(self) -> None:
        """No-op — REST is stateless."""
