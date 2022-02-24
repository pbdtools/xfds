"""Core program for running fds in docker containers."""
from __future__ import annotations

import re
import subprocess  # noqa: S404
import uuid
from pathlib import Path
from typing import Optional

import markdown
from rich import print


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

    print(f"[#ffa500]{' '.join(cmd)}[/]")

    if dry_run:
        return

    if interactive:
        subprocess.run(cmd)  # noqa: S603
    else:
        stdout = fds_file.resolve().with_suffix(".stdout")
        stderr = fds_file.resolve().with_suffix(".stderr")
        stdout.touch()
        stderr.touch()
        with stdout.open() as sout, stderr.open() as serr:
            subprocess.Popen(cmd, stdout=sout, stderr=serr)  # noqa: S603
