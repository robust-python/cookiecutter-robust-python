"""Script responsible for first time setup of the project's git repo.

Since this is a first time setup script, we intentionally only use builtin Python dependencies.
"""

import argparse
import subprocess
from pathlib import Path

from util import check_dependencies
from util import existing_dir


def main() -> None:
    """Parses command line input and passes it through to setup_git."""
    parser: argparse.ArgumentParser = get_parser()
    args: argparse.Namespace = parser.parse_args()
    setup_git(path=args.path)


def setup_git(path: Path) -> None:
    """Set up the provided cookiecutter-robust-python project's git repo."""
    commands: list[list[str]] = [
        ["git", "init"],
        ["git", "branch", "-m", "master", "main"],
        ["git", "add", "."],
        ["git", "commit", "-m", "feat: initial commit"],
        ["git", "checkout", "-b", "develop", "main"],
    ]
    check_dependencies(path=path, dependencies=["git"])

    for command in commands:
        subprocess.run(command, cwd=path, stderr=subprocess.STDOUT)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for setup-git."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="setup-git",
        usage="python ./scripts/setup-git.py . -u robust-python -n robust-python-demo",
        description="Set up the provided cookiecutter-robust-python project's git repo.",
    )
    parser.add_argument(
        "path",
        type=existing_dir,
        metavar="PATH",
        help="Path to the repo's root directory (must already exist).",
    )
    return parser


if __name__ == "__main__":
    main()
