"""Documentation generation utilities for the template."""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import tomli

from tools.config import REPO_ROOT


logger: logging.Logger = logging.getLogger(__name__)

JINJA_PATTERN: re.Pattern[str] = re.compile(r"{%.*%}")
JINJA_PATTERN2: re.Pattern[str] = re.compile(r"{{[^{]*}}")
LINE_FORMAT: str = "   {name:{width}} {description}"
CANONICALIZE_PATTERN: re.Pattern[str] = re.compile(r"[-_.]+")
DESCRIPTION_PATTERN: re.Pattern[str] = re.compile(r"\. .*")


def canonicalize_name(name: str) -> str:
    """Canonicalize package name according to PEP 503."""
    result: str = CANONICALIZE_PATTERN.sub("-", name).lower()
    return result


def truncate_description(description: str) -> str:
    """Truncate the description to the first sentence."""
    result: str = DESCRIPTION_PATTERN.sub(".", description)
    return result


def format_dependency(dependency: str) -> str:
    """Format the dependency name for the table."""
    result: str = "coverage__" if dependency == "coverage" else f"{dependency}_"
    return result


def generate_dependencies_table(project_path: Path | None = None) -> str:
    """Generate a reStructuredText table of dependencies from pyproject.toml.

    Args:
        project_path: Path to the project directory. If None, uses the template project.

    Returns:
        Formatted reStructuredText table as a string
    """
    if project_path is None:
        project_path = REPO_ROOT / "{{cookiecutter.project_name}}"

    logger.info(f"Generating dependencies table for {project_path}")

    # Read and parse pyproject.toml
    pyproject_path: Path = project_path / "pyproject.toml"
    text: str = pyproject_path.read_text()
    text = JINJA_PATTERN.sub("", text)
    text = JINJA_PATTERN2.sub("x", text)
    data: dict[Any, Any] = tomli.loads(text)

    # Extract dependencies
    dependencies: set[str] = {
        canonicalize_name(dependency)
        for section in ["dependencies", "dev-dependencies"]
        for dependency in data["tool"]["poetry"][section].keys()
        if dependency != "python"
    }

    # Read and parse poetry.lock
    lock_path: Path = project_path / "poetry.lock"
    lock_text: str = lock_path.read_text()
    lock_data: dict[Any, Any] = tomli.loads(lock_text)

    # Extract descriptions from lock file
    descriptions: dict[str, str] = {
        canonicalize_name(package["name"]): truncate_description(package["description"])
        for package in lock_data["package"]
        if canonicalize_name(package["name"]) in dependencies
    }

    # Build table
    table: dict[str, str] = {
        format_dependency(dependency): descriptions[dependency] for dependency in sorted(dependencies)
    }

    width: int = max(len(name) for name in table)
    width2: int = max(len(description) for description in table.values())
    separator: str = LINE_FORMAT.format(name="=" * width, width=width, description="=" * width2)

    lines: list[str] = [separator]
    for name, description in table.items():
        line: str = LINE_FORMAT.format(name=name, width=width, description=description)
        lines.append(line)
    lines.append(separator)

    result: str = "\n".join(lines)
    logger.info("Dependencies table generated successfully")
    return result
