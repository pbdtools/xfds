"""Stop Command."""
from pathlib import Path

import typer

from ..core import locate_fds_file
from ..settings import EPILOG

app = typer.Typer(
    name="reset",
    help="Reset a folder by clearing everything except the input files.",
    epilog=EPILOG,
)
KEEP = [".fds", ".psm", ".zip"]


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
    for file in fds_file.parent.iterdir():
        if file.suffix in KEEP:
            continue
        if chid is None:
            file.unlink()
        elif file.name.startswith(chid):
            file.unlink()
