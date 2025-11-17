"""Noxfile for the {{cookiecutter.project_name}} project."""

import os
import shlex
from pathlib import Path
from textwrap import dedent
from typing import List

import nox
from nox.command import CommandFailed
from nox.sessions import Session


nox.options.default_venv_backend = "uv"
os.environ.setdefault("PYO3_USE_ABI3_FORWARD_COMPATIBILITY", "1")

PYTHON_VERSIONS: List[str] = {{cookiecutter.python_versions}}
DEFAULT_PYTHON_VERSION: str = PYTHON_VERSIONS[-1]

REPO_ROOT: Path = Path(__file__).parent.resolve()
TESTS_FOLDER: Path = REPO_ROOT / "tests"
SCRIPTS_FOLDER: Path = REPO_ROOT / "scripts"
CRATES_FOLDER: Path = REPO_ROOT / "rust"

PROJECT_NAME: str = "{{cookiecutter.project_name}}"
PACKAGE_NAME: str = "{{cookiecutter.package_name}}"
REPOSITORY_HOST: str = "{{cookiecutter.repository_host}}"
REPOSITORY_PATH: str = "{{cookiecutter.repository_path}}"

ENV: str = "env"
FORMAT: str = "format"
LINT: str = "lint"
TYPE: str = "type"
TEST: str = "test"
COVERAGE: str = "coverage"
SECURITY: str = "security"
DOCS: str = "docs"
BUILD: str = "build"
RELEASE: str = "release"
QUALITY: str = "quality"


@nox.session(python=False, name="setup-venv", tags=[ENV])
def setup_venv(session: Session) -> None:
    """Set up the virtual environment for the current project."""
    session.run("python", SCRIPTS_FOLDER / "setup-venv.py", REPO_ROOT, "-p", PYTHON_VERSIONS[0], external=True)


@nox.session(python=False, name="setup-git", tags=[ENV])
def setup_git(session: Session) -> None:
    """Set up the git repo for the current project."""
    session.run("python", SCRIPTS_FOLDER / "setup-git.py", REPO_ROOT, external=True)


@nox.session(python=False, name="setup-remote")
def setup_remote(session: Session) -> None:
    """Set up the remote repository for the current project."""
    command: list[str] = [
        "python",
        SCRIPTS_FOLDER / "setup-remote.py",
        REPO_ROOT,
        "--host",
        REPOSITORY_HOST,
        "--path",
        REPOSITORY_PATH,
    ]
    session.run(*command, external=True)


@nox.session(python=DEFAULT_PYTHON_VERSION, name="pre-commit", tags=[QUALITY])
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args: list[str] = session.posargs or ["run", "--all-files", "--show-diff-on-failure"]

    session.log("Installing pre-commit dependencies...")
    session.install("-e", ".", "--group", "dev")

    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@nox.session(python=False, name="format-python", tags=[FORMAT, QUALITY])
def format_python(session: Session) -> None:
    """Run Python code formatter (Ruff format)."""
    session.log(f"Running Ruff formatter check with py{session.python}.")
    session.run("uvx", "ruff", "format", *session.posargs)


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="format-rust", tags=[FORMAT])
def format_rust(session: Session) -> None:
    """Run Rust code formatter (cargo fmt)."""
    session.log("Ensuring rustfmt component is available...")
    session.run("rustup", "component", "add", "rustfmt", external=True)
    session.log("Formatting Rust code...")
    session.run("cargo", "fmt", "--all", external=True)


{% endif -%}
@nox.session(python=False, name="lint-python", tags=[LINT, QUALITY])
def lint_python(session: Session) -> None:
    """Run Python code linters (Ruff check, Pydocstyle rules)."""
    session.log(f"Running Ruff check with py{session.python}.")
    session.run("uvx", "ruff", "check", "--fix", "--verbose")


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="lint-rust", tags=[LINT, QUALITY])
def lint_rust(session: Session) -> None:
    """Run Rust code linters (cargo clippy)."""
    session.log("Ensuring clippy component is available...")
    session.run("rustup", "component", "add", "clippy", external=True)
    session.log("Running clippy lints...")
    session.run("cargo", "clippy", "--all-features", "--", "-D", "warnings", external=True)


{% endif -%}
@nox.session(python=PYTHON_VERSIONS, name="typecheck")
def typecheck(session: Session) -> None:
    """Run static type checking (Pyright) on Python code."""
    session.log("Installing type checking dependencies...")
    session.install("-e", ".", "--group", "dev")

    session.log(f"Running Pyright check with py{session.python}.")
    session.run("pyright", "--pythonversion", session.python)


@nox.session(python=False, name="security-python", tags=[SECURITY])
def security_python(session: Session) -> None:
    """Run code security checks (Bandit) on Python code."""
    session.log(f"Running Bandit static security analysis with py{session.python}.")
    session.run("uvx", "bandit", "-r", PACKAGE_NAME, "-c", "bandit.yml", "-ll")

    session.log(f"Running pip-audit dependency security check with py{session.python}.")
    session.run("uvx", "pip-audit")


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="security-rust", tags=[SECURITY])
def security_rust(session: Session) -> None:
    """Run code security checks (cargo audit)."""
    session.log("Ensuring cargo-audit is available...")
    session.run("cargo", "install", "cargo-audit", "--locked", external=True)
    session.run("cargo", "audit", "--all", external=True)


