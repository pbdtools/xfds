"""Core program for running fds in docker containers."""
from __future__ import annotations

import argparse
import subprocess  # noqa: S404
from pathlib import Path

from . import settings


def get_version(version: str) -> str:
    """Ensure version is supported."""
    if version not in settings.VERSIONS:
        raise ValueError(f"Version {version} is not supported")

    return version


def build_arguments(
    interactive: bool = settings.INTERACTIVE,
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

    return args


def main() -> None:
    """Entry point for setup.py."""
    parser = argparse.ArgumentParser(
        prog="xfds",
        description="Run FDS in docker container",
        epilog="Developed by PBD Tools LLC.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )
    parser.add_argument(
        "-w",
        "--windows",
        action="store_true",
        help="Run in Windows container [Defaults to Linux]",
    )
    parser.add_argument(
        "-n",
        "--processors",
        default=1,
        type=int,
        help="Number of processors to use",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=settings.LATEST,
        choices=settings.VERSIONS.keys(),
        help="FDS version to use",
    )
    parser.add_argument(
        "fds_file",
        nargs="?",
        default=Path.cwd(),
        help="FDS input file",
    )

    args = parser.parse_args()
    cmd = build_arguments(
        args.interactive,
        args.windows,
        args.processors,
        args.version,
        Path(args.fds_file).resolve(),
    )
    print(" ".join(cmd))
    _ = subprocess.Popen(cmd)  # noqa: S603


if __name__ == "__main__":
    main()
