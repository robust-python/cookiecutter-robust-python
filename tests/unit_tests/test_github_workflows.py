from functools import partial
from typing import Any

import pytest

from tests.util import templates_matching


@pytest.mark.parametrize(
    argnames="robust_demo__is_setup",
    argvalues=[False],
    indirect=True,
    ids=["no-setup"]
)
@pytest.mark.parametrize(
    argnames="robust_demo__add_rust_extension",
    argvalues=[False, True],
    indirect=True,
    ids=["base", "maturin"]
)
@pytest.mark.parametrize(
    argnames="robust_file__path__relative",
    argvalues=templates_matching(".github/workflows/*.yml"),
    indirect=True,
    ids=lambda path: path.stem
)
class TestWorkflow:
    def test_workflow_basic_loading(self, robust_yaml: dict[str, Any]) -> None:
        assert robust_yaml
