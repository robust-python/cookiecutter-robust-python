# Contributing to cookiecutter-robust-python

Thank you for considering contributing to the `cookiecutter-robust-python` template! We welcome contributions that help improve the template, keep its tooling current, and enhance its documentation.

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

There are several ways to contribute:

1.  **Reporting Bugs:** If you find an issue with the template itself (e.g., it doesn't generate correctly, the generated project's workflow doesn't work on a specific OS, a tool is misconfigured), please open an issue on the [issue tracker](https://github.com/robust-python/cookiecutter-robust-python/issues). Provide clear steps to reproduce the bug.
2.  **Suggesting Enhancements:** Have an idea for a new feature, a different tool choice you think is better, or an improvement to the template structure or documentation? Open an issue on the [issue tracker](https://github.com/robust-python/cookiecutter-robust-python/issues) to discuss your suggestion. Clearly articulate the proposed change and the rationale behind it, ideally referencing the template's philosophy and criteria ([Template Philosophy](https://robust-python.github.io/cookiecutter-robust-python/philosophy.html), [Criteria for Tool Selection](https://robust-python.github.io/cookiecutter-robust-python/criteria.html)).
3.  **Submitting Code Contributions:** Ready to contribute code (e.g., fix a bug, implement a suggested enhancement, update a tool version)? Please fork the repository and submit a Pull Request.

## Setting Up Your Development Environment

1.  **Clone** the repository:
    ```bash
    git clone https://github.com/robust-python/cookiecutter-robust-python.git
    cd cookiecutter-robust-python
    ```

2.  **Install dependencies** using uv:
    ```bash
    uv sync --all-groups
    ```

3.  **Install pre-commit hooks**:
    ```bash
    uvx nox -s pre-commit -- install
    ```

4.  **Generate a demo project** to test changes:
    ```bash
    nox -s generate-demo
    ```

Refer to the **[Getting Started: Contributing to the Template](https://robust-python.github.io/cookiecutter-robust-python/getting-started-template-contributing.html)** section in the template documentation for more detailed instructions.

## Development Commands

### Code Quality
```bash
# Lint the template source code
nox -s lint

# Lint from generated demo project
nox -s lint-from-demo

# Run template tests
nox -s test

# Build template documentation
nox -s docs
```

### Demo Projects
```bash
# Generate a demo project for testing
nox -s generate-demo

# Generate demo with Rust extension
nox -s generate-demo -- --add-rust-extension

# Update existing demo projects
nox -s update-demo

# Clear demo cache
nox -s clear-cache
```

## Contribution Workflow

1.  **Fork** the repository and **clone** your fork.
2.  Create a **new branch** for your contribution based on the `develop` branch. Use a descriptive name (e.g., `fix/ci-workflow-on-windows`, `feat/update-uv-version`).
3.  Set up your development environment as described above.
4.  Make your **code or documentation changes**.
5.  Ensure your changes adhere to the template's **code quality standards**. Run:
    ```bash
    nox -s lint
    nox -s test
    ```
6.  Ensure the **template documentation builds correctly**:
    ```bash
    nox -s docs
    ```
7.  Write clear, concise **commit messages** following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This is **required** as we use Commitizen to generate changelogs automatically.
8.  **Push** your branch to your fork.
9.  **Open a Pull Request** from your branch to the `develop` branch of the main repository. Provide a clear description of your changes. Link to any relevant issues.

## Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages. This enables automatic changelog generation via Commitizen.

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files

### Examples
```
feat(template): add support for Python 3.13
fix(ci): correct workflow trigger for demo sync
docs(readme): update installation instructions
chore(deps): bump ruff to 0.12.0
```

## Versioning

This template uses **Calendar Versioning (CalVer)** with the format `YYYY.MM.MICRO`:
- `YYYY`: Four-digit year
- `MM`: Month (1-12, no leading zero)
- `MICRO`: Incremental patch number, resets to 0 each new month

Releases are handled automatically via CI when changes are merged to `main`. Contributors do not need to bump versions manually.

## Updating Tool Evaluations

If your contribution involves updating a major tool version or suggesting a different tool entirely, you **must** update the relevant sections in the template's documentation (`docs/topics/` files) to reflect the changes in configuration, behavior, or re-justify the choice based on the current state of the tools and criteria. This is crucial for keeping the documentation accurate and useful over time.

## Communication

For questions or discussion about contributions, open an issue or a discussion on the [GitHub repository](https://github.com/robust-python/cookiecutter-robust-python).
