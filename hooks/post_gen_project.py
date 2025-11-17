#!/usr/bin/env python
"""Cookiecutter hook that runs after template generation."""
import json
import shutil
import stat
from pathlib import Path
from typing import Any
from typing import Callable


REMOVE_PATHS: list[str] = [
    "{% if not cookiecutter.add_rust_extension %}rust{% endif %}",
    "{% if not cookiecutter.add_rust_extension %}.github/workflows/lint-rust.yml{% endif %}",
    "{% if not cookiecutter.add_rust_extension %}.github/workflows/build-rust.yml{% endif %}",
    "{% if not cookiecutter.add_rust_extension %}.github/workflows/test-rust.yml{% endif %}",
    "{% if cookiecutter.repository_provider != 'github' %}.github{% endif %}",
    "{% if cookiecutter.repository_provider != 'gitlab' %}.gitlab-ci.yml{% endif %}",
    "{% if cookiecutter.repository_provider != 'bitbucket' %}bitbucket-pipelines.yml{% endif %}",
]


def post_gen_project() -> None:
    """Run post-generation tasks."""
    reindent_cookiecutter_json()
    remove_undesired_files()


def reindent_cookiecutter_json():
    """Indent .cookiecutter.json using two spaces.

    The jsonify extension distributed with Cookiecutter uses an indentation
    width of four spaces. This conflicts with the default indentation width of
    Prettier for JSON files. Prettier is run as a pre-commit hook in CI.
    """
    path = Path(".cookiecutter.json")

    with path.open() as io:
        data = json.load(io)

    with path.open(mode="w") as io:
        json.dump(data, io, sort_keys=True, indent=2)
        io.write("\n")


def remove_undesired_files() -> None:
    """Removes any files that are not desired in the generated project based on the cookiecutter.json.

    This is done to avoid issues that tend to arise when the name of the template file contains a conditional.
    """
    for path in REMOVE_PATHS:
        if path == "":
            continue

        path: Path = Path.cwd() / path
        if path.is_dir():
            shutil.rmtree(path, onerror=remove_readonly)
        else:
            path.unlink(missing_ok=True)


def remove_readonly(func: Callable[[str], Any], path: str, _: Any) -> None:
    """Clears the readonly bit and attempts to call the provided function.

    This is passed to shutil.rmtree as the onerror kwarg.
    """
    Path(path).chmod(stat.S_IWRITE)
    func(path)


if __name__ == "__main__":
    post_gen_project()
