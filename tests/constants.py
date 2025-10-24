"""Module containing constants used throughout all tests."""

import json
from pathlib import Path
from typing import Any


REPO_FOLDER: Path = Path(__file__).parent.parent
COOKIECUTTER_FOLDER: Path = REPO_FOLDER / "{{cookiecutter.project_name}}"
HOOKS_FOLDER: Path = REPO_FOLDER / "hooks"
GITHUB_ACTIONS_FOLDER: Path = COOKIECUTTER_FOLDER / ".github"

COOKIECUTTER_JSON_PATH: Path = REPO_FOLDER / "cookiecutter.json"
COOKIECUTTER_JSON: dict[str, Any] = json.loads(COOKIECUTTER_JSON_PATH.read_text())

MIN_PYTHON_SLUG: int = int(COOKIECUTTER_JSON["min_python_version"].lstrip("3."))
MAX_PYTHON_SLUG: int = int(COOKIECUTTER_JSON["max_python_version"].lstrip("3."))
PYTHON_VERSIONS: list[str] = [f"3.{VERSION_SLUG}" for VERSION_SLUG in range(MIN_PYTHON_SLUG, MAX_PYTHON_SLUG + 1)]
DEFAULT_PYTHON_VERSION: str = PYTHON_VERSIONS[1]

TYPE_CHECK_NOX_SESSIONS: list[str] = [f"typecheck-{python_version}" for python_version in PYTHON_VERSIONS]
TESTS_NOX_SESSIONS: list[str] = [f"tests-python-{python_version}" for python_version in PYTHON_VERSIONS]

IDEMPOTENT_NOX_SESSIONS: list[str] = [
    "pre-commit",
    "lint-python",
    "format-python",
    *TYPE_CHECK_NOX_SESSIONS,
    *TESTS_NOX_SESSIONS,
    "build-docs",
    "build-python",
    "build-container",
    "tox",
    "coverage",
]
CONTEXT_DEPENDENT_NOX_SESSIONS: list[str] = [
    "coverage",
    "publish-python",
    "release",
]

ALL_NOX_SESSIONS: list[str] = IDEMPOTENT_NOX_SESSIONS + CONTEXT_DEPENDENT_NOX_SESSIONS
