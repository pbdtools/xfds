"""Core program for running fds in docker containers."""
from __future__ import annotations

import argparse
import subprocess  # noqa: S404
import uuid
from pathlib import Path

from . import settings


def container_name(interactive: bool, version: str, fds_file: Path) -> str:
    """Get container name."""
    base = f"fds-{version}" if interactive else fds_file.stem
    return f"{base}-{uuid.uuid4()}"


def build_arguments(
    interactive: bool = settings.INTERACTIVE,
    processors: int = settings.PROCESSORS,
    version: str = settings.VERSIONS[-1],
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

    # Docker run command
    args = ["docker", "run", "--rm"]

    # Set interactive
    if interactive:
        args.append("-it")

    # Set container name
    name = container_name(interactive=interactive, version=version, fds_file=fds_file)
    args.extend(["--name", name])

    # Set volume to mount
    args.extend(["-v", f"{volume}:/workdir"])

    # Select container image
    args.append(f"openbcl/fds:{version}")

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
        "-n",
        "--processors",
        default=1,
        type=int,
        help="Number of processors to use",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=settings.VERSIONS[-1],
        choices=settings.VERSIONS,
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
        args.processors,
        args.version,
        Path(args.fds_file).resolve(),
    )
    print(" ".join(cmd))
    subprocess.run(cmd)  # noqa: S603


if __name__ == "__main__":
    main()
