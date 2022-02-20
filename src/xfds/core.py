"""Core program for running fds in docker containers."""
from __future__ import annotations

import argparse
import re
import subprocess  # noqa: S404
import uuid
from pathlib import Path
from typing import Optional

import markdown
from rich import print

from . import settings
from .docker_hub import tags


def locate_fds_file(fds_file: Optional[Path]) -> Path:
    """Locate the FDS input file or directory.

    FDS input file is located in the following order:
    - File if specified
    - File in directory if specified
    - Directory if specified
    - Current working directory
    """
    if fds_file is None:
        return Path.cwd().resolve()

    if fds_file.is_file():
        return fds_file

    if fds_file.is_dir():
        try:
            _fds_file = next(fds_file.glob("*.fds"))
            return _fds_file
        except StopIteration:
            pass

    return fds_file


def volume_to_mount(fds_file: Path) -> Path:
    """Get the volume to mount.

    If the FDS input file is a directory, the directory is mounted.
    Otherwise, the parent directory of the FDS input file is mounted.
    """
    if fds_file.is_dir():
        return fds_file.resolve()
    return fds_file.parent.resolve()


def interactive_mode(fds_file: Path, interactive: bool) -> bool:
    """Interactive mode if specifically requested or if the FDS input file is a directory."""
    return interactive or fds_file.is_dir()


def fds_version(fds_file: Path, version: Optional[str] = None) -> str:
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

    return "latest"


def container_name(fds_file: Path, version: str, interactive: bool) -> str:
    """Get container name."""
    base = "fds" if interactive else fds_file.stem
    return f"{base}-{version}-{uuid.uuid4()}"


def image_name(version: str = "") -> str:
    """Get image name.

    Specify FDS version if specified, otherwise use latest version.
    """
    if version:
        return f"openbcl/fds:{version}"
    return "openbcl/fds"


def build_arguments(
    fds_file: Path,
    volume: Path = settings.CWD,
    container_name: str = "",
    interactive: bool = settings.INTERACTIVE,
    version: str = "latest",
    processors: int = settings.PROCESSORS,
) -> list[str]:
    """Build the command line arguments for the CLI."""
    # Docker run command
    args = ["docker", "run", "--rm"]

    # Set interactive
    if interactive:
        args.append("-it")

    # Set container name
    args.extend(["--name", container_name])

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
        help="FDS version to use",
    )
    parser.add_argument(
        "fds_file",
        nargs="?",
        default=None,
        help="FDS input file",
    )
    parser.add_argument(
        "--fds-versions",
        action="store_true",
        help="List available FDS versions",
    )

    args = parser.parse_args()

    if args.fds_versions:
        print("\n".join(tags()))
        return

    _fds_file = locate_fds_file(fds_file=Path(args.fds_file or "."))
    _volume = volume_to_mount(fds_file=_fds_file)
    _interactive = interactive_mode(fds_file=_fds_file, interactive=args.interactive)
    _version = fds_version(fds_file=_fds_file, version=args.version)
    _container_name = container_name(
        fds_file=_fds_file, version=_version, interactive=_interactive
    )
    _processors = args.processors

    cmd = build_arguments(
        fds_file=_fds_file,
        volume=_volume,
        interactive=_interactive,
        version=_version,
        container_name=_container_name,
        processors=_processors,
    )
    print(f"[green]{' '.join(cmd)}[/]")

    if _interactive:
        subprocess.run(cmd)  # noqa: S603
    else:
        stdout = _fds_file.resolve().with_suffix(".stdout")
        stderr = _fds_file.resolve().with_suffix(".stderr")
        stdout.touch()
        stderr.touch()
        with stdout.open() as sout, stderr.open() as serr:
            subprocess.Popen(cmd, stdout=sout, stderr=serr)  # noqa: S603

    print("\nFrom [#cc5500][link=https://pbd.tools]pbd.tools[/link][/] with 💗")


if __name__ == "__main__":
    main()
