"""Tests for DataDEX quality checks and scorecard."""

from __future__ import annotations

from datadex.config.loader import QualityConfig
from datadex.quality.checks import check_completeness, check_uniqueness
from datadex.quality.scorecard import QualityScorecard


class TestCheckCompleteness:
    """Tests for check_completeness."""

    def test_full_data(self) -> None:
        data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        assert check_completeness(data, ["a", "b"]) == 1.0

    def test_missing_data(self) -> None:
        data = [{"a": 1, "b": None}, {"a": None, "b": 4}]
        score = check_completeness(data, ["a", "b"])
        assert score == 0.5

    def test_empty_string_counts_as_missing(self) -> None:
        data = [{"a": "", "b": "ok"}]
        score = check_completeness(data, ["a", "b"])
        assert score == 0.5

    def test_empty_data(self) -> None:
        assert check_completeness([], ["a"]) == 1.0

    def test_empty_columns(self) -> None:
        assert check_completeness([{"a": 1}], []) == 1.0


class TestCheckUniqueness:
    """Tests for check_uniqueness."""

    def test_all_unique(self) -> None:
        data = [{"id": 1}, {"id": 2}, {"id": 3}]
        assert check_uniqueness(data, ["id"]) == 1.0

    def test_some_duplicates(self) -> None:
        data = [{"id": 1}, {"id": 1}, {"id": 2}]
        score = check_uniqueness(data, ["id"])
        assert abs(score - 2 / 3) < 0.01

    def test_all_same(self) -> None:
        data = [{"id": 1}, {"id": 1}]
        assert check_uniqueness(data, ["id"]) == 0.5

    def test_empty_data(self) -> None:
        assert check_uniqueness([], ["id"]) == 1.0


class TestQualityScorecard:
    """Tests for QualityScorecard."""

    def test_evaluate_full_data(self) -> None:
        data = [
            {"id": 1, "name": "a"},
            {"id": 2, "name": "b"},
        ]
        config = QualityConfig(unique_columns=["id"])
        scorecard = QualityScorecard()
        result = scorecard.evaluate(data, config, dataset_name="test")

        assert result.dataset_name == "test"
        assert result.completeness == 1.0
        assert result.uniqueness == 1.0
        assert result.overall_score == 1.0
        assert result.freshness_ok is True
        assert result.timestamp  # non-empty

    def test_evaluate_with_nulls(self) -> None:
        data = [
            {"id": 1, "name": None},
            {"id": 2, "name": "b"},
        ]
        config = QualityConfig(unique_columns=["id"])
        scorecard = QualityScorecard()
        result = scorecard.evaluate(data, config, dataset_name="partial")

        assert result.completeness < 1.0
        assert result.uniqueness == 1.0

    def test_evaluate_no_unique_columns(self) -> None:
        data = [{"a": 1}]
        config = QualityConfig()
        scorecard = QualityScorecard()
        result = scorecard.evaluate(data, config)

        assert result.uniqueness == 1.0
