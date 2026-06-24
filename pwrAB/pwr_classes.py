"""Power analysis classes for Welch's unequal-variance t-test in AB testing."""

from __future__ import annotations

from math import ceil, sqrt
from typing import TYPE_CHECKING, Any

import numpy as np
import scipy.optimize  # type: ignore[import-untyped]
import scipy.stats  # type: ignore[import-untyped]


if TYPE_CHECKING:
    from collections.abc import Callable


# ---------------------------------------------------------------------------
# Typed wrappers for scipy functions
# All type: ignore comments are isolated here so the rest of the file is clean.
# ---------------------------------------------------------------------------


def _bisect(f: Callable[[float], float], a: float, b: float) -> float:
    return float(scipy.optimize.bisect(f, a, b))  # type: ignore[no-untyped-call, arg-type]


def _brentq(f: Callable[[float], float], a: float, b: float) -> float:
    return float(scipy.optimize.brentq(f, a, b))  # type: ignore[no-untyped-call, arg-type]


def _ridder(f: Callable[[float], float], a: float, b: float) -> float:
    return float(scipy.optimize.ridder(f, a, b))  # type: ignore[no-untyped-call, arg-type]


def _nct_cdf(x: float, df: float, nc: float) -> float:
    return float(scipy.stats.nct.cdf(x, df=df, nc=nc))  # type: ignore[no-untyped-call]


def _nct_sf(x: float, df: float, nc: float) -> float:
    return float(scipy.stats.nct.sf(x, df=df, nc=nc))  # type: ignore[no-untyped-call]


def _t_ppf(q: float, df: float) -> float:
    return float(scipy.stats.t.ppf(q, df=df))  # type: ignore[no-untyped-call]


def _t_isf(q: float, df: float) -> float:
    return float(scipy.stats.t.isf(q, df=df))  # type: ignore[no-untyped-call]


# ---------------------------------------------------------------------------
# Continuous Class
# ---------------------------------------------------------------------------


