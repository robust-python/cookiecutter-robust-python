"""Noxfile for the cookiecutter-robust-python template."""

# /// script
# dependencies = ["nox>=2025.5.1", "platformdirs>=4.3.8", "python-dotenv>=1.0.0"]
# ///

import os
import shutil
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import nox
import platformdirs
from dotenv import load_dotenv
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

DEFAULT_DEMOS_CACHE_FOLDER = COOKIECUTTER_ROBUST_PYTHON_CACHE_FOLDER / "project_demos"
DEMOS_CACHE_FOLDER: Path = Path(
    os.getenv(
        "COOKIECUTTER_ROBUST_PYTHON__DEMOS_CACHE_FOLDER", default=DEFAULT_DEMOS_CACHE_FOLDER
    )
).resolve()
DEFAULT_DEMO_NAME: str = "robust-python-demo"
DEMO_ROOT_FOLDER: Path = DEMOS_CACHE_FOLDER / DEFAULT_DEMO_NAME

GENERATE_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "generate-demo.py"
GENERATE_DEMO_OPTIONS: tuple[str, ...] = (
    *("--demos-cache-folder", DEMOS_CACHE_FOLDER),
)

LINT_FROM_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "lint-from-demo.py"
LINT_FROM_DEMO_OPTIONS: tuple[str, ...] = GENERATE_DEMO_OPTIONS

UPDATE_DEMO_SCRIPT: Path = SCRIPTS_FOLDER / "update-demo.py"
UPDATE_DEMO_OPTIONS: tuple[str, ...] = (
    *GENERATE_DEMO_OPTIONS,
    *("--min-python-version", "3.10"),
    *("--max-python-version", "3.14")
)

MERGE_DEMO_FEATURE_SCRIPT: Path = SCRIPTS_FOLDER / "merge-demo-feature.py"
MERGE_DEMO_FEATURE_OPTIONS: tuple[str, ...] = GENERATE_DEMO_OPTIONS

BUMP_VERSION_SCRIPT: Path = SCRIPTS_FOLDER / "bump-version.py"
GET_RELEASE_NOTES_SCRIPT: Path = SCRIPTS_FOLDER / "get-release-notes.py"
TAG_VERSION_SCRIPT: Path = SCRIPTS_FOLDER / "tag-version.py"


@dataclass
class RepoMetadata:
    """Metadata for a given repo."""
    app_name: str
    app_author: str
    remote: str
    main_branch: str
    develop_branch: str


TEMPLATE: RepoMetadata = RepoMetadata(
    app_name=os.getenv("COOKIECUTTER_ROBUST_PYTHON__APP_NAME"),
    app_author=os.getenv("COOKIECUTTER_ROBUST_PYTHON__APP_AUTHOR"),
    remote=os.getenv("COOKIECUTTER_ROBUST_PYTHON__REMOTE"),
    main_branch=os.getenv("COOKIECUTTER_ROBUST_PYTHON__MAIN_BRANCH"),
    develop_branch=os.getenv("COOKIECUTTER_ROBUST_PYTHON__DEVELOP_BRANCH")
)

PYTHON_DEMO: RepoMetadata = RepoMetadata(
    app_name=os.getenv("ROBUST_PYTHON_DEMO__APP_NAME"),
    app_author=os.getenv("ROBUST_PYTHON_DEMO__APP_AUTHOR"),
    remote=os.getenv("ROBUST_PYTHON_DEMO__REMOTE"),
    main_branch=os.getenv("ROBUST_PYTHON_DEMO__MAIN_BRANCH"),
    develop_branch=os.getenv("ROBUST_PYTHON_DEMO__DEVELOP_BRANCH")
)

MATURIN_DEMO: RepoMetadata = RepoMetadata(
    app_name=os.getenv("ROBUST_MATURIN_DEMO__APP_NAME"),
    app_author=os.getenv("ROBUST_MATURIN_DEMO__APP_AUTHOR"),
    remote=os.getenv("ROBUST_MATURIN_DEMO__REMOTE"),
    main_branch=os.getenv("ROBUST_MATURIN_DEMO__MAIN_BRANCH"),
    develop_branch=os.getenv("ROBUST_MATURIN_DEMO__DEVELOP_BRANCH")
)


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
    shutil.rmtree(DEMOS_CACHE_FOLDER, ignore_errors=True)
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


