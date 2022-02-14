"""Tests for determining the FDS version."""
from pathlib import Path

from xfds.core import build_arguments


def format_image_name(fds_version: str) -> str:
    """Return the image name for the specified FDS version."""
    return f"openbcl/fds:{fds_version}"


def extract_container_name(cmd: list) -> str:
    """Extract the container name from the command line."""
    return [arg for arg in cmd if "openbcl/fds" in arg][0]


def test_latest_by_default(latest: str, fds_file: Path) -> None:
    """Test default FDS version is latest."""
    cmd = build_arguments(fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)


def test_latest_if_specified(latest: str, fds_file: Path) -> None:
    """Test latest FDS version is specified."""
    cmd = build_arguments(version=latest, fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)


def test_older_if_specified(fds_file: Path) -> None:
    """Test older FDS version is specified."""
    cmd = build_arguments(version="6.2.0", fds_file=fds_file)
    assert format_image_name("6.2.0") == extract_container_name(cmd)


def test_extracts_fds_version_from_file_metadata(meta_dir: Path) -> None:
    """Test FDS version is extracted from metadata."""
    for fds_file in meta_dir.glob("*.fds"):
        cmd = build_arguments(fds_file=fds_file)
        assert format_image_name(fds_file.stem) == extract_container_name(cmd)


def test_cli_version_overrides_metadata_version(meta_dir: Path, latest: str) -> None:
    """Test CLI version overrides metadata version."""
    fds_file = meta_dir / "6.2.0.fds"
    cmd = build_arguments(version=latest, fds_file=fds_file)
    assert format_image_name(latest) == extract_container_name(cmd)
