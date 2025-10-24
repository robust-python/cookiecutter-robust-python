# Template Maintenance

This section is aimed at contributors and maintainers of the **cookiecutter-robust-python** template itself. It covers the processes and tools for keeping the template up-to-date, ensuring its continued quality and relevance as the Python ecosystem evolves.

Maintaining a project template is an ongoing effort that involves updating dependencies, incorporating new tooling best practices, ensuring compatibility, and managing template releases.

---

## Template Dependencies and Development Environment

The `cookiecutter-robust-python` template repository is itself a project with dependencies needed for its development and maintenance. These include `cookiecutter`, the specific versions of the tools evaluated (to ensure compatibility and test against them), and maintenance-specific tools (like {commitizen}`Commitizen<>` for template versioning, {nox}`Nox<>` for template task automation, potentially testing frameworks for the template's functionality).

The template's `pyproject.toml` file at the **template repository root** lists these dependencies.

To set up your environment for working _on the template_, clone the repository and install its dependencies:

```bash
git clone https://github.com/56kyle/cookiecutter-robust-python.git # **UPDATE WITH TEMPLATE REPO URL**
cd cookiecutter-robust-python
uv sync # This installs deps from the template's pyproject.toml into a .venv for template dev
```

Refer to the [Getting Started: Contributing to the Template](getting-started-template-contributing.md) guide for initial setup details.

## Customizing Template Development with .env.local

The template uses environment variables to make demo generation and repository management scripts user-agnostic. Default values are provided in `.env` at the template repository root.

### Available Environment Variables

- `COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR` - App author name used for cache directory paths (default: `robust-python`)
- `COOKIECUTTER_ROBUST_PYTHON_MAIN_BRANCH` - Main branch name for version control (default: `main`)
- `COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH` - Development branch name (default: `develop`)

### Overriding Defaults

If you maintain your own forks of the demo repositories or use different branch conventions, create a `.env.local` file at the template repository root (this file is git-ignored and will not be committed):

```bash
# .env.local (not committed to git)
COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR=my-org
COOKIECUTTER_ROBUST_PYTHON_MAIN_BRANCH=master
COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH=development
```

Alternatively, you can set these as system environment variables directly, and the `.env.local` file will override them if present.

## Task Automation for Template Maintenance

The template repository uses its own `noxfile.py` at the **template repository root** (separate from the `noxfile.py` generated in projects) to automate common template maintenance tasks. These tasks run within the template's development environment.

### Architecture

The noxfile imports from a `tools/` package that provides reusable Python modules for template management:

- `tools/config.py` - Centralized environment variable loading and configuration constants
- `tools/util.py` - Shared utilities (git operations, demo generation, repository validation)
- `tools/demo.py` - Demo generation and update logic
- `tools/lint.py` - Lint-from-demo functionality (applies linting changes back to the template)
- `tools/docs.py` - Documentation generation utilities

This structure allows the noxfile to call functions directly instead of running subprocess scripts, reducing overhead and improving maintainability.

### Running Tasks

1.  **List Available Template Tasks:**

    ```bash
    uvx nox -l # See tasks defined in the template's noxfile.py
    ```

2.  **Run Core Template Checks:**
    This runs checks and tests _on the template's source code and functionality_ itself (e.g., linting the template's Python scripts, ensuring it renders correctly).

    ```bash
    uvx nox # Runs the default sessions for template maintenance
    # Often equivalent to: uvx nox -s check -s test
    ```

3.  **Build Template Documentation:**
    This builds the documentation you are currently reading, using the Sphinx configuration (`docs/conf.py`) at the template root.
    ```bash
    uvx nox -s docs # Builds the template's sphinx documentation site
    ```

4.  **Generate and Update Demo Projects:**
    ```bash
    uvx nox -s generate-demo      # Create a demo project from the current template
    uvx nox -s update-demo        # Update existing demo projects to the latest template version
    uvx nox -s lint-from-demo     # Lint a generated demo and apply changes back to template
    uvx nox -s clear-cache        # Clear the demo project cache if needed
    ```

## Keeping Template Tooling and Dependencies Current

As the tools recommended by the template ({uv}`uv<>`, {ruff}`Ruff<>`, {pyright}`Pyright<>`, {pytest-pytest-cov}`pytest<>`, etc.) release new versions, you will need to:

