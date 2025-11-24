# 18: Pre-commit Hooks

This section evaluates tools and approaches for setting up automated checks and code transformations that run _locally_ on staged files before a commit is made. Pre-commit hooks provide immediate feedback, help prevent committing code style violations or basic errors, and ensure a clean commit history, strongly supporting the "Automated is better than manual" principle.

## Goals Addressed

- Automatically run configured checks and code transformations on files staged for commit.
- Prevent commits that fail configured checks.
- Provide fast feedback to the developer about code quality or style issues _before_ they create a commit.
- Ensure the process is easy for developers to set up and manage.
- Support integrating various external tools (formatters, linters, etc.) into the Git commit workflow.
- Ensure the pre-commit hooks work reliably across development operating systems.

## Evaluation Criteria

- **Standardization (Framework):** Does the approach use a widely adopted standard framework for managing Git hooks?
- **Ease of Setup (User):** How simple is it for a developer to enable and use the hooks after cloning the project?
- **Tool Integration:** How easily can various external tools (formatters, linters, type checkers, custom scripts) be integrated as hooks?
- **Environment Isolation:** How are the hook tool dependencies managed? Does the framework prevent conflicts between tool dependencies or the project's dependencies?
- **Performance (Execution Speed):** How fast is the overhead added by the framework itself? How fast are the typical checks configured to run here? (Crucially, fast is better for pre-commit).
- **Reliability & OS Interoperability:** Does the framework and its method of running hooks work reliably and consistently across Linux, macOS, and Windows host development machines?
- **Configurability:** How easy is it to specify which hooks run on which files and with what arguments?
- **Maturity & Stability:** How stable and battle-tested is the framework?
- **Community & Documentation:** Active development, support, and comprehensive documentation.
- **Best Tool for the Job:** Considering all criteria, which tool/framework is the strongest fit for managing reliable, fast, and OS-interoperable pre-commit hooks.

## Tools and Approaches Evaluated

### Option 1: Writing Raw Git Hook Scripts

- **Description:** Manually creating or modifying scripts directly in the `.git/hooks` directory (e.g., `pre-commit`, `pre-push`). These are executed by Git at specific points.
- **Evaluation:**

  - **Standardization (Framework):** Poor. Relies on Git's built-in, low-level mechanism; no higher-level framework or standard configuration format (`.git/hooks` contents vary wildly).
  - **Ease of Setup (User):** Poor. Users have to remember to copy/link/manage these scripts manually after cloning. Difficult to update these scripts reliably.
  - **Tool Integration:** Moderate. Requires writing shell scripts to call tools. Environment management (activating project venv, ensuring tools are installed) must be done manually within the shell script itself, introducing OS/shell complexities.
  - **Environment Isolation:** Poor. Hook dependencies (tool versions) and the project's dependencies must be managed manually by the user ensuring they are compatible and available when the hook runs. No isolation mechanism provided by the framework itself. Prone to "works on my machine but not coworker's because their tools/envs are different."
  - **Performance (Execution Speed):** Excellent (Framework). Git's overhead is minimal. Execution speed depends on the scripts' content and tool calls.
  - **Reliability & OS Interoperability:** Poor (Execution Logic). Highly dependent on the shell script contents and their OS/shell compatibility. Reliably writing cross-platform shell scripts with environment activation is very difficult.
  - **Configurability:** Poor. No standard configuration file; involves directly editing shell scripts.
  - **Maturity & Stability:** Excellent (Mechanism). The Git hook mechanism itself is stable.
  - **Community & Documentation:** Poor (Mechanism). Limited community patterns for standard script sets.

- **Conclusion:** Low-level and highly flexible, but suffers from poor user setup experience, update complexity, lack of environment management/isolation, and severe OS interoperability issues for standard Python development tasks. Not suitable for a template aiming for ease of use and reliability.

### Option 2: {pre-commit}`pre-commit<>` (Framework)

- **Description:** A language-agnostic framework that manages Git hook scripts. Configuration via `.pre-commit-config.yaml`. Downloads hook tool dependencies into isolated environments managed by the framework itself. Executes tools on staged files.
- **Evaluation:**

  - **Standardization (Framework):** Excellent. **The industry standard framework** for managing Git hooks across languages, using a widely adopted YAML configuration format (`.pre-commit-config.yaml`).
  - **Ease of Setup (User):** Excellent. Requires two simple steps: `uv add pre-commit` (or `pip install pre-commit`) and `pre-commit install`. Updates are managed by changing `rev` in the config and running `pre-commit autoupdate` or `pre-commit install`. Highly automated and user-friendly.
  - **Tool Integration:** Excellent. Supports integrating tools written in many languages (Python, Node, Ruby, Docker) via a repository-based mechanism or local scripts. Configuration for adding hooks is straightforward.
  - **Environment Isolation:** Excellent. **Key Strength.** Automatically downloads and installs hook tool dependencies (specified by `repo` and `rev`) into dedicated, isolated environments it manages _for each hook repository_. This prevents conflicts between hook dependencies and the project's main dependencies and ensures hooks run with the correct, pinned tool versions regardless of the developer's local environment.
  - **Performance (Execution Speed):** High (Framework). The framework adds minimal overhead. Execution speed depends on the configured hooks/tools. Supports running fast checks efficiently.
  - **Reliability & OS Interoperability:** Excellent. The framework itself is **highly OS-interoperable**, written in Python but carefully managing OS/shell differences for hook execution. It ensures the _tools it runs_ are compatible and executed correctly within the isolated environments, abstracting away complexity from the hook configuration itself.
  - **Configurability:** Excellent. Configuration via `.pre-commit-config.yaml` is highly flexible, allowing specifying hooks, versions (`rev`), files/excludes (`files`, `exclude`), and arguments (`args`).
  - **Maturity & Stability:** Very High. Mature, stable, widely used standard across various language ecosystems.
  - **Community & Documentation:** Very High. Large, active community, extensive documentation, a vast registry of hook repositories.

