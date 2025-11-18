# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "cruft",
#   "python-dotenv",
#   "retrocookie",
#   "typer",
# ]
# ///

import os
from pathlib import Path
from typing import Annotated

import pre_commit.main
import typer
from retrocookie.core import retrocookie

from util import git
from util import FolderOption
from util import in_new_demo
from util import require_clean_and_up_to_date_repo


# These still may need linted, but retrocookie shouldn't be used on them
IGNORED_FILES: list[str] = [
    "pyproject.toml",
    "uv.lock",
]


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def lint_from_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False,
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    develop_branch: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH", "develop")
    with in_new_demo(
        demos_cache_folder=demos_cache_folder,
        add_rust_extension=add_rust_extension,
        no_cache=no_cache
    ) as demo_path:
        require_clean_and_up_to_date_repo()
        git("checkout", develop_branch)
        git("branch", "-D", "temp/lint-from-demo", ignore_error=True)
        git("checkout", "-b", "temp/lint-from-demo", develop_branch)
        pre_commit.main.main(["run", "--all-files", "--show-diff-on-failure"])

        for path in IGNORED_FILES:
            git("checkout", "HEAD", "--", path)
        git("add", ".")
        git("commit", "-m", "meta: lint-from-demo", "--no-verify")
    retrocookie(instance_path=demo_path, commits=[f"{develop_branch}..temp/lint-from-demo"])


if __name__ == '__main__':
    cli()