1.  **Update Template Dependencies:** Manually update the version specifiers for the desired tools in the template's **`pyproject.toml` at the template root**. Run `uv sync` at the template root to update the template's own `uv.lock` file with the new versions.
2.  **Update Template Configuration:** Review release notes for the updated tools. Modify the **separate configuration files** (like `.ruff.toml`, `pyrightconfig.json`, `.coveragerc`) and `pyproject.toml` (e.g., `[tool.uv]`, `[tool.pytest]`) within the **template structure** (e.g., `{{cookiecutter.project_slug}}/pyproject.toml`, `{{cookiecutter.project_slug}}/.ruff.toml`) if the tools have breaking changes in configuration or recommended settings.
3.  **Test Template:** Run the template's own checks and tests (`uvx nox`) to ensure the template still functions correctly and generates projects with working workflows using the new tool versions. This is crucial! Consider adding tests that render a project and run its default checks/tests within the template's own CI.
4.  **Update Pre-commit Hook `rev`s:** For tools used as {pre-commit}`pre-commit<>` hooks, update the `rev` (version hash/tag) for those hooks in the template's **`.pre-commit-config.yaml` at the template root** to match tested, compatible versions of the hook repositories. You can use `uvx nox -s pre-commit -- autoupdate` in the template repository to update these `rev`s interactively.
5.  **Update CI/CD Example Configs:** Ensure the versions referenced in example CI/CD workflow files (`.github/workflows/`, `bitbucket-pipelines.yml`, etc.) are current and consistent with the tested tool versions (e.g., Python versions tested against, commands to install uv/Nox if pinned).
6.  **Update Documentation:** **CRITICAL.** If tool updates change behavior, configuration, workflow steps, or even render previous justifications less valid, **update the documentation** (specifically the `docs/topics/` files) to reflect the current state and rationale. This ensures the documentation remains accurate and the justifications for tool choices are based on the _current_ versions and understanding.

## Keeping Generated Projects Updated

A project generated from this template is a copy at a point in time. Template updates do **not** automatically apply to existing generated projects. We recommend using **{cruft}`cruft<>`** to help manage updates in projects _after_ they've been generated:

1.  **Ensure `cruft` is Used:** During template generation, the `{{cookiecutter.project_slug}}` should have a `.cruft.json` file created (handled automatically by {cruft}`cruft<>` if the template is run via `cruft create`, or added as a post-gen hook). This file tracks the template version used.
2.  **Instruct Users on `cruft`:** The documentation _within the generated project's_ `docs/` (e.g., the Getting Started guide) should clearly explain how to use `cruft` (`cruft check`, `cruft update`) to bring in changes from template updates. You can mention running `uvx nox -s cruft-check` (if you add a Nox session for this) or integrating `cruft check --exit-code` into the generated project's CI workflow to alert users of template updates.

## Releasing a New Template Version

Releasing a new version of the template itself follows a standard process, often managed with Git tags and automation. This template uses Calendar Versioning (YYYY.MM.DD) for its releases.

1.  **Finalize Changes:** Ensure all desired updates for the release are committed to the main branch of the template repository.
2.  **Verify Template Health:** Run the full suite of checks and tests for the template itself (`uvx nox`) to confirm it's functioning correctly.
3.  **Run Commitizen Bump:** Use {commitizen}`Commitizen<>` (installed as a dev dependency in the template repo) to automatically bump the calendar version string(s) in your template files (e.g., `docs/conf.py`), create a Git tag (e.g., `2025.04.28`), and generate/update a `CHANGELOG.md` for the template repository.
    ```bash
    uvx cz bump # Run in template repo root; follow prompts. Updates version, tags, changelog.
    ```
    _Note: Ensure your `.cz.toml` in the template root is configured for Calendar Versioning and updates the correct file(s)._
4.  **Push Release Tag:** Push the new commit(s) (if Commitizen makes any, like changelog updates) and the release tag to the remote template repository:
    ```bash
    git push origin main --tags # Or the branch the tag was created on
    ```
5.  **Trigger Template CD:** Pushing the tag triggers any configured CD pipelines _for the template repository itself_. This typically includes building and deploying the template documentation website based on the new version, and potentially building/uploading template artifacts if you distribute them that way.

## Documenting Template Changes

Maintain a `CHANGELOG.md` file at the **template repository root** to clearly document the changes included in each template release (often generated automatically by {commitizen}`Commitizen<>`). This helps users understand the benefits and potential impacts of updating their generated projects to a newer template version. Link to specific documentation topics if updates involve significant changes in tooling or workflows.
