"""Lineage tracker — record source-to-destination data flow."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LineageEdge:
    """A single lineage relationship between source and destination."""

    source: str
    destination: str
    columns_mapping: dict[str, str] = field(default_factory=dict)


class LineageTracker:
    """Track data lineage edges in memory."""

    def __init__(self) -> None:
        self._edges: list[LineageEdge] = []

    def track(
        self,
        source: str,
        destination: str,
        columns_mapping: dict[str, str] | None = None,
    ) -> None:
        """Record a lineage edge from source to destination."""
        self._edges.append(
            LineageEdge(
                source=source,
                destination=destination,
                columns_mapping=columns_mapping or {},
            )
        )

    @property
    def edges(self) -> list[LineageEdge]:
        """Return all tracked lineage edges."""
        return list(self._edges)
