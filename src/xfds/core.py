"""Core functions."""
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from . import config, errors, log


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

    if fds_file.is_dir():
        try:
            _fds_file = next(fds_file.glob("*.fds"))
            return _fds_file
        except StopIteration:
            pass

    return fds_file


def locate_config(cwd: Path) -> Path:
    """Load the configuration file.

    Will look for a confing file in the same directory as the FDS template file.
    The config file should have the same base name as the original FDS file.
    If no config file is found, search the FDS meta for a variable "config".
    """
    cwd = cwd.resolve()
    for parent in [cwd, *cwd.parents]:
        for file in ["pbd.yaml", "pbd.yml"]:
            config_file = parent / file
            if config_file.exists():
                print(config_file)
                return config_file

    raise errors.ConfigNotFound(f"Could not find Config file pbd.yml in {cwd}.")


def read_config(config_file: Path) -> dict:
    """Read the configuration file."""
    with config_file.open() as f:
        return yaml.safe_load(f)


def volume_to_mount(fds_file: Path) -> Path:
    """Get the volume to mount.

    If the FDS input file is a directory, the directory is mounted.
    Otherwise, the parent directory of the FDS input file is mounted.
    """
    if fds_file.is_dir():
        folder = fds_file.resolve()
    else:
        folder = fds_file.parent.resolve()
    log.info(f"Mounting Volume: {folder}", icon="📂")
    return folder


def container_name(fds_file: Path, version: str, interactive: bool) -> str:
    """Get container name."""
    base = "fds" if interactive else fds_file.stem
    name = (
        f"{base}_{version}_{datetime.now().strftime(config.CONTAINER_TIMESTAMP_FORMAT)}"
    )
    log.debug(f"Container name: {name}", icon="📦")
    return name
