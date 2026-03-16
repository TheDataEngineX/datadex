"""DataDEX CLI — config-driven data pipelines from the command line."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option(package_name="datadex")
def main() -> None:
    """DataDEX — universal data pipeline engine."""


@main.command()
@click.argument("pipeline_path", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Validate without executing")
def run(pipeline_path: str, dry_run: bool) -> None:
    """Execute a data pipeline from a YAML config."""
    from datadex.config.loader import load_pipeline

    config = load_pipeline(pipeline_path)
    if dry_run:
        console.print(f"[green]✓[/green] Pipeline '{config.name}' is valid")
        return

    console.print(f"Running pipeline: [bold]{config.name}[/bold]")
    raise NotImplementedError("Pipeline execution not yet implemented — engine not connected")


@main.command()
@click.option("--pipeline", default=None, help="Filter by pipeline name")
def status(pipeline: str | None) -> None:
    """Show recent pipeline run status."""
    table = Table(title="Pipeline Runs")
    table.add_column("Pipeline", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Duration")
    table.add_column("Last Run")
    table.add_row("(no runs yet)", "-", "-", "-")
    console.print(table)


@main.command()
def connectors() -> None:
    """List available data connectors."""
    table = Table(title="Available Connectors")
    table.add_column("Name", style="cyan")
    table.add_column("Type")
    table.add_column("Status")
    for name, kind in [
        ("csv_file", "Source/Sink"),
        ("postgres", "Source/Sink"),
        ("mysql", "Source/Sink"),
        ("s3", "Source/Sink"),
        ("rest_api", "Source"),
        ("kafka", "Source/Sink"),
    ]:
        table.add_row(name, kind, "[green]available[/green]")
    console.print(table)


@main.command()
@click.argument("dataset")
def quality(dataset: str) -> None:
    """Show quality scorecard for a dataset."""
    console.print(f"Quality scorecard for: [bold]{dataset}[/bold]")
    raise NotImplementedError("Quality framework not yet connected")


@main.command()
@click.argument("dataset")
def lineage(dataset: str) -> None:
    """Show lineage graph for a dataset."""
    console.print(f"Lineage for: [bold]{dataset}[/bold]")
    raise NotImplementedError("Lineage graph rendering not yet implemented")


@main.command()
@click.option("--port", default=8001, help="Port to serve on")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
def serve(port: int, host: str) -> None:
    """Start the DataDEX API server."""
    import uvicorn

    console.print(f"Starting DataDEX API on {host}:{port}")
    uvicorn.run("datadex.api.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
