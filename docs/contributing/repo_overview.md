## .github

This directory contains Github specific information.

### workflows

The workflows folder contains all the [Github Actions](https://github.com/features/actions) scripts.

- `docs.yml`: Publish the contents of `/docs` to [https://xfds.pbd.tools](https://xfds.pbd.tools)
- `release.yml`: When a new release is initiated, this will run the tests one more time and then publish the new version to [PyPI](https://pypi.org/project/xfds/)
- `test.yml`: Runs continuious integration tests.
    - Ensures all tests are passing
    - Determines how much of the code is covered by the tests
    - Checks that all the code is formatted using [black](https://github.com/psf/black)
    - Lints the codebase for best practices and catching errors with [flake8](https://flake8.pycqa.org/en/latest/)
    - Checks for security vulnerabilities with [Safety](https://github.com/pyupio/safety)
    - Checks that all functions are correctly annotated with [mypy](http://mypy-lang.org/)

## .vscode

The .vscode folder contains configuration for using the [VS Code](https://code.visualstudio.com/) editor. You do not need to use VS Code, but this project is set up assuming you are.

- `extensions.json`: Recommended extensions from the [VS Code Marketplace](https://marketplace.visualstudio.com/vscode)
- `settings.json`: Configuration options.

## docs

Code for the documentation hosted at https://xfds.pbd.tools.

Documentation is built on [mkdocs](https://www.mkdocs.org/) and uses the [Material Theme](https://squidfunk.github.io/mkdocs-material/). You can include snippets from other files thanks to [mdx_include](https://github.com/neurobin/mdx_include).

## examples

The examples directory show ways that xFDS can be used. Most of the examples are used in the documentation. Thanks to [mdx-include](https://pypi.org/project/mdx-include/), the code below includes `/examples/variables/variables.fds`. The documentation is configured to look in the `examples` directory when looking for files to include.

```markdown title="mdx_include syntax"
\{! variables/variables.fds !}
```

```python title="included file"
{! variables/variables.fds !}
```

## src/xfds

This directory contains all the source code for the project.

### Common Files

Thse files are files necesary to setup xFDS and pull the pieces together.

- `__init__.py`: Generally empty except for the software version number.
- `cli.py`: This file is the main entry point for the command line interface.
- `config.py`: Default settings for commands.
- `core.py`: Basic functions required by multiple commands.
- `log.py`: Functions for printing information out to the terminal.

### Command Specific Files

Files that start with an underscore (`_`) contain the logic for all the xFDS subcommands.

- `_render.py`
- `_reset.py`
- `_run.py`
- `_stop.py`

## Tests

xFDS uses [pytest](https://docs.pytest.org/) to ensure things are working as expected.

- `data`: Example data for tests
- `integration`: Tests for ensuring xFDS works together as a whole.
- `unit`: Tests for individual pieces of code.
- `conftest.py`: [Fixtures](https://docs.pytest.org/en/7.1.x/how-to/fixtures.html) used across the test suite.

## Project Configuration Files

- [`.flake8`](https://flake8.pycqa.org/en/latest/): configuration for linting
- [`.gitignore` ](https://git-scm.com/docs/gitignore): Tell [Git](https://git-scm.com) which files to ignore.
- [`.pre-commit-config.yaml`](https://pre-commit.com/): Checks to perform before committing code.
- [`justfile`](https://github.com/casey/just): Common tasks for developing xFDS.
- [`LICENSE`](https://opensource.org/licenses/MIT): Defines permissions for xFDS.
- [`mkdocs.yml`](https://www.mkdocs.org/): Configuration for documentation.
- [`mypy.ini`](http://mypy-lang.org/): Configuration for static type checking.
- [`noxfile.py`](https://nox.thea.codes/en/stable/): Rules for testing xFDS on multiple versions of Python. These are checked with every push to the repo.
- [`poetry.lock`](https://python-poetry.org/): Pre-computed information for what packages xFDS needs.
- [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/): xFDS Pacakge configuration and metadata.
- `README.md`: High level info for the project.
