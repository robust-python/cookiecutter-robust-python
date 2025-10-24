"""Centralized configuration for template development tools.

Handles environment variable loading from .env and .env.local files,
and provides centralized access to configuration constants.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Repository root (parent of tools directory)
REPO_ROOT: Path = Path(__file__).resolve().parent.parent

# Load environment variables from .env and .env.local (if present)
_env_file: Path = REPO_ROOT / ".env"
_env_local_file: Path = REPO_ROOT / ".env.local"

if _env_file.exists():
    load_dotenv(_env_file)
if _env_local_file.exists():
    load_dotenv(_env_local_file, override=True)

# Configuration constants loaded from environment variables
APP_AUTHOR: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_APP_AUTHOR", "robust-python")
MAIN_BRANCH: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_MAIN_BRANCH", "main")
DEVELOP_BRANCH: str = os.getenv("COOKIECUTTER_ROBUST_PYTHON_DEVELOP_BRANCH", "develop")

# Path constants
TEMPLATE_FOLDER: Path = REPO_ROOT / "{{cookiecutter.project_name}}"
