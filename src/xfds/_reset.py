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

    files_to_keep = list(
        chain.from_iterable(
            [
                directory.glob(pattern)
                for pattern in config_data["xfds"]["reset"]["keep"]
            ]
        )
    )
    files_to_delete = [
        file
        for file in directory.iterdir()
        if not file.is_dir() and file not in files_to_keep
    ]

    for file in files_to_delete:
        log.warning(f"Deleting {file.name}")
        if not config.DRY:
            file.unlink()

    for file in files_to_keep:
        log.success(f"Keeping {file.name}")
