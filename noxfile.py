"""Noxfile for the cookiecutter-robust-python template."""

# /// script
# dependencies = ["nox>=2025.5.1", "platformdirs>=4.3.8", "python-dotenv>=1.0.0"]
# ///

import os
import shutil
from pathlib import Path

import nox
import platformdirs
from dotenv import load_dotenv
from nox.command import CommandFailed
from nox.sessions import Session


nox.options.default_venv_backend = "uv"

DEFAULT_TEMPLATE_PYTHON_VERSION = "3.10"

REPO_ROOT: Path = Path(__file__).parent.resolve()
SCRIPTS_FOLDER: Path = REPO_ROOT / "scripts"
TEMPLATE_FOLDER: Path = REPO_ROOT / "{{cookiecutter.project_name}}"


# Load environment variables from .env and .env.local (if present)
LOCAL_ENV_FILE: Path = REPO_ROOT / ".env.local"
DEFAULT_ENV_FILE: Path = REPO_ROOT / ".env"

if LOCAL_ENV_FILE.exists():
    load_dotenv(LOCAL_ENV_FILE)

if DEFAULT_ENV_FILE.exists():
    load_dotenv(DEFAULT_ENV_FILE)

APP_AUTHOR: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR", "robust-python")
COOKIECUTTER_ROBUST_PYTHON_CACHE_FOLDER: Path = Path(
    platformdirs.user_cache_path(
        appname="cookiecutter-robust-python",
        appauthor=APP_AUTHOR,
        ensure_exists=True,
    )
).resolve()

DEFAULT_PROJECT_DEMOS_FOLDER = COOKIECUTTER_ROBUST_PYTHON_CACHE_FOLDER / "project_demos"
PROJECT_DEMOS_FOLDER: Path = Path(os.getenv(
    "COOKIECUTTER_ROBUST_PYTHON_PROJECT_DEMOS_FOLDER", default=DEFAULT_PROJECT_DEMOS_FOLDER
)).resolve()
DEFAULT_DEMO_NAME: str = "robust-python-demo"
DEMO_ROOT_FOLDER: Path = PROJECT_DEMOS_FOLDER / DEFAULT_DEMO_NAME

GENERATE_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "generate-demo.py"
GENERATE_DEMO_OPTIONS: tuple[str, ...] = (
    *("--demos-cache-folder", PROJECT_DEMOS_FOLDER),
)

LINT_FROM_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "lint-from-demo.py"
LINT_FROM_DEMO_OPTIONS: tuple[str, ...] = GENERATE_DEMO_OPTIONS

UPDATE_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "update-demo.py"
UPDATE_DEMO_OPTIONS: tuple[str, ...] = GENERATE_DEMO_OPTIONS


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION, name="generate-demo")
def generate_demo(session: Session) -> None:
    """Generates a project demo using the cookiecutter-robust-python template."""
    session.install("cookiecutter", "cruft", "platformdirs", "loguru", "python-dotenv", "typer")
    session.run("python", GENERATE_DEMO_SCRIPT, *GENERATE_DEMO_OPTIONS, *session.posargs)


@nox.session(python=False, name="clear-cache")
def clear_cache(session: Session) -> None:
    """Clear the cache of generated project demos.

    Not commonly used, but sometimes permissions might get messed up if exiting mid-build and such.
    """
    session.log("Clearing cache of generated project demos...")
    shutil.rmtree(PROJECT_DEMOS_FOLDER, ignore_errors=True)
    session.log("Cache cleared.")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def lint(session: Session):
    """Lint the template's own Python files and configurations."""
    session.log("Installing linting dependencies for the template source...")
    session.install("-e", ".", "--group", "lint")

    session.log(f"Running Ruff formatter check on template files with py{session.python}.")
    session.run("ruff", "format")

    session.log(f"Running Ruff check on template files with py{session.python}.")
    session.run("ruff", "check", "--verbose", "--fix")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION, name="lint-from-demo")
