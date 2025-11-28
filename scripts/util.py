# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "cookiecutter",
#   "cruft",
#   "python-dotenv",
#   "typer",
# ]
# ///
"""Module containing utility functions used throughout cookiecutter_robust_python scripts."""

import json
import os
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Generator
from typing import Literal
from typing import Optional
from typing import TypedDict
from typing import overload

import cruft
import typer

from cookiecutter.utils import work_in
from cruft._commands.utils.cruft import get_cruft_file
from dotenv import load_dotenv
from typer.models import OptionInfo


REPO_FOLDER: Path = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    """Load environment variables from .env and .env.local (if present).

    .env.local takes precedence over .env for any overlapping variables.
    """
    env_file: Path = REPO_FOLDER / ".env"
    env_local_file: Path = REPO_FOLDER / ".env.local"

    if env_file.exists():
        load_dotenv(env_file)

    if env_local_file.exists():
        load_dotenv(env_local_file, override=True)


# Load environment variables at module import time
_load_env()

FolderOption: partial[OptionInfo] = partial(
    typer.Option, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path
)


@dataclass
class RepoMetadata:
    """Metadata for a given repo."""
    app_name: str
    app_author: str
    remote: str
    main_branch: str
    develop_branch: str


TEMPLATE: RepoMetadata = RepoMetadata(
    app_name=os.getenv("COOKIECUTTER_ROBUST_PYTHON__APP_NAME"),
    app_author=os.getenv("COOKIECUTTER_ROBUST_PYTHON__APP_AUTHOR"),
    remote=os.getenv("COOKIECUTTER_ROBUST_PYTHON__REMOTE"),
    main_branch=os.getenv("COOKIECUTTER_ROBUST_PYTHON__MAIN_BRANCH"),
    develop_branch=os.getenv("COOKIECUTTER_ROBUST_PYTHON__DEVELOP_BRANCH")
)

DEMO: RepoMetadata = RepoMetadata(
    app_name=os.getenv("ROBUST_DEMO__APP_NAME"),
    app_author=os.getenv("ROBUST_DEMO__APP_AUTHOR"),
    remote=os.getenv("ROBUST_DEMO__REMOTE"),
    main_branch=os.getenv("ROBUST_DEMO__MAIN_BRANCH"),
    develop_branch=os.getenv("ROBUST_DEMO__DEVELOP_BRANCH")
)


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function.

    Meant for use as the onerror callback in shutil.rmtree.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


@overload
def run_command(command: str, *args: str, ignore_error: Literal[True]) -> Optional[subprocess.CompletedProcess]:
    ...


@overload
def run_command(command: str, *args: str, ignore_error: Literal[False] = ...) -> subprocess.CompletedProcess:
    ...


