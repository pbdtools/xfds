"""Core program for running fds in docker containers."""
from __future__ import annotations

import argparse
import re
import subprocess  # noqa: S404
import uuid
from pathlib import Path
from typing import Optional

import markdown

from . import settings


def container_name(interactive: bool, version: str, fds_file: Path) -> str:
    """Get container name."""
    base = f"fds-{version}" if interactive else fds_file.stem
    return f"{base}-{uuid.uuid4()}"


def fds_version(fds_file: Path, version: Optional[str]) -> str:
    """Return the FDS version of the specified file.

    Version is selected in the following order:
    - Command line arguments
    - Metadata
    - File path
    - Latest version
    """
    if version is not None:
        return version

    md = markdown.Markdown(extensions=["meta"])
    try:
        md.convert(fds_file.read_text())
        if "fds" in md.Meta.keys():
            return md.Meta["fds"][0]
    except (FileNotFoundError, IsADirectoryError):
        pass

    pattern = r"((v|fds)?[._]?)(\d[._]\d[._]\d)"
    for part in fds_file.parts:
        match = re.match(pattern, part)
        if match:
            return match.group(3).replace("-", ".").replace("_", ".")

    return settings.VERSIONS[-1]


def build_arguments(
    interactive: bool = settings.INTERACTIVE,
    processors: int = settings.PROCESSORS,
    version: str = None,
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

    version = fds_version(fds_file=fds_file, version=version)

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
        default=None,
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
