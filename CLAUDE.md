# CLAUDE.md — DataDEX

> Repo-specific context. Workspace-level rules, coding standards, and git conventions are in `../CLAUDE.md`.

## Project Overview

**DataDEX** — Universal data pipeline engine. Define ingestion, transformation, quality, and lineage in YAML.

**Stack:** Python 3.12+ · FastAPI (via dataenginex[api]) · uv · Ruff · mypy strict · pytest · Port 8001

**Version:** 0.1.0 | **Depends on:** dataenginex >= 0.6.0

## Build & Run Commands

```bash
uv sync --extra api

uv run ruff check src/ tests/          # lint
uv run ruff format --check src/ tests/ # format check
uv run mypy src/datadex/ --strict      # typecheck
uv run pytest tests/ -x --tb=short -q # test

uv run datadex serve --port 8001       # dev server
uv run datadex run pipeline.yaml       # run a pipeline
```

## Key Files

| File | Purpose |
| --- | --- |
| `src/datadex/` | Core source |
| `src/datadex/cli.py` | Click CLI entry point |
| `src/datadex/api/main.py` | FastAPI app |
| `src/datadex/connectors/` | DB, S3, REST, Kafka connectors |
| `src/datadex/pipeline/` | YAML pipeline engine |
| `src/datadex/quality/` | Quality scorecards |
| `src/datadex/lineage/` | Column-level lineage |
| `pyproject.toml` | Package config |
