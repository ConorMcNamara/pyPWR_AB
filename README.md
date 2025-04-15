# pyPWR_AB

A Python implementation of the [pwrAB](https://cran.r-project.org/web/packages/pwrAB/index.html) R package; a library
for calculating the power, sample size and minimum detectable effect of t-tests using the Welch unequal variances formula. 

To quote the documentation

> Power analysis for AB testing. The calculations are based on the Welch's unequal variances t-test, which is generally preferred over the Student's t-test when sample sizes and variances of the two groups are unequal, which is frequently the case in AB testing. In such situations, the Student's t-test will give biased results due to using the pooled standard deviation, unlike the Welch's t-test.

## Quick Example

```
from pwrAB.pwr_tests import ab_t2n
results = ab_t2n(n=3000, percent_b=0.3, mean_diff=0.15, sd_a=1, sd_b=2, sig_level=0.05, alternative='two-sided')
print(round(results["power"]), 4)
0.5701
```

## Notes

Whenever possible, I tried to follow the R naming and code-style to ensure as much 1-1 comparison as possible; however,
some liberties were taken to ensure the code follows PEP-8 guidelines.

## References

William Cha. (2017). pwrAB: Power Analysis for AB Testing. https://cran.r-project.org/web/packages/pwrAB/index.html
