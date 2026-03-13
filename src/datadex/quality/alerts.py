"""Quality alerts — notify when quality drops below thresholds."""

from __future__ import annotations

from datadex.quality.scorecard import ScorecardResult


class QualityAlertManager:
    """Check quality scores against thresholds and send alerts (stub)."""

    def check_and_alert(
        self,
        scorecard_result: ScorecardResult,
        thresholds: dict[str, float],
    ) -> None:
        """Evaluate scorecard against thresholds and alert if breached."""
        raise NotImplementedError("Quality alerting not yet implemented")
