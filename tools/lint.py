"""Linting utilities for demo projects."""

import logging
from pathlib import Path

import pre_commit.main
from retrocookie.core import retrocookie

from tools.config import DEVELOP_BRANCH
from tools.util import git
from tools.util import in_new_demo
from tools.util import require_clean_and_up_to_date_repo


logger = logging.getLogger(__name__)

# Files that should not be modified by retrocookie (still linted but excluded from template changes)
IGNORED_FILES: list[str] = [
    "pyproject.toml",
    "uv.lock",
]


def lint_from_demo(
    demos_cache_folder: Path,
    add_rust_extension: bool = False,
    no_cache: bool = False,
) -> None:
    """Run pre-commit in a generated demo and apply changes back to the template.

    This function:
    1. Creates or uses an existing demo project
    2. Checks out the develop branch
    3. Creates a temp branch for linting
    4. Runs pre-commit to lint and format all files
    5. Uses retrocookie to apply changes back to the template

    Args:
        demos_cache_folder: Directory containing the demo
        add_rust_extension: Whether the demo uses Rust extension support
        no_cache: If True, regenerate the demo even if it exists

    Raises:
        RuntimeError: If git operations fail or repository is not clean
    """
    logger.info("Starting lint-from-demo process")

    with in_new_demo(
        demos_cache_folder=demos_cache_folder,
        add_rust_extension=add_rust_extension,
        no_cache=no_cache,
    ) as demo_path:
        require_clean_and_up_to_date_repo()
        logger.info(f"Repository is clean and up-to-date")

        git("checkout", DEVELOP_BRANCH)
        logger.info(f"Checked out {DEVELOP_BRANCH} branch")

        git("branch", "-D", "temp/lint-from-demo", ignore_error=True)
        git("checkout", "-b", "temp/lint-from-demo", DEVELOP_BRANCH)
        logger.info("Created temp/lint-from-demo branch")

        logger.info("Running pre-commit on all files")
        pre_commit.main.main(["run", "--all-files", "--show-diff-on-failure"])

        # Restore ignored files to their original state
        for path in IGNORED_FILES:
            git("checkout", "HEAD", "--", path)
        logger.info(f"Restored {len(IGNORED_FILES)} ignored files to original state")

        git("add", ".")
        git("commit", "-m", "meta: lint-from-demo", "--no-verify")
        logger.info("Committed linting changes")

    logger.info("Running retrocookie to apply changes back to template")
    retrocookie(
        instance_path=demo_path,
        commits=[f"{DEVELOP_BRANCH}..temp/lint-from-demo"],
    )
    logger.info("Lint-from-demo process completed")
