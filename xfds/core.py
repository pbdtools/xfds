"""Core program for running fds in docker containers."""
from __future__ import annotations

import subprocess  # noqa: S404
from pathlib import Path

import typer

from . import settings


def get_version(version: str) -> str:
    """Ensure version is supported."""
    if version not in settings.VERSIONS:
        raise typer.BadParameter(f"Version {version} is not supported")

    return version


def build_arguments(
    interactive: bool = settings.INTERACTIVE,
    linux: bool = settings.LINUX,
    windows: bool = settings.WINDOWS,
    processors: int = settings.PROCESSORS,
    version: str = settings.LATEST,
    fds_file: Path = Path(),
) -> list[str]:
    """Build the command line arguments for the CLI."""
    volume: str = str(Path.cwd()) if interactive else str(fds_file.parent.resolve())
    if fds_file.is_dir():
        try:
            fds_file = next(fds_file.glob("*.fds"))
            volume = str(fds_file.parent.resolve())
        except StopIteration:
            interactive = True
            volume = str(fds_file.resolve())

    mount: str = "C:\\workdir" if windows else "/workdir"
    _version = get_version(version)

    # Docker run command
    args = ["docker", "run", "--rm"]

    # Set interactive
    if interactive:
        args.append("-it")

    # Set container name
    name = f"fds-{_version}" if interactive else fds_file.stem
    args.extend(["--name", name])

    # Set volume to mount
    args.extend(["-v", f"{volume}:{mount}"])

    # Select container image
    args.append(f"openbcl/fds:{_version}")

    # If interactive, do not specify mpi or fds command
    if interactive:
        return args

    # Use mpi if multiple processors are specified
    if processors > 1:
        args.extend(["mpiexec", "-n", str(processors)])

    # Add fds command to run file
    args.extend(["fds", str(fds_file.name)])
    args.extend([">", str(fds_file.with_suffix(".err")), "&"])

    return args


def app(
    interactive: bool = typer.Option(
        settings.INTERACTIVE, "--interactive", "-i", help="Run in interactive mode"
    ),
    linux: bool = typer.Option(
        settings.LINUX, "--linux", "-l", help="Run in Linux container"
    ),
    windows: bool = typer.Option(
        settings.WINDOWS, "--windows", "-w", help="Run in Windows container"
    ),
    processors: int = typer.Option(
        settings.PROCESSORS, "--processors", "-n", help="Number of processors to use"
    ),
    version: str = typer.Option(
        settings.LATEST, "--version", "-v", help="FDS version to use "
    ),
    fds_file: Path = typer.Argument(None),
) -> None:
    """Entry point for app."""
    args = build_arguments(interactive, linux, windows, processors, version, fds_file)
    print(" ".join(args))
    _ = subprocess.Popen(args)  # noqa: S603


def main() -> None:
    """Entry point for setup.py."""
    typer.run(app)


if __name__ == "__main__":
    main()
