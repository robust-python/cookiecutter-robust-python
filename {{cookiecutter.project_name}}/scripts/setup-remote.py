"""Script responsible for first time setup of the project's git repo's remote connection.

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
    setup_remote(path=args.path, repository_host=args.repository_host, repository_path=args.repository_path)


def setup_remote(path: Path, repository_host: str, repository_path: str) -> None:
    """Set up the provided cookiecutter-robust-python project's git repo."""
    commands: list[list[str]] = [
        ["git", "remote", "add", "origin", f"https://{repository_host}/{repository_path}.git"],
        ["git", "remote", "set-url", "origin", f"https://{repository_host}/{repository_path}.git"],
        ["git", "fetch", "origin"],
        ["git", "checkout", "main"],
        ["git", "push", "-u", "origin", "main"],
        ["git", "checkout", "develop"],
        ["git", "push", "-u", "origin", "develop"],
    ]
    check_dependencies(path=path, dependencies=["git"])

    for command in commands:
        subprocess.run(command, cwd=path, stderr=subprocess.STDOUT)


def get_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for setup-remote."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="setup-remote",
        usage="python ./scripts/setup-remote.py . --host github.com --path robust-python/robust-python-demo",
        description="Set up the provided cookiecutter-robust-python project's remote repo connection.",
    )
    parser.add_argument(
        "path",
        type=existing_dir,
        metavar="PATH",
        help="Path to the repo's root directory (must already exist).",
    )
    parser.add_argument("--host", dest="repository_host", help="Repository host (e.g., github.com, gitlab.com).")
    parser.add_argument(
        "--path", dest="repository_path", help="Repository path (e.g., user/repo, group/subgroup/repo)."
    )
    return parser


if __name__ == "__main__":
    main()
