"""Core functions."""
from pathlib import Path
from typing import Optional


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
