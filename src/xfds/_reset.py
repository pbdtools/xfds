"""Reset Command."""
from __future__ import annotations

from itertools import chain
from pathlib import Path

import typer

from . import config, log
from .core import locate_config, read_config

app = typer.Typer(
    name="reset",
    help="Reset a folder by clearing everything except specified files.",
)


def locate_files_to_keep(directory: Path, config_data: dict) -> list[Path]:
    files_to_keep = chain.from_iterable(
        [directory.glob(pattern) for pattern in config_data["xfds"]["reset"]["keep"]]
    )
    return list(files_to_keep)


@app.callback(invoke_without_command=True)
def reset(
    directory: Path = typer.Argument(
        ".",
        help="Directory containing model files.",
    ),
) -> None:
    """Stop an FDS simulation."""
    log.section("Reset Command", icon="♻️ ")

    config_file = locate_config(directory.parent)
    config_data = read_config(config_file)

    files_to_keep = locate_files_to_keep(directory, config_data)

    for file in directory.iterdir():
        if file.is_dir():
            continue
        if file in files_to_keep:
            log.success(f"Keeping {file.name}")
        else:
            log.warning(f"Deleting {file.name}")
            if not config.DRY:
                file.unlink()
