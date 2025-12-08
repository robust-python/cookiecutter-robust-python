# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "cruft",
#   "python-dotenv",
#   "typer",
# ]
# ///
import itertools
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Annotated
from typing import Any
from typing import Optional

import cruft
import typer
from cookiecutter.utils import work_in

from util import _read_cruft_file
from util import DEMO
from util import is_ancestor
from util import get_current_branch
from util import get_current_commit
from util import get_demo_name
from util import get_last_cruft_update_commit
from util import gh
from util import git
from util import FolderOption
from util import REPO_FOLDER
from util import require_clean_and_up_to_date_demo_repo
from util import TEMPLATE
from util import uv


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def update_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False,
    min_python_version: Annotated[str, typer.Option("--min-python-version")] = "3.10",
    max_python_version: Annotated[str, typer.Option("--max-python-version")] = "3.14",
    branch_override: Annotated[Optional[str], typer.Option("--branch-override")] = None
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demo_path: Path = demos_cache_folder / demo_name

    typer.secho(f"template:\n\tcurrent_branch: {get_current_branch()}\n\tcurrent_commit: {get_current_commit()}")
    if branch_override is not None:
        typer.secho(f"Overriding current branch name for demo reference. Using '{branch_override}' instead.")
        desired_branch_name: str = branch_override
    else:
        desired_branch_name: str = get_current_branch()
    template_commit: str = get_current_commit()

    _validate_template_main_not_checked_out(branch=desired_branch_name)
    require_clean_and_up_to_date_demo_repo(demo_path=demo_path)
    _checkout_demo_develop_or_existing_branch(demo_path=demo_path, branch=desired_branch_name)
    last_update_commit: str = get_last_cruft_update_commit(demo_path=demo_path)

    if template_commit == last_update_commit:
        typer.secho(
            f"{demo_name} is already up to date with {desired_branch_name} at {last_update_commit}",
            fg=typer.colors.YELLOW
        )

    if not is_ancestor(last_update_commit, template_commit):
        raise ValueError(
            f"The last update commit '{last_update_commit}' is not an ancestor of the current commit "
            f"'{template_commit}'."
        )

    typer.secho(f"Updating demo project at {demo_path=}.", fg="yellow")
    with work_in(demo_path):
        typer.secho(f"demo:\n\tcurrent_branch: {get_current_branch()}\n\tcurrent_commit: {get_current_commit()}")
        if get_current_branch() != desired_branch_name:
            git("checkout", "-b", desired_branch_name, DEMO.develop_branch)

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
        git("push", "-u", "origin", desired_branch_name)
        if desired_branch_name != "develop":
            _create_demo_pr(demo_path=demo_path, branch=desired_branch_name, commit_start=last_update_commit)


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
        local_result: Optional[CompletedProcess] = git("branch", "--list", branch)
        return local_result is not None and branch in local_result.stdout


def __has_existing_remote_demo_branch(demo_path: Path, branch: str) -> bool:
    """Returns whether a remote branch has been made for the given branch."""
    with work_in(demo_path):
        remote_result: Optional[CompletedProcess] = git("ls-remote", DEMO.remote, branch)
        return remote_result is not None and branch in remote_result.stdout


def _validate_template_main_not_checked_out(branch: str) -> None:
    """Validates that the cookiecutter isn't currently on main.

    We allow direct develop commits (although avoid it usually), but never direct main. This may change later if the
    template moves to a trunk based structure, but for now options are being kept open due to the possibility of a
    package release handling demo creation one day.
    """
    main_like_names: list[str] = ["main", "master"]
    if branch == TEMPLATE.main_branch or branch in main_like_names:
        raise ValueError(f"Updating demos directly to main is not allowed currently.")


def _create_demo_pr(demo_path: Path, branch: str, commit_start: str) -> None:
    """Creates a PR to merge the given branch into develop."""
    gh("repo", "set-default", f"{DEMO.app_author}/{DEMO.app_name}")
    search_results: subprocess.CompletedProcess = gh("pr", "list", "--state", "open", "--search", branch)
    typer.secho(f"_create_demo_pr - {search_results.stdout}")

    if "no pull requests match your search" not in search_results.stdout:
        url: str = _get_pr_url(branch=branch)
        typer.secho(f"Skipping PR creation due to existing PR found for branch {branch} at {url}")
        return

    body: str = _get_demo_feature_pr_body(demo_path=demo_path, commit_start=commit_start)

    pr_kwargs: dict[str, Any] = {
        "--title": branch.capitalize(),
        "--body": body,
        "--base": DEMO.develop_branch,
        "--assignee": "@me",
        "--repo": f"{DEMO.app_author}/{DEMO.app_name}",
    }
    gh("pr", "create", *itertools.chain.from_iterable(pr_kwargs.items()))


def _get_pr_url(branch: str) -> str:
    """Returns the url of the current branch's PR."""
    result: subprocess.CompletedProcess = gh("pr", "view", branch, "--json", "url", "--jq", ".url")
    typer.secho(f"_get_pr_url - {result.stdout=}")
    if result.returncode != 0:
        raise ValueError(f"Failed to find a PR URL for branch {branch}.")
    return result.stdout.strip()


def _get_demo_feature_pr_body(demo_path: Path, commit_start: str) -> str:
    """Creates the body of the demo feature pull request."""
    cruft_config: dict[str, Any] = _read_cruft_file(demo_path)
    commit_end: Optional[str] = cruft_config.get("commit", None)
    if commit_end is None:
        raise ValueError(f"Unable to find latest commit in .cruft.json for demo at {demo_path}.")
    rev_range: str = f"{commit_start}..{commit_end}"
    return rev_range


if __name__ == '__main__':
    cli()