- **Conclusion:** Provides a standard, user-friendly, and technically robust solution for managing Git hooks, uniquely handling dependency isolation and OS interoperability effectively. The ideal framework for this purpose.

### Option 3: Dependency Manager Hooks (e.g., {poetry}`Poetry<>`, {hatch}`Hatch<>`)

- **Description:** Some dependency managers offer built-in ways to configure or run hooks. For example, {hatch}`Hatch<>` allows defining scripts/tasks to run pre-commit.
- **Evaluation:** These features are specific to the dependency manager. They might not provide the same level of language agnosticism or explicit hook dependency isolation/management as the {pre-commit}`pre-commit<>` framework. They tie your hook management strategy tightly to your dependency manager choice.
- **Conclusion:** Less suitable as the primary framework for managing hooks compared to a dedicated, language-agnostic tool like {pre-commit}`pre-commit<>`, which is designed solely for this purpose and excels at tool/language integration and dependency isolation across any mix of tools.

## Chosen Tool(s) and Strategy

- Pre-commit hook management framework: **{pre-commit}`pre-commit<>`**.
- Specific Hooks Used: Primarily **{ruff}`Ruff<>`** hooks (`ruff-format`, `ruff`). Add standard, language-agnostic hooks (check-yaml, end-of-file-fixer, trailing-whitespace, check-large-files).
- Strategy: Configure {pre-commit}`pre-commit<>` with **fast, essential checks** (formatting, basic linting/autofixes) to run automatically on every commit.

## Justification for the Choice

**{pre-commit}`pre-commit<>`** is selected as the framework for managing pre-commit hooks because it is the **clear standard** and offers the most robust, user-friendly, and technically sound solution for this specific workflow stage:

1.  **Reliability & OS Interoperability:** It solves the hard problem of running hooks reliably and consistently across different operating systems by handling **environment isolation** and executing tools within self-managed environments. This is a critical advantage over manually managed scripts (addressing **Reliability & OS Interoperability** and **Environment Isolation**).
2.  **User Experience:** It makes hook setup and usage **simple and highly automated** for the developer (`pre-commit install`), requiring minimal manual effort after cloning the project (addressing **Ease of Setup**). It also provides a simple default command to run hooks manually.
3.  **Flexible Tool Integration:** It provides a standard, configuration-driven way to integrate various external tools and hooks (addressing **Tool Integration** and **Configurability**).
4.  **Ensuring Quality Incrementally:** By running automated checks automatically before _each_ commit, it helps catch issues early and maintain code quality and style standards incrementally, preventing them from accumulating and simplifying subsequent reviews and automation stages (CI/CD) (addressing **Goals Addressed**).

While {pre-commit}`pre-commit<>` itself doesn't define _which_ checks are run, the template configures **{ruff}`Ruff<>`** as the primary tool used by pre-commit hooks due to its exceptional **Performance** for formatting and linting, making these checks fast enough to run reliably on every commit without causing frustration. Hooks for `ruff-format` (covering formatting and import sorting) and `ruff` (for fast linting checks with autofixing) are essential here. We include other standard hooks (like YAML check, trailing whitespace) that are simple, fast, and universally beneficial.

Comprehensive checks (full type checks via {basedpyright}`Basedpyright<>`, security scans via {bandit-bandit}`Bandit<>`/{pip-audit}`pip-audit<>`) are **not** mandated in pre-commit due to their potential performance overhead or complexity; they are deferred to the Task Automation layer ({nox}`Nox<>` - Area 12) and enforced in CI (Area 13), creating a layered approach to code quality where pre-commit provides the fastest initial feedback.

By using {pre-commit}`pre-commit<>` with well-chosen fast hooks, the template ensures that fundamental quality standards are applied consistently and automatically at the point of code contribution.

**Manual Execution:** When hooks are installed, `git commit` automatically runs them. You can also trigger them manually on staged files by running the simple command `pre-commit` from the project root. To run them on _all_ files in the repository (staged or not), use `pre-commit run --all-files`. The template's Task Automation layer provides a `nox -s pre-commit` command that **defaults to running `pre-commit` on staged files when called without arguments**, and allows passing specific `pre-commit` arguments (like `--install`, `--uninstall`, `run --all-files`) via positional arguments. This simplifies the user interface to `nox -s pre-commit`.

## Interactions with Other Topics

- **Code Formatting (03) & Linting (04):** {ruff}`Ruff<>` is configured and run as a core hook for these tasks.
- **Type Checking (05), Security (08):** Full comprehensive checks from these areas are typically not run in pre-commit, but fast subsets _could_ potentially be added using {ruff}`Ruff<>` or focused tools if performance allows in the future. The main checks for these areas run in Task Automation/CI.
- **Task Automation (12):** {nox}`Nox<>` provides commands like `nox -s pre-commit -- install` to set up the hooks and defaults to running `pre-commit` on staged files with `nox -s pre-commit`. The full `check` task in Nox (Area 12) includes all linters/checkers, including those also used by pre-commit, but runs on the entire codebase in controlled environments.
- **CI Orchestration (13):** CI acts as the final gatekeeper, verifying that even the comprehensive checks (which aren't in pre-commit) pass. It doubles as a check that pre-commit hooks are functioning correctly (by ensuring formatted code passes the linter check, etc., although CI usually checks _before_ potential manual hook fixes).
