"""Test ability to select correct file or folder."""
from pathlib import Path

from xfds.core import locate_fds_file, volume_to_mount


# Tests to Locate File or Directory To Run
def test_returns_fds_file_when_specified(fds_file: Path) -> None:
    """Test that FDS file is returned when specified."""
    assert locate_fds_file(fds_file=fds_file) == fds_file


def test_returns_fds_file_when_directory_specified(
    fds_file: Path, fds_dir: Path
) -> None:
    """Test that FDS file is returned when specified."""
    assert locate_fds_file(fds_file=fds_dir) == fds_file


def test_returns_directory_when_empty_directory_is_specified(empty_dir: Path) -> None:
    """Test that directory is returned when specified."""
    assert locate_fds_file(fds_file=empty_dir) == empty_dir


def tests_returns_cwd_when_no_file_specified() -> None:
    """Test that CWD is returned when no file is specified."""
    assert locate_fds_file(fds_file=None) == Path.cwd()


# Tests to Determine Mount Volume
def test_mount_volume_if_directory_specified(fds_dir: Path) -> None:
    """Test that directory is mounted if specified."""
    assert volume_to_mount(fds_file=fds_dir) == fds_dir


def test_mount_volume_if_file_specified(fds_file: Path) -> None:
    """Test that file is mounted if specified."""
    assert volume_to_mount(fds_file=fds_file) == fds_file.parent
