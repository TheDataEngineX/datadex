"""DataDEX plugin for DataEngineX."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DataDEXPlugin:
    """DataDEX plugin — registers with the DataEngineX plugin system."""

    name: str = "datadex"
    version: str = "0.1.0"
    description: str = "Universal data pipeline engine"

    def health_check(self) -> dict[str, str]:
        """Return plugin health status."""
        return {"status": "healthy", "plugin": self.name}
