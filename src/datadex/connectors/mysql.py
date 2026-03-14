"""MySQL connector stub — requires pymysql."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_MSG = "MySQL connector requires pymysql: pip install datadex[mysql]"


class MySQLConnector(BaseConnector):
    """MySQL data connector (stub)."""

    name: str = "mysql"

    def connect(self) -> None:
        raise NotImplementedError(_MSG)

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError(_MSG)

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        raise NotImplementedError(_MSG)

    def close(self) -> None:
        raise NotImplementedError(_MSG)
