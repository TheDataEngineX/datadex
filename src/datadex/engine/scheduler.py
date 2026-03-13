"""Pipeline scheduler — cron-based pipeline scheduling."""

from __future__ import annotations

from datetime import datetime

from datadex.config.loader import PipelineConfig


class PipelineScheduler:
    """Schedule pipeline runs using cron expressions."""

    def schedule(self, config: PipelineConfig, cron_expression: str) -> None:
        """Register a pipeline for scheduled execution."""
        raise NotImplementedError("Pipeline scheduling not yet implemented")

    def next_run(self, pipeline_name: str) -> datetime:
        """Return the next scheduled run time for a pipeline."""
        raise NotImplementedError("Pipeline scheduling not yet implemented")
