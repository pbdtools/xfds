"""Command Line Interface."""
from __future__ import annotations

from pathlib import Path
from typing import List

import typer

from . import __version__, core, docker_hub, pbs, settings

EPILOG = "Developed by pbd.tools"

app = typer.Typer(help="Manage FDS simulations.", epilog=EPILOG)


# CLI Arguments
FDS_FILE_ARG: Path = typer.Argument(
    ".",
    callback=core.locate_fds_file,
    help=(
        "The FDS file or directory to run. "
        "If a **FDS file** is specified, the FDS model will run. "
        "If a **directory** is specified, xFDS will find the first FDS file in the directory "
        "and assume that is what it should run. "
        "If no fds file exists, xFDS will default to interactive mode. "
        "if **nothing** is specified, the current directory is used and the above rules are applied. "
    ),
)

# CLI Options
INTERACTIVE_OPT: bool = typer.Option(
    settings.INTERACTIVE,
    "--interactive",
    "-i",
    help=(
        "Launch Docker container in interactive mode (`docker run -it`). "
        "By default, the Docker image will run the FDS model, "
        "but interactive mode will put you into the container where you can start the FDS model manually. "
        "This is good for when you are rapidly iterating and don't want to wait for the Docker image load time. "
    ),
)
PROCESSORS_OPT: int = typer.Option(
    settings.PROCESSORS,
    "--processors",
    "-n",
    min=1,
    help=(
        "Specify number of processors. "
        "If the number of processors is greater than 1, it will invoke MPI for you (`mpiexec -n #`). "
        "Ignored if interactive mode is enabled. "
    ),
)
VERSION_OPT: str = typer.Option(
    None,
    "--fds",
    "-v",
    help=(
        "Specify FDS version to use. "
        "The FDS version can also be extracted from the file path or metadata in the FDS file. "
        "Run `xfds versions` to see a list of available versions. "
    ),
)
DRY_RUN_OPT: bool = typer.Option(
    False, help="View the command that would be run and exit."
)
EMAIL_OPT: List[str] = typer.Option(
    [],
    "--email",
    "-m",
    help=("Specify an email address for PBS job scheduler. "),
)
MAX_TIME_OPT: float = typer.Option(
    0,
    "--wall-time",
    "-t",
    min=0,
    help=(
        "Specify maximum time in hours. "
        "If the job runs longer than the time specified, the scheduler will kill the job. "
        "A time of 0 means no time limit. "
    ),
)


@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Display xFDS Version"),
) -> None:
    if version:
        typer.echo(__version__)
        typer.Exit(code=0)


@app.command(help="Run an FDS simulation locally")
def run(
    interactive: bool = INTERACTIVE_OPT,
    processors: int = PROCESSORS_OPT,
    version: str = VERSION_OPT,
    fds_file: Path = FDS_FILE_ARG,
    dry_run: bool = DRY_RUN_OPT,
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


@app.command(help="List available FDS versions")
def versions() -> None:
    print("\n".join(docker_hub.tags()))


@app.command(name="pbs", help="Generate .pbs File")
def create_pbs(
    fds_file: Path = FDS_FILE_ARG,
    version: str = VERSION_OPT,
    email: List[str] = EMAIL_OPT,
    processors: int = PROCESSORS_OPT,
    max_time: float = MAX_TIME_OPT,
) -> None:
    _version = core.fds_version(fds_file=fds_file, version=version)
    pbs.write_pbs(
        fds_file=fds_file,
        version=_version,
        processors=processors,
        emails=email,
        max_time=max_time,
    )


for command in app.registered_commands:
    command.epilog = EPILOG
