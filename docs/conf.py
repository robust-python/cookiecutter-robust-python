# conf.py - Sphinx configuration for the cookiecutter-robust-python TEMPLATE documentation.
# This file belongs to the TEMPLATE SOURCE CODE, NOT the generated project.
# See https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import date


project = "cookiecutter-robust-python Template Documentation"
copyright = f"{date.today().year}, Kyle Oliver"  # noqa

author = "Kyle Oliver"

release = "2025.04.28"
version = "2025.04"

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "myst_parser",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
]
templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    ".nox",
    "rust",
    "tests",
    "cookiecutter.json",
    "README.md",
    "noxfile.py",
    ".pre-commit-config.yaml",
    "pyproject.toml",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]

extlinks = {
    "argocd": ("https://argo-cd.readthedocs.io/%s", None),
    "autopep8": ("https://pypi.org/project/autopep8/%s", None),
    "bandit-bandit": ("https://bandit.readthedocs.io/%s", None),
    "bandit": ("https://github.com/PyCQA/bandit/%s", None),
    "basedpyright": ("https://docs.basedpyright.com/latest/%s", None),
    "beartype": ("https://beartype.readthedocs.io/%s", None),
    "bitbucket-pipelines": ("https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/%s", None),
    "black": ("https://black.readthedocs.io/%s", None),
    "build": ("https://pypa-build.readthedocs.io/%s", None),
    "cobertura": ("https://cobertura.github.io/cobertura/xml.html%s", None),
    "commitizen": ("https://commitizen-tools.github.io/commitizen/%s", None),
    "conventional-commits": ("https://www.conventionalcommits.org/en/v1.0.0/%s", None),
    "coverage-py": ("https://coverage.readthedocs.io/%s", None),
    "cruft": ("https://cruft.github.io/cruft/%s", None),
    "docker-compose": ("https://docs.docker.com/compose/%s", None),
    "docker": ("https://docs.docker.com/%s", None),
    "docker-install": ("https://docs.docker.com/engine/install/%s", None),
    "flake8": ("https://flake8.pycqa.org/%s", None),
    "flit": ("https://flit.pypa.io/%s", None),
    "github-actions": ("https://docs.github.com/en/actions/%s", None),
    "gitlab-ci": ("https://docs.gitlab.com/ee/ci/%s", None),
    "hatch": ("https://hatch.pypa.io/%s", None),
    "hatchling": ("https://hatch.pypa.io/latest/hatchling/%s", None),
    "helm": ("https://helm.sh/%s", None),
    "invoke": ("https://www.pyinvoke.org/%s", None),
    "isort": ("https://pycqa.github.io/isort/%s", None),
    "junit": ("https://llg.cubic.org/docs/junit/%s", None),
    "just": ("https://just.systems/%s", None),
    "maturin": ("https://maturin.rs/%s", None),
    "mkdocs": ("https://www.mkdocs.org/%s", None),
    "mypy": ("https://mypy-lang.org/%s", None),
    "myst-parser": ("https://myst-parser.readthedocs.io/%s", None),
    "nox": ("https://nox.thea.codes/%s", None),
    "pdm": ("https://pdm.fming.dev/%s", None),
    "pip-audit": ("https://github.com/pypa/pip-audit/%s", None),
    "pip": ("https://pip.pypa.io/%s", None),
    "pip-tools": ("https://pip-tools.readthedocs.io/%s", None),
    "podman": ("https://podman.io/%s", None),
    "podman-install": ("https://podman.io/docs/installation/%s", None),
    "poethepoet": ("https://github.com/nat-n/poethepoet/%s", None),
    "poetry": ("https://python-poetry.org/%s", None),
    "pre-commit": ("https://pre-commit.com/%s", None),
    "pydocstyle": ("https://www.pydocstyle.org/%s", None),
    "pylint": ("https://pylint.pycqa.org/%s", None),
    "pypi-trusted-publishers": ("https://docs.pypi.org/trusted-publishers/%s", None),
    "pyright": ("https://github.com/microsoft/pyright/%s", None),
    "pytest": ("https://docs.pytest.org/%s", None),
    "pytest-pytest-cov": ("https://pytest-cov.readthedocs.io/%s", None),
    "pytype": ("https://github.com/google/pytype/%s", None),
    "ruff": ("https://docs.astral.sh/ruff/%s", None),
    "safety": ("https://pyup.io/%s", None),
    "setuptools": ("https://setuptools.pypa.io/%s", None),
    "sonarcloud": ("https://sonarcloud.io/%s", None),
    "sphinx": ("https://www.sphinx-doc.org/%s", None),
    "sphinxautodoctypehints": ("https://sphinx-autodoc-typehints.readthedocs.io/%s", None),
    "tox": ("https://tox.readthedocs.io/%s", None),
    "twine": ("https://twine.readthedocs.io/%s", None),
    "unittest": ("https://docs.python.org/3/library/unittest.html%s", None),
    "uv": ("https://docs.uv.dev/%s", None),
    "uv-install": ("https://docs.astral.sh/uv/installation/%s", None),
    "venv": ("https://docs.python.org/3/library/venv%s", None),
    "virtualenv": ("https://virtualenv.pypa.io/%s", None),
    "yapf": ("https://github.com/google/yapf/%s", None)
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "sidebar_hide_name": True,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/robust-python/cookiecutter-robust-python",
            "html": "<svg stroke='currentColor' fill='currentColor' stroke-width='0' viewBox='0 0 16 16'><path fill-rule='evenodd' d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.22.82.69 1.19 1.81.85 2.23.65.07-.51.28-.85.54-1.04-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38C13.71 14.53 16 11.53 16 8c0-4.42-3.58-8-8-8z'></path></svg>",
            "aria-label": "GitHub",
        },
    ],
    "source_repository": "https://github.com/robust-python/cookiecutter-robust-python/",
    "source_branch": "main",
    "source_directory": "docs/",
}

napoleon_google_docstrings = True
napoleon_numpy_docstrings = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_keyword = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_attr_annotations = True

set_type_checking_flag = True
always_document_param_types = False
typehints_fully_qualified = False
typehints_document_rtype = True
typehints_format = "google"
