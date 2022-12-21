from pwrAB.pwr_classes import ab_t2n_class, ab_t2n_prop_class

def ab_t2n(
    n: int = None,
    percent_b: float = None,
    mean_diff: float = None,
    sd_a: float = 1,
    sd_b: float = 1,
    sig_level: float = None,
    power: float = None,
    alternative: str = "two-sided",
    max_sample: int = 1e07,
    print_pretty: bool = True
) -> dict:
    """AB_t2n performs the power analysis for AB testing. It uses the Welch’s t-test, which allows for the standard
    deviation to vary across groups.

    Parameters
    ----------
    n: int, default=None
        Total number of observations (sum of observations for groups A and B)
    percent_b: float, default=None
        Percentage of total observations allocated to group B (between 0 and 1 - e.g. input 0.5 for 50%)
    mean_diff: float, default=None
        Difference in means of the two groups, with mean_B - mean_A
    sd_a: float, default=1
        Standard deviation of group A
    sd_b: float, default=1
        Standard deviation of group B
    sig_level: float, default=None
        Significance level (Type I error probability)
    power: float, default=None
        Power of test (1 minus Type II error probability)
    alternative: {'two-sided', 'greater', 'less'}
        Character string specifying the alternative hypothesis
    max_sample: int, default=1e07
        Maximum sample size that is searched for
    print_pretty: bool, default=True
        Whether we want our results printed our not

    Returns
    -------
    A dictionary containing n, percent_b, mean_diff, power and the sig_level of a t-test
    """
    if not any(v is None for v in [n, percent_b, mean_diff, power, sig_level]):
        raise ValueError(
            "At least one of n, percent_b, mean_diff, power, and sig_level must be None"
        )
    if sum([v is None for v in [n, percent_b, mean_diff, power, sig_level]]) > 1:
        raise ValueError("Exactly one of n, percent_b, mean_diff, power, and sig_level may be None")
    if sd_a is None or sd_b is None:
        raise ValueError("Both sd_a and sd_b must be specified")
    if sig_level is not None and (sig_level < 0 or sig_level > 1):
        raise ValueError("alpha must be between 0 and 1")
    if power is not None and (power < 0 or power > 1):
        raise ValueError("power must be between 0 and 1")
    if n is not None and n < 10:
        raise ValueError("n must be at least 10")
    test = ab_t2n_class(n, percent_b, mean_diff, sd_a, sd_b, sig_level, power, alternative, max_sample).pwr_test()
    if print_pretty:
        print(
            " " * 2 +
            f"{test['method']}"
            + "\n" * 2
            + " " * 10
            + f"N = {test['n']}"
            + "\n"
            + " " * 2
            + f"percent_b = {round(test['percent_b'], 2)}"
            + "\n"
            + " " * 2
            + f"mean_diff = {round(test['mean_diff'], 4)}"
            + "\n"
            + " " * 7
            + f"sd_a = {round(test['sd_a'], 4)}"
            + "\n"
            + " " * 7
            + f"sd_b = {round(test['sd_b'], 4)}"
            + "\n"
            + " " * 2
            + f"sig_level = {round(test['sig_level'], 4)}"
            + "\n"
            + " " * 6
            + f"power = {round(test['power'], 4)}"
            + "\n"
            + f"alternative = {test['alternative']}"
        )
    return test


def ab_t2n_prop(
        prop_a: float = None,
        prop_b: float = None,
        n: int = None,
        percent_b: float = None,
        sig_level: float = None,
        power: float = None,
        alternative: str = "two-sided",
        max_sample: int = 1e+07,
        print_pretty: bool = True,
) -> dict:
    """AB_t2n_prop performs the power analysis for AB testing, and when dependent variables are proportions
    (between 0 and 1). It uses the Welch’s t-test, which allows for the standard deviation to vary across groups.

    Parameters
    ----------
    prop_a: float,default=None
        Proportion of successes in group A (between 0 and 1)
    prop_b: float, default=None
        Proportion of successes in group B (between 0 and 1)
    n: int, default=None
        Total number of observations (sum of observations for groups A and B)
    percent_b: float, default=None
        Percentage of total observations allocated to group B (between 0 and 1 - e.g. input 0.5 for 50%)
    sig_level: float, default=None
        Significance level (Type I error probability)
    power: float, default=None
        Power of test (1 minus Type II error probability)
    alternative: {'two-sided', 'greater', 'less'}
        Character string specifying the alternative hypothesis
    max_sample: int, default=1e07
        Maximum sample size that is searched for
    print_pretty: bool, default=True
        Whether we want our results printed our not

    Returns
    -------
    A dictionary containing prop_a, prop_b, n, percent_b, sig_level and power of our test
    """
    if not any(v is None for v in [n, percent_b, prop_a, prop_b, power, sig_level]):
        raise ValueError(
            "At least one of n, percent_b, prop_a, prop_b, power, and sig_level must be None"
        )
    if sum([v is None for v in [n, percent_b, prop_a, prop_b, power, sig_level]]) > 1:
        raise ValueError("Exactly one of n, percent_b, prop_a, prop_b, power, and sig_level may be None")
    if sig_level is not None and (sig_level < 0 or sig_level > 1):
        raise ValueError("alpha must be between 0 and 1")
    if power is not None and (power < 0 or power > 1):
        raise ValueError("power must be between 0 and 1")
    if n is not None and n < 10:
        raise ValueError("n must be at least 10")
    test = ab_t2n_prop_class(prop_a, prop_b, n, percent_b, sig_level, power, alternative, max_sample).pwr_test()
    if print_pretty:
        prop_a = [round(i, 4) for i in test["prop_a"]] if isinstance(test["prop_a"], list) else test["prop_a"]
        prop_b = [round(i, 4) for i in test["prop_b"]] if isinstance(test["prop_b"], list) else test["prop_b"]
        print(
            " " * 2 +
            f"{test['method']}"
            + "\n" * 2
            + " " * 10
            + f"N = {test['n']}"
            + "\n"
            + " " * 2
            + f"percent_b = {round(test['percent_b'], 2)}"
            + "\n"
            + " " * 5
            + f"prop_a = {prop_a}"
            + "\n"
            + " " * 5
            + f"prop_b = {prop_b}"
            + "\n"
            + " " * 2
            + f"sig_level = {round(test['sig_level'], 4)}"
            + "\n"
            + " " * 6
            + f"power = {round(test['power'], 4)}"
            + "\n"
            + f"alternative = {test['alternative']}"
        )
    return test
