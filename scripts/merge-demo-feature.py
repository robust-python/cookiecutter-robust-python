# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "cookiecutter",
#    "cruft",
#    "python-dotenv",
#    "typer",
# ]
# ///
import subprocess
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from cookiecutter.utils import work_in

from util import DEMO
from util import FolderOption
from util import get_current_branch
from util import get_demo_name
from util import gh


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def merge_demo_feature(
    branch: Optional[str] = None,
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")] = None,
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False
) -> None:
    """Searches for the given demo feature branch's PR and merges it if ready."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    if demos_cache_folder is None:
        raise ValueError("Failed to provide a demos cache folder.")

    demo_path: Path = demos_cache_folder / demo_name
    branch: str = branch if branch is not None else get_current_branch()

    with work_in(demo_path):
        pr_number_query: subprocess.CompletedProcess = gh(
            "pr", "list", "--head", branch, "--base", DEMO.develop_branch, "--json", "number", "--jq", "'.[0].number'"
        )
        pr_number: str = pr_number_query.stdout.strip()
        if pr_number == "":
            raise ValueError("Failed to find an existing PR from {} to {DEMO.develop_branch}")

        gh("pr", "merge", pr_number, "--auto", "--delete-branch")


if __name__ == "__main__":
    cli()
