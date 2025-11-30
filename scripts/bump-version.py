# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "python-dotenv",
#   "typer",
#   "tomli>=2.0.0;python_version<'3.11'",
# ]
# ///
"""Script responsible for bumping the version of cookiecutter-robust-python using CalVer."""

import sys
from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Optional

import typer

from util import bump_version
from util import calculate_calver
from util import REPO_FOLDER


try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def main(
    micro: Annotated[Optional[int], typer.Argument(help="Override micro version (default: auto-increment)")] = None,
) -> None:
    """Bump version using CalVer (YYYY.MM.MICRO).

    CalVer format:
    - YYYY: Four-digit year
    - MM: Month (1-12, no leading zero)
    - MICRO: Incremental patch number, resets to 0 each month
    """
    try:
        current_version: str = get_current_version()
        new_version: str = calculate_calver(current_version, micro)

        typer.secho(f"Bumping version: {current_version} -> {new_version}", fg="blue")
        bump_version(new_version)
        typer.secho(f"Version bumped to {new_version}", fg="green")
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


def get_current_version() -> str:
    """Read current version from pyproject.toml."""

    pyproject_path: Path = REPO_FOLDER / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)
        return data["project"]["version"]


if __name__ == "__main__":
    cli()
