# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "cookiecutter",
#    "cruft",
#    "python-dotenv",
#    "typer",
# ]
# ///
import itertools
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

import typer
from cookiecutter.utils import work_in
from loguru import logger

from util import get_current_branch
from util import get_demo_name
from util import gh
from util import git
from util import nox
from util import require_clean_and_up_to_date_repo
from util import FolderOption
from util import DEMO


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def release_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False
) -> None:
    """Creates a release of the demo's current develop branch if changes exist."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demo_path: Path = demos_cache_folder / demo_name

    with work_in(demo_path):
        require_clean_and_up_to_date_repo(demo_path)
        git("checkout", DEMO.develop_branch)
        try:
            nox("setup-release", "--", "MINOR")
            logger.success(f"Successfully created release {demo_name}")
            gh("repo", "set-default", DEMO.app_author, DEMO.app_name)

        except subprocess.CalledProcessError as error:
            logger.warning(f"Failed to setup release: {error}")
            _rollback_failed_release()
            raise error

        git("push", "-u")
        _create_demo_pr()


def _rollback_failed_release() -> None:
    """Returns the demo repo back to the state it was prior to the release attempt."""
    starting_demo_branch: str = get_current_branch()

    if starting_demo_branch != "develop":
        git("checkout", DEMO.develop_branch)

    git("checkout", ".")
    git("branch", "-D", starting_demo_branch)


def _create_demo_pr() -> None:
    """Creates a pull request to merge the demo's feature branch into ."""
    current_branch: str = get_current_branch()
    if not current_branch.startswith("release/"):
        raise ValueError("Not in a release branch, canceling PR creation.")
    title: str = current_branch.capitalize()
    release_notes: str = __get_demo_release_notes()

    pr_kwargs: dict[str, str] = {
        "--title": title,
        "--body": release_notes,
        "--assignee": "@me",
        "--base": "main",
    }
    command: list[str] = ["gh", "pr", "create", *itertools.chain(pr_kwargs.items())]
    subprocess.run(command, check=True)


def __get_demo_release_notes() -> str:
    """Returns the release notes for the demo."""
    temp_folder: Path = Path(tempfile.mkdtemp()).resolve()
    notes_path: Path = temp_folder / "body.md"
    command: list[str] = ["uv", "run", "./scripts/get-release-notes.py", notes_path]
    subprocess.run(command, check=True)

    notes_contents: str = notes_path.read_text()
    return notes_contents
