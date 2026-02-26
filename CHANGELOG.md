# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project documentation (CONTRIBUTING.md, MANIFEST.in, Makefile)
- Pre-commit hooks configuration with ruff, mypy, and standard checks
- Modern GitHub Actions workflows for testing and code quality
- PEP 561 compliance with py.typed marker for type hint distribution
- Extensive test coverage configuration with pytest-cov
- Professional README with badges, examples, and complete documentation

### Changed
- Modernized type hints to use Python 3.10+ syntax (`int | None` instead of `Union[int, None]`)
- Updated all imports to use `from __future__ import annotations`
- Improved error messages with more descriptive, formatted strings
- Enhanced pyproject.toml with complete project metadata and modern build configuration
- Replaced flake8 with ruff in CI/CD workflows
- Updated GitHub Actions to latest versions (v4, v5)
- Made `print_pretty` a keyword-only argument in public API functions
- Improved code formatting and consistency throughout codebase
- Configured mypy with pragmatic settings for scientific computing
- Removed auto-commit behavior from CI workflows (best practice)

### Fixed
- Spelling error in error message: `pro_b` → `prop_b` (pwr_classes.py:346)
- Missing space in docstring parameter (pwr_tests.py:108)
- Type hints for `prop_a` and `prop_b` to properly reflect `float | list[float] | None`
- Unreachable code in validation logic
- Strategic type ignores for NumPy/SciPy type compatibility

### Developer Experience
- Added Makefile with 30+ common development tasks
- Improved test structure with modern pytest patterns
- Added comprehensive contributing guidelines
- Enhanced code quality tooling (ruff, mypy, pre-commit)
- Better documentation for all public APIs

## [1.0.0] - 2024-XX-XX

### Added
- Initial release of pyPWR_AB
- `ab_t2n()` function for power analysis with continuous outcomes
- `ab_t2n_prop()` function for power analysis with proportion outcomes
- Welch's t-test implementation for unequal variances
- Support for two-sided, greater, and less alternative hypotheses
- Flexible allocation ratios between groups A and B
- Pretty printing of results

### Features
- Calculate statistical power given sample size and effect
- Calculate required sample size given power and effect
- Calculate minimum detectable effect given sample size and power
- Calculate optimal group allocation
- Calculate significance level given other parameters
- Support for unequal variances between groups
- Root-finding algorithms for parameter estimation

## Version History

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

### Release Notes

#### [1.0.0] - Initial Release
First stable release of pyPWR_AB, a Python port of the R pwrAB package.

**Key Features:**
- Power analysis for AB testing with continuous and proportion outcomes
- Welch's t-test for handling unequal variances
- Flexible parameter solving (any one parameter can be solved for)
- Clean, typed API following modern Python best practices

**Compatibility:**
- Python 3.10+
- NumPy 2.2.3+
- SciPy 1.15.2+

**Documentation:**
- Comprehensive README with examples
- Full API documentation in docstrings
- Contributing guidelines
- MIT License

---

## Categories Explanation

### Added
New features or capabilities that have been introduced.

### Changed
Changes to existing functionality that don't break backwards compatibility.

### Deprecated
Features that are being phased out and will be removed in future versions.

### Removed
Features that have been completely removed.

### Fixed
Bug fixes and corrections.

### Security
Security vulnerability fixes and improvements.

---

## How to Update This Changelog

When contributing, please add your changes to the **[Unreleased]** section under the appropriate category. Follow these guidelines:

1. **Be Specific**: Clearly describe what changed and why
2. **Reference Issues**: Include issue numbers when applicable (e.g., "Fixed #123")
3. **User-Focused**: Write from the user's perspective
4. **Actionable**: Include migration steps for breaking changes

### Example Entry

```markdown
## [Unreleased]

### Added
- New `calculate_effect_size()` helper function for common effect size calculations (#42)

### Changed
- Improved performance of `ab_t2n()` by 30% through optimized variance calculations (#45)

### Fixed
- Fixed incorrect power calculation when `alternative='less'` and negative effect sizes (#48)
```

---

## Links

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [GitHub Releases](https://github.com/ConorMcNamara/pyPWR_AB/releases)

[Unreleased]: https://github.com/ConorMcNamara/pyPWR_AB/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ConorMcNamara/pyPWR_AB/releases/tag/v1.0.0
