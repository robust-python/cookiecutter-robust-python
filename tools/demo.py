"""Demo project generation and update utilities."""

import logging
from pathlib import Path

import cruft
from cookiecutter.utils import work_in

from tools.config import DEVELOP_BRANCH
from tools.config import REPO_ROOT
from tools.util import generate_demo as _generate_demo
from tools.util import get_demo_name
from tools.util import git
from tools.util import require_clean_and_up_to_date_repo


logger = logging.getLogger(__name__)


def generate_demo(
    demos_cache_folder: Path,
    add_rust_extension: bool = False,
    no_cache: bool = False,
) -> Path:
    """Generates a project demo using the cookiecutter-robust-python template.

    Args:
        demos_cache_folder: Directory where demos will be cached
        add_rust_extension: Whether to add Rust extension support
        no_cache: If True, regenerate even if demo exists

    Returns:
        Path to the generated demo project
    """
    logger.info(f"Generating demo project in {demos_cache_folder}")
    demo_path = _generate_demo(
        demos_cache_folder=demos_cache_folder,
        add_rust_extension=add_rust_extension,
        no_cache=no_cache,
    )
    logger.info(f"Demo generated at {demo_path}")
    return demo_path


def update_demo(
    demos_cache_folder: Path,
    add_rust_extension: bool = False,
) -> None:
    """Update an existing demo project to the latest template version.

    Uses cruft.update() to bring in template changes and commits the result.

    Args:
        demos_cache_folder: Directory containing the demo to update
        add_rust_extension: Whether the demo uses Rust extension support

    Raises:
        RuntimeError: If the repository is not clean or up-to-date
    """
    demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
    demo_path: Path = demos_cache_folder / demo_name

    logger.info(f"Updating demo project at {demo_path}")

    with work_in(demo_path):
        require_clean_and_up_to_date_repo()
        git("checkout", DEVELOP_BRANCH)
        logger.info(f"Checked out {DEVELOP_BRANCH} branch")

        cruft.update(
            project_dir=demo_path,
            template_path=REPO_ROOT,
            extra_context={"project_name": demo_name, "add_rust_extension": add_rust_extension},
        )
        logger.info("Cruft update completed")

        git("add", ".")
        git("commit", "-m", "chore: update demo to the latest cookiecutter-robust-python", "--no-verify")
        git("push")
        logger.info("Changes committed and pushed")

    logger.info("Demo update completed")
