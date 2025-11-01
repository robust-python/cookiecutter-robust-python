# Contributing to {{ cookiecutter.project_name }}

Thank you for your interest in contributing to `{{ cookiecutter.package_name }}`! We welcome bug reports, feature requests, and code contributions that help improve this project.

By participating in this project, you are expected to uphold our [Code of Conduct][code-of-conduct].

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on our [issue tracker][issues] with:

- A clear description of the bug
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment details (Python version, OS, etc.)
- Relevant error messages or logs

### Suggesting Features

For feature requests, please open an issue with:

- A clear description of the proposed feature
- The problem it would solve or use case it would address
- Any relevant examples or mockups
- Consideration of potential alternatives

### Contributing Code

We welcome pull requests! For significant changes, it's best to open an issue first to discuss the approach.

## Development Setup

### Prerequisites

- Python {{ cookiecutter.min_python_version }}+ (this project supports Python {{ cookiecutter.min_python_version }}-{{ cookiecutter.max_python_version }})
- [uv][uv-documentation] for dependency management
- Git for version control

### Setting Up Your Development Environment

1. **Fork and clone the repository:**

   ```bash
   git clone https://{{ cookiecutter.repository_host }}/{{ cookiecutter.repository_path }}.git
   cd {{ cookiecutter.project_name }}
   ```

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Set up pre-commit hooks:**

   ```bash
   uvx nox -s pre-commit -- install
   ```

4. **Verify your setup:**
   ```bash
   uvx nox -l  # List available development tasks
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following our coding standards (see below)

3. **Test your changes:**

   ```bash
   # Run the full test suite
   uvx nox -s tests-python

   # Run tests for a specific Python version
   uvx nox -s tests-python-{{ cookiecutter.max_python_version.replace('.', '') }}

   # Run a specific test file
   uvx nox -s tests-python -- tests/unit_tests/test_specific.py
   ```

4. **Check code quality:**

   ```bash
   # Format code
   uvx nox -s format-python

   # Lint code
   uvx nox -s lint-python

   # Type check
   uvx nox -s typecheck

   # Security checks
   uvx nox -s security-python

   # Or run all checks at once
   uvx nox -t ci
   ```

5. **Update documentation if needed:**
   ```bash
   # Build docs locally
   uvx nox -s build-docs
   ```

### Coding Standards

This project follows these standards:

- **Code formatting:** [Ruff][ruff-documentation] (automatically applied by pre-commit)
- **Linting:** Ruff with comprehensive rule set
- **Type checking:** [Pyright][pyright-documentation]
- **Security:** [Bandit][bandit-documentation] for security linting
- **Commit messages:** [Conventional Commits][conventional-commits] format preferred
- **Testing:** [pytest][pytest-documentation] with good coverage

### Testing Guidelines

- Write tests for new functionality in the appropriate test directory:
  - `tests/unit_tests/` - Fast, isolated unit tests
  - `tests/integration_tests/` - Tests that involve multiple components
  - `tests/acceptance_tests/` - End-to-end behavior tests
- Aim for good test coverage (check with `uvx nox -s coverage`)
- Use descriptive test names and docstrings
- Mock external dependencies appropriately

## Submitting Changes

### Pull Request Process

1. **Push your branch** to your fork
2. **Open a pull request** with:

   - Clear title describing the change
   - Description explaining what and why
   - Link to any relevant issues
   - Note any breaking changes

3. **Ensure CI passes** - all automated checks must pass
4. **Respond to review feedback** if requested
5. **Squash commits** if requested before merge

### Pull Request Guidelines

- Keep changes focused and atomic
- Update documentation for user-facing changes
- Add tests for new functionality
- Follow the existing code style
- Ensure all CI checks pass

## Development Tasks Reference

Common Nox sessions for development:

```bash
# Code quality
uvx nox -s format-python    # Format with Ruff
uvx nox -s lint-python      # Lint with Ruff
uvx nox -s typecheck        # Type check with Pyright
uvx nox -s security-python  # Security checks

# Testing
uvx nox -s tests-python     # Run full test suite
uvx nox -s coverage         # Generate coverage report

# Documentation
uvx nox -s build-docs       # Build documentation

# Building
uvx nox -s build-python     # Build package

# Run everything CI runs
uvx nox -t ci               # All CI checks
```

## Getting Help

- Check existing [issues][issues]{% if cookiecutter.repository_provider == 'github' %} and [discussions][discussions]{% endif %}
- Open a new issue for bugs or feature requests
- Start a discussion for questions or ideas

## Recognition

Contributors will be recognized in our release notes and documentation. Thank you for helping make this project better!

---

_This project was generated from the [cookiecutter-robust-python][cookiecutter-robust-python] template._

<!-- Reference Links -->

[code-of-conduct]: CODE_OF_CONDUCT.md
[issues]: https://{{ cookiecutter.repository_host }}/{{ cookiecutter.repository_path }}/issues
{% if cookiecutter.repository_provider == 'github' %}[discussions]: https://{{ cookiecutter.repository_host }}/{{ cookiecutter.repository_path }}/discussions{% endif %}
[uv-documentation]: https://docs.astral.sh/uv/
[ruff-documentation]: https://docs.astral.sh/ruff/
[pyright-documentation]: https://github.com/microsoft/pyright
[bandit-documentation]: https://bandit.readthedocs.io/
[conventional-commits]: https://www.conventionalcommits.org/
[pytest-documentation]: https://docs.pytest.org/
[cookiecutter-robust-python]: https://github.com/robust-python/cookiecutter-robust-python
