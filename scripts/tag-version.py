"""Script responsible for creating and pushing git tags for cookiecutter-robust-python releases."""
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "python-dotenv",
#   "typer",
#   "tomli>=2.0.0;python_version<'3.11'",
# ]
# ///

from pathlib import Path
from typing import Annotated
from typing import Any

import typer
from cookiecutter.utils import work_in

from scripts.util import git
from util import REPO_FOLDER


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    push: Annotated[bool, typer.Option("--push", help="Push the tag to origin after creating it")] = False
) -> None:
    """Create a git tag for the current version.

    Creates an annotated tag in the format 'vYYYY.MM.MICRO' based on the
    version in pyproject.toml. Optionally pushes the tag to origin.
    """
    version: str = get_current_version()
    tag_name: str = f"v{version}"
    with work_in(REPO_FOLDER):
        typer.secho(f"Creating tag: {tag_name}", fg="blue")
        git("tag", "-a", tag_name, "-m", f"Release {version}")
        typer.secho(f"Tag {tag_name} created successfully", fg="green")

        if push:
            typer.secho(f"Pushing tag {tag_name} to origin...", fg="blue")
            git("push", "origin", tag_name)
            typer.secho(f"Tag {tag_name} pushed to origin", fg="green")


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    pyproject_path: Path = REPO_FOLDER / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)
        return data["project"]["version"]


if __name__ == "__main__":
    cli()
