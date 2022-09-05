"""Stop Command."""
from pathlib import Path

import typer

from . import log

app = typer.Typer(
    name="stop",
    help="Stop an FDS simulation that is running locally by creating a .stop file.",
)


@app.callback(invoke_without_command=True)
def stop(
    file: Path = typer.Argument(
        ".",
        help=(
            "The FDS file or directory to stop. "
            "If a **FDS file** is specified, the FDS model will be stopped. "
            "If a **directory** is specified, xFDS will stop all FDS file in the directory. "
            "This is especially useful when &CATF is used."
            "if **nothing** is specified, the current directory is used and the above rules are applied. "
        ),
    ),
) -> None:
    """Stop an FDS simulation."""
    log.section("Stop Command", icon="🛑")

    if file.resolve().is_dir():
        fds_files = list(file.glob("*.fds"))
    else:
        fds_files = [file]

    for file in fds_files:
        stop_file = file.resolve().with_suffix(".stop")
        log.success(f"Stopping {file} with {stop_file}")
        stop_file.touch()
