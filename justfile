#!/usr/bin/env just --justfile

# Setup
install:
    @poetry install

# Development
test *args:
    @poetry run pytest {{args}}

check:
    @poetry run pre-commit run --all-files

black:
    @poetry run black .

sort:
    @poetry run isort

mypy:
    @poetry run mypy .

push:
    @git push --set-upstream origin `git rev-parse --abbrev-ref HEAD`

# Publish
pipx:
    pipx install --force `find ./dist -name "*.whl" | sort | tail -n 1`

build:
    @poetry build
