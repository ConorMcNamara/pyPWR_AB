# Contributing to pyPWR_AB

First off, thank you for considering contributing to pyPWR_AB! It's people like you that make pyPWR_AB such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by common sense and mutual respect. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conor.s.mcnamara@gmail.com](mailto:conor.s.mcnamara@gmail.com).

## Getting Started

### Types of Contributions

We welcome many types of contributions:

- 🐛 **Bug Reports**: Report bugs through GitHub Issues
- 💡 **Feature Requests**: Suggest new features or enhancements
- 📝 **Documentation**: Improve or add to the documentation
- 🔧 **Code**: Fix bugs or implement new features
- ✅ **Tests**: Add or improve test coverage
- 🎨 **Examples**: Add usage examples or tutorials

### Before You Start

1. **Check existing issues**: Look through the [issue tracker](https://github.com/ConorMcNamara/pyPWR_AB/issues) to see if someone has already reported the issue or requested the feature.
2. **Create an issue**: For significant changes, create an issue first to discuss your plans with maintainers.
3. **Get feedback**: Wait for feedback before starting work on large features.

## Development Setup

### Prerequisites

- Python 3.13 or higher
- Git
- (Optional) Poetry for dependency management

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyPWR_AB.git
   cd pyPWR_AB
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

6. **Verify your setup**:
   ```bash
   make test
   make lint
   ```

### Using the Makefile

We provide a Makefile for common development tasks:

```bash
make help          # Show all available commands
make install       # Install the package in development mode
make test          # Run tests
make test-cov      # Run tests with coverage report
make lint          # Run all linters (ruff + mypy)
make format        # Format code with ruff
make clean         # Clean up build artifacts
```

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:

- **Clear title**: Descriptive summary of the issue
- **Description**: Detailed description of the problem
- **Steps to reproduce**: Minimal code example that demonstrates the issue
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Environment**:
  - Python version
  - Operating system
  - Package version
  - Relevant dependency versions

**Example:**

```markdown
## Bug: Incorrect power calculation for one-sided tests

### Description
The `ab_t2n` function returns incorrect power values when `alternative='less'`.

### Steps to Reproduce
```python
from pwrAB.pwr_tests import ab_t2n
result = ab_t2n(n=1000, percent_b=0.5, mean_diff=-0.2,
                sd_a=1, sd_b=1, sig_level=0.05, alternative='less')
print(result['power'])
```

### Expected
Power should be approximately 0.85

### Actual
Power is 0.15

### Environment
- Python 3.14
- pypwr-ab 1.0.0
- macOS 14.0
```

### Suggesting Features

When suggesting features, please include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: What alternatives have you considered?
- **Implementation ideas**: Any thoughts on how to implement it?

### Contributing Code

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following our [coding standards](#coding-standards)

3. **Write tests** for your changes

4. **Update documentation** as needed

5. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** on GitHub

## Pull Request Process

### Before Submitting

- ✅ Run all tests: `make test`
- ✅ Run linters: `make lint`
- ✅ Format code: `make format`
- ✅ Update documentation if needed
- ✅ Add entry to CHANGELOG.md under "Unreleased"
- ✅ Ensure all CI checks pass

### PR Guidelines

1. **Title**: Use a clear, descriptive title
   - ✅ Good: "Fix power calculation for one-sided tests"
   - ❌ Bad: "Fix bug"

2. **Description**: Include:
   - What changes were made
   - Why they were made
   - Related issue number (if applicable)
   - Breaking changes (if any)

3. **Small PRs**: Keep PRs focused and reasonably sized
   - One feature/fix per PR
   - If large, consider breaking into smaller PRs

4. **Review process**:
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, maintainers will merge

### PR Template

```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran to verify your changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] I have updated CHANGELOG.md
```

## Coding Standards

### Python Style

We follow modern Python best practices:

- **PEP 8**: Standard Python style guide
- **PEP 484**: Type hints for all functions
- **PEP 257**: Docstring conventions

### Code Quality Tools

- **ruff**: For linting and formatting
- **mypy**: For type checking
- **pytest**: For testing

### Type Hints

All functions must include type hints:

```python
def calculate_power(
    n: int,
    effect_size: float,
    alpha: float = 0.05,
) -> float:
    """Calculate statistical power."""
    ...
```

### Docstrings

Use NumPy-style docstrings:

```python
def ab_t2n(
    n: int | None = None,
    power: float | None = None,
) -> dict[str, Any]:
    """
    Perform power analysis for AB testing.

    Parameters
    ----------
    n : int, optional
        Total number of observations.
    power : float, optional
        Statistical power (1 - Type II error).

    Returns
    -------
    dict[str, Any]
        Dictionary containing test results.

    Raises
    ------
    ValueError
        If parameters are invalid.

    Examples
    --------
    >>> result = ab_t2n(n=1000, power=0.8)
    >>> print(result['effect_size'])
    0.123
    """
```

### Code Organization

- **Imports**: Grouped and sorted (stdlib, third-party, local)
- **Functions**: Keep functions focused and reasonably sized
- **Comments**: Explain "why", not "what"
- **Magic numbers**: Use named constants

### Example

```python
from __future__ import annotations

from typing import Any

import numpy as np
from scipy.stats import t as t_dist

# Constants
DEFAULT_ALPHA = 0.05
MIN_SAMPLE_SIZE = 10


def calculate_power(
    n: int,
    effect_size: float,
    alpha: float = DEFAULT_ALPHA,
) -> float:
    """Calculate statistical power for given parameters."""
    if n < MIN_SAMPLE_SIZE:
        msg = f"Sample size must be at least {MIN_SAMPLE_SIZE}"
        raise ValueError(msg)

    # Calculate degrees of freedom using Welch-Satterthwaite equation
    df = n - 2
    critical_value = t_dist.ppf(1 - alpha / 2, df)

    return float(1 - t_dist.cdf(critical_value, df, loc=effect_size))
```

## Testing Guidelines

### Writing Tests

- **Coverage**: Aim for >90% code coverage
- **Test names**: Use descriptive names that explain what is being tested
- **Arrange-Act-Assert**: Follow the AAA pattern
- **Fixtures**: Use pytest fixtures for common setup

### Test Example

```python
from __future__ import annotations

import pytest

from pwrAB import pwr_tests


class TestABT2n:
    """Test suite for ab_t2n function."""

    def test_power_calculation_two_sided(self) -> None:
        """Test power calculation with two-sided alternative."""
        # Arrange
        params = {
            "n": 3000,
            "percent_b": 0.3,
            "mean_diff": 0.15,
            "sd_a": 1,
            "sd_b": 2,
            "sig_level": 0.05,
            "alternative": "two-sided",
            "print_pretty": False,
        }

        # Act
        result = pwr_tests.ab_t2n(**params)

        # Assert
        assert result["power"] == pytest.approx(0.5701, abs=1e-4)

    def test_invalid_sample_size_raises_error(self) -> None:
        """Test that invalid sample size raises ValueError."""
        with pytest.raises(ValueError, match="at least 10"):
            pwr_tests.ab_t2n(
                n=5,
                percent_b=0.5,
                mean_diff=0.1,
                sig_level=0.05,
                power=0.8,
                print_pretty=False,
            )
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest test/test_pwr_tests.py -v

# Run specific test
pytest test/test_pwr_tests.py::TestABT2n::test_power_calculation_two_sided -v
```

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Fixing bugs that affect usage
- Adding examples

### Documentation Types

1. **Docstrings**: In-code documentation
2. **README.md**: Project overview and quick start
3. **CHANGELOG.md**: Version history
4. **Examples**: Usage examples in docstrings and README

### Documentation Style

- Use clear, concise language
- Include code examples
- Explain parameters and return values
- Document exceptions and edge cases

## Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: conor.s.mcnamara@gmail.com

### Recognition

Contributors will be recognized in:
- CHANGELOG.md for each release
- GitHub contributors page
- Special thanks for significant contributions

## Questions?

Don't hesitate to ask questions! We're here to help:

- Open a [GitHub Discussion](https://github.com/ConorMcNamara/pyPWR_AB/discussions)
- Email: conor.s.mcnamara@gmail.com

Thank you for contributing to pyPWR_AB! 🎉
