"""DataDEX — Universal data pipeline engine."""

from __future__ import annotations

try:
    from importlib.metadata import version

    __version__ = version("datadex")
except Exception:
    __version__ = "0.1.0"
