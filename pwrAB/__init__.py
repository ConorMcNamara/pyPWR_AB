"""Obtaining Power Analyses for Welch's Unequal Variance T-Test."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from pwrAB import pwr_tests


try:
    # Single source of truth: the version declared in pyproject.toml, read from
    # the installed package metadata. Falls back gracefully when the package is
    # not installed (e.g. running from a source tree without an editable install).
    __version__ = version("pypwr-ab")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0.dev0"
__all__: list[str] = [
    "pwr_tests",
]


def __dir__() -> list[str]:
    """Return the public API of the module."""
    return __all__
