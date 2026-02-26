from __future__ import annotations

from typing import Any

from pwrAB.pwr_classes import ab_t2n_class, ab_t2n_prop_class


def ab_t2n(
    n: int | None = None,
    percent_b: float | None = None,
    mean_diff: float | None = None,
    sd_a: float = 1,
    sd_b: float = 1,
    sig_level: float | None = None,
    power: float | None = None,
    alternative: str = "two-sided",
    max_sample: int | float = 1e07,
    *,
    print_pretty: bool = True,
) -> dict[str, Any]:
    """
    Perform power analysis for AB testing using Welch's t-test.

    This function uses Welch's t-test, which allows for the standard deviation
    to vary across groups, making it more appropriate for AB testing scenarios
    where group variances may differ.

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
    max_sample : int | float, default=1e07
        Maximum sample size to search for when solving for n.
    print_pretty : bool, default=True
        Whether to print formatted results to stdout.

    Returns
    -------
    dict[str, Any]
        Dictionary containing: n, percent_b, mean_diff, sd_a, sd_b, sig_level,
        power, alternative, and method.

    Raises
    ------
    ValueError
        If exactly one parameter is not None, or if parameters are out of valid ranges.

    Examples
    --------
    Calculate power given other parameters:

        >>> result = ab_t2n(
        ...     n=3000, percent_b=0.3, mean_diff=0.15, sd_a=1, sd_b=2, sig_level=0.05, alternative="two-sided"
        ... )

    Calculate required sample size:

        >>> result = ab_t2n(
        ...     percent_b=0.3,
        ...     mean_diff=0.15,
        ...     sd_a=1,
        ...     sd_b=2,
        ...     sig_level=0.05,
        ...     power=0.8,
        ...     alternative="two-sided",
        ... )
    """
    # Validate exactly one parameter is None
    none_count = sum(v is None for v in [n, percent_b, mean_diff, power, sig_level])
    if none_count == 0:
        msg = "Exactly one of n, percent_b, mean_diff, power, or sig_level must be None"
        raise ValueError(msg)
    if none_count > 1:
        msg = "Exactly one of n, percent_b, mean_diff, power, or sig_level may be None"
        raise ValueError(msg)

    # Validate standard deviations
    if sd_a <= 0:
        msg = f"sd_a must be positive, got {sd_a}"
        raise ValueError(msg)
    if sd_b <= 0:
        msg = f"sd_b must be positive, got {sd_b}"
        raise ValueError(msg)

    # Validate ranges
    if sig_level is not None and not 0 < sig_level < 1:
        msg = f"sig_level must be between 0 and 1, got {sig_level}"
        raise ValueError(msg)
    if power is not None and not 0 < power < 1:
        msg = f"power must be between 0 and 1, got {power}"
        raise ValueError(msg)
    if n is not None and n < 10:
        msg = f"n must be at least 10, got {n}"
        raise ValueError(msg)
    if percent_b is not None and not 0 < percent_b < 1:
        msg = f"percent_b must be between 0 and 1, got {percent_b}"
        raise ValueError(msg)
    test = ab_t2n_class(n, percent_b, mean_diff, sd_a, sd_b, sig_level, power, alternative, max_sample).pwr_test()

    if print_pretty:
        output = (
            f"  {test['method']}\n\n"
            f"          N = {test['n']}\n"
            f"  percent_b = {round(test['percent_b'], 2):.2f}\n"
            f"  mean_diff = {round(test['mean_diff'], 4):.4f}\n"
            f"       sd_a = {round(test['sd_a'], 4):.4f}\n"
            f"       sd_b = {round(test['sd_b'], 4):.4f}\n"
            f"  sig_level = {round(test['sig_level'], 4):.4f}\n"
            f"      power = {round(test['power'], 4):.4f}\n"
            f"alternative = {test['alternative']}"
        )
        print(output)

    return test


