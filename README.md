
<h1 align="center">
  <a href="https://github.com/robust-python/cookiecutter-robust-python">
    <img alt="cookiecutter-robust-python banner" src="docs/_static/cookiecutter-robust-python-banner.png"/>
    <br>
  </a>
</h1>

<!-- badges-begin -->
[![User Guide][user-guide-badge]][user-guide-page]
[![uv][uv-badge]][uv-page]
[![Python Versions][python-versions-badge]][python-versions-page]
[![Python demo status][robust-python-demo-status-badge]][robust-python-demo-status-page]
[![Maturin demo status][robust-maturin-demo-status-badge]][robust-maturin-demo-status-page]
[![Discord][discord-badge]][discord-page]

[user-guide-badge]: https://img.shields.io/badge/user-guide-brightgreen?logo=readthedocs&style=flat-square
[user-guide-page]: https://cookiecutter-robust-python.readthedocs.io/
[uv-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square
[uv-page]: https://github.com/astral-sh/uv
[python-versions-badge]: https://img.shields.io/pypi/pyversions/robust-python-demo?style=flat-square
[python-versions-page]: https://github.com/robust-python/cookiecutter-robust-python
[robust-python-demo-status-badge]: https://img.shields.io/github/actions/workflow/status/robust-python/robust-python-demo/release-python.yml?branch=main&style=flat-square&label=robust-python-demo
[robust-python-demo-status-page]: https://github.com/robust-python/robust-python-demo
[robust-maturin-demo-status-badge]: https://img.shields.io/github/actions/workflow/status/robust-python/robust-maturin-demo/release-python.yml?branch=main&style=flat-square&label=robust-maturin-demo
[robust-maturin-demo-status-page]: https://github.com/robust-python/robust-maturin-demo
[discord-badge]: https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white&style=flat-square
[discord-page]: https://discord.gg/XZAHSBgqXU
<!-- badges-end -->

# cookiecutter-robust-python

**A template optimizing for best practices without sacrificing adaptability.**

---


<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
  - [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Project Setup](#project-setup)
- [Roadmap](#roadmap)
- [Why does this project exist?](#why-does-this-project-exist)
- [Contributing](#contributing)

</details>

## About

---

**[cookiecutter-robust-python]** is a template made with the understanding that **project needs change over time**.

The **[Robust Python Cookiecutter]** aims to provide **best practice tooling/CICD** within a structure designed for **future adaptability**.

---

### Key Features
- Uses [cruft] to allow for easily transitioning:
  - Using [maturin] vs not
  - repository/CICD provider ([github], [gitlab], [bitbucket])
  - Supported Python Versions
- Out of the box support/testing for major OS's (windows, linux, macos) and all currently supported [python] versions
- Automated template demos for integration testing generated CICD
- Rich documentation explaining [tooling decisions] and rationale
- and just about any other typical CI workflow you can think of (linting, release process, security, etc.)

### Tooling Summary
- [cruft] for project generation/update
- [uv] for dependency management
- [nox] for CI execution
- [commitizen] for version/changelog management
- [ruff] for linting/formatting
- [basedpyright] for type checking
- [pip-audit] for security vulnerability checking
- [maturin] (optional) for rust integration when needed

## Getting Started

### Prerequisites
The only requirement is installing [uv].

Besides that, it may be useful to install the following to avoid `uvx` installing dependencies at unexpected times:
```terminaloutput
uv tool install nox
uv tool install cruft
uv tool install ruff
uv tool install basedpyright
uv tool install maturin
```

### Usage
Navigate to where you want to create your project and run:

```bash
uvx cruft create https://github.com/robust-python/cookiecutter-robust-python.git
```

This will prompt you for a few inputs to customize your project:
```
[1/15] project_name (robust-python): my-awesome-project
[2/15] package_name (my_awesome_project):
[3/15] friendly_name (My Awesome Project):
...
```

### Project Setup

After generating your project, set it up for development:

```bash
cd my-awesome-project

# Sets up venv + git (same as nox -s setup-venv && nox -s setup-git)
uvx nox -t env

# Sets up remote repository (requires empty remote repo to exist)
uvx nox -s setup-remote
```

**Quick setup:** Run `uvx nox -t env` to execute all environment setup tasks at once.

## Roadmap

This is a really brief/condensed idea of what is planned for this template, and where it stands currently:
<details>
<summary>Click to expand</summary>

- [x] Swap to UV, Ruff, and Basedpyright (maybe ty later, but at the moment of writing this wasn't ready yet)
- [x] Add cruft and commitizen
- [x] Centralize CI/CD through noxfile using uv cache to maintain speed
- [x] Add CI/CD for GitHub, Gitlab, and Bitbucket (Only GitHub guaranteed to work, but others should be close enough)
- [x] Add automated integration testing with separate repos to act as demos
- [x] Add release process for demo
- [x] Ensure end to end process for base python template works fully
- [ ] Ensure maturin template works locally
- [ ] Add modified CI/CD for the maturin version
- [ ] Add CI/CD for the cookiecutter itself
- [x] Add github actions to automate demo publishing on merge to main or develop in cookiecutter
- [x] Better define out templates for issues, pull requests, etc.
- [ ] Improve generated changelogs
- [ ] Clean up documentation and make it readable
- [ ] Possibly swap documentation to follow MADR (Maybe during clean up process, but low priority for the time being)
- [x] Move to an organization (Will be done whenever there are other users besides myself)
- [ ] Add any missing automation for administrative tasks
- [ ] Designate backup plans for the projects lifecycle over time
</details>


## Why does this project exist?

Unfortunately, the [Hypermodern Python Cookiecutter] is no longer maintained nor modern.
While it will always have a place in my heart, there have been far too many improvements in Python tooling to keep using it as is.

For a while I maintained [a personal fork](https://github.com/56kyle/cookiecutter-hypermodern-python) that I would update, however, when it came time to switch
to new tooling such as [ruff], [uv], [maturin], etc., I found the process of updating the existing tooling to be extremely painful.

The [Hypermodern Python Cookiecutter] remains as a fantastic sendoff point for devs interested in building a 2021-style Python Package. However, there were
a handful of issues with it that prevented it from being able to adapt to new Python developments over the years.

The goal is for [cookiecutter-robust-python] to fill the gap that exists for a best practices template that is structured to be adaptable from the start.


## Contributing

For more information on contributing to the [Robust Python Cookiecutter], please visit the [contributing] docs.


[basedpyright]: https://github.com/DetachHead/basedpyright
[bitbucket]: https://bitbucket.org
[bitbucket-pipelines]: https://support.atlassian.com/bitbucket-cloud/docs/write-a-pipe-for-bitbucket-pipelines/
[commitizen]: https://commitizen-tools.github.io/commitizen/
[contributing]: CONTRIBUTING.md
[cookiecutter]: https://cookiecutter.readthedocs.io/en/stable/
[cookiecutter-hypermodern-python]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[cookiecutter-robust-python]: https://github.com/robust-python/cookiecutter-robust-python
[cruft]: https://cruft.github.io/cruft/
[github]: https://github.com
[github-actions]: https://docs.github.com/en/actions
[gitlab]: https://gitlab.com
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[just]: https://github.com/casey/just?tab=readme-ov-fil
[maturin]: https://github.com/PyO3/maturin
[monorepos]: https://en.wikipedia.org/wiki/Monorepo
[my personal fork]: https://github.com/56kyle/cookiecutter-hypermodern-python
[nox]: https://nox.thea.codes/
[noxfile]: https://github.com/robust-python/cookiecutter-robust-python/blob/main/%7B%7Bcookiecutter.project_name%7D%7D/noxfile.py
[pip-audit]: https://github.com/pypa/pip-audit
[poetry]: https://python-poetry.org/docs/
[polars]: https://github.com/pola-rs/polars
[python]: https://www.python.org/
[robust python cookiecutter]: https://github.com/robust-python/cookiecutter-robust-python
[ruff]: https://docs.astral.sh/ruff/
[rust]: https://www.rust-lang.org/learn
[rye]: https://rye.astral.sh/
[tooling decisions]: https://cookiecutter-robust-python.readthedocs.io/en/latest/our-chosen-toolchain.html
[install uv]: https://docs.astral.sh/uv/getting-started/installation/
[uv]: https://docs.astral.sh/uv/
