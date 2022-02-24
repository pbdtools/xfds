from __future__ import annotations

from pathlib import Path

import typer

from . import core, docker_hub, settings

EPILOG = "Developed by pbd.tools"


app = typer.Typer(
    help="Manage FDS simulations.",
    epilog=EPILOG,
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Display xFDS Version"),
) -> None:
    if version:
        typer.echo("0.2.0")
        typer.Exit(code=0)


@app.command(help="Run an FDS simulation locally", epilog=EPILOG)
def run(
    interactive: bool = typer.Option(
        settings.INTERACTIVE, "--interactive", "-i", help="Run in interactive mode"
    ),
    processors: int = typer.Option(
        settings.PROCESSORS, "--processors", "-n", help="Number of processors to use"
    ),
    version: str = typer.Option(None, "--fds", "-v", help="Specify FDS version to use"),
    fds_file: Path = typer.Argument(
        settings.CWD, help="FDS input file", callback=core.locate_fds_file
    ),
    dry_run: bool = typer.Option(
        False, help="View the command that would be run and exit"
    ),
) -> None:
    """Run an FDS simulation."""
    _volume = core.volume_to_mount(fds_file=fds_file)
    _interactive = core.interactive_mode(fds_file=fds_file, interactive=interactive)
    _version = core.fds_version(fds_file=fds_file, version=version)
    _container = core.container_name(
        fds_file=fds_file, version=_version, interactive=_interactive
    )

    core.execute(
        fds_file=fds_file,
        volume=_volume,
        interactive=_interactive,
        version=_version,
        container=_container,
        processors=processors,
        dry_run=dry_run,
    )


@app.command(help="List available FDS versions", epilog=EPILOG)
def versions() -> None:
    print("\n".join(docker_hub.tags()))
