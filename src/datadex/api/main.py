"""DataDEX API — FastAPI application."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

from fastapi import FastAPI

from datadex.api.routers import pipelines, quality, runs

try:
    _version = str(_pkg_version("datadex"))
except PackageNotFoundError:
    _version = "0.0.0"

app = FastAPI(
    title="DataDEX API",
    description="Universal data pipeline engine API",
    version=_version,
)

app.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
app.include_router(runs.router, prefix="/runs", tags=["runs"])
app.include_router(quality.router, prefix="/quality", tags=["quality"])


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "datadex"}