@nox.parametrize(
    arg_names="demo",
    arg_values_list=[PYTHON_DEMO, MATURIN_DEMO],
    ids=["robust-python-demo", "robust-maturin-demo"]
)
@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION, name="update-demo")
def update_demo(session: Session, demo: RepoMetadata) -> None:
    session.log("Installing script dependencies for updating generated project demos...")
    session.install("cookiecutter", "cruft", "platformdirs", "loguru", "python-dotenv", "typer")

    session.log("Updating generated project demos...")
    args: list[str] = [*UPDATE_DEMO_OPTIONS]
    if "maturin" in demo.app_name:
        args.append("--add-rust-extension")

    if session.posargs:
        args.extend(session.posargs)

    demo_env: dict[str, Any] = {f"ROBUST_DEMO__{key.upper()}": value for key, value in asdict(demo).items()}
    session.run("uv", "run", UPDATE_DEMO_SCRIPT, *args, env=demo_env)


@nox.parametrize(
    arg_names="demo",
    arg_values_list=[PYTHON_DEMO, MATURIN_DEMO],
    ids=["robust-python-demo", "robust-maturin-demo"]
)
@nox.session(python=DEFAULT_TEMPLATE_PYTHON_VERSION, name="merge-demo-feature")
def merge_demo_feature(session: Session, demo: RepoMetadata) -> None:
    """Automates merging the current feature branch to develop in all templates.

    Assumes that all PR's already exist.
    """
    args: list[str] = [*MERGE_DEMO_FEATURE_OPTIONS]
    if "maturin" in demo.app_name:
        args.append("--add-rust-extension")
    if session.posargs:
        args.extend(session.posargs)
    session.run("uv", "run", MERGE_DEMO_FEATURE_SCRIPT, *args)


@nox.session(python=False, name="bump-version")
def bump_version(session: Session) -> None:
    """Bump version using CalVer (YYYY.MM.MICRO).

    Usage:
      nox -s bump-version          # Auto-increment micro for current month
      nox -s bump-version -- 5     # Force micro version to 5
    """
    session.run("python", BUMP_VERSION_SCRIPT, *session.posargs, external=True)


@nox.session(python=False, name="build-python")
def build_python(session: Session) -> None:
    """Build sdist and wheel packages for the template."""
    session.log("Building sdist and wheel packages...")
    dist_dir = REPO_ROOT / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    session.run("uv", "build", external=True)
    session.log(f"Packages built in {dist_dir}")


@nox.session(python=False, name="publish-python")
def publish_python(session: Session) -> None:
    """Publish packages to PyPI.

    Usage:
      nox -s publish-python                    # Publish to PyPI
      nox -s publish-python -- --test-pypi     # Publish to TestPyPI
    """
    session.log("Checking built packages with Twine.")
    session.run("uvx", "twine", "check", "dist/*", external=True)

    if "--test-pypi" in session.posargs:
        session.log("Publishing packages to TestPyPI.")
        session.run("uv", "publish", "--publish-url", "https://test.pypi.org/legacy/", external=True)
    else:
        session.log("Publishing packages to PyPI.")
        session.run("uv", "publish", external=True)


@nox.session(python=False, name="tag-version")
def tag_version(session: Session) -> None:
    """Create and push a git tag for the current version.

    Usage:
      nox -s tag-version           # Create tag locally
      nox -s tag-version -- push   # Create and push tag
    """
    args: list[str] = ["--push"] if "push" in session.posargs else []
    session.run("python", TAG_VERSION_SCRIPT, *args, external=True)


@nox.session(python=False, name="get-release-notes")
def get_release_notes(session: Session) -> None:
    """Extract release notes for the current version.

    Usage:
      nox -s get-release-notes                      # Write to release_notes.md
      nox -s get-release-notes -- /path/to/file.md  # Write to custom path
    """
    session.run("python", GET_RELEASE_NOTES_SCRIPT, *session.posargs, external=True)


@nox.session(python=False, name="remove-demo-release")
def remove_demo_release(session: Session) -> None:
    """Deletes the latest demo release."""
    session.run("git", "branch", "-d", f"release/{session.posargs[0]}", external=True)
    session.run("git", "push", "--progress", "--porcelain", "origin", f"release/{session.posargs[0]}", external=True)
