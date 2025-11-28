"""Module containing util."""

import argparse
import stat
import subprocess
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional


REPO_FOLDER: Path = Path(__file__).resolve().parent.parent
MAIN_BRANCH: str = "main"
DEVELOP_BRANCH: str = "develop"


class MissingDependencyError(Exception):
    """Exception raised when a depedency is missing from the system running setup-repo."""

    def __init__(self, project: Path, dependency: str):
        """Initializes MisssingDependencyError."""
        message_lines: list[str] = [
            f"Unable to find {dependency=}.",
            f"Please ensure that {dependency} is installed before setting up the repo at {project.absolute()}",
        ]
        message: str = "\n".join(message_lines)
        super().__init__(message)


def check_dependencies(path: Path, dependencies: list[str]) -> None:
    """Checks for any passed dependencies."""
    for dependency in dependencies:
        try:
            subprocess.check_call([dependency, "--version"], cwd=path)
        except subprocess.CalledProcessError as e:
            raise MissingDependencyError(path, dependency) from e


def require_clean_and_up_to_date_repo() -> None:
    """Checks if the repo is clean and up to date with any important branches."""
    commands: list[list[str]] = [
        ["git", "fetch"],
        ["git", "merge-base", "--is-ancestor", MAIN_BRANCH, f"origin/{MAIN_BRANCH}"],
        ["git", "merge-base", "--is-ancestor", f"origin/{MAIN_BRANCH}", MAIN_BRANCH],
        ["git", "merge-base", "--is-ancestor", DEVELOP_BRANCH, f"origin/{DEVELOP_BRANCH}"],
        ["git", "merge-base", "--is-ancestor", f"origin/{DEVELOP_BRANCH}", DEVELOP_BRANCH],
        ["git", "merge-base", "--is-ancestor", MAIN_BRANCH, DEVELOP_BRANCH],
        ["git", "status", "--porcelain"],
    ]

    for command in commands:
        subprocess.run(command, cwd=REPO_FOLDER, check=True)


def existing_dir(value: str) -> Path:
    """Responsible for validating argparse inputs and returning them as pathlib Path's if they meet criteria."""
    path = Path(value).expanduser().resolve()

    if not path.exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist.")
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path} is not a directory.")

    return path


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function.

    This is passed to shutil.rmtree as the onerror kwarg.
    """
    Path(path).chmod(stat.S_IWRITE)
    func(path)


def get_package_version() -> str:
    """Gets the package version."""
    result: subprocess.CompletedProcess = subprocess.run(
        ["uvx", "--from", "commitizen", "cz", "version", "-p"], cwd=REPO_FOLDER, capture_output=True
    )
    return result.stdout.decode("utf-8").strip()


def get_bumped_package_version(increment: Optional[str] = None) -> str:
    """Gets the bumped package version."""
    args: list[str] = ["uvx", "--from", "commitizen", "cz", "bump", "--get-next", "--yes", "--dry-run"]
    if increment is not None:
        args.extend(["--increment", increment])
    result: subprocess.CompletedProcess = subprocess.run(args, cwd=REPO_FOLDER, capture_output=True)
    return result.stdout.decode("utf-8").strip()


def create_release_branch(new_version: str) -> None:
    """Creates a release branch."""
    commands: list[list[str]] = [
        ["git", "status", "--porcelain"],
        ["git", "checkout", "-b", f"release/{new_version}", "develop"],
    ]
    for command in commands:
        subprocess.run(command, cwd=REPO_FOLDER, capture_output=True, check=True)


def bump_version(increment: Optional[str] = None) -> None:
    """Bumps the package version."""
    bump_cmd: list[str] = ["uvx", "--from", "commitizen", "cz", "bump", "--yes", "--files-only", "--changelog"]
    if increment is not None:
        bump_cmd.extend(["--increment", increment])
    subprocess.run(bump_cmd, cwd=REPO_FOLDER, check=True)


def get_latest_tag() -> Optional[str]:
    """Gets the latest git tag."""
    sort_tags: list[str] = ["git", "tag", "--sort=-creatordate"]
    find_last: list[str] = ["grep", "-v", '"${GITHUB_REF_NAME}"']
    echo_none: list[str] = ["echo", "''"]
    result: subprocess.CompletedProcess = subprocess.run(
        [*sort_tags, "|", *find_last, "|", "tail", "-n1", "||", *echo_none], cwd=REPO_FOLDER, capture_output=True
    )
    tag: str = result.stdout.decode("utf-8").strip()
    if tag == "":
        return None
    return tag


def get_latest_release_notes() -> str:
    """Gets the release notes.

    Assumes the latest_tag hasn't been applied yet.
    """
    latest_tag: Optional[str] = get_latest_tag()
    latest_version: str = get_package_version()
    if latest_tag == latest_version:
        raise ValueError(
            "The latest tag and version are the same. Please ensure the release notes are taken before tagging."
        )
    rev_range: str = "" if latest_tag is None else f"{latest_tag}..{latest_version}"
    command: list[str] = [
        "uvx",
        "--from",
        "commitizen",
        "cz",
        "changelog",
        rev_range,
        "--dry-run",
        "--unreleased-version",
        latest_version,
    ]
    result: subprocess.CompletedProcess = subprocess.run(command, cwd=REPO_FOLDER, capture_output=True, check=True)
    return result.stdout.decode("utf-8")


def tag_release() -> None:
    """Tags the release using commitizen bump with tag only."""
    subprocess.run(["uvx", "--from", "commitizen", "cz", "bump", "--tag-only", "--yes"], cwd=REPO_FOLDER, check=True)
