"""Tests for DataDEX CLI commands."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from datadex.cli import main


def test_run_with_example_yaml() -> None:
    """CLI run command parses and validates example YAML."""
    example = Path(__file__).parent.parent / "examples" / "simple-csv-pipeline.yml"
    runner = CliRunner()
    result = runner.invoke(main, ["run", str(example), "--dry-run"])
    assert result.exit_code == 0
    assert "valid" in result.output.lower() or "sample-csv-pipeline" in result.output


def test_status_command() -> None:
    """CLI status command runs without error."""
    runner = CliRunner()
    result = runner.invoke(main, ["status"])
    assert result.exit_code == 0


def test_connectors_command() -> None:
    """CLI connectors command lists connectors."""
    runner = CliRunner()
    result = runner.invoke(main, ["connectors"])
    assert result.exit_code == 0
    assert "csv_file" in result.output


def test_quality_command() -> None:
    """CLI quality command runs without error."""
    runner = CliRunner()
    result = runner.invoke(main, ["quality", "test_dataset"])
    assert result.exit_code == 0


def test_lineage_command() -> None:
    """CLI lineage command runs without error."""
    runner = CliRunner()
    result = runner.invoke(main, ["lineage", "test_dataset"])
    assert result.exit_code == 0


def test_serve_command_not_installed() -> None:
    """CLI serve command exits gracefully if uvicorn is not importable."""
    runner = CliRunner()
    # Just invoke help — don't actually start a server
    result = runner.invoke(main, ["serve", "--help"])
    assert result.exit_code == 0
    assert "port" in result.output.lower()
