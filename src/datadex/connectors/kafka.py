"""Kafka connector stub — requires confluent-kafka."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_MSG = "Kafka connector requires confluent-kafka: pip install datadex[kafka]"


class KafkaConnector(BaseConnector):
    """Apache Kafka data connector (stub)."""

    name: str = "kafka"

    def connect(self) -> None:
        raise NotImplementedError(_MSG)

    def read(self, **kwargs: Any) -> list[dict[str, Any]]:
        raise NotImplementedError(_MSG)

    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int:
        raise NotImplementedError(_MSG)

    def close(self) -> None:
        raise NotImplementedError(_MSG)
