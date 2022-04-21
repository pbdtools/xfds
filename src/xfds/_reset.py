"""Reset Command."""
from __future__ import annotations

from pathlib import Path

import typer

from . import config, log
from .core import locate_fds_file

app = typer.Typer(
    name="reset",
    help="Reset a folder by clearing everything except the input files.",
)
ALWAYS_KEEP = [".fds", ".psm", ".zip", ".pbs"]


@app.callback(invoke_without_command=True)
def reset(
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
    chid: str = typer.Option(
        None, "--chid", help=("If specified, only files matching CHID will be deleted.")
    ),
) -> None:
    """Stop an FDS simulation."""
    log.section("Reset Command", icon="♻️ ")

    for file in fds_file.parent.iterdir():
        if file.suffix in ALWAYS_KEEP:
            log.success(f"Keeping {file.name}")
            continue
        if chid is None or file.name.startswith(chid):
            log.warning(f"Deleting {file.name}")
            if not config.DRY:
                file.unlink()
