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
from util import RepoMetadata
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
        require_clean_and_up_to_date_repo()
        git("checkout", DEMO.develop_branch)
        try:
            nox("setup-release", "--", "MINOR")
            logger.success(f"Successfully created release {demo_name}")
            _ensure_github_repo_set(repo=DEMO)

        except subprocess.CalledProcessError as error:
            logger.warning(f"Failed to setup release: {error}")
            _rollback_failed_release()
            raise error

        git("push", "-u")


def _ensure_github_repo_set(repo: RepoMetadata) -> None:
    """Ensures the repo has a github repo set."""
    gh("repo", "set-default", repo.app_author, repo.app_name)


def _rollback_failed_release() -> None:
    """Returns the demo repo back to the state it was prior to the release attempt."""
    starting_demo_branch: str = get_current_branch()

    if starting_demo_branch != "develop":
        git("checkout", DEMO.develop_branch)

    git("checkout", ".")
    git("branch", "-D", starting_demo_branch)


def _create_demo_pr(version: str) -> None:
    """Creates a pull request to merge the demo's feature branch into ."""
    pr_kwargs: dict[str, str] = {
        "--title": f"Release/{version}"
    }
    publish_release_commands: list[list[str]] = [
        ["gh", "pr", "create", *itertools.chain(pr_kwargs.items())],
    ]

