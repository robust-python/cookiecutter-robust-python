# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **cookiecutter-robust-python**, a Cookiecutter template for generating production-ready Python projects with modern tooling. The template itself is meta-code that generates complete Python projects with CI/CD, testing, documentation, and optional Rust extension support.

**Key Distinction**: This repository contains both:
1. The **template source** (root level files and `{{cookiecutter.project_name}}/` directory)
2. Development tools for **managing and testing** the template (in `tools/` package and `noxfile.py`)

## Essential Commands

### Template Development

```bash
# Install template development dependencies
uv sync --all-groups

# Install pre-commit hooks for the template
uvx nox -s pre-commit -- install

# Lint template's own Python files (tools/, hooks/, etc.)
uvx nox -s lint

# Build template documentation (the docs you're reading)
uvx nox -s docs

# Run template tests
uvx nox -s test

# Generate a demo project to test template output
uvx nox -s generate-demo

# Update existing demo projects
uvx nox -s update-demo

# Lint the generated demo project
uvx nox -s lint-from-demo

# Clear demo cache (if permissions get corrupted)
uvx nox -s clear-cache

# List all available nox sessions
uvx nox -l
```

### Template Release

```bash
# Release the template using Commitizen (bumps version, creates tag)
uvx nox -s release-template

# Push release to remote
git push origin HEAD --tags
```

## Architecture & Key Concepts

### Template Structure

The template uses **Cookiecutter** with **Jinja2 templating** to generate projects:

- `{{cookiecutter.project_name}}/` - The actual template directory that gets rendered
- `cookiecutter.json` - Template variables (project_name, license, Python versions, etc.)
- `hooks/post_gen_project.py` - Post-generation cleanup (removes conditional files based on choices)
- `tools/` - Development tools package (demo generation, linting, utilities)
- `docs/` - Template documentation (Sphinx, explains tooling decisions and philosophy)
- `noxfile.py` - Template development automation (orchestrates tools package)
- `.env` - Default environment variables for template development (committed to repo)
- `.env.local` - Local environment variable overrides (git-ignored, per-user)

### Cookiecutter Variables

Key template variables that control generation:
- `project_name` - Kebab-case name (e.g., "my-project")
- `package_name` - Snake_case Python package name (auto-derived)
- `friendly_name` - Title case display name (auto-derived)
- `min_python_version` / `max_python_version` - Python version support range
- `repository_provider` - Choice: github, gitlab, or bitbucket
- `add_rust_extension` - Boolean: enables Maturin/Rust support
- `license` - Choice: MIT, Apache-2.0, GPL-3.0

### Generated Project Structure

When the template is rendered, it creates a Python project with:

**Source Code**:
- `src/{{package_name}}/` - Main package with CLI entry point (Typer)
- `tests/` - Organized as unit_tests/, integration_tests/, acceptance_tests/
- `scripts/` - Project setup scripts (setup-venv.py, setup-git.py, etc.)
- `docs/` - Sphinx documentation

**Configuration**:
- `pyproject.toml` - PEP 517 build config, UV dependencies, conditional Maturin/setuptools
- `noxfile.py` - 15+ nox sessions (lint, test, docs, build, release, etc.)
- `.ruff.toml` - Ruff linter/formatter (120 char lines, Google docstrings)
- `pyrightconfig.json` - Pyright type checker (strict mode)
- `.cz.toml` - Commitizen semantic versioning config
- `.pre-commit-config.yaml` - Pre-commit hooks

**CI/CD** (conditional based on repository_provider):
- `.github/workflows/` - GitHub Actions (lint, test, security, docs, release)
- `.gitlab-ci.yml` - GitLab CI pipeline
- `bitbucket-pipelines.yml` - Bitbucket Pipelines

### Demo Projects

The template maintains auto-generated demo projects to validate template output:
- Location: `~/.cache/cookiecutter-robust-python/project_demos/` (configurable via env var)
- Default demo: `robust-python-demo` and `robust-maturin-demo` (with Rust extension)
- Used for integration testing and as living examples

### Tools Package Architecture

The `tools/` package contains the development infrastructure for template management:

**Core Modules**:
- `tools/config.py` - Centralized environment loading and configuration constants
- `tools/util.py` - Shared utilities (git operations, demo generation helpers)
- `tools/demo.py` - Demo generation and update logic
- `tools/lint.py` - Lint-from-demo functionality (applies linting changes back to template)
- `tools/docs.py` - Documentation utilities (generates dependency tables)

**Key Features**:
- Direct function calls from `noxfile.py` (no subprocess overhead)
- Comprehensive type hints throughout
- Logging via `loguru` for consistent output
- Reusable logic for future tooling needs

