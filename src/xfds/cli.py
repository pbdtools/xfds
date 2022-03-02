"""Command Line Interface."""
from __future__ import annotations

import typer

from . import __version__
from .cli_commands import commands
from .settings import EPILOG

app = typer.Typer(help="Manage FDS simulations.", epilog=EPILOG)

for command in commands:
    app.add_typer(command)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Display xFDS Version"),
) -> None:
    if version:
        typer.echo(__version__)
        typer.Exit(code=0)
