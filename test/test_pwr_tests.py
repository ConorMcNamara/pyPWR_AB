from __future__ import annotations

import numpy as np
import pytest

from pwrAB import pwr_tests


class TestABT2n:
    """Test suite for ab_t2n function."""

    @staticmethod
    def test_power_results() -> None:
        """Test power calculation with known parameters."""
        power_results = pwr_tests.ab_t2n(
            n=3000,
            percent_b=0.3,
            mean_diff=0.15,
            sd_a=1,
            sd_b=2,
            sig_level=0.05,
            alternative="two-sided",
            print_pretty=False,
        )["power"]
        # AB_t2n(N = 3000, percent_B = .3, mean_diff = .15, sd_A = 1, sd_B = 2,
        #        sig_level = .05, alternative = 'two_sided')
        #      t-test Power Calculation
        #
        #               N = 3000
        #       percent_B = 0.3
        #       mean_diff = 0.15
        #            sd_A = 1
        #            sd_B = 2
        #       sig_level = 0.05
        #           power = 0.5700792
        #     alternative = two_sided
        expected = 0.5700792
        assert power_results == pytest.approx(expected, abs=1e-05)

    @staticmethod
    def test_n_results() -> None:
        n_results = pwr_tests.ab_t2n(
            percent_b=0.3,
            mean_diff=0.15,
            sd_a=1,
            sd_b=2,
            sig_level=0.05,
            power=0.8,
            alternative="two-sided",
            max_sample=1e05,
            print_pretty=False,
        )["n"]
        # AB_t2n(percent_B = .3, mean_diff = .15, sd_A = 1,
        # +        sd_B = 2, sig_level = .05, power = .8, alternative = 'two_sided')
        #
        #      t-test Power Calculation
        #
        #               N = 5154.769
        #       percent_B = 0.3
        #       mean_diff = 0.15
        #            sd_A = 1
        #            sd_B = 2
        #       sig_level = 0.05
        #           power = 0.8
        #     alternative = two_sided
        expected = 5_155
        assert n_results == expected

    @staticmethod
    def test_mean_diff_results() -> None:
        mean_diff_results = pwr_tests.ab_t2n(
            n=3_000,
            percent_b=0.3,
            sd_a=1,
            sd_b=2,
            sig_level=0.05,
            power=0.8,
            alternative="less",
            print_pretty=False,
        )["mean_diff"]
        # AB_t2n(N = 3000, percent_B = .3, sd_A = 1,
        # +        sd_B = 2, sig_level = .05, power = .8, alternative = 'less')
        #
        #      t-test Power Calculation
        #
        #               N = 3000
        #       percent_B = 0.3
        #       mean_diff = -0.1745265
        #            sd_A = 1
        #            sd_B = 2
        #       sig_level = 0.05
        #           power = 0.8
        #     alternative = less
        expected = -0.1745265
        assert mean_diff_results == pytest.approx(expected, abs=1e-05)

    @staticmethod
    def test_sig_level_results() -> None:
        sig_level_results = pwr_tests.ab_t2n(
            n=1500,
            percent_b=0.3,
            mean_diff=0.3,
            sd_a=1,
            sd_b=2,
            power=0.8,
            alternative="greater",
            print_pretty=False,
        )["sig_level"]
        # AB_t2n(N = 1500, percent_B = .3, mean_diff = 0.3, sd_A = 1,
        # +        sd_B = 2, power = .8, alternative = 'greater')
        #
        #      t-test Power Calculation
        #
        #               N = 1500
        #       percent_B = 0.3
        #       mean_diff = 0.3
        #            sd_A = 1
        #            sd_B = 2
        #       sig_level = 0.01477979
        #           power = 0.8
        #     alternative = greater
        expected = 0.01477979
        assert sig_level_results == pytest.approx(expected, abs=1e-05)

    @staticmethod
    def test_percent_b_results() -> None:
        percent_b_results = pwr_tests.ab_t2n(
            n=1500,
            mean_diff=0.3,
            sd_a=1,
            sd_b=2,
            sig_level=0.10,
            power=0.8,
            alternative="two-sided",
            print_pretty=False,
        )["percent_b"]
        # AB_t2n(N = 1500, mean_diff = 0.3, sd_A = 1,
        # +        sd_B = 2, sig_level = 0.10, power = .8, alternative = 'two_sided')
        #
        #      t-test Power Calculation
        #
        #               N = 1500
        #       percent_B = 0.1951667
        #       mean_diff = 0.3
        #            sd_A = 1
        #            sd_B = 2
        #       sig_level = 0.1
        #           power = 0.8
        #     alternative = two_sided
        expected = 0.1951667
        assert percent_b_results == pytest.approx(expected, abs=1e-05)