{% endif -%}
@nox.session(python=PYTHON_VERSIONS, name="tests-python", tags=[TEST])
def tests_python(session: Session) -> None:
    """Run the Python test suite (pytest with coverage)."""
    session.log("Installing test dependencies...")
    session.install("-e", ".", "--group", "dev")

    session.log(f"Running test suite with py{session.python}.")
    test_results_dir = TESTS_FOLDER / "results"
    test_results_dir.mkdir(parents=True, exist_ok=True)
    junitxml_file = test_results_dir / f"test-results-py{session.python.replace('.', '')}.xml"

    session.run(
        "pytest",
        "--cov={}".format(PACKAGE_NAME),
        "--cov-append",
        "--cov-report=term",
        "--cov-report=xml",
        f"--junitxml={junitxml_file}",
        "tests/",
    )


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="tests-rust", tags=[TEST])
def tests_rust(session: Session) -> None:
    """Test the project's rust crates."""
    crates: list[Path] = [cargo_toml.parent for cargo_toml in CRATES_FOLDER.glob("*/Cargo.toml")]
    crate_kwargs: list[str] = [f"-p {crate.name}" for crate in crates]
    session.run("cargo", "test", "--all-features", "--no-run", *crate_kwargs, external=True)
    session.run("cargo", "test", "--all-features", *crate_kwargs, external=True)


{% endif -%}
@nox.session(python=DEFAULT_PYTHON_VERSION, name="build-docs", tags=[DOCS, BUILD])
def docs_build(session: Session) -> None:
    """Build the project documentation (Sphinx)."""
    session.log("Installing documentation dependencies...")
    session.install("-e", ".", "--group", "docs")

    session.log(f"Building documentation with py{session.python}.")
    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning build directory: {docs_build_dir}")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E")

    session.log("Building documentation.")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W")


@nox.session(python=DEFAULT_PYTHON_VERSION, name="docs", tags=[DOCS, BUILD])
def docs(session: Session) -> None:
    """Build and serve the project documentation (Sphinx)."""
    session.log("Installing documentation dependencies...")
    session.install("-e", ".", "--group", "docs")

    session.log(f"Building documentation with py{session.python}.")
    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning build directory: {docs_build_dir}")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E")

    session.log("Building and serving documentation.")
    session.run("sphinx-autobuild", "--open-browser", "docs", str(docs_build_dir))


@nox.session(python=False, name="build-python", tags=[BUILD])
def build_python(session: Session) -> None:
    """Build sdist and wheel packages (uv build)."""
    session.log(f"Building sdist and wheel packages with py{session.python}.")
    {% if cookiecutter.add_rust_extension -%}
    session.run("uvx", "maturin", "develop", "--uv")
    {% else -%}
    session.run("uv", "build", "--sdist", "--wheel", "--out-dir", "dist/", external=True)
    {% endif -%}

    session.log("Built packages in ./dist directory:")
    for path in Path("dist/").glob("*"):
        session.log(f"- {path.name}")


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="build-rust", tags=[BUILD])
def build_rust(session: Session) -> None:
    """Build standalone Rust crates for potential independent publishing."""
    session.log("Building Rust crates...")
    session.run("cargo", "build", "--release", "--manifest-path", "rust/Cargo.toml", external=True)


{% endif -%}
@nox.session(python=False, name="build-container", tags=[BUILD])
def build_container(session: Session) -> None:
    """Build the Docker container image.

    Requires Docker or Podman installed and running on the host.
    Ensures core project dependencies are synced in the current environment
    *before* the build context is prepared.
    """
    session.log("Building application container image...")
    try:
        session.run("docker", "info", success_codes=[0], external=True, silent=True)
        container_cli = "docker"
    except CommandFailed:
        try:
            session.run("podman", "info", success_codes=[0], external=True, silent=True)
            container_cli = "podman"
        except CommandFailed:
            session.log("Neither Docker nor Podman command found. Please install a container runtime.")
            session.skip("Container runtime not available.")

    current_dir: Path = Path.cwd()
    session.log(f"Ensuring core dependencies are synced in {current_dir.resolve()} for build context...")
    session.install("-e", ".")

    session.log(f"Building Docker image using {container_cli}.")
    project_image_name = PACKAGE_NAME.replace("_", "-").lower()
    session.run(
        container_cli,
        "build",
        str(current_dir),
        "-t",
        f"{project_image_name}:latest",
        "--progress=plain",
        external=True,
    )

    session.log(f"Container image {project_image_name}:latest built locally.")


@nox.session(python=False, name="setup-release", tags=[RELEASE])
def setup_release(session: Session) -> None:
    """Prepares a release by creating a release branch and bumping the version.

    Additionally, creates the initial bump commit but doesn't push it.
    """
    session.log("Setting up release...")

    session.run("python", SCRIPTS_FOLDER / "setup-release.py", *session.posargs, external=True)


