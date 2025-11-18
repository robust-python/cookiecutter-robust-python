# /// script
# requires-python = ">=3.10"
# dependencies = [
#     cookiecutter,
#     cruft,
#     typer,
# ]
# ///
from pathlib import Path
from typing import Annotated

import typer
from cookiecutter.utils import work_in

from util import get_demo_name
from util import git
from util import is_ancestor
from util import uv
from util import validate_is_synced_ancestor
from util import FolderOption


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def release_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    min_python_version: Annotated[str, typer.Option("--min-python-version")],
    max_python_version: Annotated[str, typer.Option("--max-python-version")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False
) -> None:
    """Creates a release of the demo's current develop branch if changes exist."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demo_path: Path = demos_cache_folder / demo_name




def _validate_demo_develop_up_to_date(demo_path: Path) -> None:
    """Ensures the demo's develop branch is up to date."""
    with work_in(demo_path):
        validate_is_synced_ancestor(ancestor=)







