"""Python script for generating a demo project."""
import sys
from pathlib import Path
from typing import Annotated

import typer

from util import FolderOption
from util import generate_demo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False,
    no_cache: Annotated[bool, typer.Option("--no-cache", "-n")] = False
) -> None:
    """Generates a project demo using the cookiecutter-robust-python template."""
    try:
        generate_demo(
            demos_cache_folder=demos_cache_folder,
            add_rust_extension=add_rust_extension,
            no_cache=no_cache
        )
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
