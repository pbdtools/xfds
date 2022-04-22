"""Render Command."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Union

import markdown
import typer
from jinja2 import Environment

from . import config, log
from .core import locate_fds_file

app = typer.Typer(
    name="render",
    help="Render an FDS template file into scenarios.",
)


def output_dir(base_path: Path, date: bool = False) -> Path:
    """Return the output directory."""
    if date:
        return base_path / datetime.now().strftime(config.RENDER_TIMESTAMP_FORMAT)
    return base_path / "models"


def _normalize(value: str) -> Union[str, float, int]:
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def get_meta(file_contents: str) -> dict:
    md = markdown.Markdown(extensions=["meta"])
    md.convert(file_contents)
    meta = md.Meta

    for key, value in meta.items():
        value = [_normalize(v) for v in value]
        if len(value) == 1:
            meta[key] = value[0]

    return meta


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
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(contents)


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
    date: bool = typer.Option(True, help="Use a timestamp for the output directory."),
) -> None:
    """Render an FDS template into scenarios."""
    log.section("Render Command", icon="🖨️ ")

    output = output_dir(fds_file.parent, date)
    log.debug(f"Output directory: {output}")

    contents = fds_file.read_text()
    meta = get_meta(contents)

    output_file = output / fds_file.stem / fds_file.name
    write(output_file, compile(contents, meta))
    log.success(f"Created: {output_file}")
