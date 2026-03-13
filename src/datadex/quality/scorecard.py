"""Quality scorecard — aggregate quality metrics for a dataset."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from datadex.config.loader import QualityConfig
from datadex.quality.checks import check_completeness, check_uniqueness


@dataclass
class ScorecardResult:
    """Aggregated quality scores for a dataset."""

    dataset_name: str
    completeness: float
    uniqueness: float
    freshness_ok: bool
    overall_score: float
    timestamp: str


class QualityScorecard:
    """Evaluate data quality and produce a scorecard."""

    def evaluate(
        self,
        data: list[dict[str, Any]],
        config: QualityConfig,
        dataset_name: str = "unknown",
    ) -> ScorecardResult:
        """Run quality checks and return a scorecard."""
        all_columns = list(data[0].keys()) if data else []

        completeness = check_completeness(data, all_columns)
        uniqueness = check_uniqueness(data, config.unique_columns) if config.unique_columns else 1.0
        overall = (completeness + uniqueness) / 2

        return ScorecardResult(
            dataset_name=dataset_name,
            completeness=completeness,
            uniqueness=uniqueness,
            freshness_ok=True,  # stub: freshness not yet implemented
            overall_score=overall,
            timestamp=datetime.now(tz=UTC).isoformat(),
        )
