"""Pipeline runner — executes pipeline configs end-to-end."""

from __future__ import annotations

from dataclasses import dataclass, field

from datadex.config.loader import PipelineConfig


@dataclass
class PipelineResult:
    """Result of a pipeline execution."""

    pipeline_name: str
    status: str  # "success" | "failed"
    records_processed: int = 0
    duration_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)


class PipelineRunner:
    """Execute a pipeline from a PipelineConfig."""

    def run(self, config: PipelineConfig) -> PipelineResult:
        """Run the full pipeline: extract → transform → quality → load."""
        raise NotImplementedError("Pipeline execution engine not yet implemented")
