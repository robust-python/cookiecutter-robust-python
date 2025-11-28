# Our Chosen Toolchain: The cookiecutter-robust-python Stack

After extensively evaluating various tools against the established criteria (see [Criteria](criteria.md)) derived from the template's philosophy ([Template Philosophy](philosophy.md)), this document presents the curated set of recommended tools and practices that form the foundation of `cookiecutter-robust-python`.

This summary provides a concise overview of the chosen tool(s) for each defined topic area, the primary reason for their selection, and how they integrate into the overall workflow. For the detailed evaluations, including comparisons with alternative tools and specific criteria breakdowns, please refer to the individual [Toolchain Topics](topics/index.md) pages.

---

## Foundation Principles Reflected in Tooling:

- **Performance & Automation:** Prioritizing fast, reliable execution for automated workflows.
- **Standards & Compatibility:** Adhering to relevant PEPs and widely supported formats for broad interoperability.
- **Maintainability & Simplicity:** Choosing tools that contribute to long-term project health through clarity and reduced complexity.
- **OS Interoperability:** Core tools work seamlessly across Linux, macOS, and Windows.

---

## The cookiecutter-robust-python Stack Overview

Here is the breakdown of the chosen tool(s) for each defined area:

- **01: Project Structure and Basic Setup:**

  - **Chosen:** `pyproject.toml` (PEP 621) with `src/` layout.
  - **Why:** Adheres to modern PEPs and recommended packaging layout for robustness and clarity. ([Details](topics/01_project-structure.md))

- **02: Dependency Management:**

  - **Chosen:** {uv}`uv<>`.
  - **Why:** Selected for its **exceptional performance** and excellent developer experience with a modern CLI and adherence to PEP 621 for dependency declaration. ([Details](topics/02_dependency-management.md))

- **03: Code Formatting:**

  - **Chosen:** {ruff}`Ruff<>` (Formatter).
  - **Why:** Offers **unmatched performance** and consolidates formatting and import sorting into a single, OS-interoperable tool with a popular PEP 8 compatible style. ([Details](topics/03_code-formatting.md))

- **04: Code Linting and Quality Checks:**

  - **Chosen:** {ruff}`Ruff<>` (Linter) + {pydocstyle}`pydocstyle<>` (via Ruff).
  - **Why:** Delivers **excellent performance** and consolidates a wide range of linting rules from various sources into a single tool. ([Details](topics/04_code-linting.md))

- **05: Type Checking:**

  - **Chosen:** {basedpyright}`Basedpyright<>`.
  - **Why:** Provides **significantly faster static analysis** while maintaining comprehensive and strict PEP-compliant type checking, backed by active community maintenance. ([Details](topics/05_type-checking.md))

- **06: Testing and Coverage:**

  - **Chosen:** {pytest}`pytest<>` + {coverage.py}`coverage.py<>` (via {pytest-pytest-cov}`pytest-cov<>`).
  - **Why:** The standard, feature-rich combination for modern Python testing, offering excellent DX for writing tests and robust, standard coverage reporting. ([Details](topics/06_testing-coverage.md))

- **07: Documentation Generation and Building:**

  - **Chosen:** {sphinx}`Sphinx<>` + MyST Markdown + `autodoc` + `napoleon` + `sphinx-autodoc-typehints`.
  - **Why:** Provides robust, standards-compliant **API documentation from code** and flexible narrative authoring in Markdown, using the de-facto standard Python documentation tool. ([Details](topics/07_documentation.md))

- **08: Code Security and Safety Checks:**

  - **Chosen:** {pip-audit}`pip-audit<>` (Deps) + {bandit-bandit}`Bandit<>` (Code).
  - **Why:** Provides comprehensive coverage for both dependency vulnerabilities and code security patterns using standard, OS-interoperable CLI tools suitable for automation. ([Details](topics/08_security-checks.md))

- **09: Distribution Package Building (sdist/wheel):**

  - **Chosen:** {uv}`uv<>` (frontend) + {setuptools}`setuptools<>` (pure Python backend) or {maturin}`Maturin<>` (Rust backend).
  - **Why:** Selects standard PEP 517 frontends/backends, using {setuptools}`setuptools<>` for standard PEP 621 projects and {maturin}`Maturin<>` as the best-in-class option for complex cross-platform native builds with Rust. ([Details](topics/09_packaging-build.md))

- **10: Package Publishing (to PyPI/Index Servers):**

  - **Chosen:** {uv}`uv<>` (`uv publish` command).
  - **Why:** Utilizes the integrated, standard-following publish command from the core dependency manager {uv}`uv<>`, providing a simple and secure way to upload artifacts based on underlying {twine}`twine<>`-equivalent logic. ([Details](topics/10_packaging-publish.md))

- **11: Application Container Building:**

  - **Chosen:** `Dockerfile` + {docker}`Docker<>`/{podman}`Podman<>` CLI + {uv}`uv<>` (inside container).
  - **Why:** Uses the industry-standard format and tools, supports essential best practices for security and size, and integrates with {uv}`uv<>` for efficient dependency installation within the image. ([Details](topics/11_container-build.md))

