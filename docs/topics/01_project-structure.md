# 01: Project Structure and Basic Setup

This section evaluates approaches for establishing the initial directory layout and primary configuration entry point for generated projects. A well-structured project is easier to navigate, build, test, and maintain for all developers, aligning with the template's goal of providing a robust and user-friendly foundation.

## Goals Addressed

- Provide a clean, conventional, and easy-to-navigate initial directory and file layout.
- Establish a clear central configuration entry point for project metadata and tooling.
- Ensure the structure supports standard Python packaging, testing, and development workflows.

## Evaluation Criteria

- **Adherence to Standards (PEPs & Conventions):** How well does the structure and primary configuration file follow established Python Packaging standards (PEP 518 for build systems, PEP 621 for project metadata) and widely accepted community conventions (e.g., src/ layout)?
- **Centralization & Discoverability:** How well does the primary configuration method centralize essential project metadata and configuration? How easy is it for a new developer or automation tool to find core project settings and source code?
- **Simplicity & Intuition:** Is the initial structure straightforward to understand for developers familiar with Python projects? Is the primary configuration file easy to read for core information?
- **Compatibility:** How well is the structure and primary configuration file supported by the ecosystem of modern build tools, dependency managers, testers, linters, and IDEs?
- **Maintainability:** Does the structure and configuration approach simplify managing project settings and dependencies long-term? Does the chosen configuration file approach minimize potential conflicts (e.g., during template updates via tools like {cruft}`cruft<>`)?

## Approaches and Tools Evaluated

We evaluated different combinations of configuration file formats and directory layouts:

### Option 1: `setup.py` / `setup.cfg` (Legacy) with Flat Layout

- **Description:** This approach uses the older configuration files (`setup.py` for imperative logic and `setup.cfg` for declarative metadata) that predate `pyproject.toml`. The package source code is placed directly at the root of the project directory alongside other top-level directories like `tests/` and `docs/`.
- **Evaluation:**

  - **Adherence to Standards:** Poor. This approach relies on older standards that are largely superseded by PEP 518 and PEP 621. The flat layout is discouraged in favor of the `src/` layout for preventing import conflicts.
  - **Centralization & Discoverability:** Moderate. Project metadata is split between `setup.py` (sometimes declarative in `setup.cfg`) and dependencies often managed separately in `requirements.txt`. Configuration is scattered and potentially embedded in imperative code (`setup.py`).
  - **Simplicity & Intuition:** The flat layout can appear deceptively simple initially ("just put everything here"). However, managing configurations across `setup.py`/`setup.cfg`/`requirements.txt` and understanding custom logic in `setup.py` can be complex.
  - **Compatibility:** High (Historically). This was the standard for many years and remains widely supported by older tooling. However, newer tools increasingly prioritize or exclusively use `pyproject.toml`.
  - **Maintainability:** Poor. The flat layout is highly prone to subtle bugs related to import resolution (a package installed in editable mode might import the source code from the root instead of the installed package from site-packages). Managing configuration spread across multiple files adds maintenance overhead. Template updates involving changes to `setup.py` (which can contain arbitrary code) are prone to conflicts.

- **Conclusion:** This approach relies on deprecated standards and practices that introduce complexity and potential issues. Not suitable for a template aiming for modern, robust development based on current best practices.

### Option 2: `pyproject.toml` with Flat Layout

- **Description:** This approach adopts the modern `pyproject.toml` file for defining the build system (PEP 518) and project metadata (PEP 621). However, it retains the flat layout, placing the package source code directly at the project root.
- **Evaluation:**

  - **Adherence to Standards:** High (Configuration). Adheres to PEP 518 and PEP 621 for configuration format and location. Poor (Layout). Conflicts with the widely recommended `src/` layout convention aimed at preventing import conflicts during editable installs.
  - **Centralization & Discoverability:** High. Consolidates core project metadata, build system, and often tool configurations (via `[tool.<name>]`) into a single file, significantly improving **discoverability**.
  - **Simplicity & Intuition:** The structure with a central `pyproject.toml` is straightforward. The flat layout might still appear simple visually but masks potential import issues.
  - **Compatibility:** Excellent. `pyproject.toml` and the standard build process are fully supported by modern tooling (build frontends, dependency managers, build backends).
  - **Maintainability:** Moderate. Improved significantly by the centralization of configuration in `pyproject.toml`. However, the flat layout still introduces **maintainability issues** related to import resolution bugs, which can be time-consuming to debug. Conflicts during template updates (via {cruft}`cruft<>`) might occur in `pyproject.toml`, but separating tool configs helps mitigate this (as decided in the synthesis).

- **Conclusion:** While adopting `pyproject.toml` is a necessary step towards modern standards, retaining the flat layout compromises robustness and maintainability by failing to address a known source of development/testing issues.

### Option 3: `pyproject.toml` with `src/` Layout

