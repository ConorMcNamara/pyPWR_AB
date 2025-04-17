from math import pow, sqrt, ceil
from typing import Union

from scipy.stats import t as t_dist, nct
from scipy.optimize import brentq, bisect, ridder

import numpy as np


# Continuous Class
class ab_t2n_class:
    def __init__(
        self,
        n: int = None,
        percent_b: float = None,
        mean_diff: float = None,
        sd_a: float = 1,
        sd_b: float = 1,
        sig_level: float = None,
        power: float = None,
        alternative: str = "two-sided",
        max_sample: Union[int, float] = 1e07,
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
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = self.mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            power = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat)
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            power = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat)
        else:
            power = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat)
        return power

    def _get_n(self, n: int) -> float:
        n_b = n * self.percent_b
        n_a = n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = self.mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            n = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            n = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            n = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return n

    def _get_percent_b(self, percent_b: float) -> float:
        n_b = self.n * percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = self.mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            percent_b = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            percent_b = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            percent_b = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return percent_b

    def _get_mean_diff(self, mean_diff: float) -> float:
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            mean_diff = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            mean_diff = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            mean_diff = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return mean_diff

    def _get_sig_level(self, sig_level) -> float:
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = self.mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            sig_level = nct.cdf(t_dist.ppf(sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(sig_level / 2, df=df_ws)
            sig_level = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            sig_level = nct.sf(t_dist.isf(sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return sig_level

    def pwr_test(self) -> dict:
        if self.power is None:
            self.power = self._get_power()
        elif self.n is None:
            min_n = max((5 / self.percent_b), (5 / (1 - self.percent_b)))
            try:
                self.n = ceil(bisect(self._get_n, min_n, self.max_sample + 1))
            except ValueError:
                self.n = ceil(bisect(self._get_n, min_n, self.max_sample / 10 + 1))
        elif self.percent_b is None:
            min_percent_b = max(0.001, 10 / self.n)
            search_grid = np.arange(min_percent_b, 1 - min_percent_b, 0.0001)
            diff_power = np.array(list(map(self._get_percent_b, search_grid)))
            self.percent_b = search_grid[min(np.where(diff_power > 0)[0])]
        elif self.mean_diff is None:
            if self.alternative == "less":
                self.mean_diff = brentq(self._get_mean_diff, -10_000, 0)
            else:
                self.mean_diff = brentq(self._get_mean_diff, 0, 10_000)
        elif self.sig_level is None:
            self.sig_level = brentq(self._get_sig_level, 1e-10, 1 - 1e-10)
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


# Proportion Class
class ab_t2n_prop_class:
    def __init__(
        self,
        prop_a: float = None,
        prop_b: float = None,
        n: int = None,
        percent_b: float = None,
        sig_level: float = None,
        power: float = None,
        alternative: str = "two-sided",
        max_sample: Union[int, float] = 1e07,
    ) -> None:
        self.prop_a = prop_a
        self.prop_b = prop_b
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

    def _get_n(self, n: int) -> float:
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

    def _get_sig_level(self, sig_level) -> float:
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
        mean_diff = abs(self.prop_b - prop_a) if self.alternative == "two-sided" else self.prop_b - prop_a
        sd_a = sqrt(prop_a * (1 - prop_a))
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b, 2) / (
            pow(pow(sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(self.sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = mean_diff / sqrt(pow(sd_a, 2) / n_a + pow(self.sd_b, 2) / n_b)
        if self.alternative == "less":
            prop_a = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            prop_a = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            prop_a = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return prop_a

    def _get_prop_b(self, prop_b: float) -> float:
        mean_diff = abs(prop_b - self.prop_a) if self.alternative == "two-sided" else prop_b - self.prop_a
        sd_b = sqrt(prop_b * (1 - prop_b))
        n_b = self.n * self.percent_b
        n_a = self.n - n_b
        df_ws = pow(pow(self.sd_a, 2) / n_a + pow(sd_b, 2) / n_b, 2) / (
            pow(pow(self.sd_a, 2) / n_a, 2) / (n_a - 1) + pow(pow(sd_b, 2) / n_b, 2) / (n_b - 1)
        )
        t_stat = mean_diff / sqrt(pow(self.sd_a, 2) / n_a + pow(sd_b, 2) / n_b)
        if self.alternative == "less":
            prop_b = nct.cdf(t_dist.ppf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        elif self.alternative == "two-sided":
            qu = t_dist.isf(self.sig_level / 2, df=df_ws)
            prop_b = nct.sf(qu, df=df_ws, nc=t_stat) + nct.cdf(-qu, df=df_ws, nc=t_stat) - self.power
        else:
            prop_b = nct.sf(t_dist.isf(self.sig_level, df=df_ws), df=df_ws, nc=t_stat) - self.power
        return prop_b

    def pwr_test(self) -> dict:
        if self.power is None:
            self.power = self._get_power()
        elif self.n is None:
            min_n = max((5 / self.percent_b), (5 / (1 - self.percent_b)))
            self.n = ceil(bisect(self._get_n, min_n, self.max_sample + 1))
        elif self.prop_a is None:
            if self.alternative == "less":
                self.prop_a = brentq(self._get_prop_a, self.prop_b, 1)
            elif self.alternative == "two-sided":
                try:
                    root_1 = brentq(self._get_prop_a, self.prop_b, 1)
                except ValueError:
                    try:
                        root_1 = brentq(self._get_prop_a, self.prop_b, 0.75)
                    except ValueError:
                        try:
                            root_1 = brentq(self._get_prop_a, self.prop_b, 0.5)
                        except ValueError:
                            root_1 = None
                try:
                    root_2 = brentq(self._get_prop_a, 0, self.prop_b)
                except ValueError:
                    try:
                        root_2 = brentq(self._get_prop_a, 0.1, self.prop_b)
                    except ValueError:
                        try:
                            root_2 = brentq(self._get_prop_a, 0.2, self.prop_b)
                        except ValueError:
                            root_2 = None
                if root_1 is not None:
                    if root_2 is not None:
                        self.prop_a = [root_2, root_1]
                    else:
                        self.prop_a = root_1
                else:
                    if root_2 is not None:
                        self.prop_a = root_2
                    else:
                        self.prop_a = None
            else:
                self.prop_a = brentq(self._get_prop_a, 0, self.prop_b)
        elif self.prop_b is None:
            if self.alternative == "less":
                self.prop_b = brentq(self._get_prop_b, self.prop_a, 1)
            elif self.alternative == "two-sided":
                try:
                    root_1 = ridder(self._get_prop_b, self.prop_a, 1)
                except ValueError:
                    try:
                        root_1 = ridder(self._get_prop_b, self.prop_a, 0.75)
                    except ValueError:
                        try:
                            root_1 = ridder(self._get_prop_b, self.prop_a, 0.5)
                        except ValueError:
                            root_1 = ridder(self._get_prop_b, self.prop_a, self.prop_a + 0.1)
                try:
                    root_2 = ridder(self._get_prop_b, 0, self.prop_a)
                except ValueError:
                    try:
                        root_2 = ridder(self._get_prop_b, 0.1, self.prop_a)
                    except ValueError:
                        try:
                            root_2 = ridder(self._get_prop_b, 0.2, self.prop_a)
                        except ValueError:
                            root_2 = ridder(self._get_prop_b, self.prop_a - 0.1, self.prop_a)
                if root_1 is not None:
                    self.prop_b = [root_2, root_1] if root_2 is not None else root_1
                else:
                    self.prop_b = root_2 if root_2 is not None else None
            else:
                self.prop_b = brentq(self._get_prop_b, 0, self.prop_a)
        elif self.percent_b is None:
            min_percent_b = max(0.001, 10 / self.n)
            search_grid = np.arange(min_percent_b, 1 - min_percent_b, 0.0001)
            diff_power = np.array(list(map(self._get_percent_b, search_grid)))
            self.percent_b = search_grid[min(np.where(diff_power > 0)[0])]
        elif self.sig_level is None:
            self.sig_level = brentq(self._get_sig_level, 1e-10, 1 - 1e-10)
        else:
            raise ValueError("One of power, n, percent_b, prop_a, pro_b or sig_level must be None")
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