def lint_from_demo(session: Session):
    """Lint the generated project's Python files and configurations."""
    session.log("Installing linting dependencies for the generated project...")
    session.install("-e", ".", "--group", "dev", "--group", "lint")
    session.run("python", LINT_FROM_DEMO_SCRIPT, *LINT_FROM_DEMO_OPTIONS, *session.posargs)


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def docs(session: Session):
    """Build the template documentation website."""
    session.log("Installing documentation dependencies for the template docs...")
    session.install("-e", ".", "--group", "docs")

    session.log(f"Building template documentation with py{session.python}.")
    # Set path to allow Sphinx to import from template root if needed (e.g., __version__.py)
    # session.env["PYTHONPATH"] = str(Path(".").resolve()) # Add template root to PYTHONPATH for Sphinx

    docs_build_dir = Path("docs") / "_build" / "html"

    session.log(f"Cleaning template docs build directory: {docs_build_dir}")
    docs_build_dir.parent.mkdir(parents=True, exist_ok=True)
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-E")

    session.log("Building template documentation.")
    session.run("sphinx-build", "-b", "html", "docs", str(docs_build_dir), "-W")

    session.log(f"Template documentation built in {docs_build_dir.resolve()}.")


@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION)
def test(session: Session) -> None:
    """Run tests for the template's own functionality.

    This could involve:
    1. Rendering a project from the template into a temporary directory.
    2. Changing into the temporary directory.
    3. Running essential checks and tests *in the generated project* using uv run nox.
    """
    session.log("Running template tests...")
    session.log("Installing template testing dependencies...")
    # Sync deps from template's own pyproject.toml, e.g., 'dev' group that includes 'pytest', 'cookiecutter'
    session.install("-e", ".", "--group", "dev", "--group", "test")
    session.run("pytest", "tests")


@nox.parametrize(arg_names="add_rust_extension", arg_values_list=[False, True], ids=["no-rust", "rust"])
@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION, name="update-demo")
def update_demo(session: Session, add_rust_extension: bool) -> None:
    session.log("Installing script dependencies for updating generated project demos...")
    session.install("cookiecutter", "cruft", "platformdirs", "loguru", "python-dotenv", "typer")

    session.log("Updating generated project demos...")
    args: list[str] = [*UPDATE_DEMO_OPTIONS]
    if add_rust_extension:
        args.append("--add-rust-extension")
    session.run("python", UPDATE_DEMO_SCRIPT, *args)


@nox.session(python=False, name="release-template")
def release_template(session: Session):
    """Run the release process for the TEMPLATE using Commitizen.

    Requires uvx in PATH (from uv install). Requires Git.
    Assumes Conventional Commits practice is followed for TEMPLATE repository.
    Optionally accepts increment level (major, minor, patch) after '--'.
    """
    session.log("Running release process for the TEMPLATE using Commitizen...")
    try:
        session.run("git", "version", success_codes=[0], external=True, silent=True)
    except CommandFailed:
        session.log("Git command not found. Commitizen requires Git.")
        session.skip("Git not available.")

    session.log("Checking Commitizen availability via uvx.")
    session.run("cz", "--version", successcodes=[0])

    increment = session.posargs[0] if session.posargs else None
    session.log(
        "Bumping template version and tagging release (increment: %s).",
        increment if increment else "default",
    )

    cz_bump_args = ["uvx", "cz", "bump", "--changelog"]

    if increment:
        cz_bump_args.append(f"--increment={increment}")

    session.log("Running cz bump with args: %s", cz_bump_args)
    # success_codes=[0, 1] -> Allows code 1 which means 'nothing to bump' if no conventional commits since last release
    session.run(*cz_bump_args, success_codes=[0, 1], external=True)

    session.log("Template version bumped and tag created locally via Commitizen/uvx.")
    session.log("IMPORTANT: Push commits and tags to remote (`git push --follow-tags`) to trigger CD for the TEMPLATE.")


@nox.session(python=False, name="remove-demo-release")
def remove_demo_release(session: Session) -> None:
    """Deletes the latest demo release."""
    session.run("git", "branch", "-d", f"release/{session.posargs[0]}", external=True)
    session.run("git", "push", "--progress", "--porcelain", "origin", f"release/{session.posargs[0]}", external=True)

