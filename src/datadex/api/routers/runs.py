"""Pipeline run endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_runs() -> list[dict[str, Any]]:
    """List recent pipeline runs (stub)."""
    return []


@router.get("/latest")
async def latest_runs() -> list[dict[str, Any]]:
    """Get the latest run per pipeline (stub)."""
    return []


@router.get("/{run_id}")
async def get_run(run_id: str) -> dict[str, Any]:
    """Get details of a specific run (stub)."""
    raise NotImplementedError(f"Run lookup not yet implemented: {run_id}")
