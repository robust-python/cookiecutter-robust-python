"""Shared utility functions for template development tools."""

import os
import shutil
import stat
import subprocess
import sys
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Generator
from typing import Literal
from typing import Optional
from typing import overload

import cruft
from cookiecutter.utils import work_in
from loguru import logger

from tools.config import DEVELOP_BRANCH
from tools.config import MAIN_BRANCH
from tools.config import REPO_ROOT


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
        if error.stdout:
            logger.error(error.stdout)
        if error.stderr:
            logger.error(error.stderr)
        raise


git: partial[subprocess.CompletedProcess] = partial(run_command, "git")
uv: partial[subprocess.CompletedProcess] = partial(run_command, "uv")


def require_clean_and_up_to_date_repo() -> None:
    """Checks if the repo is clean and up to date with any important branches."""
    git("fetch")
    git("status", "--porcelain")
    if not is_branch_synced_with_remote(DEVELOP_BRANCH):
        raise ValueError(f"{DEVELOP_BRANCH} is not synced with origin/{DEVELOP_BRANCH}")
    if not is_branch_synced_with_remote(MAIN_BRANCH):
        raise ValueError(f"{MAIN_BRANCH} is not synced with origin/{MAIN_BRANCH}")
    if not is_ancestor(MAIN_BRANCH, DEVELOP_BRANCH):
        raise ValueError(f"{MAIN_BRANCH} is not an ancestor of {DEVELOP_BRANCH}")


def is_branch_synced_with_remote(branch: str) -> bool:
    """Checks if the branch is synced with its remote."""
    return is_ancestor(branch, f"origin/{branch}") and is_ancestor(f"origin/{branch}", branch)


def is_ancestor(ancestor: str, descendent: str) -> bool:
    """Checks if ancestor is an ancestor of descendent."""
    return git("merge-base", "--is-ancestor", ancestor, descendent).returncode == 0


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
        template_git_url=str(REPO_ROOT),
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
            logger.warning(f"No pyproject.toml found at {previous_demo_pyproject}")
            response: str = input("This folder may not be a demo. Continue? [y/N]: ").strip().lower()
            if response != "y":
                raise RuntimeError("Aborted removal of non-demo directory")

        logger.info(f"Removing existing demo project at {demo_path}")
        shutil.rmtree(demo_path, onerror=remove_readonly)


def get_demo_name(add_rust_extension: bool) -> str:
    """Get the demo project name based on rust extension setting."""
    name_modifier: str = "maturin" if add_rust_extension else "python"
    return f"robust-{name_modifier}-demo"
