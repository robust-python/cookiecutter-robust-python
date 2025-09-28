"""Module containing utility functions used by tests."""
from pathlib import Path

from tests.constants import COOKIECUTTER_FOLDER


def templates_matching(pattern: str) -> list[Path]:
    """Return a list of relative file paths matching the given pattern."""
    return [path.relative_to(COOKIECUTTER_FOLDER) for path in COOKIECUTTER_FOLDER.glob(pattern)]
