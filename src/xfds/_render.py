"""Render Command."""
from __future__ import annotations

import json
import pprint
from itertools import product
from pathlib import Path
from typing import Optional, Union

import markdown
import toml
import typer
import yaml
from jinja2 import Environment

from . import config, log
from .core import locate_fds_file

app = typer.Typer(
    name="render",
    help="Render an FDS template file into scenarios.",
)


def _normalize(value: str) -> Union[str, float, int]:
    """Normalize a value.

    Will return as int or float if possible, otherwise will return as string.
    """
    for cast in [int, float, str]:
        try:
            return cast(value)
        except ValueError:
            pass

    return value


def get_meta(file_contents: str) -> dict:
    """Process metadata from the FDS template file.

    Values will be normalized to numbers if possible.
    If a singular value is present, the value will be
    returned rather than a list.
    """
    md = markdown.Markdown(extensions=["meta"])
    md.convert(file_contents)
    meta = md.Meta

    for key, value in meta.items():
        if len(value) == 1:
            meta[key] = _normalize(value[0])
        else:
            meta[key] = [_normalize(v) for v in value]

    return meta


def locate_config(fds_file: Path, meta: dict) -> Optional[Path]:
    """Load the configuration file.

    Will look for a confing file in the same directory as the FDS template file.
    The config file should have the same base name as the original FDS file.
    If no config file is found, search the FDS meta for a variable "config".
    """
    for suffix in [".yaml", ".yml", ".toml", ".json"]:
        config_file = fds_file.with_suffix(suffix)
        if config_file.exists():
            return config_file

    if "config" in meta:
        config_file = Path(meta["config"])
        if config_file.is_absolute():
            return config_file
        return fds_file.parent / config_file

    return None


def read_config(config_file: Path) -> dict:
    """Read the configuration file."""
    func = {
        ".yml": yaml.safe_load,
        ".yaml": yaml.safe_load,
        ".toml": toml.load,
        ".json": json.load,
    }[config_file.suffix]

    with config_file.open() as f:
        return func(f)


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


def generate_models(
    fds_file: Path,
    template_text: str,
    model_name: str,
    model_data: dict,
    defaults: dict,
    meta: dict,
) -> None:
    """Generate a model."""
    log.debug(f"Model: {model_name}")
    log.debug(f"Model data: {model_data}")

    output_dir = fds_file.parent / "output"

    if "matrix" not in model_data:
        log.warning(f"No matrix specified for model {model_name}")
        data = meta.copy()
        data.update(defaults)
        log.debug(f"=== Data ===\n{pprint.pformat(data)}")
        contents = compile(template_text, data)
        output_file = output_dir / model_name / f"{model_name}.fds"
        write(output_file, contents)
        return

    keys, values = zip(*model_data["matrix"].items())
    for matrix_values in product(*values):
        data = meta.copy()
        data.update(defaults)
        data.update(zip(keys, matrix_values))
        log.debug(f"=== Data ===\n{pprint.pformat(data)}")

        contents = compile(template_text, data)
        file_name = compile(model_name, data)
        output_file = output_dir / file_name / f"{file_name}.fds"
        write(output_file, contents)
        log.success(f"Created: {output_file}")


def main(fds_file: Path) -> None:

    template_text = fds_file.read_text()
    meta = get_meta(template_text)
    log.debug(pprint.pformat(meta))

    config_file = locate_config(fds_file, meta)
    if config_file is None or not config_file.exists():
        log.warning("No config file found.")
    else:
        log.info(f"Config file: {config_file}", icon="📄")
    config_data = read_config(config_file) if config_file is not None else {}

    defaults = config_data.get("defaults", {}).copy()
    log.debug(f"Defaults: {defaults}")

    models = config_data.get("models", {fds_file.name: {}}).copy()

    for model_name, model_data in models.items():
        generate_models(
            fds_file=fds_file,
            template_text=template_text,
            model_name=model_name,
            model_data=model_data,
            defaults=defaults,
            meta=meta,
        )


@app.callback(invoke_without_command=True)
def render(
    fds_file: Path = typer.Argument(
        ".",
        callback=locate_fds_file,
        help=(
            "The FDS file or directory to reset. "
            "If a **FDS file** is specified, the FDS outputs will be cleared. "
            "If a **directory** is specified, xFDS will find the first FDS file in the directory "
            "and assume that is what it should reset. "
            "if **nothing** is specified, the current directory is used and the above rules are applied. "
        ),
    ),
) -> None:
    """Render an FDS template into scenarios."""
    log.section("Render Command", icon="🖨️ ")
    main(fds_file)
