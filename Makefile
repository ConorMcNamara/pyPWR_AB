.PHONY: help install install-dev test test-cov test-watch lint format type-check clean clean-build clean-pyc clean-test build publish publish-test pre-commit run-example docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
RUFF := ruff
MYPY := mypy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install package in production mode
	$(PIP) install -e .

install-dev: ## Install package with development dependencies
	$(PIP) install -e ".[dev]"
	pre-commit install

# Testing targets
test: ## Run tests
	$(PYTEST) test/ -v

test-cov: ## Run tests with coverage report
	$(PYTEST) test/ -v --cov=pwrAB --cov-report=term-missing --cov-report=html --cov-report=xml

test-watch: ## Run tests in watch mode
	$(PYTEST) test/ -v --watch

test-all: ## Run all tests across multiple Python versions (requires tox)
	tox

# Code quality targets
lint: ## Run all linters (ruff + mypy)
	@echo "Running ruff check..."
	$(RUFF) check .
	@echo "\nRunning mypy..."
	$(MYPY) pwrAB --ignore-missing-imports
	@echo "\n✅ All linting checks passed!"

format: ## Format code with ruff
	@echo "Formatting code with ruff..."
	$(RUFF) format .
	@echo "✅ Code formatted!"

format-check: ## Check if code is formatted (CI mode)
	$(RUFF) format --check .

type-check: ## Run type checking with mypy
	$(MYPY) pwrAB --ignore-missing-imports

# Cleaning targets
clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artifacts

clean-build: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## Remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## Remove test and coverage artifacts
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml

# Build and publish targets
build: clean ## Build source and wheel package
	$(PYTHON) -m build

publish: build ## Build and publish package to PyPI
	@echo "Publishing to PyPI..."
	$(PYTHON) -m twine upload dist/*
	@echo "✅ Published to PyPI!"

publish-test: build ## Build and publish package to TestPyPI
	@echo "Publishing to TestPyPI..."
	$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "✅ Published to TestPyPI!"

# Pre-commit targets
pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks to latest versions
	pre-commit autoupdate

# Development workflow targets
check: format lint test ## Run formatting, linting, and tests (full check)
	@echo "\n✅ All checks passed! Ready to commit."

ci: format-check lint test ## Run CI checks (format check, lint, test)
	@echo "\n✅ All CI checks passed!"

# Example target
run-example: ## Run a quick example
	@$(PYTHON) -c "from pwrAB.pwr_tests import ab_t2n; result = ab_t2n(n=3000, percent_b=0.3, mean_diff=0.15, sd_a=1, sd_b=2, sig_level=0.05, alternative='two-sided'); print(f\"Power: {result['power']:.4f}\")"

# Version management
version: ## Show current version
	@$(PYTHON) -c "from pwrAB import __version__; print(__version__)"

# Dependencies management
update-deps: ## Update all dependencies to latest versions
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --upgrade -e ".[dev]"

freeze-deps: ## Freeze current dependencies to requirements.txt
	$(PIP) freeze > requirements-frozen.txt

# Documentation targets
docs: ## Generate documentation (placeholder for future)
	@echo "Documentation generation not yet implemented"

# Git helpers
git-status: ## Show git status with branch info
	@echo "Current branch:"
	@git branch --show-current
	@echo "\nStatus:"
	@git status --short

# Info targets
info: ## Show project information
	@echo "Project: pyPWR_AB"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Location: $(shell pwd)"
	@echo "Version: $(shell $(PYTHON) -c 'from pwrAB import __version__; print(__version__)')"
	@echo "Python Path: $(shell which $(PYTHON))"

# Quick development cycle
dev: format lint test ## Quick development cycle: format, lint, and test
	@echo "\n✅ Development cycle complete!"

# Install all dev tools
bootstrap: ## Bootstrap development environment from scratch
	$(PYTHON) -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Unix/macOS)"
	@echo "  venv\\Scripts\\activate     (Windows)"
	@echo "Then run: make install-dev"
