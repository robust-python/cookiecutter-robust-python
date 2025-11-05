import os
import sys
from pathlib import Path
from typing import Annotated

import cruft
import typer
from cookiecutter.utils import work_in

from util import is_ancestor
from util import get_current_branch
from util import get_current_commit
from util import get_demo_name
from util import get_last_cruft_update_commit
from util import git
from util import FolderOption
from util import REPO_FOLDER
from util import require_clean_and_up_to_date_repo


cli: typer.Typer = typer.Typer()


@cli.callback(invoke_without_command=True)
def update_demo(
    demos_cache_folder: Annotated[Path, FolderOption("--demos-cache-folder", "-c")],
    add_rust_extension: Annotated[bool, typer.Option("--add-rust-extension", "-r")] = False
) -> None:
    """Runs precommit in a generated project and matches the template to the results."""
    try:
        demo_name: str = get_demo_name(add_rust_extension=add_rust_extension)
        demo_path: Path = demos_cache_folder / demo_name
        develop_branch: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH", "develop")

        current_branch: str = get_current_branch()
        current_commit: str = get_current_commit()

        _validate_is_feature_branch(branch=current_branch)

        typer.secho(f"Updating demo project at {demo_path=}.", fg="yellow")
        with work_in(demo_path):
            require_clean_and_up_to_date_repo()
            git("checkout", develop_branch)

            last_update_commit: str = get_last_cruft_update_commit(demo_path=demo_path)
            if not is_ancestor(last_update_commit, current_commit):
                raise ValueError(
                    f"The last update commit '{last_update_commit}' is not an ancestor of the current commit "
                    f"'{current_commit}'."
                )

            git("checkout", "-b", current_branch)
            cruft.update(
                project_dir=demo_path,
                template_path=REPO_FOLDER,
                extra_context={"project_name": demo_name, "add_rust_extension": add_rust_extension},
            )
            git("add", ".")
            git("commit", "-m", "chore: update demo to the latest cookiecutter-robust-python", "--no-verify")
            git("push")

    except Exception as error:
        typer.secho(f"error: {error}", fg="red")
        sys.exit(1)


def _validate_is_feature_branch(branch: str) -> None:
    """Validates that the cookiecutter has a feature branch checked out."""
    if not branch.startswith("feature/"):
        raise ValueError(f"Received branch '{branch}' is not a feature branch.")


if __name__ == '__main__':
    cli()
