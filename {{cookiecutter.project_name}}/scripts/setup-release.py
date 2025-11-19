"""Script responsible for preparing a release of the {{cookiecutter.project_name}} package."""

import argparse
import subprocess
from typing import Optional

from scripts.util import require_clean_and_up_to_date_repo
from util import REPO_FOLDER
from util import bump_version
from util import check_dependencies
from util import create_release_branch
from util import get_bumped_package_version
from util import get_package_version


def main() -> None:
    """Parses args and passes through to setup_release."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    setup_release(increment=args.increment)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for prepare-release."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="prepare-release", usage="python ./scripts/prepare-release.py patch"
    )
    parser.add_argument(
        "increment",
        nargs="?",
        default=None,
        type=str,
        help="Increment type to use when preparing the release.",
        choices=["MAJOR", "MINOR", "PATCH", "PRERELEASE"],
    )
    return parser


def setup_release(increment: Optional[str] = None) -> None:
    """Prepares a release of the {{cookiecutter.project_name}} package.

    Will try to create the release and push, however will return to pre-existing state on error.
    """
    check_dependencies(path=REPO_FOLDER, dependencies=["git"])
    require_clean_and_up_to_date_repo()

    current_version: str = get_package_version()
    new_version: str = get_bumped_package_version(increment=increment)
    try:
        _setup_release(increment=increment, current_version=current_version, new_version=new_version)
    except Exception as error:
        _rollback_release(version=new_version)
        raise error


def _setup_release(increment: str, current_version: str, new_version: str) -> None:
    """Prepares a release of the {{cookiecutter.project_name}} package.

    Sets up a release branch from the branch develop, bumps the version, and creates a release commit. Does not tag the
    release or push any changes.
    """
    create_release_branch(new_version=new_version)
    bump_version(increment=increment)

    commands: list[list[str]] = [
        ["uv", "sync", "--all-groups"],
        ["git", "add", "."],
        ["git", "commit", "-m", f"bump: version {current_version} → {new_version}", "--no-verify"],
    ]

    for command in commands:
        subprocess.run(command, cwd=REPO_FOLDER, capture_output=True, check=True)


def _rollback_release(version: str) -> None:
    """Rolls back to the pre-existing state on error."""
    commands: list[list[str]] = [
        ["git", "checkout", "develop"],
        ["git", "checkout", "."],
        ["git", "branch", "-D", f"release/{version}"]
    ]

    for command in commands:
        subprocess.run(command, cwd=REPO_FOLDER, check=False)


if __name__ == "__main__":
    main()
