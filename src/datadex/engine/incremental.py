"""Incremental extraction — watermark-based change tracking."""

from __future__ import annotations

from typing import Any


class WatermarkTracker:
    """Track extraction watermarks per pipeline (in-memory)."""

    def __init__(self) -> None:
        self._watermarks: dict[str, Any] = {}

    def get_watermark(self, pipeline_name: str) -> Any | None:
        """Return the current watermark value, or None if unset."""
        return self._watermarks.get(pipeline_name)

    def update_watermark(self, pipeline_name: str, value: Any) -> None:
        """Store a new watermark value for the given pipeline."""
        self._watermarks[pipeline_name] = value
