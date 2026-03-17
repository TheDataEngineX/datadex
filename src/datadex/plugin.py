"""DataDEX plugin for DataEngineX."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version


def _get_version() -> str:
    try:
        return _pkg_version("datadex")
    except PackageNotFoundError:
        return "0.0.0"


@dataclass
class DataDEXPlugin:
    """DataDEX plugin — registers with the DataEngineX plugin system."""

    name: str = "datadex"
    version: str = field(default_factory=_get_version)
    description: str = "Universal data pipeline engine"

    def health_check(self) -> dict[str, str]:
        """Return plugin health status."""
        return {"status": "healthy", "plugin": self.name}