### Environment Configuration

The template uses environment variables to support user-agnostic demo management:

**Default Configuration** (`.env`, committed):
```bash
COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR=robust-python
COOKIECUTTER_ROBUST_PYTHON_MAIN_BRANCH=main
COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH=develop
```

**Custom Configuration** (`.env.local`, git-ignored):
Create `.env.local` at the template root to override defaults for your setup:
```bash
COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR=my-org
COOKIECUTTER_ROBUST_PYTHON_MAIN_BRANCH=master
COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH=development
```

The configuration loader checks `.env` first, then applies any overrides from `.env.local`, allowing each developer to maintain their own demo repositories without modifying committed files.

## Working with the Template

### Modifying Template Files

When editing files in `{{cookiecutter.project_name}}/`:
1. Use Jinja2 syntax for variables: `{{cookiecutter.variable_name}}`
2. Use conditionals for optional features: `{% if cookiecutter.add_rust_extension == "true" %}...{% endif %}`
3. **Important**: The Ruff config excludes `{{cookiecutter.project_name}}/` from linting to avoid Jinja syntax errors

### Testing Template Changes

1. Make changes to template files
2. Generate a demo: `uvx nox -s generate-demo`
3. Navigate to demo: `cd ~/.cache/cookiecutter-robust-python/project_demos/robust-python-demo`
4. Test the generated project: `uvx nox -s test` (inside demo)
5. Lint from template root: `uvx nox -s lint-from-demo`

### Post-Generation Hook

`hooks/post_gen_project.py` runs after project generation to:
- Reindent `.cookiecutter.json` to 2-space format (Prettier compatibility)
- Remove files not applicable to selected options (unused CI/CD configs, Rust files if not selected)
- Handle Windows readonly file permissions

### Documentation Philosophy

The template's docs (`docs/topics/`) explain **why** tooling decisions were made, not just **what** tools are used. This allows future maintainers to evaluate if decisions are still valid. When updating major tools, also update the relevant topic documentation.

## Common Development Patterns

### Adding a New Tool to Generated Projects

1. Add dependency to `{{cookiecutter.project_name}}/pyproject.toml`
2. Add configuration file if needed (e.g., `.tool-name.toml`)
3. Add nox session in `{{cookiecutter.project_name}}/noxfile.py`
4. Add CI/CD workflow if applicable
5. Document in `docs/topics/` with rationale
6. Update demo and test: `uvx nox -s generate-demo`

### Supporting a New Repository Provider

1. Add choice to `cookiecutter.json` `repository_provider`
2. Create CI/CD config file in `{{cookiecutter.project_name}}/` (e.g., `.new-provider-ci.yml`)
3. Add conditional logic in `hooks/post_gen_project.py` to remove unused CI files
4. Test with demo using new provider choice

### Updating Python Version Support

1. Update `min_python_version` / `max_python_version` in `cookiecutter.json`
2. Update `requires-python` in `{{cookiecutter.project_name}}/pyproject.toml`
3. Update test matrices in CI/CD workflows
4. Update `noxfile.py` Python version parametrization
5. Update `.readthedocs.yml` if needed

## Tool Stack

**Template Development**:
- UV - Dependency management
- Nox - Task automation
- Cookiecutter - Template engine
- Cruft - Template update propagation
- Sphinx - Documentation
- Loguru - Structured logging
- Python-dotenv - Environment configuration

**Generated Projects**:
- UV - Package/dependency management
- Ruff - Linting and formatting
- Pyright - Type checking
- Pytest - Testing with coverage
- Bandit + pip-audit - Security scanning
- Commitizen - Semantic versioning
- Typer - CLI framework
- Sphinx - Documentation
- Maturin (optional) - Rust extension building

## Important Notes

### Conventional Commits

The template uses Conventional Commits for semantic versioning. Commit messages should follow:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `refactor:` - Code refactoring

### Multi-OS Support

The template is designed for Windows, Linux, and macOS. Be mindful of:
- Path separators (use `pathlib.Path`)
- File permissions (especially in post-gen hook)
- Shell commands in CI/CD (test on multiple platforms)

### Template vs Generated Project

Always be clear which context you're working in:
- **Template level**: Root `noxfile.py`, `tools/` package, template docs, `.env` configuration
- **Generated project level**: `{{cookiecutter.project_name}}/noxfile.py`, generated scripts, generated configuration

Commands like `uvx nox -s lint` run on template source code, while `uvx nox -s lint-from-demo` lints the generated demo project and applies changes back to the template source.
