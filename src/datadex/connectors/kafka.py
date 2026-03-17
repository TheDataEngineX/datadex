"""Kafka connector — requires ``datadex[kafka]`` (confluent-kafka)."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_INSTALL_MSG = "Kafka connector requires confluent-kafka: pip install datadex[kafka]"


class KafkaConnector(BaseConnector):
    """Produce and consume messages from Apache Kafka.

    In *consumer mode* (``topics`` provided): ``read()`` polls messages from
    the subscribed topics and returns them as dicts with ``topic``, ``partition``,
    ``offset``, ``key``, and ``value`` fields.

    In *producer mode* (``topic`` provided): ``write()`` produces messages to
    the configured topic.

    Parameters
    ----------
    bootstrap_servers:
        Comma-separated ``host:port`` pairs (e.g. ``"localhost:9092"``).
    topic:
        Default topic for producing messages.
    topics:
        List of topics to subscribe to for consuming messages.
    group_id:
        Consumer group ID (required for consuming).
    extra_config:
        Additional confluent-kafka config key-value pairs.
    """

    name: str = "kafka"

    def __init__(
        self,
        bootstrap_servers: str,
        *,
        topic: str = "",
        topics: list[str] | None = None,
        group_id: str = "datadex-consumer",
        extra_config: dict[str, str] | None = None,
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._topics = topics or []
        self._group_id = group_id
        self._extra_config = extra_config or {}
        self._producer: Any = None
        self._consumer: Any = None

    def connect(self) -> None:
        """Initialise producer and/or consumer clients."""
        try:
            from confluent_kafka import Consumer, Producer  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(_INSTALL_MSG) from exc

        base_cfg = {"bootstrap.servers": self._bootstrap_servers, **self._extra_config}

        if self._topic:
            self._producer = Producer(base_cfg)

        if self._topics:
            consumer_cfg = {**base_cfg, "group.id": self._group_id, "auto.offset.reset": "earliest"}
            self._consumer = Consumer(consumer_cfg)
            self._consumer.subscribe(self._topics)

    def read(
        self,
        max_messages: int = 100,
        timeout: float = 5.0,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Poll messages from subscribed topics.

        Parameters
        ----------
        max_messages:
            Maximum number of messages to return.
        timeout:
            Per-poll timeout in seconds.
        """
        if self._consumer is None:
            raise RuntimeError("No consumer — pass topics= to the constructor and call connect()")

        messages: list[dict[str, Any]] = []
        while len(messages) < max_messages:
            msg = self._consumer.poll(timeout=timeout)
            if msg is None:
                break
            if msg.error():
                break
            value = msg.value()
            messages.append(
                {
                    "topic": msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                    "key": msg.key().decode() if msg.key() else None,
                    "value": value.decode() if isinstance(value, bytes) else value,
                }
            )
        return messages

    def write(self, data: list[dict[str, Any]], topic: str = "", **kwargs: Any) -> int:
        """Produce messages to Kafka.

        Each dict in *data* must contain a ``value`` key.  An optional ``key``
        key is used as the Kafka message key.

        Parameters
        ----------
        data:
            List of message dicts, each with at least a ``value`` field.
        topic:
            Override the constructor's default topic.
        """
        if not data:
            return 0
        if self._producer is None:
            raise RuntimeError("No producer — pass topic= to the constructor and call connect()")

        target = topic or self._topic
        if not target:
            raise ValueError("Specify a target topic via the topic parameter or constructor")

        for item in data:
            value = item.get("value", "")
            key = item.get("key")
            self._producer.produce(
                topic=target,
                value=str(value).encode(),
                key=str(key).encode() if key else None,
            )

        self._producer.flush()
        return len(data)

    def close(self) -> None:
        """Flush producer and close consumer."""
        if self._producer is not None:
            self._producer.flush()
            self._producer = None
        if self._consumer is not None:
            self._consumer.close()
            self._consumer = None

    def health_check(self) -> bool:
        """Return True if at least one client is initialised."""
        return self._producer is not None or self._consumer is not None