class ab_t2n_class:
    """
    Power analysis class for AB testing with continuous outcomes using Welch's t-test.

    Parameters
    ----------
    n : int, optional
        Total number of observations (sum of observations for groups A and B).
    percent_b : float, optional
        Percentage of total observations allocated to group B (between 0 and 1,
        e.g., input 0.5 for 50%).
    mean_diff : float, optional
        Difference in means of the two groups (mean_B - mean_A).
    sd_a : float, default=1
        Standard deviation of group A. Must be positive.
    sd_b : float, default=1
        Standard deviation of group B. Must be positive.
    sig_level : float, optional
        Significance level (Type I error probability). Must be between 0 and 1.
    power : float, optional
        Power of test (1 minus Type II error probability). Must be between 0 and 1.
    alternative : {'two-sided', 'greater', 'less'}, default='two-sided'
        Specifies the alternative hypothesis.
    max_sample : int or float, default=1e07
        Maximum sample size to search for when solving for n.
    """

    def __init__(
        self,
        n: int | None = None,
        percent_b: float | None = None,
        mean_diff: float | None = None,
        sd_a: float = 1,
        sd_b: float = 1,
        sig_level: float | None = None,
        power: float | None = None,
        alternative: str = "two-sided",
        max_sample: int | float = 1e07,
    ) -> None:
        self.n = n
        self.percent_b = percent_b
        self.sd_a = sd_a
        self.sd_b = sd_b
        self.sig_level = sig_level
        self.power = power
        self.alternative = alternative.casefold()
        self.max_sample = ceil(max_sample)
        self.mean_diff = abs(mean_diff) if self.alternative == "two-sided" else mean_diff

    def _get_power(self) -> float:
        """Calculate power for given parameters."""
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        var_a = self.sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = self.mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            power = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat)
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            power = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat)
        else:
            power = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat)
        return power

    def _get_n(self, n: float) -> float:
        """Calculate power difference for given sample size (root finding helper)."""
        n_b = n * self.percent_b
        n_a = n - n_b
        var_a = self.sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = self.mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        return result

    def _get_percent_b(self, percent_b: float) -> float:
        """Calculate power difference for given percent_b (root finding helper)."""
        n_b = self.n * percent_b
        n_a = self.n - n_b
        var_a = self.sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = self.mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        return result

    def _get_mean_diff(self, mean_diff: float) -> float:
        """Calculate power difference for given mean difference (root finding helper)."""
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        var_a = self.sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        return result

    def _get_sig_level(self, sig_level: float) -> float:
        """Calculate power difference for given significance level (root finding helper)."""
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        var_a = self.sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = self.mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(sig_level, df_ws), df_ws, t_stat) - self.power
        return result

    def pwr_test(self) -> dict[str, Any]:
        """
        Perform power analysis for AB testing.

        Returns
        -------
        dict[str, Any]
            Dictionary containing test results with keys: n, percent_b, mean_diff,
            sd_a, sd_b, sig_level, power, alternative, method.
        """
        if self.power is None:
            self.power = self._get_power()
        elif self.n is None:
            min_n = max((5 / self.percent_b), (5 / (1 - self.percent_b)))
            try:
                self.n = ceil(_bisect(self._get_n, min_n, self.max_sample + 1))
            except ValueError:
                self.n = ceil(_bisect(self._get_n, min_n, self.max_sample / 10 + 1))
        elif self.percent_b is None:
            min_percent_b = max(0.001, 10 / self.n)
            search_grid = np.arange(min_percent_b, 1 - min_percent_b, 0.0001)
            diff_power = np.array(list(map(self._get_percent_b, search_grid)))  # type: ignore[arg-type]
            self.percent_b = search_grid[min(np.where(diff_power > 0)[0])]
        elif self.mean_diff is None:
            if self.alternative == "less":  # type: ignore[unreachable]
                self.mean_diff = _brentq(self._get_mean_diff, -10_000, 0)
            else:
                self.mean_diff = _brentq(self._get_mean_diff, 0, 10_000)
        elif self.sig_level is None:
            self.sig_level = _brentq(self._get_sig_level, 1e-10, 1 - 1e-10)
        else:
            raise ValueError("One of power, n, percent_b, mean_diff or sig_level must be None")
        return {
            "n": self.n,
            "percent_b": self.percent_b,
            "mean_diff": self.mean_diff,
            "sd_a": self.sd_a,
            "sd_b": self.sd_b,
            "sig_level": self.sig_level,
            "power": self.power,
            "alternative": self.alternative,
            "method": "t-test Power Calculation",
        }


# ---------------------------------------------------------------------------
# Proportion Class
# ---------------------------------------------------------------------------


