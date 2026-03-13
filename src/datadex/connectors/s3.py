"""S3 connector stub — requires boto3."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_MSG = "S3 connector requires boto3: pip install datadex[s3]"


class S3Connector(BaseConnector):
    """Amazon S3 data connector (stub)."""

    name: str = "s3"

    def connect(self) -> None:
        raise NotImplementedError(_MSG)

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError(_MSG)

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        raise NotImplementedError(_MSG)
