"""Pipeline YAML config loader and validator."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    """Data source configuration."""

    type: str
    connection: str | None = None
    table: str | None = None
    path: str | None = None
    mode: str = "full"  # full | incremental
    watermark_column: str | None = None


class QualityConfig(BaseModel):
    """Data quality thresholds."""

    min_completeness: float = 0.9
    min_freshness: str | None = None
    unique_columns: list[str] = Field(default_factory=list)


class DestinationConfig(BaseModel):
    """Data destination configuration."""

    type: str = "parquet"
    layer: str = "silver"
    partition_by: list[str] = Field(default_factory=list)


class PipelineConfig(BaseModel):
    """Complete pipeline configuration parsed from YAML."""

    name: str
    schedule: str | None = None
    source: SourceConfig
    transforms: list[dict[str, object]] = Field(default_factory=list)
    quality: QualityConfig = Field(default_factory=QualityConfig)
    destination: DestinationConfig = Field(default_factory=DestinationConfig)


def load_pipeline(path: str | Path) -> PipelineConfig:
    """Load and validate a pipeline config from a YAML file."""
    with open(path) as f:
        raw = yaml.safe_load(f)

    pipeline_data = raw.get("pipeline", raw)
    return PipelineConfig(**pipeline_data)
