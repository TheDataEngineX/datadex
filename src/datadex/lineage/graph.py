"""Lineage graph — in-memory directed graph of column-level lineage."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GraphEdge:
    """An edge in the lineage graph."""

    source: str
    target: str
    column: str


class LineageGraph:
    """Directed graph for column-level data lineage."""

    def __init__(self) -> None:
        self._edges: list[GraphEdge] = []
        self._forward: dict[str, list[str]] = {}
        self._backward: dict[str, list[str]] = {}

    def add_edge(self, source: str, target: str, column: str) -> None:
        """Add a directed lineage edge."""
        self._edges.append(GraphEdge(source=source, target=target, column=column))

        src_key = f"{source}.{column}"
        tgt_key = f"{target}.{column}"

        self._forward.setdefault(src_key, []).append(tgt_key)
        self._backward.setdefault(tgt_key, []).append(src_key)

    def get_downstream(self, column: str) -> list[str]:
        """Get all downstream dependents of a column (format: 'table.column')."""
        return list(self._forward.get(column, []))

    def get_upstream(self, column: str) -> list[str]:
        """Get all upstream sources of a column (format: 'table.column')."""
        return list(self._backward.get(column, []))

    @property
    def edges(self) -> list[GraphEdge]:
        """Return all edges in the graph."""
        return list(self._edges)

    @property
    def nodes(self) -> set[str]:
        """Return all unique node keys (table.column)."""
        result: set[str] = set()
        for edge in self._edges:
            result.add(f"{edge.source}.{edge.column}")
            result.add(f"{edge.target}.{edge.column}")
        return result
