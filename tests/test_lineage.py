"""Tests for DataDEX lineage tracking."""

from __future__ import annotations

import json

from datadex.lineage.export import export_json
from datadex.lineage.graph import LineageGraph
from datadex.lineage.tracker import LineageTracker


class TestLineageTracker:
    """Tests for LineageTracker."""

    def test_track_adds_edges(self) -> None:
        tracker = LineageTracker()
        tracker.track("source_a", "sink_b", {"col1": "col1"})
        tracker.track("source_b", "sink_c")

        assert len(tracker.edges) == 2
        assert tracker.edges[0].source == "source_a"
        assert tracker.edges[0].destination == "sink_b"
        assert tracker.edges[0].columns_mapping == {"col1": "col1"}

    def test_track_empty(self) -> None:
        tracker = LineageTracker()
        assert tracker.edges == []


class TestLineageGraph:
    """Tests for LineageGraph."""

    def test_add_edge(self) -> None:
        graph = LineageGraph()
        graph.add_edge("orders", "order_summary", "amount")

        assert len(graph.edges) == 1
        assert graph.edges[0].source == "orders"
        assert graph.edges[0].target == "order_summary"

    def test_get_downstream(self) -> None:
        graph = LineageGraph()
        graph.add_edge("raw", "clean", "id")

        downstream = graph.get_downstream("raw.id")
        assert downstream == ["clean.id"]

    def test_get_upstream(self) -> None:
        graph = LineageGraph()
        graph.add_edge("raw", "clean", "id")

        upstream = graph.get_upstream("clean.id")
        assert upstream == ["raw.id"]

    def test_no_upstream(self) -> None:
        graph = LineageGraph()
        assert graph.get_upstream("nothing.col") == []

    def test_no_downstream(self) -> None:
        graph = LineageGraph()
        assert graph.get_downstream("nothing.col") == []

    def test_nodes(self) -> None:
        graph = LineageGraph()
        graph.add_edge("a", "b", "x")
        assert graph.nodes == {"a.x", "b.x"}


class TestLineageExport:
    """Tests for lineage export."""

    def test_export_json_valid(self) -> None:
        graph = LineageGraph()
        graph.add_edge("src", "tgt", "col")

        result = export_json(graph)
        parsed = json.loads(result)

        assert "edges" in parsed
        assert "nodes" in parsed
        assert len(parsed["edges"]) == 1
        assert parsed["edges"][0]["source"] == "src"
        assert parsed["edges"][0]["target"] == "tgt"

    def test_export_json_empty_graph(self) -> None:
        graph = LineageGraph()
        result = export_json(graph)
        parsed = json.loads(result)
        assert parsed["edges"] == []
        assert parsed["nodes"] == []
