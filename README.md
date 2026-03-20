# DataDEX

[![CI](https://github.com/TheDataEngineX/datadex/actions/workflows/ci.yml/badge.svg)](https://github.com/TheDataEngineX/datadex/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/TheDataEngineX/datadex)](https://github.com/TheDataEngineX/datadex/releases)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Universal data pipeline engine** — define ingestion, transformation, quality, and lineage in YAML. Run anywhere.

Built on [dataenginex](https://github.com/TheDataEngineX/dataenginex).

______________________________________________________________________

## Quick Start

```bash
# Install
uv add datadex               # core
uv add datadex[api]          # + FastAPI server

# Install a connector
uv add datadex[postgres]     # PostgreSQL
uv add datadex[kafka]        # Kafka
uv add datadex[s3]           # AWS S3

# Run from source
git clone https://github.com/TheDataEngineX/datadex && cd datadex
uv sync --extra api
datadex run examples/simple-csv-pipeline.yml
```

## CLI

```bash
datadex run pipeline.yml             # Execute a pipeline
datadex run pipeline.yml --dry-run   # Validate without executing
datadex status                       # Show recent pipeline runs
datadex status --pipeline orders     # Status of specific pipeline
datadex connectors                   # List available connectors
datadex quality my-dataset           # Show quality scorecard
datadex lineage my-dataset           # Show lineage graph (terminal)
datadex serve --port 17001            # Start DataDEX API server
```

## Example Pipeline

```yaml
# my-pipeline.yml
pipeline:
  name: ecommerce-orders
  schedule: "@hourly"
  source:
    type: postgres
    connection: $DB_URL
    table: orders
    mode: incremental
    watermark_column: updated_at
  transforms:
    - deduplicate: [order_id]
    - cast: {amount: float, created_at: timestamp}
    - derive:
        total_with_tax: "amount * 1.08"
  quality:
    min_completeness: 0.95
    min_freshness: "2 hours"
    unique_columns: [order_id]
  destination:
    type: parquet
    layer: silver
    partition_by: [region, date]
```

## Features

| Feature | Description |
|---|---|
| **Declarative YAML pipelines** | Define pipelines in config, not code |
| **Connectors** | PostgreSQL, MySQL, S3, REST API, CSV, Kafka |
| **Incremental extraction** | Watermark-based CDC — only process what changed |
| **Transforms** | Deduplicate, cast, derive, filter, join |
| **Quality scorecards** | Completeness, freshness, uniqueness per dataset |
| **Column-level lineage** | Track every field from source to destination |
| **API server** | Optional FastAPI for pipeline management |

## Development

```bash
git clone https://github.com/TheDataEngineX/datadex && cd datadex
uv sync --extra api

uv run ruff check src/ tests/          # lint
uv run ruff format --check src/ tests/ # format check
uv run mypy src/datadex/ --strict      # typecheck
uv run pytest tests/ -x --tb=short -q # test
```

______________________________________________________________________

**Part of [TheDataEngineX](https://github.com/TheDataEngineX) ecosystem** | **License**: MIT
