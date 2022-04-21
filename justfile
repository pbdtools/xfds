#!/usr/bin/env just --justfile

# Setup
install:
    @poetry install

# Development
test *args:
    @poetry run pytest {{args}}

check:
    @poetry run pre-commit run --all-files

tests:
    @nox -rs tests

black:
    @nox -rs black

lint:
    @nox -rs lint

safety:
    @nox -rs safety

mypy:
    @nox -rs mypy

coverage:
    @nox -rs coverage

# Manual Test
run-fds *args:
    @poetry run xfds {{args}} tests/data/fds/test.fds

# Publish
push:
    @git push --set-upstream origin `git rev-parse --abbrev-ref HEAD`

build:
    rm -Rf dist
    @poetry build

pipx:
    just build
    pipx install --force `find ./dist -name "*.whl" | sort | tail -n 1`

# URLs
repo:
    #!/usr/bin/env python3
    import toml
    import webbrowser
    pyproject_toml = toml.load("pyproject.toml")
    url = pyproject_toml['tool']['poetry']['repository']
    webbrowser.open(url)

home:
    #!/usr/bin/env python3
    import toml
    import webbrowser
    pyproject_toml = toml.load("pyproject.toml")
    url = pyproject_toml['tool']['poetry']['homepage']
    webbrowser.open(url)

docs:
    #!/usr/bin/env python3
    import toml
    import webbrowser
    pyproject_toml = toml.load("pyproject.toml")
    url = pyproject_toml['tool']['poetry']['documentation']
    webbrowser.open(url)
