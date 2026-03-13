"""Lineage export — serialize lineage graphs."""

from __future__ import annotations

import json
from dataclasses import asdict

from datadex.lineage.graph import LineageGraph


def export_json(graph: LineageGraph) -> str:
    """Serialize the lineage graph edges to a JSON string."""
    return json.dumps(
        {"edges": [asdict(e) for e in graph.edges], "nodes": sorted(graph.nodes)},
        indent=2,
    )


def export_openlineage(graph: LineageGraph) -> dict[str, object]:
    """Export lineage in OpenLineage format (stub)."""
    raise NotImplementedError("OpenLineage export not yet implemented")
