"""Tests for determining the FDS version."""
from pathlib import Path

from xfds.core import build_arguments


def format_image_name(fds_version: str) -> str:
    """Return the image name for the specified FDS version."""
    return f"openbcl/fds:{fds_version}"


def test_latest_by_default(latest: str, fds_file: Path) -> None:
    """Test default FDS version is latest."""
    cmd = build_arguments(fds_file=fds_file)
    assert format_image_name(latest) in cmd


def test_latest_if_specified(latest: str, fds_file: Path) -> None:
    """Test latest FDS version is specified."""
    cmd = build_arguments(version=latest, fds_file=fds_file)
    assert format_image_name(latest) in cmd


def test_older_if_specified(fds_file: Path) -> None:
    """Test older FDS version is specified."""
    cmd = build_arguments(version="6.2.0", fds_file=fds_file)
    assert format_image_name("6.2.0") in cmd
