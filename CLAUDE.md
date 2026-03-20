# CLAUDE.md — DataDEX

Always Be pragmatic, straight forward and challenge my ideas and system design focus on creating a consistent, scalable, and accessible user experience while improving development efficiency. Always refer to up to date resources as of today. Question my assumptions, point out the blank/blind spots and highlight opportunity costs. No sugarcoating. No pandering. No bias. No both siding. No retro active reasoning. If there is something wrong or will not work let me know even if I don't ask it specifically. If it is an issue/bug/problem find the root problem and suggest a solution refering to latest day resources — don't skip, bypass, supress or don't fallback to a defense mode.

> Repo-specific context. Workspace-level rules, coding standards, and git conventions are in `../CLAUDE.md`.

## Project Overview

**DataDEX** — Config-driven data pipeline engine. Define ingestion, transformation, quality checks, and lineage in YAML; DataDEX executes them.

**Stack:** Python 3.13+ · FastAPI (optional `api` extra) · uv · Ruff · mypy strict · pytest · Port 17001

**Version:** `uv run poe version` | **Depends on:** dataenginex (see `pyproject.toml`)

______________________________________________________________________

## Build & Run Commands

```bash
# Install
uv run poe setup             # install core + api extras
uv run poe install           # install core only

# Quality
uv run poe lint              # ruff check
uv run poe lint-fix          # ruff check --fix + format
uv run poe typecheck         # mypy --strict (src/datadex/ only)
uv run poe check-all         # lint + typecheck + test

# Test
uv run poe test              # all tests
uv run poe test-unit         # unit tests only
uv run poe test-cov          # tests with coverage (HTML + XML + terminal)

# Run
uv run poe dev               # API server on port 17001 (DEX must be on 17000)
uv run datadex run pipeline.yaml  # execute a pipeline directly

# Deps
uv run poe uv-sync           # install from lockfile
uv run poe uv-lock           # regenerate lockfile
uv run poe security          # pip-audit vulnerability scan
uv run poe clean             # remove caches and build artifacts
```

______________________________________________________________________

## Architecture

DataDEX follows a **YAML-defined pipeline** model: config → parse → validate → execute (extract → transform → quality → load).

```text
src/datadex/
├── api/                  # FastAPI app (optional extra)
│   ├── main.py           # App factory, lifespan
│   └── routers/          # pipelines, quality, runs endpoints
├── cli.py                # datadex CLI (Click)
├── config/               # YAML pipeline config loader + defaults
│   ├── loader.py         # PipelineConfig Pydantic model
│   └── defaults.py       # Default config values
├── connectors/           # Data sources and sinks (BaseConnector ABC)
│   ├── base.py           # BaseConnector: connect/read/write/close
│   ├── csv_file.py       # CSV file connector
│   ├── postgres.py       # PostgreSQL connector
│   ├── mysql.py          # MySQL connector
│   ├── s3.py             # S3-compatible object storage
│   ├── rest_api.py       # REST API connector
│   └── kafka.py          # Kafka connector
├── engine/               # Pipeline execution engine
│   ├── runner.py         # PipelineRunner: extract→transform→quality→load
│   ├── parallel.py       # Parallel step execution
│   ├── incremental.py    # Incremental/CDC pipeline support
│   └── scheduler.py      # Cron-based pipeline scheduling
├── transforms/           # Data transformation steps
│   ├── base.py           # BaseTransform ABC
│   ├── cast.py           # Type casting
│   ├── filter.py         # Row filtering
│   ├── deduplicate.py    # Deduplication
│   ├── derive.py         # Derived columns
│   └── join.py           # Join operations
├── quality/              # Data quality framework
│   ├── checks.py         # Null/range/regex/uniqueness checks
│   ├── scorecard.py      # Quality scorecard aggregation
│   └── alerts.py         # Quality alert routing
├── lineage/              # Column-level data lineage
│   ├── tracker.py        # LineageTracker
│   ├── graph.py          # DAG graph representation
│   └── export.py         # OpenLineage / JSON export
└── plugin.py             # DataDEXPlugin (dataenginex plugin system)
```

______________________________________________________________________

## Key Patterns

### Adding a New Connector

Subclass `BaseConnector` in `connectors/`:

```python
from datadex.connectors.base import BaseConnector

class MyConnector(BaseConnector):
    name = "my_connector"

    def connect(self) -> None: ...
    def read(self, **kwargs: Any) -> list[dict[str, Any]]: ...
    def write(self, data: list[dict[str, Any]], **kwargs: Any) -> int: ...
    def close(self) -> None: ...
```

Register in `connectors/__init__.py` and add YAML schema to `config/loader.py`.

### Adding a New Transform

Subclass `BaseTransform` in `transforms/`:

```python
from datadex.transforms.base import BaseTransform

class MyTransform(BaseTransform):
    def apply(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]: ...
```

### Pipeline Config (YAML)

```yaml
name: my_pipeline
source:
  type: postgres
  connection: postgresql://user:pass@host/db
  query: "SELECT * FROM orders"
transforms:
  - type: filter
    condition: "status == 'active'"
  - type: cast
    column: amount
    dtype: float
quality:
  - check: not_null
    columns: [id, amount]
  - check: range
    column: amount
    min: 0
sink:
  type: s3
  bucket: my-bucket
  key: output/orders.parquet
```

______________________________________________________________________

## Key Files

| File | Purpose |
| --- | --- |
| `pyproject.toml` | Package config |
| `poe_tasks.toml` | All poe task definitions |
| `src/datadex/config/loader.py` | PipelineConfig Pydantic schema |
| `src/datadex/connectors/base.py` | BaseConnector ABC — implement to add sources/sinks |
| `src/datadex/engine/runner.py` | PipelineRunner — ETL orchestration |
| `src/datadex/transforms/base.py` | BaseTransform ABC |
| `src/datadex/quality/checks.py` | Built-in quality checks |
| `src/datadex/lineage/tracker.py` | Column-level lineage tracking |
| `src/datadex/api/main.py` | FastAPI app |
| `src/datadex/cli.py` | CLI entry point |
| `tasks/todo.md` | Task tracker |
| `tasks/lessons.md` | Lessons learned |
| `tasks/findings.md` | Research log |

______________________________________________________________________

## API Endpoints

Start with `uv run poe dev` (requires `uv run poe setup` first).

- `GET /health` — Health check
- `GET /pipelines` — List pipeline definitions
- `POST /pipelines/{name}/run` — Execute a pipeline
- `GET /runs` — List pipeline run history
- `GET /quality/{pipeline}` — Quality scorecard for a pipeline

______________________________________________________________________

## Current State

- `PipelineRunner.run()` raises `NotImplementedError` — engine execution not yet wired up
- CLI commands (`run`, `quality`, `lineage`) raise `NotImplementedError` — stubs awaiting engine connection
- Connectors, transforms, quality checks, and lineage tracker are scaffolded but not fully integrated
- API routers exist and are wired but depend on the engine being implemented