def ab_t2n_prop(
    prop_a: float | None = None,
    prop_b: float | None = None,
    n: int | None = None,
    percent_b: float | None = None,
    sig_level: float | None = None,
    power: float | None = None,
    alternative: str = "two-sided",
    max_sample: int | float = 1e07,
    *,
    print_pretty: bool = True,
) -> dict[str, Any]:
    """
    Perform power analysis for AB testing with proportion outcomes.

    This function performs power analysis for AB testing when the dependent
    variables are proportions (between 0 and 1). It uses Welch's t-test, which
    allows for the standard deviation to vary across groups.

    Parameters
    ----------
    prop_a : float, optional
        Proportion of successes in group A (between 0 and 1).
    prop_b : float, optional
        Proportion of successes in group B (between 0 and 1).
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
    max_sample : int | float, default=1e07
        Maximum sample size to search for when solving for n.
    print_pretty : bool, default=True
        Whether to print formatted results to stdout.

    Returns
    -------
    dict[str, Any]
        Dictionary containing: prop_a, prop_b, n, percent_b, sig_level, power,
        alternative, and method.

    Raises
    ------
    ValueError
        If exactly one parameter is not None, or if parameters are out of valid ranges.

    Examples
    --------
    Calculate power given other parameters:

        >>> result = ab_t2n_prop(
        ...     prop_a=0.2, prop_b=0.25, n=3000, percent_b=0.3, sig_level=0.05, alternative="two-sided"
        ... )

    Calculate required sample size:

        >>> result = ab_t2n_prop(
        ...     prop_a=0.2, prop_b=0.25, percent_b=0.3, sig_level=0.05, power=0.8, alternative="two-sided"
        ... )
    """
    # Validate exactly one parameter is None
    none_count = sum(v is None for v in [n, percent_b, prop_a, prop_b, power, sig_level])
    if none_count == 0:
        msg = "Exactly one of n, percent_b, prop_a, prop_b, power, or sig_level must be None"
        raise ValueError(msg)
    if none_count > 1:
        msg = "Exactly one of n, percent_b, prop_a, prop_b, power, or sig_level may be None"
        raise ValueError(msg)

    # Validate proportions
    if prop_a is not None and not 0 < prop_a < 1:
        msg = f"prop_a must be between 0 and 1, got {prop_a}"
        raise ValueError(msg)
    if prop_b is not None and not 0 < prop_b < 1:
        msg = f"prop_b must be between 0 and 1, got {prop_b}"
        raise ValueError(msg)

    # Validate ranges
    if sig_level is not None and not 0 < sig_level < 1:
        msg = f"sig_level must be between 0 and 1, got {sig_level}"
        raise ValueError(msg)
    if power is not None and not 0 < power < 1:
        msg = f"power must be between 0 and 1, got {power}"
        raise ValueError(msg)
    if n is not None and n < 10:
        msg = f"n must be at least 10, got {n}"
        raise ValueError(msg)
    if percent_b is not None and not 0 < percent_b < 1:
        msg = f"percent_b must be between 0 and 1, got {percent_b}"
        raise ValueError(msg)
    test = ab_t2n_prop_class(prop_a, prop_b, n, percent_b, sig_level, power, alternative, max_sample).pwr_test()

    if print_pretty:
        # Format proportions for display
        prop_a_display = (
            [round(i, 4) for i in test["prop_a"]]
            if isinstance(test["prop_a"], list)
            else round(test["prop_a"], 4)
            if test["prop_a"] is not None
            else None
        )
        prop_b_display = (
            [round(i, 4) for i in test["prop_b"]]
            if isinstance(test["prop_b"], list)
            else round(test["prop_b"], 4)
            if test["prop_b"] is not None
            else None
        )

        output = (
            f"  {test['method']}\n\n"
            f"          N = {test['n']}\n"
            f"  percent_b = {round(test['percent_b'], 2):.2f}\n"
            f"     prop_a = {prop_a_display}\n"
            f"     prop_b = {prop_b_display}\n"
            f"  sig_level = {round(test['sig_level'], 4):.4f}\n"
            f"      power = {round(test['power'], 4):.4f}\n"
            f"alternative = {test['alternative']}"
        )
        print(output)

    return test