def run_command(command: str, *args: str, ignore_error: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Runs the provided command in a subprocess."""
    try:
        process = subprocess.run([command, *args], check=True, capture_output=True, text=True)
        return process
    except subprocess.CalledProcessError as error:
        if ignore_error:
            return None
        print(error.stdout, end="")
        print(error.stderr, end="", file=sys.stderr)
        raise error


git: partial[subprocess.CompletedProcess] = partial(run_command, "git")
uv: partial[subprocess.CompletedProcess] = partial(run_command, "uv")
nox: partial[subprocess.CompletedProcess] = partial(run_command, "nox")
gh: partial[subprocess.CompletedProcess] = partial(run_command, "gh")


def require_clean_and_up_to_date_repo(demo_path: Path) -> None:
    """Checks if the repo is clean and up to date with any important branches."""
    with work_in(demo_path):
        git("fetch")
        git("status", "--porcelain")
        validate_is_synced_ancestor(ancestor=DEMO.main_branch, descendent=DEMO.develop_branch)
    typer.secho


def validate_is_synced_ancestor(ancestor: str, descendent: str) -> None:
    """Returns whether the given ancestor is actually an up-to-date ancestor of the given descendent branch."""
    if not is_branch_synced_with_remote(branch=descendent):
        raise ValueError(f"{descendent} is not synced with origin/{descendent}")
    if not is_branch_synced_with_remote(branch=ancestor):
        raise ValueError(f"{ancestor} is not synced with origin/{ancestor}")
    if not is_ancestor(ancestor=ancestor, descendent=descendent):
        raise ValueError(f"{ancestor} is not an ancestor of {descendent}")


def is_branch_synced_with_remote(branch: str) -> bool:
    """Checks if the branch is synced with its remote."""
    return is_ancestor(branch, f"origin/{branch}") and is_ancestor(f"origin/{branch}", branch)


def is_ancestor(ancestor: str, descendent: str) -> bool:
    """Checks if the branch is synced with its remote."""
    try:
        git("merge-base", "--is-ancestor", ancestor, descendent)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_branch() -> str:
    """Returns the current branch name."""
    return git("branch", "--show-current").stdout.strip()


def get_current_commit() -> str:
    """Returns the current commit reference."""
    return git("rev-parse", "HEAD").stdout.strip()


def get_last_cruft_update_commit(demo_path: Path) -> str:
    """Returns the commit id for the last time cruft update was ran."""
    existing_cruft_config: dict[str, Any] = _read_cruft_file(demo_path)
    last_cookiecutter_commit: Optional[str] = existing_cruft_config.get("commit", None)
    if last_cookiecutter_commit is None:
        raise ValueError("Could not find last commit id used to generate demo.")
    return last_cookiecutter_commit


def _read_cruft_file(project_path: Path) -> dict[str, Any]:
    """Reads the cruft file for the project path provided and returns the results."""
    cruft_path: Path = get_cruft_file(project_dir_path=project_path)
    cruft_text: str = cruft_path.read_text()
    cruft_config: dict[str, Any] = json.loads(cruft_text)
    return cruft_config


@contextmanager
def in_new_demo(
    demos_cache_folder: Path,
    add_rust_extension: bool,
    no_cache: bool,
    **kwargs: Any
) -> Generator[Path, None, None]:
    """Returns a context manager for working within a new demo."""
    demo_path: Path = generate_demo(
        demos_cache_folder=demos_cache_folder,
        add_rust_extension=add_rust_extension,
        no_cache=no_cache,
        **kwargs
    )
    with work_in(demo_path):
        yield demo_path


def generate_demo(
    demos_cache_folder: Path,
    add_rust_extension: bool,
    no_cache: bool,
    **kwargs: Any
) -> Path:
    """Generates a demo project and returns its root path."""
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demos_cache_folder.mkdir(exist_ok=True)
    if no_cache:
        _remove_existing_demo(demo_path=demos_cache_folder / demo_name)
    cruft.create(
        template_git_url=str(REPO_FOLDER),
        output_dir=demos_cache_folder,
        extra_context={"project_name": demo_name, "add_rust_extension": add_rust_extension, **kwargs},
        no_input=True,
        overwrite_if_exists=True
    )
    return demos_cache_folder / demo_name


def _remove_existing_demo(demo_path: Path) -> None:
    """Removes the existing demo if present."""
    if demo_path.exists() and demo_path.is_dir():
        previous_demo_pyproject: Path = Path(demo_path, "pyproject.toml")
        if not previous_demo_pyproject.exists():
            typer.secho(f"No pyproject.toml found at {previous_demo_pyproject=}.", fg="red")
            typer.confirm(
                "This folder may not be a demo, are you sure you would like to continue?",
                default=False,
                abort=True,
                show_default=True
            )

        typer.secho(f"Removing existing demo project at {demo_path=}.", fg="yellow")
        shutil.rmtree(demo_path, onerror=remove_readonly)


def get_demo_name(add_rust_extension: bool) -> str:
    name_modifier: str = "maturin" if add_rust_extension else "python"
    return f"robust-{name_modifier}-demo"