- **12: Task Automation / Developer Workflow:**

  - **Chosen:** {nox}`Nox<>` + {commitizen}`Commitizen<>` + {uv}`uvx<>`.
  - **Why:** Provides the central, OS-interoperable, CI/CD-agnostic automation layer with robust environment management and Python scripting. ([Details](topics/12_task-automation.md))

- **13: Continuous Integration (CI) Orchestration:**

  - **Chosen:** Platform-specific workflow configurations (e.g., {github-actions}`GitHub Actions<>`).
  - **Why:** Leverages standard CI platform features for triggers and environment setup to orchestrate {nox}`Nox<>` task calls, simplifying CI config and enabling agnosticism from execution logic. ([Details](topics/13_ci-orchestration.md))

- **14: Continuous Deployment / Delivery (CD) Orchestration:**

  - **Chosen:** Platform-specific workflow configurations (e.g., {github-actions}`GitHub Actions<>`).
  - **Why:** Utilizes platform features for triggers and secure secret management to orchestrate {nox}`Nox<>` build and publish tasks, ensuring a secure and automated release pipeline. ([Details](topics/14_cd-orchestration.md))

- **15: Container Orchestration (Local / Single Host):**

  - **Chosen:** {docker-compose}`Docker Compose<>`.
  - **Why:** The standard, intuitive tool for defining and running multi-container applications locally, seamlessly integrating with built container images for development and testing stacks. ([Details](topics/15_compose-local.md))

- **16: Deployment to Production Orchestrators:**

  - **Chosen:** Documentation and Guidance (No specific tool config included).
  - **Why:** Acknowledges the complexity of production deployment, ensures template artifacts (images, packages) are standard inputs, and guides users on utilizing common external orchestration tools. ([Details](topics/16_prod-deploy-guidance.md))

- **17: Containerized Development Environments:**

  - **Chosen:** `devcontainer.json` + `Dockerfile` + {uv}`uv<>` (inside container).
  - **Why:** Provides a repeatable, consistent, and editor-integrated containerized development environment, simplifying setup and ensuring tooling consistency using standard specs and {uv}`uv<>`. ([Details](topics/17_dev-containers.md))

- **18: Pre-commit Hooks:**
  - **Chosen:** {pre-commit}`pre-commit<>` framework + {ruff}`Ruff<>` hooks.
  - **Why:** Uses the standard framework for managing fast local checks, ensuring basic code quality and style are enforced automatically before every commit using highly performant tools. ([Details](topics/18_pre-commit-hooks.md))

---

## The Integrated Workflow in Practice

The true power of this template lies in how these chosen tools work together cohesively. The workflow centers around:

1.  **Configuration:** Defined primarily in `pyproject.toml` and separate tool config files ([01](topics/01_project-structure.md)).
2.  **Dependency/Environment Management:** Handled efficiently by {uv}`uv<>`, creating standard virtual environments and managing packages based on `pyproject.toml` and `uv.lock` ([02](topics/02_dependency-management.md)).
3.  **Task Automation:** Orchestrated by {nox}`Nox<>`, calling commands from other tools via `uv run` (or `uvx`), providing the single interface for developers and CI/CD to run workflows ([12](topics/12_task-automation.md)).
4.  **Code Quality & Testing:** Ensured by {ruff}`Ruff<>` (formatting/linting), {basedpyright}`Basedpyright<>` (typing), {pip-audit}`pip-audit<>` (dep security), and {bandit-bandit}`Bandit<>` (code security), along with {pytest-pytest-cov}`pytest<>`/{coveragepy}`coverage.py<>` for testing. These tools are installed via {uv}`uv<>` and executed via Task Automation ([03](topics/03_code-formatting.md)-[08](topics/08_security-checks.md), orchestrated by [12](topics/12_task-automation.md)).
5.  **Packaging & Distribution:** Artifacts created via {uv}`uv<>` build using selected backends, and published via {uv}`uv<>` publish, orchestrated by Task Automation ([09](topics/09_packaging-build.md)-[10](topics/10_packaging-publish.md)).
6.  **Containerization:** Defined by `Dockerfile`, built by {docker}`Docker<>`/{podman}`Podman<>` (often via `uv` installing deps inside), orchestrated by Task Automation. Local multi-container setups managed by {docker}`Docker Compose<>` ([11](topics/11_container-build.md), [15](topics/15_compose-local.md)).
7.  **Automated Workflows:** Triggered by CI/CD platforms (configured to call Task Automation commands), handling matrices, secrets, and reporting ([13](topics/13_ci-orchestration.md)-[14](topics/14_cd-orchestration.md)).
8.  **Development Environment:** Consistent locally ({uv}`uv<>` venvs, {pre-commit}`pre-commit<>`) and reproducibly within a container via Dev Containers ([17](topics/17_dev-containers.md)), simplifying setup and ensuring uniformity.

By choosing `cookiecutter-robust-python`, users gain this pre-configured, integrated, and documented workflow, allowing them to focus on building their application with a strong, modern, and robust foundation.
