# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "cruft",
#   "python-dotenv",
#   "typer",
# ]
# ///
"""Script responsible for extracting release notes for the cookiecutter-robust-python template."""

import sys
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer

from util import get_latest_release_notes


cli: typer.Typer = typer.Typer()

DEFAULT_RELEASE_NOTES_PATH: Path = Path("release_notes.md")


@cli.callback(invoke_without_command=True)
def main(
    path: Annotated[
        Optional[Path],
        typer.Argument(help=f"Path to write release notes (default: {DEFAULT_RELEASE_NOTES_PATH})")
    ] = None,
) -> None:
    """Extract release notes for the current version.

    Uses commitizen to generate changelog entries for unreleased changes.
    Must be run before tagging the release.
    """
    try:
        output_path: Path = path if path else DEFAULT_RELEASE_NOTES_PATH
        release_notes: str = get_latest_release_notes()
        output_path.write_text(release_notes)
        typer.secho(f"Release notes written to {output_path}", fg="green")
    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
