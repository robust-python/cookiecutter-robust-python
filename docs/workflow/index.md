# The Integrated Workflow

The true strength of the **cookiecutter-robust-python** template lies in how the chosen tools work together seamlessly to create a powerful, automated, and efficient developer workflow. This section details the typical lifecycle of development and how the different pieces of the toolchain fit together in practice.

This workflow is designed to be consistent whether you are developing locally, working within a containerized environment, or running automated checks and deployments in Continuous Integration (CI) and Continuous Deployment (CD) pipelines.

---

## Central Automation with Nox

At the heart of the template's workflow automation is **{nox}`Nox<>`** ([Task Automation (12)](../topics/12_task-automation.md)). {nox}`Nox<>` provides a single, standard command-line interface (CLI) for executing _all_ common development tasks defined in the `noxfile.py` file.

- To see available tasks: `uvx nox -l`
- To run a task: `uvx nox -s <session_name>`

Every significant automated process in this template – from linting and testing to building and publishing – is exposed as one or more {nox}`Nox<>` sessions. This simplifies the workflow by providing one tool (`uvx nox`) to remember and call for automation.

## The Local Development Loop

Here's how the template facilitates your day-to-day coding work:

1.  **Project Setup & Dependencies:** After cloning/generating the project, set up the virtual environment and install dependencies using **{uv}`uv<>`** ([Dependency Management (02)](../topics/02_dependency-management.md)):

    ```bash
    uv sync
    # Use uv add/remove to manage dependencies
    ```

    Your environment is isolated using standard virtual environments ({venv}`venv<>`/{virtualenv}`virtualenv<>`).

2.  **Code, Stage, and Commit:** As you write code, static analysis tools are often integrated into your editor via Language Server Protocol (LSP) for real-time feedback (using configurations like `pyrightconfig.json` ([Basedpyright (05)](../topics/05_type-checking.md)) and `.ruff.toml` ([Ruff (03, 04)](../topics/03_code-formatting.md))). When you're ready to commit changes:

    ```bash
    git add .
    git commit
    ```

    The **{pre-commit}`pre-commit<>`** framework ([Pre-commit Hooks (18)](../topics/18_pre-commit-hooks.md)) automatically runs configured hooks (like {ruff}`Ruff<>` formatter/linter with autofixes) on your staged files before the commit is finalized. This catches basic errors and style violations instantly.

3.  **On-Demand Local Checks:** For more comprehensive checks (full linting, type checking, security scans, running the test suite) _before_ pushing or for dedicated development cycles, use **{nox}`Nox<>`**:

    ```bash
    uvx nox -s check # Runs linters, type checker, security scans (Topic 04, 05, 08)
    uvx nox -s test  # Runs tests with coverage (Topic 06)
    # ... run other specific tasks
    ```

    {nox}`Nox<>` handles running these tools within the correct, consistent environments using {uv}`uv run<>`.

4.  **Local Container Development (Optional):** If your project involves multiple services or you prefer an encapsulated environment, use **Dev Containers** ([Containerized Development Environments (17)](../topics/17_dev-containers.md)) for a consistent development environment, and **{docker-compose}`Docker Compose<>`** ([Container Orchestration (Local) (15)](../topics/15_compose-local.md)) to orchestrate local multi-service stacks.
    ```bash
    # From project root with Docker/Podman running:
    # (Inside VS Code Dev Container or with compose installed)
    # docker compose up --build -d # Build images (Topic 11) and start services
    # docker compose logs -f      # View logs
    ```

## Automated Workflows: CI/CD

The workflow extends seamlessly to automation platforms using the Task Automation layer.

1.  **Continuous Integration (CI):** Triggered by pushes or pull requests. The CI configuration ([CI Orchestration (13)](../topics/13_ci-orchestration.md)) is a thin layer that:

    - Sets up the necessary Python version(s) and environment.
    - Installs {uv}`uv<>` and {nox}`Nox<>`.
    - Runs key Task Automation commands: `uvx nox -s check`, `uvx nox -s test`.
    - Collects reports ({junit}`JUnit XML<>`, {cobertura}`Cobertura XML<>`).
    - Reports status back to the version control platform.
      This process runs tests and checks reliably across the matrix of Python versions defined in the `noxfile.py` and potentially operating systems supported by the CI platform.

2.  **Continuous Deployment / Delivery (CD):** Triggered by events like successful CI runs on the main branch or Git tags. The CD configuration ([CD Orchestration (14)](../topics/14_cd-orchestration.md)) is also a thin orchestration layer:
    - Sets up the environment.
    - Manages secure credentials ({pypi-trusted-publishers}`API tokens<>` for PyPI, registry secrets).
    - Runs Task Automation commands to build artifacts: `uvx nox -s build:package` ([Packaging Build (09)](../topics/09_packaging-build.md)), `uvx nox -s build:container` ([Container Build (11)](../topics/11_container-build.md)).
    - Runs Task Automation commands to publish artifacts: `uvx nox -s publish` ([Packaging Publishing (10)](../topics/10_packaging-publish.md)), or uses Docker CLI to push container images.

## Release Management

When preparing a project release (often following Conventional Commits practice), use **{commitizen}`Commitizen<>`** ([Task Automation (12)](../topics/12_task-automation.md)) via {nox}`Nox<>`:

```bash
# Example: bump version based on commit history, create tag
uvx nox -s release -- [major|minor|patch|...] # Use uvx nox to run commitizen
```

This automates version string updates, tag creation, and changelog generation, often triggering the CD pipeline upon pushing the new tag.

## Production Deployment

The artifacts produced by the CI/CD workflow (standard packages and container images) are inputs for production deployment. The template's outputs are compatible with standard production orchestration tools and platforms ([Deployment to Production Orchestrators (16)](../topics/16_prod-deploy-guidance.md)) like Kubernetes (managed via {helm}`Helm<>` or {argocd}`Argo CD<>`) or serverless platforms. The template itself does not include specific production infrastructure configuration but ensures its outputs can be consumed by these systems.

---

This integrated workflow provides a comprehensive development lifecycle, from coding to deployment, leveraging automation, standards, and reliable tools orchestrated by {nox}`Nox<>` to provide a consistent and efficient experience across environments.