class ab_t2n_prop_class:
    """
    Power analysis class for AB testing with proportion outcomes using Welch's t-test.

    Parameters
    ----------
    prop_a : float, optional
        Proportion (success rate) of group A. Must be between 0 and 1.
    prop_b : float, optional
        Proportion (success rate) of group B. Must be between 0 and 1.
    n : int, optional
        Total number of observations (sum of observations for groups A and B).
    percent_b : float, optional
        Percentage of total observations allocated to group B (between 0 and 1,
        e.g., input 0.5 for 50%).
    sig_level : float, optional
        Significance level (Type I error probability). Must be between 0 and 1.
    power : float, optional
        Power of test (1 minus Type II error probability). Must be between 0 and 1.
    alternative : {'two-sided', 'greater', 'less'}, default='two-sided'
        Specifies the alternative hypothesis.
    max_sample : int or float, default=1e07
        Maximum sample size to search for when solving for n.
    """

    def __init__(
        self,
        prop_a: float | None = None,
        prop_b: float | None = None,
        n: int | None = None,
        percent_b: float | None = None,
        sig_level: float | None = None,
        power: float | None = None,
        alternative: str = "two-sided",
        max_sample: int | float = 1e07,
    ) -> None:
        self.prop_a: float | list[float] | None = prop_a
        self.prop_b: float | list[float] | None = prop_b
        self.n = n
        self.percent_b = percent_b
        self.sig_level = sig_level
        self.power = power
        self.alternative = alternative.casefold()
        self.max_sample = max_sample
        if sum(v is None for v in [prop_a, prop_b]) > 0:
            self.mean_diff = None
        else:
            self.mean_diff = abs(prop_b - prop_a) if self.alternative == "two-sided" else prop_b - prop_a
        self.sd_a = sqrt(prop_a * (1 - prop_a)) if prop_a is not None else None
        self.sd_b = sqrt(prop_b * (1 - prop_b)) if prop_b is not None else None

    def _get_power(self) -> float:
        return ab_t2n_class(
            self.n,
            self.percent_b,
            self.mean_diff,
            self.sd_a,
            self.sd_b,
            self.sig_level,
            self.power,
            self.alternative,
            self.max_sample,
        )._get_power()

    def _get_n(self, n: float) -> float:
        return ab_t2n_class(
            self.n,
            self.percent_b,
            self.mean_diff,
            self.sd_a,
            self.sd_b,
            self.sig_level,
            self.power,
            self.alternative,
            self.max_sample,
        )._get_n(n)

    def _get_percent_b(self, percent_b: float) -> float:
        return ab_t2n_class(
            self.n,
            self.percent_b,
            self.mean_diff,
            self.sd_a,
            self.sd_b,
            self.sig_level,
            self.power,
            self.alternative,
            self.max_sample,
        )._get_percent_b(percent_b)

    def _get_sig_level(self, sig_level: float) -> float:
        return ab_t2n_class(
            self.n,
            self.percent_b,
            self.mean_diff,
            self.sd_a,
            self.sd_b,
            self.sig_level,
            self.power,
            self.alternative,
            self.max_sample,
        )._get_sig_level(sig_level)

    def _get_prop_a(self, prop_a: float) -> float:
        """Calculate power difference for given prop_a (root finding helper)."""
        mean_diff = abs(self.prop_b - prop_a) if self.alternative == "two-sided" else self.prop_b - prop_a  # type: ignore[operator]
        sd_a = sqrt(prop_a * (1 - prop_a))
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        var_a = sd_a**2
        var_b = self.sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        return float(result)

    def _get_prop_b(self, prop_b: float) -> float:
        """Calculate power difference for given prop_b (root finding helper)."""
        mean_diff = abs(prop_b - self.prop_a) if self.alternative == "two-sided" else prop_b - self.prop_a  # type: ignore[operator]
        sd_b = sqrt(prop_b * (1 - prop_b))
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        var_a = self.sd_a**2
        var_b = sd_b**2
        pooled_var = var_a / n_a + var_b / n_b

        df_ws = pooled_var**2 / ((var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1))
        t_stat = mean_diff / sqrt(pooled_var)

        if self.alternative == "less":
            result = _nct_cdf(_t_ppf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = _t_isf(self.sig_level / 2, df_ws)
            result = _nct_sf(qu, df_ws, t_stat) + _nct_cdf(-qu, df_ws, t_stat) - self.power
        else:
            result = _nct_sf(_t_isf(self.sig_level, df_ws), df_ws, t_stat) - self.power
        return float(result)

    def pwr_test(self) -> dict[str, Any]:
        """
        Perform power analysis for AB testing with proportions.

        Returns
        -------
        dict[str, Any]
            Dictionary containing test results with keys: n, percent_b, mean_diff,
            sd_a, sd_b, prop_a, prop_b, sig_level, power, alternative, method.
        """
        if self.power is None:
            self.power = self._get_power()
        elif self.n is None:
            min_n = max((5 / self.percent_b), (5 / (1 - self.percent_b)))
            self.n = ceil(_bisect(self._get_n, min_n, self.max_sample + 1))
        elif self.prop_a is None:
            if not isinstance(self.prop_b, float):
                raise TypeError(f"prop_b must be a float, got {type(self.prop_b).__name__}")
            if self.alternative == "less":
                self.prop_a = _brentq(self._get_prop_a, self.prop_b, 1)
            elif self.alternative == "two-sided":
                try:
                    root_1: float | None = _brentq(self._get_prop_a, self.prop_b, 1)
                except ValueError:
                    try:
                        root_1 = _brentq(self._get_prop_a, self.prop_b, 0.75)
                    except ValueError:
                        try:
                            root_1 = _brentq(self._get_prop_a, self.prop_b, 0.5)
                        except ValueError:
                            root_1 = None
                try:
                    root_2: float | None = _ridder(self._get_prop_a, 0, self.prop_b)
                except ValueError:
                    try:
                        root_2 = _ridder(self._get_prop_a, 0.1, self.prop_b)
                    except ValueError:
                        try:
                            root_2 = _ridder(self._get_prop_a, 0.2, self.prop_b)
                        except ValueError:
                            try:
                                root_2 = _ridder(self._get_prop_a, 0.3, self.prop_b)
                            except ValueError:
                                root_2 = None
                if root_1 is not None:
                    if root_2 is not None:
                        self.prop_a = [root_2, root_1]
                    else:
                        self.prop_a = root_1  # type: ignore[unreachable]
                elif root_2 is not None:
                    self.prop_a = root_2
                else:
                    self.prop_a = None  # type: ignore[unreachable]
            else:
                self.prop_a = _brentq(self._get_prop_a, 0, self.prop_b)
        elif self.prop_b is None:
            if not isinstance(self.prop_a, float):
                raise TypeError(f"prop_a must be a float, got {type(self.prop_a).__name__}")
            if self.alternative == "less":
                self.prop_b = _brentq(self._get_prop_b, self.prop_a, 1)
            elif self.alternative == "two-sided":
                try:
                    root_1 = _ridder(self._get_prop_b, self.prop_a, 1)
                except ValueError:
                    try:
                        root_1 = _ridder(self._get_prop_b, self.prop_a, 0.75)
                    except ValueError:
                        try:
                            root_1 = _ridder(self._get_prop_b, self.prop_a, 0.5)
                        except ValueError:
                            root_1 = _ridder(self._get_prop_b, self.prop_a, self.prop_a + 0.1)
                try:
                    root_2 = _ridder(self._get_prop_b, 0, self.prop_a)
                except ValueError:
                    try:
                        root_2 = _ridder(self._get_prop_b, 0.1, self.prop_a)
                    except ValueError:
                        try:
                            root_2 = _ridder(self._get_prop_b, 0.2, self.prop_a)
                        except ValueError:
                            root_2 = _ridder(self._get_prop_b, self.prop_a - 0.1, self.prop_a)
                self.prop_b = [root_2, root_1]
            else:
                self.prop_b = _brentq(self._get_prop_b, 0, self.prop_a)
        elif self.percent_b is None:
            min_percent_b = max(0.001, 10 / self.n)
            search_grid = np.arange(min_percent_b, 1 - min_percent_b, 0.0001)
            diff_power = np.array(list(map(self._get_percent_b, search_grid)))  # type: ignore[arg-type]
            self.percent_b = search_grid[min(np.where(diff_power > 0)[0])]
        elif self.sig_level is None:
            self.sig_level = _brentq(self._get_sig_level, 1e-10, 1 - 1e-10)
        else:
            raise ValueError("One of power, n, percent_b, prop_a, prop_b or sig_level must be None")
        return {
            "n": self.n,
            "percent_b": self.percent_b,
            "mean_diff": self.mean_diff,
            "sd_a": self.sd_a,
            "sd_b": self.sd_b,
            "prop_a": self.prop_a,
            "prop_b": self.prop_b,
            "sig_level": self.sig_level,
            "power": self.power,
            "alternative": self.alternative,
            "method": "t-test Power Calculation",
        }