- **Description:** This approach uses `pyproject.toml` (PEP 518 & 621) as the central configuration file for metadata and the build system. The project's source code package is placed within a dedicated `src/` subdirectory (e.g., `src/your_package_name/`). Standard directories for tests (`tests/`), documentation (`docs/`), automation configs (`.github/workflows/`, etc.) are placed alongside `src/` at the project root.
- **Evaluation:**

  - **Adherence to Standards:** Excellent. This combination of using `pyproject.toml` (PEP 518, 621) and adopting the `src/` layout aligns with the **current widely accepted best practices** and recommendations from the Python Packaging Authority (PyPA) for library and application packaging. It sets a strong foundation based on robust standards.
  - **Centralization & Discoverability:** High. Core project metadata, build system definition, and links to tool configurations are centralized in `pyproject.toml`. The separation of source code (`src/`), tests (`tests/`), and documentation (`docs/`) into dedicated, conventionally named directories enhances **discoverability** for developers and automation tools.
  - **Simplicity & Intuition:** While adding the `src/` directory is an extra level, the overall structure with clearly defined directories for different project components is intuitive and easy to navigate for anyone familiar with Python project conventions. `pyproject.toml` as the config hub is straightforward for finding setup information.
  - **Compatibility:** Excellent. This structure is **fully supported and expected** by the entire modern Python tooling ecosystem, including build frontends/backends (Topic 09), dependency managers (Topic 02 - {uv}`uv<>`), testers (Topic 06 - {pytest}`pytest<>`), linters (Topic 04 - {ruff}`Ruff<>`), type checkers (Topic 05 - {basedpyright}`Basedpyright<>`), and documentation generators (Topic 07 - {sphinx}`Sphinx<>`).
  - **Maintainability:** Excellent. The `src/` layout prevents common and subtle import resolution bugs that plague flat layouts, leading to a more **reliable and maintainable** development and testing environment. Centralizing metadata in `pyproject.toml` (while using separate files for most tool configs as decided in the synthesis) improves configuration **maintainability** compared to scattered legacy files. Standard structure and config practices aid collaboration and reduce onboarding friction.

- **Conclusion:** This approach represents the current consensus for robust, maintainable, and standard-compliant Python project structure, offering significant advantages over legacy methods or the flat layout.

## Chosen Approach

- **`pyproject.toml`** as the **single, central configuration file** for project metadata (`[project]`) and build system definition (`[build-system]`).
- Adoption of the **`src/` directory layout** for placing the project's source code package.
- Inclusion of standard top-level directories (`tests/`, `docs/`, `.github/workflows/`, `.devcontainer/`, `rust/` - if applicable) and essential root files (`.gitignore`, `.editorconfig`, `README.md`, `LICENSE`, and separate tool config files like `.ruff.toml`, `pyrightconfig.json`, etc.).

## Justification for the Choice

This approach was selected because it excels across all evaluation criteria, providing the most technically sound, reliable, and maintainable foundation for a modern Python project generated by this template:

1.  **Strict Adherence to Standards:** The combination of using **`pyproject.toml`** and the **`src/` layout** strictly adheres to **PEP 621**, **PEP 518**, and the recommended packaging layout conventions from the PyPA. This is the **correct and standardized way** to structure a modern Python package and its metadata ("PEP compliant is better").
2.  **Elimination of Import Bugs:** The `src/` layout proactively eliminates common import resolution bugs that can occur with flat layouts, significantly improving the **reliability and maintainability** of the testing and development environment ("Maintainable is better than feature-filled" - preventing bugs is key).
3.  **Centralized & Discoverable Metadata:** `pyproject.toml` serves as the single source for core project metadata, making essential information easy to find and understand ("Documented is better than implied" implicitly applies to config clarity, "Obvious way to do it"). Standard directory names further enhance **discoverability**.
4.  **Broadest Tool Compatibility:** This structure and primary configuration file are **fully supported and expected** by the entire suite of modern Python tools recommended in other topics of this template (Dependency Management - {uv}`uv<>`, Testing - {pytest}`pytest<>`, etc.). Choosing this structure ensures seamless **compatibility** throughout the workflow.

By making this well-considered and opinionated choice ("Opinionated is better than impartial", "Thought out is better than preferred") based on established standards and practical reliability benefits, the template provides a solid base that avoids legacy issues and facilitates integrating the rest of the modern toolchain effectively.

The alternative (Option 2, `pyproject.toml` + flat) failed primarily due to the maintenance issues introduced by the flat layout. Legacy options (Option 1) were discounted entirely due to their reliance on outdated standards and complexity.

## Interactions with Other Topics

- **Dependency Management (02):** {uv}`uv<>` relies on `pyproject.toml` for dependency declarations and works optimally with the `src/` layout and virtual environments within the project structure.
- **Code Formatting (03), Linting (04), Type Checking (05), Security Checks (08):** Tool configurations (in separate files like `.ruff.toml` or linked from `pyproject.toml`) define how these tools analyze code within the `src/` directory.
- **Testing (06):** {pytest-pytest-cov}`pytest<>` finds tests in `tests/` and runs against the code in `src/`, with the `src/` layout preventing import issues during testing of the installed package.
- **Documentation (07):** {sphinx}`Sphinx<>` uses the `docs/` directory for source files and extracts API documentation from code within `src/`.
- **Packaging Build (09):** The build backend ({setuptools}`setuptools<>` or {maturin}`Maturin<>`) configured in `pyproject.toml` finds package source code in `src/` to build distribution artifacts.
- **Task Automation (12):** {nox}`Nox<>` sessions navigate the project structure (e.g., `session.run("uv", "run", "ruff", "check", "src", "tests")`) and manage environments within this structure.
- **Container Build (11):** Dockerfiles copy code from the project structure (likely copying the built package from `dist/` or code from `src/`) into the container image.
- **Pre-commit Hooks (18):** The `.pre-commit-config.yaml` defines hooks that run on files within this structure (e.g., format Python files in `src/` and `tests/`).
