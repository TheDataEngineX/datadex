"""PostgreSQL connector stub — requires psycopg."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_MSG = "PostgreSQL connector requires psycopg: pip install datadex[postgres]"


class PostgresConnector(BaseConnector):
    """PostgreSQL data connector (stub)."""

    name: str = "postgres"

    def connect(self) -> None:
        raise NotImplementedError(_MSG)

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError(_MSG)

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        raise NotImplementedError(_MSG)
