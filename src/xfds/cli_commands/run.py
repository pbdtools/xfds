"""Show Command.

Provides information about services.
"""
from pathlib import Path
from textwrap import dedent
from typing import List

import typer

from .. import core, pbs
from ..enums import Location
from ..services import DockerHub
from ..settings import EPILOG

app = typer.Typer(name="run", help="Run an FDS simulation locally.", epilog=EPILOG)
dh_openbcl_fds = DockerHub("openbcl", "fds")


@app.callback(invoke_without_command=True)
def run(
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help=(
            "Launch Docker container in interactive mode (`docker run -it`). "
            "By default, the Docker image will run the FDS model, "
            "but interactive mode will put you into the container where you can start the FDS model manually. "
            "This is good for when you are rapidly iterating and don't want to wait for the Docker image load time. "
        ),
    ),
    processors: int = typer.Option(
        1,
        "--processors",
        "-n",
        min=1,
        help=(
            "Specify number of processors. "
            "If the number of processors is greater than 1, it will invoke MPI for you (`mpiexec -n #`). "
            "Ignored if interactive mode is enabled. "
        ),
    ),
    version: str = typer.Option(
        None,
        "--fds",
        "-v",
        help=(
            "Specify FDS version to use. "
            "The FDS version can also be extracted from the file path or metadata in the FDS file. "
            "Run `xfds versions` to see a list of available versions. "
        ),
    ),
    fds_file: Path = typer.Argument(
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
    ),
    dry_run: bool = typer.Option(
        False, help="View the command that would be run and exit."
    ),
    location: Location = typer.Option(
        Location.LOCAL.value,
        "--location",
        "-l",
        case_sensitive=False,
        help=("Where to run the FDS file."),
    ),
    email: List[str] = typer.Option(
        [],
        "--email",
        "-m",
        help=("Specify an email address for PBS job scheduler. "),
    ),
    max_time: float = typer.Option(
        0,
        "--wall-time",
        "-t",
        min=0,
        help=(
            "Specify maximum time in hours. "
            "If the job runs longer than the time specified, the scheduler will kill the job. "
            "A time of 0 means no time limit. "
        ),
    ),
) -> None:
    """Run an FDS simulation."""
    _volume = core.volume_to_mount(fds_file=fds_file)
    _interactive = core.interactive_mode(fds_file=fds_file, interactive=interactive)
    _version = core.fds_version(fds_file=fds_file, version=version)
    _container = core.container_name(
        fds_file=fds_file, version=_version, interactive=_interactive
    )

    if _version and _version not in dh_openbcl_fds.tag_list() + ["latest"]:
        raise typer.Exit(
            dedent(
                f"""
            Version {_version} is not available.
            Available versions: {", ".join(dh_openbcl_fds.tag_list())}
            """
            ).strip()
        )

    if location == Location.LOCAL:
        core.execute(
            fds_file=fds_file,
            volume=_volume,
            interactive=_interactive,
            version=_version,
            container=_container,
            processors=processors,
            dry_run=dry_run,
        )
    elif location == Location.SABALCORE:
        pbs.write_pbs(
            fds_file=fds_file,
            version=_version,
            processors=processors,
            emails=email,
            max_time=max_time,
        )
