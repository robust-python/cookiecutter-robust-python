# General Usage

This section provides a guide to using the core features and workflows provided by the `cookiecutter-robust-python` template after you have generated a project. It covers common development tasks and how to leverage the template's integrated toolchain.

Make sure you have completed the steps in the [Quickstart](quickstart.md) guide first.

---

## Dependency Management with uv

Your project uses {uv}`uv<>` to manage dependencies, environments, and basic project tasks. The primary configuration is in `pyproject.toml` ([Topic 01](topics/01_project-structure.md), [Topic 02](topics/02_dependency-management.md)).

- **Add a new dependency:**

  ```bash
  uv add <package_name> [==<version_specifier>] [--group <optional_group>]
  # Example: uv add requests --group dev # Add requests to the dev group
  ```

  This updates `pyproject.toml`, resolves the dependency, and updates `uv.lock`.

- **Remove a dependency:**

  ```bash
  uv remove <package_name> [--group <optional_group>]
  ```

- **Install/Update dependencies:**

  ```bash
  uv sync # Installs/updates deps based on pyproject.toml and uv.lock into your .venv
  uv sync --locked # Ensures installation strictly follows uv.lock (recommended in automation)
  uv update <package_name> # Updates a specific package and its dependents within constraints
  uv update # Updates all packages within constraints and uv.lock
  ```

- **Run commands in environment:**

  ```bash
  uv run <command> [args...] # Executes a command within the project's virtual environment
  # Example: uv run pytest # Runs pytest in the environment
  ```

- **Manage Environments:**
  ```bash
  uv venv # Creates a new virtual environment (.venv by default)
  # For alternative venv locations or naming, see uv documentation
  # Manual activation: source .venv/bin/activate (Linux/macOS), .venv\Scripts\activate.bat (Windows cmd)
  ```

Refer to the {uv}`uv documentation<>` for more advanced usage.

## Code Quality Checks

The template provides a suite of tools for maintaining code quality, integrated via Task Automation ([Topic 12](topics/12_task-automation.md)) and pre-commit ([Topic 18](topics/18_pre-commit-hooks.md)).

- **Format Code:** Code formatting and import sorting is handled by {ruff}`Ruff<>` ([Topic 03](topics/03_code-formatting.md)) using the configuration in `.ruff.toml`. Your pre-commit hooks automatically fix these on commit. To format manually:

  ```bash
  uvx nox -s format-python # Format Python code with Ruff
  uvx nox -s lint-python   # Lint Python code with Ruff (includes formatting check)
  ```

- **Lint Code:** Linting checks for code style (beyond formatting), errors, potential bugs, and code smells using {ruff}`Ruff<>` and {pydocstyle}`pydocstyle<>` ([Topic 04](topics/04_code-linting.md)). Run checks via Task Automation:

  ```bash
  uvx nox -s lint-python
  ```

- **Type Check Code:** Static type analysis using {pyright}`Pyright<>` ([Topic 05](topics/05_type-checking.md)) based on `pyrightconfig.json`:

  ```bash
  uvx nox -s typecheck
  ```

- **Security Checks:** Scan for dependency vulnerabilities with {pip-audit}`pip-audit<>` and code security issues with {bandit-bandit}`Bandit<>` ([Topic 08](topics/08_security-checks.md)):

  ```bash
  uvx nox -s security-python
  ```

- **Run All Core Checks:**
  ```bash
  # Run individual checks:
  uvx nox -s format-python lint-python typecheck security-python
  # Or use quality tag:
  uvx nox -t quality
  ```

## Testing

The template uses {pytest-pytest-cov}`pytest<>` ([Topic 06](topics/06_testing-coverage.md)) as the test framework.

- **Write Tests:** Place test files (e.g., `test_*.py` or `*_test.py`) in the `tests/` directory.
- **Run Tests with Coverage:**
  ```bash
  uvx nox -s tests-python
  ```
  This runs tests across applicable Python versions and measures code coverage with {coveragepy}`coverage.py<>` ([Topic 06](topics/06_testing-coverage.md)) based on `.coveragerc`. Reports are generated (JUnit XML for CI, terminal summary).

## Building and Publishing

Create and publish your package following Python standards ([Topic 09](topics/09_packaging-build.md), [Topic 10](topics/10_packaging-publish.md)).

- **Build Package:** Create standard `sdist` (`.tar.gz`) and `wheel` (`.whl`) files in the `dist/` directory.
  ```bash
  uvx nox -s build-python
  ```
- **Publish Package:** Upload built packages using {uv}`uv<>`'s publish command. Requires credentials set via environment variables (e.g., `UV_TOKEN` or `TWINE_API_KEY`).
  ```bash
  uvx nox -s publish-python
  ```

## Containerization

Define and build Docker container images for your application ([Topic 11](topics/11_container-build.md)) and orchestrate multi-service local setups ([Topic 15](topics/15_compose-local.md)).

- **Build Application Image:** Uses the `Dockerfile` in the project root.
  ```bash
  uvx nox -s build-container
  ```
- **Run with Docker Compose:**
  ```bash
  docker compose up --build -d # Or podman compose up --build -d
  ```
  This uses the `compose.yaml` file.

## Release Management

Use {commitizen}`Commitizen<>` ([Topic 12](topics/12_task-automation.md)) via {uv}`uvx<>` to manage project versions based on Conventional Commits and create Git tags.

- **Bump Version:** Automatically determine the next version (major, minor, patch, etc.) based on commit messages since the last tag, update version strings, and create a Git tag.
  ```bash
  uvx nox -s setup-release -- [major|minor|patch] # e.g., uvx nox -s setup-release -- minor
  ```
  Follow the prompts. Requires following {conventional-commits}`Conventional Commits<>`. Pushing the resulting tag often triggers the CD pipeline.

## Advanced Usage & Customization

- **Template Update Management:** Use {cruft}`cruft<>` to update your project from newer versions of the template. (See [Template Maintenance](maintenance.md) in the template documentation for maintainers).
- **CI/CD Configuration:** Explore the example workflow files in `.github/workflows/` (etc.) and adapt them to your specific needs ([Topic 13](topics/13_ci-orchestration.md), [Topic 14](topics/14_cd-orchestration.md)).
- **Custom Task Automation:** Modify the `noxfile.py` to add or change automation tasks ([Topic 12](topics/12_task-automation.md)).
- **Tool Configuration:** Adjust the configuration files (e.g., `.ruff.toml`, `pyrightconfig.json`) to tailor tool behavior to your project's specific requirements. Refer to each tool's official documentation (linked from the [Criteria](criteria.md) and [Toolchain Topics](topics/index.md) pages).
- **Dev Container Customization:** Modify the `.devcontainer/` configuration for specific editor settings or tools needed in the container ([Topic 17](topics/17_dev-containers.md)).
- **Native Extensions:** If you chose to add Rust extensions during template generation, see the `rust/` directory and the role of {maturin}`Maturin<>` in the build process ([Topic 09](topics/09_packaging-build.md)).
- **Production Deployment:** Review guidance on deploying the generated artifacts to production ([Topic 16](topics/16_prod-deploy-guidance.md)).

This guide covers the main interactions you will have with the template's toolchain. The remaining documentation topics provide the in-depth rationale and evaluation process that led to these choices.
