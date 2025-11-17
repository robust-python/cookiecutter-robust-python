"""Cookiecutter hook that runs before template generation."""


ESCAPED_JINJA_SETUP: str = """
{%- set min_minor = cookiecutter.min_python_version.split('.')[1] | int %}
{%- set max_minor = cookiecutter.max_python_version.split('.')[1] | int %}

{{ cookiecutter.update({
    "_min_python_version_minor_int": min_minor,
    "_max_python_version_minor_int": max_minor,
    "python_versions": ["3." + (i|string) for i in range(min_minor, max_minor + 1)]
}) }}
"""
