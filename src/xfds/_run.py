"""Run Command."""
from __future__ import annotations

import re
import subprocess  # noqa: S404
from pathlib import Path
from typing import Optional

import markdown
import typer

from . import config, log
from .core import container_name, locate_fds_file, volume_to_mount


def interactive_mode(fds_file: Path, interactive: bool) -> bool:
    """Interactive mode if specifically requested or if the FDS input file is a directory."""
    is_interactive = interactive or fds_file.is_dir()
    log.info(f"Interactive mode: {is_interactive}", icon="👉")
    return is_interactive


def fds_version(fds_file: Path, version: Optional[str] = None) -> str:
    """Return the FDS version of the specified file.

    Version is selected in the following order:
    - Command line arguments
    - Metadata
    - File path
    - Latest version
    """
    if version is not None:
        log.info(f"Using version specified: {version}", icon="⚙️ ")
        return version

    md = markdown.Markdown(extensions=["meta"])
    try:
        md.convert(fds_file.read_text())
        if "fds" in md.Meta.keys():
            version = md.Meta["fds"][0]
            log.info(f"Using version from metadata: {version}", icon="⚙️ ")
            return version
    except (FileNotFoundError, IsADirectoryError):
        pass

    pattern = r"((v|fds)?[._]?)(\d[._]\d[._]\d)"
    for part in fds_file.parts:
        match = re.match(pattern, part)
        if match:
            version = match.group(3).replace("-", ".").replace("_", ".")
            log.info(f"Using version from file path: {version}", icon="⚙️ ")
            return version

    log.info("Using latest version", icon="⚙️ ")
    return "latest"


def image_name(version: str = "") -> str:
    """Get image name.

    Specify FDS version if specified, otherwise use latest version.
    """
    image = "openbcl/fds"
    if version:
        image = f"openbcl/fds:{version}"
    log.debug(f"Image name: {image}", icon="🖼️ ")
    return image


def build_arguments(
    fds_file: Path,
    volume: Path,
    container: str,
    interactive: bool,
    version: str,
    processors: int,
) -> list[str]:
    """Build the command line arguments for the CLI."""
    # Docker run command
    args = ["docker", "run", "--rm"]

    # Set interactive
    if interactive:
        args.append("-it")

    # Set container name
    args.extend(["--name", container])

    # Set volume to mount
    args.extend(["-v", f"{volume}:/workdir"])

    # Select container image
    args.append(image_name(version))

    # If interactive, do not specify mpi or fds command
    if interactive:
        return args

    args.extend(["bash", "-c"])

    # Use mpi if multiple processors are specified
    cmd = f"fds {fds_file.name} 1> {fds_file.with_suffix('.log').name} 2> {fds_file.with_suffix('.err').name}"
    if processors > 1:
        cmd = f"mpiexec -n {processors} " + cmd

    args.append(cmd)

    return args


def execute(
    fds_file: Path,
    volume: Path,
    container: str,
    interactive: bool,
    version: str,
    processors: int,
    dry_run: bool = False,
) -> None:
    """Entry point for setup.py."""

    cmd = build_arguments(
        fds_file=fds_file,
        volume=volume,
        interactive=interactive,
        version=version,
        container=container,
        processors=processors,
    )

    log.success(" ".join(cmd), icon="🚀")

    if dry_run:
        log.warning("Dry run, not executing command", icon="🚫")
        return

    if interactive:
        subprocess.run(cmd)  # pragma: no cover # noqa: S603
    else:
        subprocess.Popen(cmd)  # noqa: S603


app = typer.Typer(name="run", help="Run an FDS in a Docker container.")


@app.callback(invoke_without_command=True)
def run(
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help=(
            "Launch Docke-r container in interactive mode (`docker run -it`). "
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
        ),
    ),
    fds_file: Path = typer.Argument(
        ".",
        callback=locate_fds_file,
        help=(
            "The FDS file or directory to run. "
            "If a **FDS file** is specified, the FDS model will run. "
            "If a **directory** is specified, xFDS will find the first FDS file in the directory "
            "and assume that is what it should run. "
            "If no fds file exists, xFDS will default to interactive mode. "
            "if **nothing** is specified, the current directory is used and the above rules are applied. "
        ),
    ),
) -> None:
    """Run an FDS simulation."""
    log.section("Run Command", icon="👟")

    _volume = volume_to_mount(fds_file=fds_file)
    _interactive = interactive_mode(fds_file=fds_file, interactive=interactive)
    _version = fds_version(fds_file=fds_file, version=version)
    _container = container_name(
        fds_file=fds_file, version=_version, interactive=_interactive
    )

    execute(
        fds_file=fds_file,
        volume=_volume,
        interactive=_interactive,
        version=_version,
        container=_container,
        processors=processors,
        dry_run=config.DRY,
    )
