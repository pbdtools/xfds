"""Render Command."""
from __future__ import annotations

import importlib.util
import os
import sys
from inspect import getmembers, isfunction
from itertools import product
from pathlib import Path
from types import ModuleType
from typing import Any

import typer
from jinja2 import Environment

from . import config, errors, filters, log
from .core import locate_config, read_config
from .units import ureg

app = typer.Typer(
    name="render",
    help="Render an FDS template file into scenarios.",
)

ENV = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True,
)


def load_filters(module: ModuleType) -> None:
    for filter in [o for o in getmembers(module) if isfunction(o[1])]:
        ENV.filters[filter[0]] = filter[1]


def load_filters_from_path(file_path: Path) -> bool:
    if not file_path.exists():
        return False

    module_name = "user_filters"
    spec: Any = importlib.util.spec_from_file_location(module_name, file_path)
    module: Any = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    load_filters(module)
    return True


load_filters(filters)


def _values_match_for_shared_keys(d1: dict, d2: dict) -> bool:
    keys = set(d1.keys()).intersection(d2.keys())
    for key in keys:
        if d1[key] != d2[key]:
            return False
    return True


def _parse_model(model_spec: dict) -> list[dict]:

    if "name" not in model_spec:
        raise errors.ModelNameNotDefiend(
            "You must specify the pattern for naming the output files."
        )

    variables = model_spec.get("variables", dict())
    params = model_spec.get("parameters", dict())
    includes = params.get("include", [])
    excludes = params.get("exclude", [])
    params = {k: v for k, v in params.items() if k not in ["include", "exclude"]}

    models = []
    if not params:
        models.append({"data": variables})
    else:
        keys, values = zip(*params.items())
        for parameters in product(*values):
            models.append({"data": dict(zip(keys, parameters))})

        for model in models:
            for include in includes:
                if _values_match_for_shared_keys(model["data"], include):
                    model["data"].update(include)

        models = [
            model
            for model in models
            if not any(
                _values_match_for_shared_keys(model["data"], exclude)
                for exclude in excludes
            )
        ]

    for model in models:
        data = variables.copy()
        data.update(model["data"])
        model["data"] = data

        model.update(
            {
                key: value
                for key, value in model_spec.items()
                if key not in ["variables", "parameters"]
            }
        )

        model["name"] = compile(model["name"], model["data"])
        model["data"]["name"] = model["name"]

    return models


def parse_models(config_data: dict) -> list[dict]:
    """Create scenarios as defined in the config file."""
    if "xfds" not in config_data.keys():
        raise errors.xFDSNotDefined(
            "'xfds' is not defined as a top-level key in config file."
        )
    if "render" not in config_data["xfds"].keys():
        raise errors.RenderNotDefined(
            "'render' is not defined under 'xfds' in config file."
        )

    models = []
    for model in config_data["xfds"]["render"]:
        models.extend(_parse_model(model))
    return models


def compile(file_contents: str, data: dict) -> str:
    """Compile the FDS template file."""
    template = ENV.from_string(file_contents)
    return template.render(**data)


def write(output_file: Path, contents: str) -> None:
    if config.DRY:
        return
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(contents)


@app.callback(invoke_without_command=True)
def render(
    directory: Path = typer.Argument(
        ".", help="Directory containing pbd.yml configuration file."
    )
) -> None:
    """Render an FDS template into scenarios."""
    log.section("Render Command", icon="🖨️ ")

    config_file = locate_config(Path(directory))
    log.debug(f"Config File: {config_file}", icon="🛠️")
    os.chdir(config_file.parent)

    user_filters = directory / "filters.py"
    if load_filters_from_path(user_filters):
        log.debug(f"Loaded Custom Filters: {user_filters}", icon="🛠️")

    user_units = directory / "units.txt"
    if user_units.exists():
        ureg.load_definitions(user_units.resolve())

    config_data = read_config(config_file)
    models = parse_models(config_data)

    for model in models:
        for file in model["files"]:
            input_file = directory / file
            if not input_file.exists():
                raise FileNotFoundError(
                    f"Could not find {input_file.name} in {input_file.parent}"
                )
            output_dir = directory / "output" / model["name"]
            output_file = output_dir / f"{model['name']}{input_file.suffix}"
            output_text = compile(input_file.read_text(), model["data"])
            write(output_file=output_file, contents=output_text)
