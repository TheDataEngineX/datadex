"""Quality endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/{dataset}")
async def get_quality(dataset: str) -> dict[str, Any]:
    """Get quality scorecard for a dataset (stub)."""
    raise NotImplementedError(f"Quality scorecard not yet implemented: {dataset}")
