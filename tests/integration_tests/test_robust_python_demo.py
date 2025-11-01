"""Tests project generation and template functionality using a Python build backend."""

import subprocess
from pathlib import Path

import pytest

from tests.constants import IDEMPOTENT_NOX_SESSIONS


@pytest.mark.parametrize("session", IDEMPOTENT_NOX_SESSIONS)
def test_demo_project_nox_session(robust_demo: Path, session: str) -> None:
    command: list[str] = ["nox", "-s", session]
    try:
        subprocess.run(
            command,
            cwd=robust_demo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"nox session '{session}' failed with exit code {e.returncode}\n"
            f"{'-'*20} STDOUT {'-'*20}\n{e.stdout}\n"
            f"{'-'*20} STDERR {'-'*20}\n{e.stderr}"
        )


def test_demo_project_nox_pre_commit(robust_demo: Path) -> None:
    command: list[str] = ["nox", "-s", "pre-commit"]
    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_demo,
        capture_output=True,
        text=True,
        timeout=20.0
    )
    assert result.returncode == 0


@pytest.mark.parametrize(
    argnames="robust_demo__add_rust_extension",
    argvalues=[True, False],
    indirect=True,
    ids=["maturin", "python"]
)
@pytest.mark.parametrize(argnames="robust_demo__is_setup", argvalues=[False], indirect=True, ids=["no-setup"])
def test_demo_project_nox_pre_commit_with_install(robust_demo: Path) -> None:
    command: list[str] = ["nox", "-s", "pre-commit", "--", "install"]
    pre_commit_hook_path: Path = robust_demo / ".git" / "hooks" / "pre-commit"
    assert not pre_commit_hook_path.exists()

    result: subprocess.CompletedProcess = subprocess.run(
        command,
        cwd=robust_demo,
        capture_output=True,
        text=True,
        timeout=20.0
    )
    assert pre_commit_hook_path.exists()
    assert pre_commit_hook_path.is_file()

    assert result.returncode == 0
