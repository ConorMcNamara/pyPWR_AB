"""Obtaining Power Analyses for Welch's Unequal Variance T-Test."""

from __future__ import annotations

from pwrAB import pwr_tests


__version__ = "1.0.0"
__all__: list[str] = [
    "pwr_tests",
]


def __dir__() -> list[str]:
    """Return the public API of the module."""
    return __all__
