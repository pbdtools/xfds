"""Render Command."""
from __future__ import annotations

from itertools import product
from pathlib import Path

import typer
import yaml
from jinja2 import Environment

from . import config, errors, log

app = typer.Typer(
    name="render",
    help="Render an FDS template file into scenarios.",
)


def locate_config(cwd: Path) -> Path:
    """Load the configuration file.

    Will look for a confing file in the same directory as the FDS template file.
    The config file should have the same base name as the original FDS file.
    If no config file is found, search the FDS meta for a variable "config".
    """
    for file in ["pbd.yaml", "pbd.yml"]:
        config_file = cwd / file
        if config_file.exists():
            return config_file

    raise errors.ConfigNotFound(f"Could not find Config file pbd.yml in {cwd}.")


def read_config(config_file: Path) -> dict:
    """Read the configuration file."""
    with config_file.open() as f:
        return yaml.safe_load(f)


def _values_match_for_shared_keys(d1: dict, d2: dict) -> bool:
    keys = set(d1.keys()).intersection(d2.keys())
    for key in keys:
        if d1[key] != d2[key]:
            return False
    return True


def _parse_model(model_spec: dict) -> list[dict]:

    if "file" not in model_spec:
        raise errors.InputFileNotDefined(
            "You must specify the input file for each model definition."
        )
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
    env = Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )
    template = env.from_string(file_contents)
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

    config_data = read_config(config_file)
    models = parse_models(config_data)

    for model in models:
        input_file = directory / model["file"]
        output_file = directory / "output" / model["name"] / f"{model['name']}.fds"
        output_text = compile(input_file.read_text(), model["data"])
        write(output_file=output_file, contents=output_text)
