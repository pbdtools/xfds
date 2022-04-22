"""Command Line Interface."""
from __future__ import annotations

import typer

from . import __version__, config, log
from ._render import app as _render
from ._reset import app as _reset
from ._run import app as _run
from ._stop import app as _stop

EPILOG = "Developed by pbd.tools"
app = typer.Typer(help="Manage FDS simulations.", epilog=EPILOG)

commands = [_run, _render, _stop, _reset]
for command in commands:
    app.add_typer(command, epilog=EPILOG)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", help="Display xFDS Version"),
    verbose: bool = typer.Option(False, "--verbose", "-V", help="Verbose output"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Dry Run, show what would happen."
    ),
    icons: bool = typer.Option(True, help="Show icons in output.", hidden=True),
) -> None:
    if version:
        typer.echo(__version__)
        typer.Exit(code=0)

    config.VERBOSE = verbose
    config.DRY = dry_run
    config.MESSAGE_ICONS = icons

    log.info(f"Verbose Mode: {verbose}", icon="📢")
    log.debug(f"Message Icons: {icons}")
    log.info(f"Dry Run: {dry_run}", icon="🏜️ ")
