# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "cruft",
#   "python-dotenv",
#   "typer",
# ]
# ///

import sys
from pathlib import Path
from subprocess import CompletedProcess
from typing import Annotated
from typing import Optional

import cruft
import typer
from cookiecutter.utils import work_in

from util import DEMO
from util import is_ancestor
from util import get_current_branch
from util import get_current_commit
from util import get_demo_name
from util import get_last_cruft_update_commit
from util import git
from util import FolderOption
from util import REPO_FOLDER
from util import require_clean_and_up_to_date_repo
from util import TEMPLATE
from util import uv


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def update_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False,
    min_python_version: Annotated[str, typer.Option("--min-python-version")] = "3.10",
    max_python_version: Annotated[str, typer.Option("--max-python-version")] = "3.14"
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demo_path: Path = demos_cache_folder / demo_name

    current_branch: str = get_current_branch()
    template_commit: str = get_current_commit()

    _validate_template_main_not_checked_out(branch=current_branch)
    require_clean_and_up_to_date_repo(demo_path=demo_path)
    _checkout_demo_develop_or_existing_branch(demo_path=demo_path, branch=current_branch)
    last_update_commit: str = get_last_cruft_update_commit(demo_path=demo_path)

    if not is_ancestor(last_update_commit, template_commit):
        raise ValueError(
            f"The last update commit '{last_update_commit}' is not an ancestor of the current commit "
            f"'{template_commit}'."
        )

    typer.secho(f"Updating demo project at {demo_path=}.", fg="yellow")
    with work_in(demo_path):
        if current_branch != "develop":
            git("checkout", "-b", current_branch)

        uv("python", "pin", min_python_version)
        uv("python", "install", min_python_version)
        cruft.update(
            project_dir=demo_path,
            template_path=REPO_FOLDER,
            extra_context={
                "project_name": demo_name,
                "add_rust_extension": add_rust_extension,
                "min_python_version": min_python_version,
                "max_python_version": max_python_version
            },
        )
        uv("lock")
        git("add", ".")
        git("commit", "-m", f"chore: {last_update_commit} -> {template_commit}", "--no-verify")
        git("push", "-u", "origin", current_branch)


def _checkout_demo_develop_or_existing_branch(demo_path: Path, branch: str) -> None:
    """Checkout either develop or an existing demo branch."""
    with work_in(demo_path):
        if __has_existing_local_demo_branch(demo_path=demo_path, branch=branch):
            typer.secho(f"Local demo found, updating demo from base {branch}")
            git("checkout", branch)
            return

        if __has_existing_remote_demo_branch(demo_path=demo_path, branch=branch):
            remote_branch: str = f"{DEMO.remote}/{branch}"
            typer.secho(f"Remote demo found, updating demo from base {remote_branch}")
            git("checkout", "-b", branch, remote_branch)
            return

        git("checkout", "develop")


def __has_existing_local_demo_branch(demo_path: Path, branch: str) -> bool:
    """Returns whether a local branch has been made for the given branch."""
    with work_in(demo_path):
        local_result: Optional[CompletedProcess] = git("branch", "--list", branch, text=True)
        return local_result is not None and branch in local_result.stdout


def __has_existing_remote_demo_branch(demo_path: Path, branch: str) -> bool:
    """Returns whether a remote branch has been made for the given branch."""
    with work_in(demo_path):
        remote_result: Optional[CompletedProcess] = git("ls-remote", DEMO.remote, branch, text=True)
        return remote_result is not None and branch in remote_result.stdout


def _set_demo_to_clean_branch(demo_path: Path, branch: str) -> None:
    """Checks out the demo branch and validates it is up to date."""
    with work_in(demo_path):
        git("checkout", "develop")


def _validate_template_main_not_checked_out(branch: str) -> None:
    """Validates that the cookiecutter isn't currently on main.

    We allow direct develop commits (although avoid it usually), but never direct main. This may change later if the
    template moves to a trunk based structure, but for now options are being kept open due to the possibility of a
    package release handling demo creation one day.
    """
    main_like_names: list[str] = ["main", "master"]
    if branch == TEMPLATE.main_branch or branch in main_like_names:
        raise ValueError(f"Updating demos directly to main is not allowed currently.")


if __name__ == '__main__':
    cli()
