# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "python-dotenv",
#   "typer",
#   "tomli>=2.0.0;python_version<'3.11'",
# ]
# ///
"""Script responsible for preparing a release of the cookiecutter-robust-python template."""

import sys
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Optional

import typer
from cookiecutter.utils import work_in

from util import bump_version
from util import calculate_calver
from util import git
from util import REPO_FOLDER
from util import TEMPLATE


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    micro: Annotated[
        Optional[int],
        typer.Argument(help="Override micro version (default: auto-increment)")
    ] = None,
) -> None:
    """Prepare a release by creating a release branch and bumping the version.

    Creates a release branch from develop, bumps the version using CalVer,
    and creates the initial bump commit. Does not push any changes.

    CalVer format: YYYY.MM.MICRO
    """
    try:
        current_version: str = get_current_version()
        new_version: str = calculate_calver(current_version, micro)

        typer.secho(f"Setting up release: {current_version} -> {new_version}", fg="blue")

        setup_release(current_version=current_version, new_version=new_version, micro=micro)

        typer.secho(f"Release branch created: release/{new_version}", fg="green")
        typer.secho("Next steps:", fg="blue")
        typer.secho(f"  1. Review changes and push: git push -u origin release/{new_version}", fg="white")
        typer.secho("  2. Create a pull request to main", fg="white")
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    pyproject_path: Path = REPO_FOLDER / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)
        return data["project"]["version"]


def setup_release(current_version: str, new_version: str, micro: Optional[int] = None) -> None:
    """Prepares a release of the cookiecutter-robust-python template.

    Creates a release branch from develop, bumps the version, and creates a release commit.
    Rolls back on error.
    """
    with work_in(REPO_FOLDER):
        try:
            _setup_release(current_version=current_version, new_version=new_version, micro=micro)
        except Exception as error:
            _rollback_release(version=new_version)
            raise error


def _setup_release(current_version: str, new_version: str, micro: Optional[int] = None) -> None:
    """Internal setup release logic."""
    develop_branch: str = TEMPLATE.develop_branch
    release_branch: str = f"release/{new_version}"

    # Create release branch from develop
    typer.secho(f"Creating branch {release_branch} from {develop_branch}...", fg="blue")
    git("checkout", "-b", release_branch, develop_branch)

    # Bump version
    typer.secho(f"Bumping version to {new_version}...", fg="blue")
    bump_version(new_version)

    # Sync dependencies
    typer.secho("Syncing dependencies...", fg="blue")
    git("add", ".")

    # Create bump commit
    typer.secho("Creating bump commit...", fg="blue")
    git("commit", "-m", f"bump: version {current_version} → {new_version}")


def _rollback_release(version: str) -> None:
    """Rolls back to the pre-existing state on error."""
    develop_branch: str = TEMPLATE.develop_branch
    release_branch: str = f"release/{version}"

    typer.secho(f"Rolling back release {version}...", fg="yellow")

    # Checkout develop and discard changes
    git("checkout", develop_branch, ignore_error=True)
    git("checkout", ".", ignore_error=True)

    # Delete the release branch if it exists
    git("branch", "-D", release_branch, ignore_error=True)


if __name__ == "__main__":
    cli()
