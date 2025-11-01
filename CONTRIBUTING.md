# Contributing to cookiecutter-robust-python

Thank you for considering contributing to the `cookiecutter-robust-python` template! We welcome contributions that help improve the template, keep its tooling current, and enhance its documentation.

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

There are several ways to contribute:

1.  **Reporting Bugs:** If you find an issue with the template itself (e.g., it doesn't generate correctly, the generated project's workflow doesn't work on a specific OS, a tool is misconfigured), please open an issue on the [issue tracker](https://github.com/robust-python/cookiecutter-robust-python/issues). Provide clear steps to reproduce the bug.
2.  **Suggesting Enhancements:** Have an idea for a new feature, a different tool choice you think is better, or an improvement to the template structure or documentation? Open an issue on the [issue tracker](https://github.com/robust-python/cookiecutter-robust-python/issues) to discuss your suggestion. Clearly articulate the proposed change and the rationale behind it, ideally referencing the template's philosophy and criteria ([Template Philosophy](https://56kyle.github.io/cookiecutter-robust-python/philosophy.html), [Criteria for Tool Selection](https://56kyle.github.io/cookiecutter-robust-python/criteria.html)).
3.  **Submitting Code Contributions:** Ready to contribute code (e.g., fix a bug, implement a suggested enhancement, update a tool version)? Please fork the repository and submit a Pull Request.

## Setting Up Your Development Environment

Refer to the **[Getting Started: Contributing to the Template](https://56kyle.github.io/cookiecutter-robust-python/getting-started-template-contributing.html)** section in the template documentation for instructions on cloning the repository, installing template development dependencies (using uv), setting up the template's pre-commit hooks, and running template checks/tests.

## Contribution Workflow

1.  **Fork** the repository and **clone** your fork.
2.  Create a **new branch** for your contribution based on the main branch. Use a descriptive name (e.g., `fix/ci-workflow-on-windows`, `feat/update-uv-version`).
3.  Set up your development environment following the [Getting Started](https://56kyle.github.io/cookiecutter-robust-python/getting-started-template-contributing.html) guide (clone, `uv sync`, `uvx nox -s pre-commit -- install`).
4.  Make your **code or documentation changes**.
5.  Ensure your changes adhere to the template's **code quality standards** (configured in the template's `.pre-commit-config.yaml`, `.ruff.toml`, etc.). The pre-commit hooks will help with this. Run `uvx nox -s lint`, `uvx nox -s check` in the template repository for more comprehensive checks.
6.  Ensure your changes **do not break existing functionality**. Run the template's test suite: `uvx nox -s test`. Ideally, add tests for new functionality or bug fixes.
7.  Ensure the **template documentation builds correctly** with your changes: `uvx nox -s docs`.
8.  Write clear, concise **commit messages** following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification where possible, especially for significant changes (fixes, features, chore updates, etc.).
9.  **Push** your branch to your fork.
10. **Open a Pull Request** from your branch to the main branch of the main template repository. Provide a clear description of your changes. Link to any relevant issues.

## Updating Tool Evaluations

If your contribution involves updating a major tool version or suggesting a different tool entirely, you **must** update the relevant sections in the template's documentation (`docs/topics/` files) to reflect the changes in configuration, behavior, or re-justify the choice based on the current state of the tools and criteria. This is crucial for keeping the documentation accurate and useful over time.

## Communication

For questions or discussion about contributions, open an issue or a discussion on the [GitHub repository](https://github.com/robust-python/cookiecutter-robust-python).

---