@nox.session(python=False, name="get-release-notes", tags=[RELEASE])
def get_release_notes(session: Session) -> None:
    """Gets the latest release notes if between bumping the version and tagging the release."""
    session.log("Getting release notes...")
    session.run("python", SCRIPTS_FOLDER / "get-release-notes.py", *session.posargs, external=True)


@nox.session(python=False, name="publish-python", tags=[RELEASE])
def publish_python(session: Session) -> None:
    """Publish sdist and wheel packages to PyPI via uv publish.

    Requires packages to be built first (`nox -s build-python` or `nox -s build`).
    Requires TWINE_USERNAME/TWINE_PASSWORD or TWINE_API_KEY environment variables set (usually in CI).
    """
    session.log("Checking built packages with Twine.")
    session.run("uvx", "twine", "check", "dist/*")

    session.log("Publishing packages to PyPI.")
    session.run("uv", "publish", "dist/*", *session.posargs, external=True)


{% if cookiecutter.add_rust_extension -%}
@nox.session(python=False, name="publish-rust", tags=[RELEASE])
def publish_rust(session: Session) -> None:
    """Publish built crates to crates.io."""
    session.log("Publishing crates to crates.io")
    for cargo_toml in CRATES_FOLDER.glob("*/Cargo.toml"):
        crate_folder: Path = cargo_toml.parent
        session.run("cargo", "publish", "-p", crate_folder.name)


{% endif -%}
@nox.session(python=False)
def tox(session: Session) -> None:
    """Run the 'tox' test matrix.

    Requires uvx in PATH. Requires tox.ini file.
    Useful for specific ecosystem conventions (e.g., pytest plugins,
    cookiecutter-driven matrix testing).
    Accepts tox args after '--' (e.g., `nox -s tox -- -e py39`).
    """
    session.log("Running Tox test matrix via uvx...")
    session.install("-e", ".", "--group", "dev")

    tox_ini_path = Path("tox.ini")
    if not tox_ini_path.exists():
        session.log("tox.ini file not found at %s. Tox requires this file.", str(tox_ini_path))
        session.skip("tox.ini not present.")

    session.log("Checking Tox availability via uvx.")
    session.run("tox", "--version", success_codes=[0])

    session.run("tox", *session.posargs)


@nox.session(python=DEFAULT_PYTHON_VERSION, tags=[COVERAGE])
def coverage(session: Session) -> None:
    """Collect and report coverage.

    Requires tests to have been run with --cov and --cov-report=xml across matrix
    (e.g., via `nox -s test-python`).
    """
    session.log("Collecting and reporting coverage across all test runs.")
    session.log(
        "Note: Ensure 'nox -s test-python' was run across all desired Python versions first to generate coverage data."
    )

    session.log("Installing dependencies for coverage report session...")
    session.install("-e", ".", "--group", "dev")

    coverage_combined_file: Path = Path.cwd() / ".coverage"

    session.log("Combining coverage data.")
    try:
        session.run("coverage", "combine")
        session.log(f"Combined coverage data into {coverage_combined_file.resolve()}")
    except CommandFailed as e:
        if e.returncode == 1:
            session.log("No coverage data found to combine. Run tests first with coverage enabled.")
        else:
            session.error(f"Failed to combine coverage data: {e}")
        session.skip("Could not combine coverage data.")

    session.log("Generating HTML coverage report.")
    coverage_html_dir = Path("coverage-html")
    session.run("coverage", "html", "--directory", str(coverage_html_dir))

    session.log("Running terminal coverage report.")
    session.run("coverage", "report")

    session.log(f"Coverage reports generated in ./{coverage_html_dir} and terminal.")


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the
    session's virtual environment. This allows pre-commit to locate hooks in
    that environment when invoked from git.

    Args:
        session: The Session object.
    """
    assert session.bin is not None  # nosec

    # Only patch hooks containing a reference to this session's bindir. Support
    # quoting rules for Python and bash, but strip the outermost quotes so we
    # can detect paths within the bindir, like <bindir>/python.
    bindirs = [
        bindir[1:-1] if bindir[0] in "'\"" else bindir for bindir in (repr(session.bin), shlex.quote(session.bin))
    ]

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    headers = {
        # pre-commit < 2.16.0
        "python": f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """,
        # pre-commit >= 2.16.0
        "bash": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
        # pre-commit >= 2.17.0 on Windows forces sh shebang
        "/bin/sh": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
    }

    hookdir: Path = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        if not hook.read_bytes().startswith(b"#!"):
            continue

        text: str = hook.read_text()

        if not any((Path("A") == Path("a") and bindir.lower() in text.lower()) or bindir in text for bindir in bindirs):
            continue

        lines: list[str] = text.splitlines()

        for executable, header in headers.items():
            if executable in lines[0].lower():
                lines.insert(1, dedent(header))
                hook.write_text("\n".join(lines))
                break
