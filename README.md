# pyPWR_AB

[![Tests](https://github.com/ConorMcNamara/pyPWR_AB/actions/workflows/python-package.yml/badge.svg)](https://github.com/ConorMcNamara/pyPWR_AB/actions/workflows/python-package.yml)
[![Code Quality](https://github.com/ConorMcNamara/pyPWR_AB/actions/workflows/linter.yml/badge.svg)](https://github.com/ConorMcNamara/pyPWR_AB/actions/workflows/linter.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python implementation of the [pwrAB](https://cran.r-project.org/web/packages/pwrAB/index.html) R package for power analysis in AB testing. This library calculates statistical power, required sample size, and minimum detectable effect for t-tests using **Welch's unequal variances formula**.

## Why Welch's t-test?

> Power analysis for AB testing. The calculations are based on Welch's unequal variances t-test, which is generally preferred over the Student's t-test when sample sizes and variances of the two groups are unequal, which is frequently the case in AB testing. In such situations, the Student's t-test will give biased results due to using the pooled standard deviation, unlike the Welch's t-test.

## ✨ Features

- 🎯 **Power Analysis**: Calculate statistical power for AB tests with continuous or proportion outcomes
- 📊 **Sample Size Calculation**: Determine required sample size for desired power
- 📈 **Effect Size Detection**: Find minimum detectable effect given constraints
- ⚖️ **Unequal Variances**: Uses Welch's t-test for robust analysis when variances differ
- 🔄 **Flexible Allocation**: Support for unequal group sizes (e.g., 70/30 splits)
- 🐍 **Modern Python**: Type hints, comprehensive documentation, and clean API

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Continuous Outcomes](#continuous-outcomes)
  - [Proportion Outcomes](#proportion-outcomes)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## 🚀 Installation

### Via pip (recommended)

```bash
pip install pypwr-ab
```

### Via Poetry

```bash
poetry add pypwr-ab
```

### From source

```bash
git clone https://github.com/ConorMcNamara/pyPWR_AB.git
cd pyPWR_AB
pip install -e .
```

## 🎯 Quick Start

```python
from pwrAB.pwr_tests import ab_t2n

# Calculate power given sample size and effect
results = ab_t2n(
    n=3000,
    percent_b=0.3,
    mean_diff=0.15,
    sd_a=1,
    sd_b=2,
    sig_level=0.05,
    alternative='two-sided'
)

print(f"Statistical Power: {results['power']:.4f}")
# Output: Statistical Power: 0.5701
```

## 📚 Usage Examples

### Continuous Outcomes

#### Calculate Required Sample Size

```python
from pwrAB.pwr_tests import ab_t2n

# Find sample size needed for 80% power
results = ab_t2n(
    percent_b=0.3,        # 30% in group B
    mean_diff=0.15,       # Expected effect size
    sd_a=1,               # Standard deviation group A
    sd_b=2,               # Standard deviation group B
    sig_level=0.05,       # Alpha level
    power=0.8,            # Desired power
    alternative='two-sided'
)

print(f"Required sample size: {results['n']}")
# Output: Required sample size: 5155
```

#### Calculate Minimum Detectable Effect

```python
from pwrAB.pwr_tests import ab_t2n

# Find minimum effect detectable with given constraints
results = ab_t2n(
    n=3000,
    percent_b=0.3,
    sd_a=1,
    sd_b=2,
    sig_level=0.05,
    power=0.8,
    alternative='less'  # One-sided test
)

print(f"Minimum detectable effect: {results['mean_diff']:.4f}")
```

#### Calculate Optimal Group Allocation

```python
from pwrAB.pwr_tests import ab_t2n

# Find optimal allocation between groups
results = ab_t2n(
    n=1500,
    mean_diff=0.3,
    sd_a=1,
    sd_b=2,
    sig_level=0.10,
    power=0.8,
    alternative='two-sided'
)

print(f"Optimal allocation to group B: {results['percent_b']:.2%}")
```

### Proportion Outcomes

#### Calculate Power for Conversion Rate Test

```python
from pwrAB.pwr_tests import ab_t2n_prop

# Calculate power for a conversion rate experiment
results = ab_t2n_prop(
    prop_a=0.20,     # 20% conversion in control
    prop_b=0.25,     # 25% conversion in treatment
    n=3000,
    percent_b=0.3,
    sig_level=0.05,
    alternative='two-sided'
)

print(f"Statistical Power: {results['power']:.4f}")
# Output: Statistical Power: 0.8419
```

#### Calculate Required Sample Size for Proportions

```python
from pwrAB.pwr_tests import ab_t2n_prop

# Find sample size for proportion test
results = ab_t2n_prop(
    prop_a=0.20,
    prop_b=0.25,
    percent_b=0.5,   # Equal allocation
    sig_level=0.05,
    power=0.8,
    alternative='two-sided'
)

print(f"Required sample size: {results['n']}")
```

#### Find Detectable Proportion Difference

```python
from pwrAB.pwr_tests import ab_t2n_prop

# Find detectable proportions given constraints
results = ab_t2n_prop(
    prop_a=0.2,      # Fixed baseline
    n=3000,
    percent_b=0.3,
    power=0.8,
    sig_level=0.05,
    alternative='two-sided'
)

print(f"Detectable prop_b values: {results['prop_b']}")
# Output: Detectable prop_b values: [0.1580, 0.2472]
```

## 📖 API Reference

### `ab_t2n()`

Power analysis for continuous outcomes.

**Parameters:**
- `n` (int, optional): Total sample size
- `percent_b` (float, optional): Proportion allocated to group B (0-1)
- `mean_diff` (float, optional): Difference in means (mean_B - mean_A)
- `sd_a` (float): Standard deviation of group A (default: 1)
- `sd_b` (float): Standard deviation of group B (default: 1)
- `sig_level` (float, optional): Significance level (Type I error)
- `power` (float, optional): Statistical power (1 - Type II error)
- `alternative` (str): 'two-sided', 'greater', or 'less' (default: 'two-sided')
- `max_sample` (int): Maximum sample size for search (default: 1e7)
- `print_pretty` (bool): Print formatted results (default: True)

**Returns:** Dictionary with test parameters and results

**Note:** Exactly one of {n, percent_b, mean_diff, sig_level, power} must be None.

### `ab_t2n_prop()`

Power analysis for proportion outcomes.

**Parameters:**
- `prop_a` (float, optional): Proportion in group A (0-1)
- `prop_b` (float, optional): Proportion in group B (0-1)
- `n` (int, optional): Total sample size
- `percent_b` (float, optional): Proportion allocated to group B (0-1)
- `sig_level` (float, optional): Significance level
- `power` (float, optional): Statistical power
- `alternative` (str): 'two-sided', 'greater', or 'less' (default: 'two-sided')
- `max_sample` (int): Maximum sample size for search (default: 1e7)
- `print_pretty` (bool): Print formatted results (default: True)

**Returns:** Dictionary with test parameters and results

**Note:** Exactly one of {n, percent_b, prop_a, prop_b, sig_level, power} must be None.

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ConorMcNamara/pyPWR_AB.git
cd pyPWR_AB

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pwrAB --cov-report=html

# Run specific test file
pytest test/test_pwr_tests.py -v
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy pwrAB --ignore-missing-imports
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

1. Follow [PEP 8](https://pep8.org/) style guidelines
2. Add type hints to all functions
3. Write docstrings for public APIs
4. Add tests for new features
5. Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This library is a Python port of the [pwrAB](https://cran.r-project.org/web/packages/pwrAB/index.html) R package. While the implementation follows modern Python best practices, the core methodology and API design are inspired by the original R package to enable easy comparison and migration.

## 📚 References

- Cha, William. (2017). *pwrAB: Power Analysis for AB Testing*. R package version 0.1.0. https://cran.r-project.org/web/packages/pwrAB/index.html
- Welch, B. L. (1947). *The generalization of "Student's" problem when several different population variances are involved*. Biometrika, 34(1-2), 28-35.

## 📮 Contact

- **Author**: Conor McNamara
- **Email**: conor.s.mcnamara@gmail.com
- **GitHub**: [@ConorMcNamara](https://github.com/ConorMcNamara)
- **Issues**: [GitHub Issues](https://github.com/ConorMcNamara/pyPWR_AB/issues)

---

Made with ❤️ by the Python community