class TestABPropT2n:
    """Test suite for ab_t2n_prop function."""

    @staticmethod
    def test_power_results() -> None:
        """Test power calculation with proportion parameters."""
        power_results = pwr_tests.ab_t2n_prop(
            prop_a=0.2,
            prop_b=0.25,
            n=3_000,
            percent_b=0.3,
            sig_level=0.05,
            alternative="two-sided",
            print_pretty=False,
        )["power"]
        # AB_t2n_prop(prop_A = .2, prop_B = .25, N = 3000, percent_B = .3,
        # +             sig_level = .05, alternative = 'two_sided')
        #
        #      t-test Power Calculation
        #
        #               N = 3000
        #       percent_B = 0.3
        #          prop_A = 0.2
        #          prop_B = 0.25
        #       sig_level = 0.05
        #           power = 0.8419403
        #     alternative = two_sided
        expected = 0.8419403
        assert power_results == pytest.approx(expected, abs=1e-05)

    @staticmethod
    def test_n_results() -> None:
        n_results = pwr_tests.ab_t2n_prop(
            prop_a=0.8,
            prop_b=0.5,
            n=None,
            percent_b=0.3,
            power=0.8,
            sig_level=0.05,
            alternative="less",
            print_pretty=False,
        )["n"]
        # AB_t2n_prop(prop_A = 0.8, prop_B = 0.5, N = NULL, percent_B = .3, power = .8, sig_level = .05,
        # alternative = 'less')
        #
        #      t-test Power Calculation
        #
        #               N = 75.94481
        #       percent_B = 0.3
        #          prop_A = 0.8
        #          prop_B = 0.5
        #       sig_level = 0.05
        #           power = 0.8
        #     alternative = less
        expected = 76
        assert n_results == expected

    @staticmethod
    def test_percent_b_results() -> None:
        percent_b_results = pwr_tests.ab_t2n_prop(
            prop_a=0.4,
            prop_b=0.8,
            n=500,
            percent_b=None,
            power=0.8,
            sig_level=0.05,
            alternative="greater",
            print_pretty=False,
        )["percent_b"]
        # AB_t2n_prop(prop_A = 0.4, prop_B = 0.8, N = 500, percent_B = NULL, power = .8, sig_level = .05,
        # alternative = 'greater')
        #
        #      t-test Power Calculation
        #
        #               N = 500
        #       percent_B = 0.02
        #          prop_A = 0.4
        #          prop_B = 0.8
        #       sig_level = 0.05
        #           power = 0.8
        #     alternative = greater
        expected = 0.02
        assert percent_b_results == pytest.approx(expected, abs=1e-03)

    @staticmethod
    def test_prop_b_results() -> None:
        prop_b_results = pwr_tests.ab_t2n_prop(
            prop_a=0.2,
            n=3_000,
            percent_b=0.3,
            power=0.8,
            sig_level=0.05,
            alternative="two-sided",
            print_pretty=False,
        )["prop_b"]
        # AB_t2n_prop(prop_A = .2, N = 3000, percent_B = .3, power = .8, sig_level = .05, alternative = 'two_sided')
        #
        #      t-test Power Calculation
        #
        #               N = 3000
        #       percent_B = 0.3
        #          prop_A = 0.2
        #          prop_B = 0.1580145, 0.2471605
        #       sig_level = 0.05
        #           power = 0.8
        #     alternative = two_sided
        expected = [0.1580145, 0.2471605]
        np.testing.assert_allclose(prop_b_results, expected, atol=1e-04)


@staticmethod
def test_prop_a_results() -> None:
    prop_a_results = pwr_tests.ab_t2n_prop(
        prop_b=0.4,
        n=3_000,
        percent_b=0.3,
        power=0.8,
        sig_level=0.05,
        alternative="two-sided",
        print_pretty=False,
    )["prop_a"]
    # AB_t2n_prop(prop_B = .4, N = 3000, percent_B = .3, power = .8, sig_level = .05, alternative = 'two_sided')
    #
    #      t-test Power Calculation
    #
    #               N = 3000
    #       percent_B = 0.3
    #          prop_A = 0.3457812, 0.4549985
    #          prop_B = 0.4
    #       sig_level = 0.05
    #           power = 0.8
    #     alternative = two_sided'
    expected = [0.3457812, 0.4549985]
    np.testing.assert_allclose(prop_a_results, expected, atol=1e-04)


if __name__ == "__main__":
    pytest.main()
