# DataDEX

[![CI](https://github.com/TheDataEngineX/datadex/actions/workflows/ci.yml/badge.svg)](https://github.com/TheDataEngineX/datadex/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Universal data pipeline engine** — define ingestion, transformation, quality, and lineage in YAML. Run anywhere.

Built on [dataenginex](https://github.com/TheDataEngineX/dataenginex).

---

## Quick Start

```bash
pip install datadex
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
datadex serve --port 8001            # Start DataDEX API server
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
uv sync
uv run poe test
```

---

**Part of [TheDataEngineX](https://github.com/TheDataEngineX) ecosystem** | **License**: MIT
