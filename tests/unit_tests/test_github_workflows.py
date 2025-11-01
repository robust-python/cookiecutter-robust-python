from typing import Any

import pytest

from tests.util import templates_matching


@pytest.mark.parametrize(
    argnames="robust_demo__is_setup",
    argvalues=[False],
    indirect=True,
    ids=["no-setup"]
)
class TestWorkflow:
    @pytest.mark.parametrize(
        argnames="robust_demo__add_rust_extension",
        argvalues=[False],
        indirect=True,
        ids=["base"]
    )
    @pytest.mark.parametrize(
        argnames="robust_file__path__relative",
        argvalues=templates_matching(".github/workflows/*[!rust].yml"),
        indirect=True,
        ids=lambda path: path.stem
    )
    def test_workflow_basic_loading_with_python(self, robust_yaml: dict[str, Any]) -> None:
        assert robust_yaml

    @pytest.mark.parametrize(
        argnames="robust_demo__add_rust_extension",
        argvalues=[True],
        indirect=True,
        ids=["maturin"]
    )
    @pytest.mark.parametrize(
        argnames="robust_file__path__relative",
        argvalues=templates_matching(".github/workflows/*.yml"),
        indirect=True,
        ids=lambda path: path.stem
    )
    def test_workflow_basic_loading_with_maturin(self, robust_yaml: dict[str, Any]) -> None:
        assert robust_yaml
