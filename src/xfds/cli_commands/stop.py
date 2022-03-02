"""Stop Command."""
from pathlib import Path

import typer

from ..core import locate_fds_file
from ..settings import EPILOG

app = typer.Typer(
    name="stop", help="Stop an FDS simulation that is running locally.", epilog=EPILOG
)


@app.callback(invoke_without_command=True)
def stop(
    fds_file: Path = typer.Argument(
        ".",
        callback=locate_fds_file,
        help=(
            "The FDS file or directory to stop. "
            "If a **FDS file** is specified, the FDS model will be stopped. "
            "If a **directory** is specified, xFDS will find the first FDS file in the directory "
            "and assume that is what it should stop. "
            "if **nothing** is specified, the current directory is used and the above rules are applied. "
        ),
    ),
) -> None:
    """Stop an FDS simulation."""
    stop_file = fds_file.resolve().with_suffix(".stop")
    stop_file.touch()
