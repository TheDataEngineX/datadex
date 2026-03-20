"""DataDEX plugin for DataEngineX."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Any

from dataenginex.plugins import DataEngineXPlugin


def _get_version() -> str:
    try:
        return str(_pkg_version("datadex"))
    except PackageNotFoundError:
        return "0.0.0"


class DataDEXPlugin(DataEngineXPlugin):
    """DataDEX plugin — registers with the DataEngineX plugin system."""

    @property
    def name(self) -> str:
        return "datadex"

    @property
    def version(self) -> str:
        return _get_version()

    def health_check(self) -> dict[str, Any]:
        """Return plugin health status."""
        return {"status": "healthy", "plugin": self.name}
