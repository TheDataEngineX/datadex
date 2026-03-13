"""Pipeline management endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_pipelines() -> list[dict[str, Any]]:
    """List all pipeline configurations."""
    return []


@router.post("/", status_code=201)
async def create_pipeline(config: dict[str, Any]) -> dict[str, str]:
    """Create a new pipeline configuration (stub)."""
    raise NotImplementedError("Pipeline creation not yet implemented")


@router.get("/{name}")
async def get_pipeline(name: str) -> dict[str, Any]:
    """Get a pipeline configuration by name (stub)."""
    raise NotImplementedError(f"Pipeline lookup not yet implemented: {name}")
