#!/usr/bin/env just --justfile

# Setup
install:
    @poetry install

# Development
test:
    @poetry run pytest

check:
    @poetry run pre-commit run --all-files

black:
    @poetry run black .

sort:
    @poetry run isort

mypy:
    @poetry run mypy .

# Publish
build:
    @poetry build
